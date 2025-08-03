import os
import time
import logging
import json
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess
import sys
from config import Config

# Optional email imports
try:
    import smtplib
    from email.mime.text import MimeText
    from email.mime.multipart import MimeMultipart
    EMAIL_AVAILABLE = True
except ImportError:
    EMAIL_AVAILABLE = False

# Configure logging
logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL),
    format=Config.LOG_FORMAT,
    handlers=[
        logging.FileHandler(os.path.join(Config.LOG_PATH, 'auto_watcher.log')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ProductionSMITCHHandler(FileSystemEventHandler):
    def __init__(self):
        self.last_run = 0
        self.cooldown = Config.COOLDOWN_SECONDS
        self.stats = {
            'total_processed': 0,
            'successful_runs': 0,
            'failed_runs': 0,
            'last_run_time': None,
            'uptime_start': datetime.now()
        }
        self.load_stats()
    
    def load_stats(self):
        """Load processing statistics from file"""
        stats_file = os.path.join(Config.LOG_PATH, 'watcher_stats.json')
        try:
            if os.path.exists(stats_file):
                with open(stats_file, 'r') as f:
                    saved_stats = json.load(f)
                    self.stats.update(saved_stats)
                    # Convert string back to datetime
                    if self.stats['last_run_time']:
                        self.stats['last_run_time'] = datetime.fromisoformat(self.stats['last_run_time'])
        except Exception as e:
            logger.warning(f"Could not load stats: {e}")
    
    def save_stats(self):
        """Save processing statistics to file"""
        stats_file = os.path.join(Config.LOG_PATH, 'watcher_stats.json')
        try:
            # Convert datetime to string for JSON serialization
            stats_to_save = self.stats.copy()
            if stats_to_save['last_run_time']:
                stats_to_save['last_run_time'] = stats_to_save['last_run_time'].isoformat()
            stats_to_save['uptime_start'] = stats_to_save['uptime_start'].isoformat()
            
            with open(stats_file, 'w') as f:
                json.dump(stats_to_save, f, indent=2)
        except Exception as e:
            logger.error(f"Could not save stats: {e}")
    
    def send_notification(self, subject: str, message: str):
        """Send email notification if configured"""
        if not EMAIL_AVAILABLE or not Config.EMAIL_USER or not Config.NOTIFICATION_EMAILS[0]:
            logger.info(f"Notification (email disabled): {subject}")
            return
        
        try:
            msg = MimeMultipart()
            msg['From'] = Config.EMAIL_USER
            msg['To'] = ', '.join(Config.NOTIFICATION_EMAILS)
            msg['Subject'] = f"SMITCH Auto-Watcher: {subject}"
            
            msg.attach(MimeText(message, 'plain'))
            
            server = smtplib.SMTP(Config.SMTP_SERVER, Config.SMTP_PORT)
            server.starttls()
            server.login(Config.EMAIL_USER, Config.EMAIL_PASSWORD)
            server.send_message(msg)
            server.quit()
            
            logger.info(f"Notification sent: {subject}")
        except Exception as e:
            logger.error(f"Failed to send notification: {e}")
    
    def on_modified(self, event):
        if not event.is_directory and event.src_path.endswith(Config.SUPPORTED_EXTENSIONS):
            current_time = time.time()
            if current_time - self.last_run > self.cooldown:
                file_name = os.path.basename(event.src_path)
                
                # Wait a moment for file operations to complete
                time.sleep(0.5)
                
                # Safely get file size with error handling
                try:
                    if not os.path.exists(event.src_path):
                        logger.warning(f"File no longer exists, skipping: {file_name}")
                        return
                    
                    # Check if file is still being written to (try to open for writing)
                    try:
                        with open(event.src_path, 'r+b'):
                            pass
                    except PermissionError:
                        logger.info(f"File is still being written, skipping: {file_name}")
                        return
                    
                    file_size = os.path.getsize(event.src_path) / (1024 * 1024)  # MB
                except (FileNotFoundError, OSError, PermissionError) as e:
                    logger.warning(f"Cannot access file {file_name}: {e}")
                    return
                
                logger.info(f"File changed: {file_name} ({file_size:.2f}MB)")
                
                # Check file size limit
                if file_size > Config.MAX_FILE_SIZE_MB:
                    logger.warning(f"File too large: {file_size:.2f}MB > {Config.MAX_FILE_SIZE_MB}MB")
                    return
                
                self.stats['total_processed'] += 1
                
                try:
                    logger.info("Starting extraction process...")
                    result = subprocess.run(
                        [sys.executable, "test_runner.py"], 
                        capture_output=True, 
                        text=True, 
                        timeout=Config.TIMEOUT_SECONDS
                    )
                    
                    if result.returncode == 0:
                        self.stats['successful_runs'] += 1
                        self.stats['last_run_time'] = datetime.now()
                        
                        logger.info("Extraction completed successfully!")
                        
                        # Log output summary
                        output_lines = result.stdout.strip().split('\n')
                        for line in output_lines[-3:]:
                            if line.strip():
                                logger.info(f"    {line}")
                    else:
                        self.stats['failed_runs'] += 1
                        error_msg = f"Extraction failed for {file_name}: {result.stderr}"
                        logger.error(error_msg)
                        self.send_notification("Extraction Failed", error_msg)
                        
                except subprocess.TimeoutExpired:
                    self.stats['failed_runs'] += 1
                    error_msg = f"Extraction timed out ({Config.TIMEOUT_SECONDS}s) for {file_name}"
                    logger.error(error_msg)
                    self.send_notification("Extraction Timeout", error_msg)
                    
                except Exception as e:
                    self.stats['failed_runs'] += 1
                    error_msg = f"Error running extraction for {file_name}: {e}"
                    logger.error(error_msg)
                    self.send_notification("Extraction Error", error_msg)
                
                self.last_run = current_time
                self.save_stats()
                logger.info("Watching for more changes...")

def health_check():
    """Perform system health check"""
    config_status = Config.validate()
    
    health_info = {
        'timestamp': datetime.now().isoformat(),
        'status': 'healthy' if config_status['valid'] else 'unhealthy',
        'config': config_status,
        'python_version': sys.version,
        'working_directory': os.getcwd()
    }
    
    # Save health check results
    health_file = os.path.join(Config.LOG_PATH, 'health_check.json')
    with open(health_file, 'w') as f:
        json.dump(health_info, f, indent=2)
    
    return health_info

def main():
    """Main production watcher function with SharePoint support"""
    logger.info("SMITCH Production Auto-Watcher Starting...")
    
    # Perform initial health check
    health_info = health_check()
    if health_info['status'] != 'healthy':
        logger.error("Health check failed!")
        for issue in health_info['config']['issues']:
            logger.error(f"   {issue}")
        return 1
    
    logger.info("Health check passed")
    
    # Show configuration details
    if health_info['config'].get('sharepoint_detected'):
        logger.info("SharePoint/OneDrive path detected")
        logger.info("   Ensure sync is active and permissions are correct")
    
    for warning in health_info['config'].get('warnings', []):
        logger.warning(f"WARNING: {warning}")
    
    logger.info(f"Monitoring: {Config.WATCH_PATH}")
    logger.info(f"Output: {Config.OUTPUT_PATH}")
    logger.info(f"Cooldown: {Config.COOLDOWN_SECONDS}s")
    logger.info(f"Timeout: {Config.TIMEOUT_SECONDS}s")
    
    if Config.SHAREPOINT_MODE:
        logger.info(f"SharePoint mode enabled (timeout: {Config.NETWORK_TIMEOUT}s)")
    
    event_handler = ProductionSMITCHHandler()
    observer = Observer()
    observer.schedule(event_handler, Config.WATCH_PATH, recursive=True)
    
    observer.start()
    logger.info("File watcher started successfully")
    
    try:
        last_health_check = time.time()
        
        while True:
            time.sleep(1)
            
            # Periodic health checks
            if time.time() - last_health_check > Config.HEALTH_CHECK_INTERVAL:
                health_check()
                last_health_check = time.time()
                
                # Log statistics
                uptime = datetime.now() - event_handler.stats['uptime_start']
                logger.info(f"Stats - Processed: {event_handler.stats['total_processed']}, "
                          f"Success: {event_handler.stats['successful_runs']}, "
                          f"Failed: {event_handler.stats['failed_runs']}, "
                          f"Uptime: {uptime}")
                
    except KeyboardInterrupt:
        logger.info("Shutdown signal received")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return 1
    finally:
        observer.stop()
        logger.info("Stopping file watcher...")
        observer.join()
        logger.info("Auto-watcher stopped gracefully")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

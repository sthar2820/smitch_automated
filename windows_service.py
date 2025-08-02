import os
import sys
import time
import servicemanager
import socket
import win32event
import win32service
import win32serviceutil
import logging

class SMITCHWatcherService(win32serviceutil.ServiceFramework):
    """Windows Service for SMITCH Auto-Watcher - Production Server Version"""
    
    _svc_name_ = "SMITCHWatcher"
    _svc_display_name_ = "SMITCH File Watcher Service"
    _svc_description_ = "Automatically processes SMITCH Excel files when modified. Monitors SharePoint folders and extracts S.M.I.T.C.H. data in real-time."
    _svc_deps_ = ["EventLog"]  # Dependencies
    
    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)
        self.is_alive = True
        
        # Setup logging for service
        self.setup_service_logging()

    def setup_service_logging(self):
        """Setup logging for Windows Service"""
        try:
            log_dir = r"C:\SMITCH_Logs"
            os.makedirs(log_dir, exist_ok=True)
            
            logging.basicConfig(
                level=logging.INFO,
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                handlers=[
                    logging.FileHandler(os.path.join(log_dir, 'service.log')),
                ]
            )
            self.logger = logging.getLogger('SMITCHService')
        except Exception as e:
            # Fallback to event log only
            servicemanager.LogErrorMsg(f"Failed to setup file logging: {e}")

    def log_info(self, msg):
        """Log info message to both file and event log"""
        try:
            if hasattr(self, 'logger'):
                self.logger.info(msg)
        except:
            pass
        servicemanager.LogInfoMsg(msg)

    def log_error(self, msg):
        """Log error message to both file and event log"""
        try:
            if hasattr(self, 'logger'):
                self.logger.error(msg)
        except:
            pass
        servicemanager.LogErrorMsg(msg)

    def SvcStop(self):
        """Stop the service"""
        self.log_info("SMITCH Watcher Service stop requested")
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.is_alive = False

    def SvcDoRun(self):
        """Main service loop"""
        self.log_info("SMITCH Watcher Service starting...")
        
        # Change to script directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(script_dir)
        
        self.log_info(f"Working directory: {script_dir}")
        
        # Import and run the production watcher
        try:
            # Ensure the path is correct
            sys.path.insert(0, script_dir)
            
            # Import configuration first to validate
            from config import Config
            config_result = Config.validate()
            
            if not config_result['valid']:
                error_msg = "Configuration validation failed: " + "; ".join(config_result['issues'])
                self.log_error(error_msg)
                return
            
            self.log_info(f"Configuration valid - Input: {Config.WATCH_PATH}, Output: {Config.OUTPUT_PATH}")
            
            # Import and start the production watcher
            from production_watcher import main
            self.log_info("Starting production watcher...")
            
            result = main()
            
            if result != 0:
                self.log_error(f"Production watcher exited with code: {result}")
            else:
                self.log_info("Production watcher exited normally")
                
        except ImportError as e:
            self.log_error(f"Import error: {e}")
        except Exception as e:
            self.log_error(f"Service error: {e}")
            import traceback
            self.log_error(f"Traceback: {traceback.format_exc()}")

def install_service():
    """Install the service with proper configuration"""
    try:
        win32serviceutil.InstallService(
            SMITCHWatcherService._svc_reg_class_,
            SMITCHWatcherService._svc_name_,
            SMITCHWatcherService._svc_display_name_,
            description=SMITCHWatcherService._svc_description_,
            startType=win32service.SERVICE_AUTO_START,  # Auto start
            errorControl=win32service.SERVICE_ERROR_NORMAL,
            dependencies=SMITCHWatcherService._svc_deps_
        )
        print("✓ Service installed successfully!")
        print("  Service will start automatically on system boot")
        print("  Use 'net start SMITCHWatcher' to start now")
        
    except Exception as e:
        print(f"✗ Failed to install service: {e}")
        return False
    return True

if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.PrepareToHostSingle(SMITCHWatcherService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        if 'install' in sys.argv:
            install_service()
        else:
            win32serviceutil.HandleCommandLine(SMITCHWatcherService)

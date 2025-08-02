import os
import logging
from typing import Dict, Any

class Config:
    """Production configuration class with SharePoint support"""
    
    # File paths - use environment variables for flexibility
    # These can be SharePoint paths, network drives, or local paths
    WATCH_PATH = os.getenv('WATCH_PATH', r'C:\Users\RShrestha\OneDrive - Dura-Shiloh\SMITCH_2025')
    OUTPUT_PATH = os.getenv('OUTPUT_PATH', r'C:\Users\RShrestha\OneDrive - Dura-Shiloh\smitch_extracted')
    LOG_PATH = os.getenv('LOG_PATH', './logs')
    
    # SharePoint specific settings
    SHAREPOINT_MODE = os.getenv('SHAREPOINT_MODE', 'false').lower() == 'true'
    NETWORK_TIMEOUT = int(os.getenv('NETWORK_TIMEOUT', '30'))  # seconds
    RETRY_ATTEMPTS = int(os.getenv('RETRY_ATTEMPTS', '3'))
    
    # Common SharePoint path examples:
    # OneDrive Business: "C:\Users\username\OneDrive - Company\SharedFolder"
    # Mapped Drive: "Z:\SharedFolder\SMITCH_Files"
    # UNC Path: "\\sharepoint.company.com\sites\team\Shared Documents\SMITCH"
    
    # Watcher settings
    COOLDOWN_SECONDS = int(os.getenv('COOLDOWN_SECONDS', '10'))
    TIMEOUT_SECONDS = int(os.getenv('TIMEOUT_SECONDS', '120'))
    
    # File settings
    SUPPORTED_EXTENSIONS = ('.xlsm', '.xlsx')
    MAX_FILE_SIZE_MB = int(os.getenv('MAX_FILE_SIZE_MB', '100'))
    
    # Logging configuration
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Health check settings
    HEALTH_CHECK_INTERVAL = int(os.getenv('HEALTH_CHECK_INTERVAL', '300'))  # 5 minutes
    
    # Email notifications (optional)
    SMTP_SERVER = os.getenv('SMTP_SERVER', '')
    SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
    EMAIL_USER = os.getenv('EMAIL_USER', '')
    EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', '')
    NOTIFICATION_EMAILS = os.getenv('NOTIFICATION_EMAILS', '').split(',')
    
    @classmethod
    def validate(cls) -> Dict[str, Any]:
        """Validate configuration and return status with SharePoint support"""
        issues = []
        warnings = []
        
        # Check if paths look like SharePoint/OneDrive paths
        sharepoint_indicators = ['OneDrive', 'SharePoint', 'Sites', '\\\\']
        is_likely_sharepoint = any(indicator in cls.WATCH_PATH for indicator in sharepoint_indicators)
        
        if is_likely_sharepoint:
            warnings.append("SharePoint/OneDrive path detected - ensure sync is active")
        
        # Validate watch path with network timeout consideration
        if not os.path.exists(cls.WATCH_PATH):
            if is_likely_sharepoint:
                issues.append(f"SharePoint path not accessible (check sync): {cls.WATCH_PATH}")
            else:
                issues.append(f"Watch path does not exist: {cls.WATCH_PATH}")
        
        # Create output path if it doesn't exist
        if not os.path.exists(cls.OUTPUT_PATH):
            try:
                os.makedirs(cls.OUTPUT_PATH, exist_ok=True)
                warnings.append(f"Created output directory: {cls.OUTPUT_PATH}")
            except Exception as e:
                issues.append(f"Cannot create output path: {e}")
        
        # Create log path
        if not os.path.exists(cls.LOG_PATH):
            try:
                os.makedirs(cls.LOG_PATH, exist_ok=True)
            except Exception as e:
                issues.append(f"Cannot create log path: {e}")
        
        return {
            'valid': len(issues) == 0,
            'issues': issues,
            'warnings': warnings,
            'sharepoint_detected': is_likely_sharepoint,
            'config': {
                'watch_path': cls.WATCH_PATH,
                'output_path': cls.OUTPUT_PATH,
                'log_path': cls.LOG_PATH,
                'cooldown': cls.COOLDOWN_SECONDS,
                'timeout': cls.TIMEOUT_SECONDS,
                'sharepoint_mode': cls.SHAREPOINT_MODE,
                'network_timeout': cls.NETWORK_TIMEOUT
            }
        }

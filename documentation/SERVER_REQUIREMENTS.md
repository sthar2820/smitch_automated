# SMITCH Server Requirements & Installation Guide 🖥️

## Server Requirements

### Minimum System Requirements

- **OS**: Windows Server 2016 or newer (Windows 10 Pro also supported)
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 10GB free space for logs and temporary files
- **CPU**: 2 cores minimum, 4+ cores recommended
- **Network**: Reliable connection to SharePoint/OneDrive

### Software Requirements

- **Python**: 3.8 or newer (will be installed during setup)
- **PowerShell**: 5.1 or newer (usually pre-installed)
- **Administrator Access**: Required for service installation
- **SharePoint Access**: Read/write permissions to SMITCH folders

### Network Requirements

- **SharePoint Access**: UNC path or mapped drive to SharePoint
- **Internet**: For Python package downloads (initial setup only)
- **Firewall**: Allow Python.exe outbound connections
- **DNS**: Resolve SharePoint server names

## Installation Steps

### Step 1: Prepare Server

1. **Login** as Administrator
2. **Create dedicated folder**: `C:\SMITCH_Pipeline\`
3. **Copy all files** from development machine
4. **Open PowerShell** as Administrator

### Step 2: Run Server Deployment

```cmd
# Navigate to pipeline folder
cd C:\SMITCH_Pipeline\

# Run server deployment tool
server_deploy.bat
```

### Step 3: Installation Menu

Follow the deployment menu options in order:

1. **Install Python and Dependencies**
2. **Configure SharePoint Paths**
3. **Install as Windows Service**
4. **Test Configuration**
5. **Start Production Service**

### Step 4: Verify Installation

- Check Windows Services for "SMITCH File Watcher Service"
- Verify logs in `C:\SMITCH_Logs\`
- Test with a sample Excel file change

## SharePoint Configuration Options

### Option A: Network Share (Recommended)

```
Input:  \\sharepoint-server\sites\team\SMITCH_2025
Output: \\sharepoint-server\sites\team\SMITCH_Extracted
```

### Option B: Mapped Drive

```
# Map SharePoint as S: drive first
Input:  S:\SMITCH_2025
Output: S:\SMITCH_Extracted
```

### Option C: OneDrive Business Sync

```
# If server has OneDrive Business client
Input:  C:\SharePoint\Company\SMITCH_2025
Output: C:\SharePoint\Company\SMITCH_Extracted
```

## Service Management

### Start/Stop Service

```cmd
# Start service
net start SMITCHWatcher

# Stop service
net stop SMITCHWatcher

# Check status
sc query SMITCHWatcher
```

### Service Properties

- **Name**: SMITCHWatcher
- **Display Name**: SMITCH File Watcher Service
- **Startup Type**: Automatic (starts with Windows)
- **Log On As**: Local System Account
- **Dependencies**: EventLog

## Monitoring & Maintenance

### Log Files Location

```
C:\SMITCH_Logs\
├── auto_watcher.log      # Main application log
├── service.log           # Windows service log
├── watcher_stats.json    # Performance statistics
└── health_check.json     # System health status
```

### Windows Event Viewer

- **Path**: Windows Logs > Application
- **Source**: SMITCHWatcher
- **Event Types**: Information, Warning, Error

### Performance Monitoring

- **CPU Usage**: Should be minimal (<5%)
- **Memory Usage**: ~50-100MB typical
- **Disk I/O**: Spikes during file processing
- **Network**: SharePoint file transfers

## Troubleshooting

### Common Issues

#### Service Won't Start

1. Check Windows Event Viewer
2. Verify SharePoint paths are accessible
3. Ensure Python dependencies installed
4. Check file permissions

#### Files Not Processing

1. Verify SharePoint sync is active
2. Check cooldown settings (15 seconds default)
3. Review file size limits (200MB default)
4. Test with a small Excel file

#### SharePoint Access Issues

1. Test UNC path from server manually
2. Verify service account permissions
3. Check network connectivity
4. Consider mapped drive alternative

### Support Commands

```cmd
# Test configuration
python -c "from config import Config; print(Config.validate())"

# View recent logs
powershell "Get-Content 'C:\SMITCH_Logs\auto_watcher.log' -Tail 20"

# Service diagnostics
sc qc SMITCHWatcher
```

## Security Considerations

### Service Account

- Runs as Local System by default
- Consider dedicated service account for enhanced security
- Ensure minimum required SharePoint permissions

### File Access

- Read access to SharePoint input folder
- Write access to SharePoint output folder
- Full control of log directory

### Network Security

- Service only needs outbound connections
- No incoming ports required
- SharePoint communication encrypted

## Backup & Recovery

### What to Backup

- Configuration files (`.env`)
- Custom modifications to Python scripts
- Log files (for troubleshooting history)

### Recovery Process

1. Reinstall Python and dependencies
2. Restore configuration files
3. Reinstall Windows service
4. Test configuration and start service

## Performance Tuning

### For High Volume

```env
# Reduce cooldown for faster processing
COOLDOWN_SECONDS=5

# Increase timeout for large files
TIMEOUT_SECONDS=600

# More frequent health checks
HEALTH_CHECK_INTERVAL=300
```

### For Stability

```env
# Conservative settings
COOLDOWN_SECONDS=30
RETRY_ATTEMPTS=5
NETWORK_TIMEOUT=120
```

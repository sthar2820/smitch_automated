# SharePoint Configuration Guide 🔧

## Quick Setup for SharePoint Integration

### Option 1: OneDrive Business Sync (Recommended) ⭐

```bash
# 1. Sync your SharePoint folder to local computer
# 2. Copy .env.example to .env
# 3. Update paths in .env:

WATCH_PATH=C:\Users\[username]\OneDrive - [Company]\Shared Documents\SMITCH_2025
OUTPUT_PATH=C:\Users\[username]\OneDrive - [Company]\Shared Documents\SMITCH_Extracted
SHAREPOINT_MODE=true
```

### Option 2: Mapped Network Drive

```bash
# 1. Map SharePoint as network drive (e.g., Z:)
# 2. Update .env:

WATCH_PATH=Z:\SMITCH_Files\SMITCH_2025
OUTPUT_PATH=Z:\SMITCH_Files\Extracted
SHAREPOINT_MODE=true
```

### Option 3: Direct UNC Path

```bash
# For advanced users with direct SharePoint access:

WATCH_PATH=\\company.sharepoint.com\sites\team\Shared Documents\SMITCH_2025
OUTPUT_PATH=\\company.sharepoint.com\sites\team\Shared Documents\Extracted
SHAREPOINT_MODE=true
NETWORK_TIMEOUT=60
```

## How to Change Paths Later

### Method 1: Environment File (Recommended)

1. Edit `.env` file
2. Change `WATCH_PATH` and `OUTPUT_PATH`
3. Restart the watcher

### Method 2: Windows Environment Variables

1. Open System Properties → Environment Variables
2. Add/modify:
   - `WATCH_PATH` = your SharePoint input folder
   - `OUTPUT_PATH` = your SharePoint output folder

### Method 3: Batch File Parameters

Create custom batch files for different environments:

**SharePoint_Production.bat:**

```batch
set WATCH_PATH=C:\Users\%USERNAME%\OneDrive - Company\SMITCH_2025
set OUTPUT_PATH=C:\Users\%USERNAME%\OneDrive - Company\SMITCH_Extracted
python production_watcher.py
```

## SharePoint Best Practices

### Recommended Setup:

- Use OneDrive Business sync for best performance
- Keep output folder in same SharePoint site for easy access
- Enable notifications for team members
- Set up proper permissions (read/write for processors, read-only for viewers)

### Important Considerations:

- Ensure SharePoint sync is always active
- Test network connectivity before deploying
- Consider file locking when multiple users access files
- Monitor sync status to avoid processing outdated files

### Troubleshooting:

- **Sync Issues**: Check OneDrive sync status in system tray
- **Permission Errors**: Verify SharePoint folder permissions
- **Network Timeouts**: Increase `NETWORK_TIMEOUT` in .env
- **File Locks**: Enable `RETRY_ATTEMPTS` for busy files

## Multi-Environment Support

You can easily switch between environments:

```bash
# Development
set WATCH_PATH=C:\Dev\SMITCH_Test
set OUTPUT_PATH=C:\Dev\Output

# Staging
set WATCH_PATH=\\sharepoint-test\sites\staging\SMITCH
set OUTPUT_PATH=\\sharepoint-test\sites\staging\Output

# Production
set WATCH_PATH=C:\Users\%USERNAME%\OneDrive - Company\SMITCH_2025
set OUTPUT_PATH=C:\Users\%USERNAME%\OneDrive - Company\SMITCH_Extracted
```

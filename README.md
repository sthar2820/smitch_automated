# SMITCH Auto-Extractor 🚀

**Automatically extracts S.M.I.T.C.H. data from Excel files when they change.**

## What This Does

- Monitors Excel files for changes
- Automatically extracts S.M.I.T.C.H. data when files are saved
- Saves extracted data to a separate folder
- Works with SharePoint and local folders

## Quick Start

### 🖥️ For Local Use (Your Computer)

```
1. Double-click: start_auto_watcher.bat
2. Modify any Excel file in your SMITCH folder
3. Save the file - extraction happens automatically!
```

### 🏢 For Company Server Deployment

```
1. Copy all files to server
2. Run as Administrator: server_deploy.bat
3. Follow the menu options (takes 5 minutes)
4. Service runs automatically 24/7
```

## File Structure

```
📁 Essential Files:
├── start_auto_watcher.bat    ← Start monitoring (local use)
├── server_deploy.bat         ← Deploy to company server
├── production_watcher.py     ← Main monitoring program
├── test_runner.py           ← Data extraction engine
├── config.py                ← Configuration settings
├── windows_service.py       ← Windows service version
├── utils/                   ← Data processing modules
└── logs/                    ← Runtime logs and statistics

📖 Documentation:
├── README.md                ← This file
├── SERVER_REQUIREMENTS.md   ← Server installation guide
├── SHAREPOINT_SETUP.md      ← SharePoint configuration
├── TEAM_HANDOVER.md        ← Team documentation
└── DEPLOYMENT_CHECKLIST.md ← Server deployment steps
```

## Configuration

### Current Paths (Change in .env file):

- **Input**: `C:\Users\sthar\Downloads\SMITCH_2025\SMITCH_2025`
- **Output**: `C:\Users\sthar\Downloads\smitch_extracted`

### For SharePoint:

1. Copy `.env.example` to `.env`
2. Update paths to your SharePoint folders
3. Restart the watcher

## How It Works

1. **File Monitoring**: Watches for .xlsx and .xlsm file changes
2. **Smart Processing**: 15-second cooldown prevents duplicate processing
3. **Data Extraction**: Processes S.M.I.T.C.H. categories from all plant files
4. **Automatic Output**: Saves extracted data with timestamps
5. **Health Monitoring**: Tracks statistics and performance

## Support Files

- **Plants Supported**: Birmingham, Blatna, Genk, Komarom, Wolfsburg, Palencia, Setubal, Brugge
- **Data Categories**: S.M.I.T.C.H. metrics + APW + EBIT data
- **File Types**: Excel .xlsm and .xlsx files

## Need Help?

- Check `logs/auto_watcher.log` for detailed information
- Review `TEAM_HANDOVER.md` for team usage guide
- See `SERVER_REQUIREMENTS.md` for server deployment

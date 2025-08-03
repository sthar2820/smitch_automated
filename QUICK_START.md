# SMITCH Auto-Watcher - Quick Start Guide

## 🚀 Quick Start

1. **Setup & Test**: Run `setup.py` to verify everything is ready
   ```
   python setup.py
   ```

2. **Start Monitoring**: Double-click `start_auto_watcher.bat`

3. **Choose Your Mode**:
   - **Option 1**: Run once (stops after completion)
   - **Option 2**: Persistent (auto-restart, perfect for work computers)
   - **Option 3**: Test configuration
   - **Option 4**: Process existing files

## 📁 File Structure

```
smitch_automated/
├── start_auto_watcher.bat    # Main launcher (interactive menu)
├── setup.py                  # Setup and diagnostics tool
├── production_watcher.py     # Core monitoring service
├── test_runner.py           # Process existing files
├── config.py                # Configuration settings
├── windows_service.py       # Windows service installer
├── utils/                   # Core utilities
│   ├── extractor.py        # Excel data extraction
│   ├── saver.py           # Data saving logic
│   ├── file_utils.py      # File operations
│   └── logger.py          # Logging utilities
└── logs/                   # Application logs
```

## ⚙️ Configuration

Your paths are configured in `config.py`:
- **Input**: `C:\Users\RShrestha\OneDrive - Dura-Shiloh\SMITCH_2025`
- **Output**: `C:\Users\RShrestha\OneDrive - Dura-Shiloh\smitch_extracted`

## 🔧 Troubleshooting

1. **Run setup first**: `python setup.py`
2. **Check logs**: Look in the `logs/` folder
3. **Test config**: Use option 3 in the main menu
4. **Process existing files**: Use option 4 to test with current files

## 🏢 For Work Computers

**Persistent Mode (Option 2)** is perfect for work computers:
- Automatically restarts if stopped
- Runs continuously in background
- Shows timestamps for monitoring
- Easy to stop with Ctrl+C

## 📋 Startup Options

**Manual**: Double-click `start_auto_watcher.bat`

**Auto-start**: 
1. Press `Win + R`, type `shell:startup`
2. Copy `start_auto_watcher.bat` to that folder
3. Choose option 2 (Persistent) when it starts

**Windows Service** (Most Robust):
See `DEPLOYMENT_CHECKLIST.md` for Windows service setup.

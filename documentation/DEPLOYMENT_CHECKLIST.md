# 🚀 SMITCH Server Deployment Checklist

## Pre-Deployment Checklist ✅

### Development Machine (Your Computer)

- [ ] All files tested and working locally
- [ ] Unicode errors fixed
- [ ] SharePoint paths configured (if applicable)
- [ ] Documentation completed
- [ ] All team members identified and notified

### Server Preparation

- [ ] Windows Server access confirmed
- [ ] Administrator privileges verified
- [ ] SharePoint network access tested
- [ ] Dedicated folder created: `C:\SMITCH_Pipeline\`
- [ ] IT department notified

## Deployment Steps 📋

### Step 1: Copy Files to Server

```
Transfer these files to C:\SMITCH_Pipeline\:
├── 🔧 server_deploy.bat          # Main deployment tool
├── 🏠 production_watcher.py      # Core watcher
├── ⚙️ config.py                  # Configuration
├── 🏃 test_runner.py             # Extraction engine
├── 🪟 windows_service.py         # Windows service
├── 🔧 service_installer.bat      # Service management
├── 📋 requirements.txt           # Dependencies
├── 📖 .env.example               # Config template
├── 📁 utils/                     # Processing modules
├── 📖 README.md                  # Documentation
├── 📖 SERVER_REQUIREMENTS.md     # Server guide
├── 📖 TEAM_HANDOVER.md          # Team documentation
└── 📖 SHAREPOINT_SETUP.md       # SharePoint guide
```

### Step 2: Run Server Deployment

```cmd
# On the Windows Server:
1. Open Command Prompt as Administrator
2. cd C:\SMITCH_Pipeline\
3. server_deploy.bat
4. Follow menu options 1→2→3→4→5
```

### Step 3: Menu Options (In Order)

1. ✅ **Install Python and Dependencies**

   - Installs Python packages
   - Installs Windows service components

2. ✅ **Configure SharePoint Paths**

   - Set input folder (where team uploads SMITCH files)
   - Set output folder (where extracted data is saved)
   - Creates server configuration

3. ✅ **Install as Windows Service**

   - Registers SMITCHWatcher service
   - Sets to start automatically on boot

4. ✅ **Test Configuration**

   - Validates all paths and settings
   - Tests SharePoint connectivity

5. ✅ **Start Production Service**
   - Starts the monitoring service
   - Begins automatic file processing

## Post-Deployment Verification ✔️

### Immediate Tests (Day 1)

- [ ] Service shows "Running" in Windows Services
- [ ] Log files created in `C:\SMITCH_Logs\`
- [ ] Test file processing with sample Excel file
- [ ] Team can access output folder
- [ ] SharePoint sync working correctly

### Week 1 Monitoring

- [ ] Service continues running after server reboot
- [ ] Multiple file changes processed correctly
- [ ] No memory leaks or performance issues
- [ ] Log rotation working properly
- [ ] Team comfortable with the system

## Team Handover 👥

### Training Sessions

- [ ] **IT Team**: Service management and troubleshooting
- [ ] **Data Team**: File processing and output location
- [ ] **Business Users**: Where to find extracted data

### Documentation Delivery

- [ ] **TEAM_HANDOVER.md** → Data Team
- [ ] **SERVER_REQUIREMENTS.md** → IT Team
- [ ] **SHAREPOINT_SETUP.md** → SharePoint Admin
- [ ] **Service credentials** → IT Security

### Contact Information

- [ ] Update emergency contacts in documentation
- [ ] Provide transition support timeline
- [ ] Schedule follow-up check after 30 days

## Success Criteria 🎯

### Technical Success

✅ Service runs 24/7 without intervention  
✅ Processes files within 15 seconds of change  
✅ 99%+ successful extraction rate  
✅ Automatic restart after server reboot  
✅ Comprehensive logging for troubleshooting

### Business Success

✅ Team can access extracted data immediately  
✅ No manual intervention required  
✅ SharePoint integration seamless  
✅ Processing scales with file volume  
✅ Data quality maintained

## Rollback Plan 🔄

If deployment fails:

1. **Stop service**: `net stop SMITCHWatcher`
2. **Uninstall service**: `python windows_service.py remove`
3. **Revert to manual processing** temporarily
4. **Troubleshoot issues** using logs
5. **Retry deployment** with fixes

## Support & Maintenance 🛠️

### Daily Operations

- **Zero intervention** required when working properly
- **Monitor logs** weekly for any warnings
- **Test with sample files** monthly

### Quarterly Tasks

- **Review performance** statistics
- **Update Python packages** if needed
- **Archive old logs** to save disk space

### Annual Tasks

- **Review SharePoint permissions**
- **Update documentation** with any changes
- **Train new team members**

---

## 🎉 Deployment Complete!

Once all checkboxes are completed, your SMITCH pipeline will be running independently on the company server, ready to serve your team long after you've moved on to your next adventure! 🚀

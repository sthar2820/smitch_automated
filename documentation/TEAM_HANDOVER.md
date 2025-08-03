# SMITCH Pipeline - Team Handover Guide 📋

## Quick Start for New Team Members

### What This Pipeline Does

- Monitors SharePoint/OneDrive SMITCH Excel files
- Automatically extracts S.M.I.T.C.H. data when files change
- Saves processed data to shared output folder
- Provides comprehensive logging and statistics

### Current Setup

- **Input**: `C:\Users\RShrestha\OneDrive - Dura-Shiloh\SMITCH_2025`
- **Output**: `C:\Users\RShrestha\OneDrive - Dura-Shiloh\smitch_extracted`
- **Logs**: `./logs/`

### How to Use

#### Option 1: Run Locally (Temporary)

1. Double-click: `start_auto_watcher.bat`
2. Leave console window open
3. Modify Excel files - they process automatically

#### Option 2: Install as Service (Permanent)

1. Double-click: `service_installer.bat`
2. Choose "Install SMITCH Service"
3. Choose "Start SMITCH Service"
4. Runs automatically forever

#### Option 3: Change Paths (SharePoint Setup)

1. Double-click: `configure_paths.bat`
2. Choose SharePoint option
3. Enter your SharePoint paths
4. Start the service

### Team Responsibilities

#### IT Administrator:

- Install on company server
- Configure SharePoint access
- Monitor service health
- Handle updates and maintenance

#### Data Team:

- Upload SMITCH files to input folder
- Monitor extracted outputs
- Report any processing issues
- Validate data quality

#### Process Owner:

- Coordinate file uploads
- Manage extraction schedule
- Handle business requirements
- Training new users

### Troubleshooting

#### Common Issues:

1. **Service not starting**: Check paths in `.env` file
2. **Files not processing**: Verify SharePoint sync
3. **Permission errors**: Check folder permissions
4. **Unicode errors**: Ensure Windows UTF-8 support

#### Log Files:

- `logs/auto_watcher.log` - Main application log
- `logs/watcher_stats.json` - Performance statistics
- `logs/health_check.json` - System health status

### Emergency Contacts

- **Pipeline Creator**: [Your Name] - [Your Email]
- **IT Support**: [IT Contact]
- **Business Owner**: [Business Contact]

### Handover Checklist

- [ ] Pipeline installed on server
- [ ] SharePoint paths configured
- [ ] Team trained on usage
- [ ] Documentation shared
- [ ] Emergency contacts updated
- [ ] Service running successfully
- [ ] First successful extraction tested

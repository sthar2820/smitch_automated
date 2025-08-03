#!/usr/bin/env python3
"""
SMITCH Auto-Watcher Setup and Diagnostic Tool
Helps with initial setup and troubleshooting
"""

import os
import sys
import json
from pathlib import Path

def check_python_version():
    """Check Python version compatibility"""
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ is required")
        return False
    print("✅ Python version is compatible")
    return True

def check_dependencies():
    """Check if all required packages are installed"""
    required_packages = [
        ('pandas', 'pandas'),
        ('openpyxl', 'openpyxl'), 
        ('watchdog', 'watchdog'),
        ('python-dotenv', 'dotenv'),
        ('requests', 'requests')
    ]
    
    missing = []
    for package_name, import_name in required_packages:
        try:
            __import__(import_name)
            print(f"✅ {package_name}")
        except ImportError:
            print(f"❌ {package_name} - MISSING")
            missing.append(package_name)
    
    return missing

def check_paths():
    """Check if all required paths exist"""
    from config import Config
    
    paths = {
        'Watch Path': Config.WATCH_PATH,
        'Output Path': Config.OUTPUT_PATH,
        'Log Path': Config.LOG_PATH
    }
    
    issues = []
    for name, path in paths.items():
        if os.path.exists(path):
            print(f"✅ {name}: {path}")
        else:
            print(f"❌ {name}: {path} - MISSING")
            issues.append((name, path))
    
    return issues

def create_missing_paths(issues):
    """Create missing directories"""
    for name, path in issues:
        try:
            os.makedirs(path, exist_ok=True)
            print(f"✅ Created {name}: {path}")
        except Exception as e:
            print(f"❌ Failed to create {name}: {e}")

def test_configuration():
    """Test the complete configuration"""
    try:
        from config import Config
        result = Config.validate()
        
        print("\n=== CONFIGURATION TEST ===")
        print(f"Valid: {'✅ YES' if result['valid'] else '❌ NO'}")
        
        if result['issues']:
            print("Issues:")
            for issue in result['issues']:
                print(f"  ❌ {issue}")
        
        if result['warnings']:
            print("Warnings:")
            for warning in result['warnings']:
                print(f"  ⚠️  {warning}")
        
        return result['valid']
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def main():
    """Main setup function"""
    print("=" * 50)
    print("  SMITCH AUTO-WATCHER SETUP & DIAGNOSTICS")
    print("=" * 50)
    print()
    
    # Check Python version
    print("1. Checking Python version...")
    if not check_python_version():
        return 1
    print()
    
    # Check dependencies
    print("2. Checking dependencies...")
    missing = check_dependencies()
    if missing:
        print(f"\n❌ Missing packages: {', '.join(missing)}")
        print("Run: pip install " + " ".join(missing))
        return 1
    print()
    
    # Check paths
    print("3. Checking paths...")
    path_issues = check_paths()
    if path_issues:
        print("\n🔧 Creating missing directories...")
        create_missing_paths(path_issues)
    print()
    
    # Test configuration
    print("4. Testing configuration...")
    if test_configuration():
        print("\n🎉 Setup complete! Ready to run SMITCH Auto-Watcher")
        print("\nNext steps:")
        print("  • Run: start_auto_watcher.bat")
        print("  • Or use option 2 for persistent monitoring")
        return 0
    else:
        print("\n❌ Setup incomplete. Please fix the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

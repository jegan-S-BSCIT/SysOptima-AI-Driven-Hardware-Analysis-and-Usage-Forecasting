# PyInstaller Build Guide - SysOptima Desktop Application

## 📦 Creating Standalone Executable

This guide explains how to build a standalone `.exe` file that can be distributed and run on Windows without Python installed.

---

## Prerequisites

```bash
# Install PyInstaller
pip install pyinstaller

# Verify installation
pyinstaller --version  # Should show version number
```

---

## Build Steps

### Step 1: Prepare Project
```bash
# Navigate to project directory
cd e:\project\SysOptima

# Ensure all dependencies installed
pip install -r requirements.txt

# Ensure .env file exists (if using Gemini API)
# Copy: copy .env .env.example (for distribution)
```

### Step 2: Build Executable

#### Option A: Using Provided Spec File (Recommended)
```bash
pyinstaller build.spec
```

#### Option B: Single-File Executable
```bash
pyinstaller --onefile --windowed --name="SysOptima" main.py
```

#### Option C: One-Folder Distribution
```bash
pyinstaller --windowed --name="SysOptima" main.py
```

### Step 3: Find Output

**Single-File Build** (build.spec):
```
dist/SysOptima/SysOptima.exe
```

**One-File Build**:
```
dist/SysOptima.exe
```

---

## Building with build.spec

### What the spec file does:

```python
# Includes necessary modules
hidden_imports=[
    'psutil',
    'GPUtil',
    'matplotlib',
    'matplotlib.backends.backend_tkagg',
    'google.generativeai',
    'dotenv',
]

# Includes data files
datas=[
    ('core', 'core'),
    ('data', 'data'),
    ('.env', '.'),
]

# Windowed mode (no console)
console=False
```

### Build command:
```bash
pyinstaller build.spec
```

### Output:
```
dist/SysOptima/
├── SysOptima.exe          (main executable)
├── core/                  (included modules)
├── _internal/             (dependencies)
├── .env                   (if including API key)
└── [other libraries]
```

---

## Customizing the Build

### Add Application Icon

1. Create or find an icon file: `icon.ico` (256×256 or larger)
2. Place in project root
3. Edit `build.spec`:
   ```python
   exe = EXE(
       ...
       icon='icon.ico',  # Add this line
       ...
   )
   ```
4. Rebuild

### Change Executable Name

Edit `build.spec`:
```python
exe = EXE(
    ...
    name='SysOptima_v1.0',  # Change name here
    ...
)
```

### Remove Matplotlib Console

Edit `build.spec`:
```python
a = Analysis(
    ...
    excludedimports=['tkinter.test', 'matplotlib.backends.backend_qt5'],
    ...
)
```

### Reduce Executable Size

```bash
# Use UPX (Ultimate Packer for eXecutables)
pip install upx

# UPX will automatically compress if available
pyinstaller build.spec
```

---

## Distribution Package

### Step 1: Create Distribution Folder

```bash
# Copy the dist folder content
xcopy dist\SysOptima dist_package\SysOptima /E /I

# Create installer script
echo @echo off > dist_package\run.bat
echo SysOptima\SysOptima.exe >> dist_package\run.bat
echo pause >> dist_package\run.bat
```

### Step 2: Add Documentation

```bash
copy DESKTOP_APP_README.md dist_package\README.md
copy DESKTOP_APP_QUICKSTART.md dist_package\QUICKSTART.md
copy requirements.txt dist_package\requirements.txt
copy .env dist_package\.env.example
```

### Step 3: Create ReadMe for Users

Create `dist_package\START_HERE.txt`:

```text
╔════════════════════════════════════════╗
║  SysOptima Desktop Application v1.0    ║
║  System Performance Analysis Tool      ║
╚════════════════════════════════════════╝

🚀 TO RUN:
   Double-click: SysOptima/SysOptima.exe

📋 FEATURES:
   • Real-time system monitoring
   • Automatic diagnostics
   • AI assistant chat

📚 DOCUMENTATION:
   • README.md - Full documentation
   • QUICKSTART.md - Quick start guide

⚙️  OPTIONAL SETUP:
   Edit .env file to add Gemini API key
   for conversational AI features

✓ No installation required!
✓ Runs on Windows 7+
✓ No Python needed

Questions? See README.md
```

### Step 4: Create Installer (Optional)

Use Inno Setup or NSIS for professional installer:

```bash
# Download Inno Setup from: https://jrsoftware.org/isinfo.php
# Create: setup.iss
# Run: iscc setup.iss
```

Example `setup.iss`:
```ini
[Setup]
AppName=SysOptima
AppVersion=1.0.0
DefaultDirName={pf}\SysOptima
DefaultGroupName=SysOptima
SetupIconFile=icon.ico
OutputDir=installers
OutputBaseFilename=SysOptima_Setup_1.0.0

[Files]
Source: "dist_package\SysOptima\*"; DestDir: "{app}"; Flags: recursesubdirs

[Icons]
Name: "{group}\SysOptima"; Filename: "{app}\SysOptima.exe"
Name: "{group}\Uninstall"; Filename: "{uninstallexe}"

[Run]
Filename: "{app}\SysOptima.exe"; Flags: nowait
```

---

## Testing the Build

### Local Testing

```bash
# Navigate to dist folder
cd dist\SysOptima

# Run the executable
SysOptima.exe
```

### Deployment Testing

Test on clean Windows machine:
1. Copy `dist\SysOptima` folder to test machine
2. Run `SysOptima.exe`
3. Verify all features work
4. Check for any missing dependencies

### Common Issues During Testing

| Issue | Solution |
|-------|----------|
| "DLL not found" | Add to hidden_imports in spec |
| "Module not found" | Check if module is pure Python |
| "matplotlib not rendering" | Add matplotlib backends to hidden_imports |
| "Slow startup" | Normal for first run; UPX can help |

---

## Build Troubleshooting

### Problem: "ModuleNotFoundError when building"
```bash
# Solution: Add to hidden_imports in build.spec
hidden_imports=['module_name']

# Rebuild
pyinstaller build.spec
```

### Problem: "Executable won't start"
```bash
# Debug by running with console
pyinstaller --console --name="SysOptima_Debug" main.py
cd dist
SysOptima_Debug.exe
```

### Problem: "Executable too large"
```bash
# Solution 1: Use UPX
pip install upx
pyinstaller build.spec  # UPX will auto-compress

# Solution 2: Reduce included modules
# Edit build.spec and remove unused modules
```

### Problem: "GPU detection fails in executable"
```bash
# Add GPUtil to hidden_imports
hidden_imports=['GPUtil', 'pynvml']
```

---

## Version Updates

### For Version 1.1

1. Update version in `build.spec`:
   ```python
   # In EXE section:
   name='SysOptima_v1.1'
   ```

2. Update documentation:
   ```bash
   # Edit DESKTOP_APP_README.md
   # Change version references
   ```

3. Rebuild:
   ```bash
   pyinstaller build.spec
   ```

4. Tag in git (if using):
   ```bash
   git tag v1.1.0
   git push --tags
   ```

---

## Distribution Checklist

Before distributing, verify:

- [ ] Executable runs without Python installed
- [ ] All features work (monitor, diagnostics, AI)
- [ ] Charts display correctly
- [ ] Diagnostics generate appropriate alerts
- [ ] AI responds to queries (with and without API key)
- [ ] .env file (with API key example) included
- [ ] Documentation files included (README, QUICKSTART)
- [ ] Icon displays correctly (if added)
- [ ] File size is reasonable (<300MB with all dependencies)
- [ ] Tested on clean Windows machine

---

## Advanced: Multiple Python Versions

Build for both 32-bit and 64-bit:

```bash
# 64-bit build (current)
pyinstaller build.spec
rename dist\SysOptima dist\SysOptima_x64

# Switch to 32-bit Python (if available)
# Repeat build
pyinstaller build.spec
rename dist\SysOptima dist\SysOptima_x86
```

---

## Advanced: Code Signing (Professional)

For enterprise distribution:

```bash
# Sign executable with certificate
signtool sign /f certificate.pfx /p password /t http://timestamp.server SysOptima.exe

# Verify signature
signtool verify /pa SysOptima.exe
```

---

## Final Distribution

### Package Structure

```
SysOptima_v1.0_Release/
├── SysOptima/
│   └── SysOptima.exe
├── README.md
├── QUICKSTART.md
├── .env.example
└── START_HERE.txt
```

### Distribution Methods

1. **Direct Download**: Host on Google Drive, GitHub Releases
2. **Installer**: Use Inno Setup or NSIS
3. **Portable ZIP**: Users extract and run
4. **GitHub Releases**: Tag releases with builds

### Create GitHub Release

```bash
# Tag version
git tag -a v1.0.0 -m "SysOptima Desktop v1.0"

# Push tag
git push origin v1.0.0

# Upload dist/SysOptima folder as release asset
```

---

## Maintenance

### After Deployment

- Monitor user feedback
- Log common issues
- Plan improvements for v1.1
- Update documentation based on questions
- Consider adding auto-update feature

### Checklist for Next Version

- [ ] Review user feedback
- [ ] Update documentation
- [ ] Add new features
- [ ] Fix reported bugs
- [ ] Re-test all features
- [ ] Rebuild executable
- [ ] Create new release
- [ ] Update version number

---

## Quick Commands Reference

```bash
# Build standard
pyinstaller build.spec

# Build with console (debugging)
pyinstaller --console --name="SysOptima" main.py

# Clean build files
rmdir /s build dist
del SysOptima.spec

# Run built executable
dist\SysOptima\SysOptima.exe

# Check for missing modules before building
pip check
```

---

**Happy building! Your SysOptima desktop application is ready for distribution! 🚀**

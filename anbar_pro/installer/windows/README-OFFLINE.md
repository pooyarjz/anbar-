
# Offline Setup Builder (No Python needed on target)

This builds a full offline installer that bundles Python and all packages.

## Build steps (on your build PC)
1) Ensure Python 3.11 is installed (only needed to build).
2) Open PowerShell in project root and run:
```
installer/windows/build_offline_installer.ps1
```
What it does:
- Creates a virtualenv and installs requirements
- Copies the venv into `runtime/venv` (bundled Python)
- If Inno Setup is installed, compiles `AnbarPro_Offline.iss` and produces `AnbarPro-Setup-Offline.exe`

## Install on target PC
- Just run `AnbarPro-Setup-Offline.exe`
- After install, Start Menu → **Anbar Pro → Start Anbar Pro**
- Dashboard: `http://127.0.0.1:8000/`

## Notes
- Fully offline; no internet or Python needed on the target.

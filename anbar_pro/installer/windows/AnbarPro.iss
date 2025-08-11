;
 Inno Setup Script for Anbar Pro
#define MyAppName "Anbar Pro"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Anbar Co."
#define MyAppExeName "installer\windows\start_app.bat"

[Setup]
AppId={{65A36FCB-77C6-4D85-9E45-ABF8FA6A1C11}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={pf}\AnbarPro
DefaultGroupName=Anbar Pro
DisableDirPage=no
DisableProgramGroupPage=no
OutputDir=.
OutputBaseFilename=AnbarPro-Setup
SetupIconFile=installer\windows\anbar.ico
Compression=lzma
SolidCompression=yes
ArchitecturesInstallIn64BitMode=x64

[Languages]
Name: "farsi"; MessagesFile: "compiler:Languages\Farsi.isl"

[Files]
Source: "*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs ignoreversion

[Icons]
Name: "{group}\Start Anbar Pro"; Filename: "{app}\installer\windows\start_app.bat"; IconFilename: "{app}\installer\windows\anbar.ico"
Name: "{group}\Stop Anbar Pro"; Filename: "{app}\installer\windows\stop_app.bat"; IconFilename: "{app}\installer\windows\anbar.ico"
Name: "{group}\Open Reports (Browser)"; Filename: "http://127.0.0.1:8000/reports"
Name: "{group}\Uninstall {#MyAppName}"; Filename: "{uninstallexe}"
Name: "{commondesktop}\Anbar Pro"; Filename: "{app}\installer\windows\start_app.bat"; IconFilename: "{app}\installer\windows\anbar.ico"

[Run]
Filename: "powershell.exe"; Parameters: "-ExecutionPolicy Bypass -File ""{app}\installer\windows\post_install.ps1"""; Flags: postinstall runhidden; Description: "پیکربندی اولیه (اینترنت لازم است)"

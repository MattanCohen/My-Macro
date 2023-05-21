; Include the MUI2.nsh file to use the Modern User Interface
!include "MUI2.nsh"

; Set the name of the installer
Name "My Macro Installer"

; Set the output file name
OutFile "MyMacroInstaller.exe"

; Set the installation directory
InstallDir "C:\Users\User\Documents\MyMacro"

; Request application privileges for Windows Vista and higher
RequestExecutionLevel admin

; Pages to display
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES


; Languages to support
!insertmacro MUI_LANGUAGE "English"

Section "MainSection" SEC01

    ; Set the output path for the extracted filees
    SetOutPath $INSTDIR

    ; Extract the zip file to the installation directory
    File /r "my_macro.py"
    File /r "my_macro.vbs"
    File /r "runner.bat"

    ; Create shortcut to the vbs file to the shell:startup folder
    CreateShortCut "$SMSTARTUP\my_macro.lnk" "$INSTDIR\my_macro.vbs"
	
    ; Write the uninstaller
    WriteUninstaller "$INSTDIR\uninstall.exe"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\MyMacroInstaller" "DisplayName" "My Macro Installer"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\MyMacroInstaller" "UninstallString" '"$INSTDIR\uninstall.exe"'

SectionEnd



Section "Uninstall"
    ; Remove the installed files
    Delete "$INSTDIR\my_macro.py"
    Delete "$INSTDIR\my_macro.vbs"
    Delete "$INSTDIR\runner.bat"

    ; Remove the shortcut
    Delete "$SMSTARTUP\my_macro.lnk"

    ; Remove the installation directory
    RMDir /r "$INSTDIR"

    ; Remove the uninstaller
    Delete "$INSTDIR\uninstall.exe"

    ; Remove the registry key for the uninstaller
    DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\MyMacroInstaller"
SectionEnd
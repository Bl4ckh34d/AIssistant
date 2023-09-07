import helpers
import command_list as cl
import subprocess
import os
import pyautogui

# LOCATIONS
home_folder = os.environ['USERPROFILE']
program_files_folder = os.environ['ProgramFiles']
program_files_x86_folder = os.environ['ProgramFiles(x86)']

# APPLICATIONS
# Define the paths to the applications
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
firefox_path = r"C:\Program Files\Mozilla Firefox\firefox.exe"
explorer_path = "explorer.exe"
vlc_path = r"C:\Program Files (x86)\VideoLAN\VLC\vlc.exe"
mpc_path = r"C:\Program Files (x86)\K-Lite Codec Pack\MPC-HC64\mpc-hc64.exe"
keepass_path = r"C:\Program Files\KeePass Password Safe 2\KeePass.exe"
steam_path = r"C:\Program Files (x86)\Steam\steam.exe"
discord_path = r"C:\Users\ROG\AppData\Local\Discord\app-1.0.9017\Discord.exe"
word_path = r"C:\Program Files (x86)\Microsoft Office\Office12\WINWORD.EXE"
excel_path = r"C:\Program Files (x86)\Microsoft Office\Office12\EXCEL.EXE"
powerpoint_path = r"C:\Program Files (x86)\Microsoft Office\Office12\POWERPNT.EXE"
notepadpp_path = r"C:\Program Files\Notepad++\notepad++.exe"
vsc_path = r"C:\Program Files\Microsoft VS Code\Code.exe"
pureref_path = r"C:\Program Files\PureRef\PureRef.exe"
audacity_path = r"C:\Program Files\Audacity\Audacity.exe"
blender_path = r"C:\Program Files\Blender Foundation\Blender 3.6\blender.exe"
stablediffusion_path = r"D:\SD\run.bat"
calculator_path = r"C:\Windows\System32\calc.exe"

def check_for_command(message):
    # OPENING
    if helpers.check_for_keywords_from_list(cl.openingList,message) is not None:
        print(f"- - - {helpers.check_for_keywords_from_list(cl.openingList,message).upper()} - - -")
        
        # CHROME
        if helpers.check_for_keywords_from_list(cl.chromeList,message) is not None:
            print(f"- - - {helpers.check_for_keywords_from_list(cl.chromeList,message).upper()} - - -")
            subprocess.Popen([chrome_path])
        
        # EXPLORER
        if helpers.check_for_keywords_from_list(cl.explorerList,message) is not None:
            print(f"- - - {helpers.check_for_keywords_from_list(cl.explorerList,message).upper()} - - -")
            subprocess.Popen([explorer_path, "::{20D04FE0-3AEA-1069-A2D8-08002B30309D}"])
            
        # EXPLORER (C Drive)
        if helpers.check_for_keywords_from_list(cl.cDriveList,message) is not None:
            print(f"- - - {helpers.check_for_keywords_from_list(cl.cDriveList,message).upper()} - - -")
            subprocess.Popen([explorer_path, r"C:"])
        
        # EXPLORER (D Drive)
        if helpers.check_for_keywords_from_list(cl.dDriveList,message) is not None:
            print(f"- - - {helpers.check_for_keywords_from_list(cl.dDriveList,message).upper()} - - -")
            subprocess.Popen([explorer_path, r"D:"])
            
        # EXPLORER (AppData)
        if helpers.check_for_keywords_from_list(cl.appDataList,message) is not None:
            print(f"- - - {helpers.check_for_keywords_from_list(cl.appDataList,message).upper()} - - -")
            subprocess.Popen([explorer_path, home_folder + r"\AppData"])
            
        # EXPLORER (Programs)
        if helpers.check_for_keywords_from_list(cl.programsFolderList,message) is not None:
            # EXPLORER (Programs86)
            if helpers.check_for_keywords_from_list(cl.programs86FolderList,message) is not None:
                print(f"- - - {helpers.check_for_keywords_from_list(cl.programs86FolderList,message).upper()} - - -")
                subprocess.Popen([explorer_path, program_files_x86_folder])
            else:
                print(f"- - - {helpers.check_for_keywords_from_list(cl.programsFolderList,message).upper()} - - -")
                subprocess.Popen([explorer_path, program_files_folder])
                
        # EXPLORER (Home)
        if helpers.check_for_keywords_from_list(cl.homeFolderList,message) is not None:
            print(f"- - - {helpers.check_for_keywords_from_list(cl.homeFolderList,message).upper()} - - -")
            subprocess.Popen([explorer_path, home_folder])
        
        # FIREFOX
        if helpers.check_for_keywords_from_list(cl.firefoxList,message) is not None:
            # FIREFOX INCOGNITO
            if helpers.check_for_keywords_from_list(cl.incognitoList,message) is not None:
                print(f"- - - {helpers.check_for_keywords_from_list(cl.incognitoList,message).upper()} - - -")
                subprocess.Popen([firefox_path, "-private-window"])
            else:
                print(f"- - - {helpers.check_for_keywords_from_list(cl.firefoxList,message).upper()} - - -")
                subprocess.Popen([firefox_path])        
            
        # VLC
        if helpers.check_for_keywords_from_list(cl.vlcList,message) is not None:
            print(f"- - - {helpers.check_for_keywords_from_list(cl.vlcList,message).upper()} - - -")
            subprocess.Popen([vlc_path])
            
        # MEDIA PLAYER CLASSIC
        if helpers.check_for_keywords_from_list(cl.mpcList,message) is not None:
            print(f"- - - {helpers.check_for_keywords_from_list(cl.mpcList,message).upper()} - - -")
            subprocess.Popen([mpc_path])
            
        # KEEPASS
        if helpers.check_for_keywords_from_list(cl.keepassList,message) is not None:
            print(f"- - - {helpers.check_for_keywords_from_list(cl.keepassList,message).upper()} - - -")
            subprocess.Popen([keepass_path])
            
        # STEAM
        if helpers.check_for_keywords_from_list(cl.steamList,message) is not None:
            print(f"- - - {helpers.check_for_keywords_from_list(cl.steamList,message).upper()} - - -")
            subprocess.Popen([steam_path])
        
        # DISCORD
        if helpers.check_for_keywords_from_list(cl.discordList,message) is not None:
            print(f"- - - {helpers.check_for_keywords_from_list(cl.discordList,message).upper()} - - -")
            subprocess.Popen([discord_path])
            
        # MS WORD
        if helpers.check_for_keywords_from_list(cl.wordList,message) is not None:
            print(f"- - - {helpers.check_for_keywords_from_list(cl.wordList,message).upper()} - - -")
            subprocess.Popen([word_path])
        
        # MS EXCEL
        if helpers.check_for_keywords_from_list(cl.excelList,message) is not None:
            print(f"- - - {helpers.check_for_keywords_from_list(cl.excelList,message).upper()} - - -")
            subprocess.Popen([excel_path])
            
        # MS POWWERPOINT
        if helpers.check_for_keywords_from_list(cl.powerpointList,message) is not None:
            print(f"- - - {helpers.check_for_keywords_from_list(cl.powerpointList,message).upper()} - - -")
            subprocess.Popen([powerpoint_path])
        
        # NOTEPAD++
        if helpers.check_for_keywords_from_list(cl.notepadppList,message) is not None:
            print(f"- - - {helpers.check_for_keywords_from_list(cl.notepadppList,message).upper()} - - -")
            subprocess.Popen([notepadpp_path])
            
        # VSC
        if helpers.check_for_keywords_from_list(cl.vscList,message) is not None:
            print(f"- - - {helpers.check_for_keywords_from_list(cl.vscList,message).upper()} - - -")
            subprocess.Popen([vsc_path])
            
        # PUREREF
        if helpers.check_for_keywords_from_list(cl.purerefList,message) is not None:
            print(f"- - - {helpers.check_for_keywords_from_list(cl.purerefList,message).upper()} - - -")
            subprocess.Popen([pureref_path])
        
        # AUDACITY
        if helpers.check_for_keywords_from_list(cl.audacityList,message) is not None:
            print(f"- - - {helpers.check_for_keywords_from_list(cl.audacityList,message).upper()} - - -")
            subprocess.Popen([audacity_path])
        
        # BLENDER
        if helpers.check_for_keywords_from_list(cl.blenderList,message) is not None:
            print(f"- - - {helpers.check_for_keywords_from_list(cl.blenderList,message).upper()} - - -")
            subprocess.Popen([blender_path])
            
        # STABLE DIFFUSION
        if helpers.check_for_keywords_from_list(cl.stablediffusionList,message) is not None:
            print(f"- - - {helpers.check_for_keywords_from_list(cl.stablediffusionList,message).upper()} - - -")
            subprocess.Popen([stablediffusion_path])
            
        # CALCULATOR
        if helpers.check_for_keywords_from_list(cl.calculatorList,message) is not None:
            print(f"- - - {helpers.check_for_keywords_from_list(cl.calculatorList,message).upper()} - - -")
            subprocess.Popen([calculator_path])
            
        # SYSTEM SETTINGS
        if helpers.check_for_keywords_from_list(cl.controlList,message) is not None:
            print(f"- - - {helpers.check_for_keywords_from_list(cl.controlList,message).upper()} - - -")
            subprocess.Popen(["control.exe", "/name", "Microsoft.System"])
            
        # AUDIO SETTINGS
        if helpers.check_for_keywords_from_list(cl.audioList,message) is not None:
            print(f"- - - {helpers.check_for_keywords_from_list(cl.audioList,message).upper()} - - -")
            subprocess.Popen(["control", "mmsys.cpl"])
        
        # DISPLAY SETTINGS   
        if helpers.check_for_keywords_from_list(cl.videoList,message) is not None:
            print(f"- - - {helpers.check_for_keywords_from_list(cl.videoList,message).upper()} - - -")
            subprocess.Popen(["rundll32.exe", "shell32.dll,Control_RunDLL desk.cpl"])
            
        # DESKTOP SETTINGS   
        if helpers.check_for_keywords_from_list(cl.desktopList,message) is not None:
            print(f"- - - {helpers.check_for_keywords_from_list(cl.desktopList,message).upper()} - - -")
            subprocess.Popen(["control", "desk.cpl"])
            
            
            
    # CLOSING
    elif helpers.check_for_keywords_from_list(cl.closingList,message) is not None:
        print(f"- - - {helpers.check_for_keywords_from_list(cl.closingList,message).upper()} - - -")
        pyautogui.hotkey('alt', 'f4')
        # Close something like:
            # Program List
            # Folder List
            # Pretty much everyrhing
            # Tab
            
    # SWITCHING
    elif helpers.check_for_keywords_from_list(cl.switchingList,message) is not None:
        print(f"- - - {helpers.check_for_keywords_from_list(cl.switchingList,message).upper()} - - -")
        pyautogui.hotkey('alt', 'tab')
        # Switch something like:
            # Program List
            # Folder List
            # Pretty much everyrhing
            # Tab
            
    # MINIMIZING
    elif helpers.check_for_keywords_from_list(cl.minimizingList,message) is not None:
        print(f"- - - {helpers.check_for_keywords_from_list(cl.minimizingList,message).upper()} - - -")
        pyautogui.hotkey('win', 'down')
        # Minimize something like:
            # Program List
            # Folder List
            # Pretty much everyrhing
            # Tab
            
    # MAXIMIZING
    elif helpers.check_for_keywords_from_list(cl.maximizingList,message) is not None:
        print(f"- - - {helpers.check_for_keywords_from_list(cl.maximizingList,message).upper()} - - -")
        pyautogui.hotkey('win', 'up')
        # Maximize something like:
            # Program List
            # Folder List
            # Pretty much everyrhing
            # Tab
            
        
    # if message contains word from list of words, trigger next function tree
        # Youtube
        # Close Tab
        # Open Tab
        # Close Window
        # Switch Tab
        
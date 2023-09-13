import helpers
import command_list as cl
import variables as vars
import subprocess
import os
import pyautogui
import websockets
import asyncio
import re
import json
import pygetwindow as gw

# LOCATIONS
home_folder = os.environ['USERPROFILE']
download_folder = "Downloads"
my_computer_folder = "::{20D04FE0-3AEA-1069-A2D8-08002B30309D}"
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

async def send_command(message):
    async with websockets.connect("ws://localhost:3000") as websocket:
        pattern = r'\b(?:' + '|'.join(re.escape(word) for word in ["find", "tab"]) + r')\b'
        result_string = re.sub(pattern, '', message)
        command = {
            "command": "find_tab",
            "query": result_string
        }
        await websocket.send(json.dumps(command))  # Serialize the command to JSON
        response = await websocket.recv()
        try:
            response_data = json.loads(response)  # Deserialize the response JSON
            print("Matching tab titles:")
            for title in response_data:
                print(title)
        except json.JSONDecodeError as e:
            print("Error decoding JSON response:", e)
        print(f"- - - {task['object'].upper()} - - -")
        pyautogui.hotkey('win', 'up')
        # Maximize something like:
            # Program List
            # Folder List
            # Pretty much everyrhing
            # Tab

def check_for_command(message):
    # FIND FIREFOX EXTENSION
    if helpers.check_for_keywords_from_list(cl.findList,message) is not None:
        print(f"- - - {helpers.check_for_keywords_from_list(cl.findList,message).upper()} - - -")
        asyncio.get_event_loop().run_until_complete(send_command(message))
    
    # TYPE
    if helpers.check_for_keywords_from_list(cl.typingList,message) is not None:
        print(f"- - - {helpers.check_for_keywords_from_list(cl.typingList,message).upper()} - - -")
        # pyautogui.typewrite(STRING, interval=0.2)
            
    # OPENING
    if helpers.check_for_keywords_from_list(cl.openingList,message) is not None:
        print(f"- - - {helpers.check_for_keywords_from_list(cl.openingList,message).upper()} - - -")
        
        # EXPLORER
        if helpers.check_for_keywords_from_list(cl.explorerList,message) is not None and helpers.check_for_keywords_from_list(cl.tabList,message) is None:            
            # EXPLORER (C Drive)
            if helpers.check_for_keywords_from_list(cl.cDriveList,message) is not None:
                print(f"- - - {helpers.check_for_keywords_from_list(cl.cDriveList,message).upper()} - - -")
                subprocess.Popen([explorer_path, r"C:"])
            
            # EXPLORER (D Drive)
            elif helpers.check_for_keywords_from_list(cl.dDriveList,message) is not None:
                print(f"- - - {helpers.check_for_keywords_from_list(cl.dDriveList,message).upper()} - - -")
                subprocess.Popen([explorer_path, r"D:"])
                
            # EXPLORER (AppData)
            elif helpers.check_for_keywords_from_list(cl.appDataList,message) is not None:
                print(f"- - - {helpers.check_for_keywords_from_list(cl.appDataList,message).upper()} - - -")
                subprocess.Popen([explorer_path, home_folder + r"\AppData"])
                
            # EXPLORER (Programs)
            elif helpers.check_for_keywords_from_list(cl.programsFolderList,message) is not None:
                # EXPLORER (Programs86)
                if helpers.check_for_keywords_from_list(cl.programs86FolderList,message) is not None:
                    print(f"- - - {helpers.check_for_keywords_from_list(cl.programs86FolderList,message).upper()} - - -")
                    subprocess.Popen([explorer_path, program_files_x86_folder])
                else:
                    print(f"- - - {helpers.check_for_keywords_from_list(cl.programsFolderList,message).upper()} - - -")
                    subprocess.Popen([explorer_path, program_files_folder])
                    
            # EXPLORER (Home)
            elif helpers.check_for_keywords_from_list(cl.homeFolderList,message) is not None:
                print(f"- - - {helpers.check_for_keywords_from_list(cl.homeFolderList,message).upper()} - - -")
                subprocess.Popen([explorer_path, home_folder])
                
            # EXPLORER (Downloads)
            elif helpers.check_for_keywords_from_list(cl.downloadFolderList,message) is not None:
                print(f"- - - {helpers.check_for_keywords_from_list(cl.downloadFolderList,message).upper()} - - -")
                subprocess.Popen([explorer_path, download_folder])
            else:
                print(f"- - - {helpers.check_for_keywords_from_list(cl.explorerList,message).upper()} - - -")
                subprocess.Popen([explorer_path, my_computer_folder])
            
        # CHROME
        elif helpers.check_for_keywords_from_list(cl.chromeList,message) is not None:
            print(f"- - - {helpers.check_for_keywords_from_list(cl.chromeList,message).upper()} - - -")
            subprocess.Popen([chrome_path])
        
        # FIREFOX
        elif helpers.check_for_keywords_from_list(cl.firefoxList,message) is not None:
            # FIREFOX INCOGNITO
            if helpers.check_for_keywords_from_list(cl.incognitoList,message) is not None:
                print(f"- - - {helpers.check_for_keywords_from_list(cl.incognitoList,message).upper()} - - -")
                subprocess.Popen([firefox_path, "-private-window"])
            else:
                print(f"- - - {helpers.check_for_keywords_from_list(cl.firefoxList,message).upper()} - - -")
                subprocess.Popen([firefox_path])        
            
        # VLC
        elif helpers.check_for_keywords_from_list(cl.vlcList,message) is not None:
            print(f"- - - {helpers.check_for_keywords_from_list(cl.vlcList,message).upper()} - - -")
            subprocess.Popen([vlc_path])
            
        # MEDIA PLAYER CLASSIC
        elif helpers.check_for_keywords_from_list(cl.mpcList,message) is not None:
            print(f"- - - {helpers.check_for_keywords_from_list(cl.mpcList,message).upper()} - - -")
            subprocess.Popen([mpc_path])
            
        # KEEPASS
        elif helpers.check_for_keywords_from_list(cl.keepassList,message) is not None:
            print(f"- - - {helpers.check_for_keywords_from_list(cl.keepassList,message).upper()} - - -")
            subprocess.Popen([keepass_path])
            
        # STEAM
        elif helpers.check_for_keywords_from_list(cl.steamList,message) is not None:
            print(f"- - - {helpers.check_for_keywords_from_list(cl.steamList,message).upper()} - - -")
            subprocess.Popen([steam_path])
        
        # DISCORD
        elif helpers.check_for_keywords_from_list(cl.discordList,message) is not None:
            print(f"- - - {helpers.check_for_keywords_from_list(cl.discordList,message).upper()} - - -")
            subprocess.Popen([discord_path])
            
        # MS WORD
        elif helpers.check_for_keywords_from_list(cl.wordList,message) is not None:
            print(f"- - - {helpers.check_for_keywords_from_list(cl.wordList,message).upper()} - - -")
            subprocess.Popen([word_path])
        
        # MS EXCEL
        elif helpers.check_for_keywords_from_list(cl.excelList,message) is not None:
            print(f"- - - {helpers.check_for_keywords_from_list(cl.excelList,message).upper()} - - -")
            subprocess.Popen([excel_path])
            
        # MS POWWERPOINT
        elif helpers.check_for_keywords_from_list(cl.powerpointList,message) is not None:
            print(f"- - - {helpers.check_for_keywords_from_list(cl.powerpointList,message).upper()} - - -")
            subprocess.Popen([powerpoint_path])
        
        # NOTEPAD++
        elif helpers.check_for_keywords_from_list(cl.notepadppList,message) is not None:
            print(f"- - - {helpers.check_for_keywords_from_list(cl.notepadppList,message).upper()} - - -")
            subprocess.Popen([notepadpp_path])
            
        # VSC
        elif helpers.check_for_keywords_from_list(cl.vscList,message) is not None:
            print(f"- - - {helpers.check_for_keywords_from_list(cl.vscList,message).upper()} - - -")
            subprocess.Popen([vsc_path])
            
        # PUREREF
        elif helpers.check_for_keywords_from_list(cl.purerefList,message) is not None:
            print(f"- - - {helpers.check_for_keywords_from_list(cl.purerefList,message).upper()} - - -")
            subprocess.Popen([pureref_path])
        
        # AUDACITY
        elif helpers.check_for_keywords_from_list(cl.audacityList,message) is not None:
            print(f"- - - {helpers.check_for_keywords_from_list(cl.audacityList,message).upper()} - - -")
            subprocess.Popen([audacity_path])
        
        # BLENDER
        elif helpers.check_for_keywords_from_list(cl.blenderList,message) is not None:
            print(f"- - - {helpers.check_for_keywords_from_list(cl.blenderList,message).upper()} - - -")
            subprocess.Popen([blender_path])
            
        # STABLE DIFFUSION
        elif helpers.check_for_keywords_from_list(cl.stablediffusionList,message) is not None:
            print(f"- - - {helpers.check_for_keywords_from_list(cl.stablediffusionList,message).upper()} - - -")
            subprocess.Popen([stablediffusion_path])
            
        # CALCULATOR
        elif helpers.check_for_keywords_from_list(cl.calculatorList,message) is not None:
            print(f"- - - {helpers.check_for_keywords_from_list(cl.calculatorList,message).upper()} - - -")
            subprocess.Popen([calculator_path])
            
        # SYSTEM SETTINGS
        elif helpers.check_for_keywords_from_list(cl.controlList,message) is not None:
            print(f"- - - {helpers.check_for_keywords_from_list(cl.controlList,message).upper()} - - -")
            subprocess.Popen(["control.exe", "/name", "Microsoft.System"])
            
        # AUDIO SETTINGS
        elif helpers.check_for_keywords_from_list(cl.audioList,message) is not None:
            print(f"- - - {helpers.check_for_keywords_from_list(cl.audioList,message).upper()} - - -")
            subprocess.Popen(["control", "mmsys.cpl"])
        
        # DISPLAY SETTINGS   
        elif helpers.check_for_keywords_from_list(cl.videoList,message) is not None:
            print(f"- - - {helpers.check_for_keywords_from_list(cl.videoList,message).upper()} - - -")
            subprocess.Popen(["rundll32.exe", "shell32.dll,Control_RunDLL desk.cpl"])
            
        # DESKTOP SETTINGS   
        elif helpers.check_for_keywords_from_list(cl.desktopList,message) is not None:
            print(f"- - - {helpers.check_for_keywords_from_list(cl.desktopList,message).upper()} - - -")
            subprocess.Popen(["control", "desk.cpl"])
            
        # NEW TAB   
        elif helpers.check_for_keywords_from_list(cl.tabList,message) is not None:
            # FOLDER TAB
            if helpers.check_for_keywords_from_list(cl.folderList,message) is not None:
                print(f"- - - {helpers.check_for_keywords_from_list(cl.folderList,message).upper()} - - -")
                pyautogui.hotkey('ctrl', 't')
                pyautogui.hotkey('f4')
                if helpers.check_for_keywords_from_list(cl.downloadFolderList,message) is not None:
                    print(f"- - - {helpers.check_for_keywords_from_list(cl.downloadFolderList,message).upper()} - - -")
                    pyautogui.typewrite(download_folder, interval=vars.ai_type_speed)
                elif helpers.check_for_keywords_from_list(cl.homeFolderList,message) is not None:
                    print(f"- - - {helpers.check_for_keywords_from_list(cl.homeFolderList,message).upper()} - - -")
                    pyautogui.typewrite(home_folder, interval=vars.ai_type_speed)
                elif helpers.check_for_keywords_from_list(cl.programs86FolderList,message) is not None:
                    print(f"- - - {helpers.check_for_keywords_from_list(cl.programs86FolderList,message).upper()} - - -")
                    pyautogui.typewrite(program_files_x86_folder, interval=vars.ai_type_speed)
                elif helpers.check_for_keywords_from_list(cl.programsFolderList,message) is not None:
                    print(f"- - - {helpers.check_for_keywords_from_list(cl.programsFolderList,message).upper()} - - -")
                    pyautogui.typewrite(program_files_folder, interval=vars.ai_type_speed)
                elif helpers.check_for_keywords_from_list(cl.appDataList,message) is not None:
                    print(f"- - - {helpers.check_for_keywords_from_list(cl.appDataList,message).upper()} - - -")
                    pyautogui.typewrite(home_folder + r"\AppData", interval=vars.ai_type_speed)
                elif helpers.check_for_keywords_from_list(cl.dDriveList,message) is not None:
                    print(f"- - - {helpers.check_for_keywords_from_list(cl.dDriveList,message).upper()} - - -")
                    pyautogui.typewrite(r"D:", interval=vars.ai_type_speed)
                elif helpers.check_for_keywords_from_list(cl.cDriveList,message) is not None:
                    print(f"- - - {helpers.check_for_keywords_from_list(cl.cDriveList,message).upper()} - - -")
                    pyautogui.typewrite(r"C:", interval=vars.ai_type_speed)
                elif helpers.check_for_keywords_from_list(cl.myComputerList,message) is not None:
                    print(f"- - - {helpers.check_for_keywords_from_list(cl.myComputerList,message).upper()} - - -")
                    pyautogui.typewrite(my_computer_folder, interval=vars.ai_type_speed)
                else:
                    print(f"- - - MY COMPUTER: - - -")
                    pyautogui.typewrite(my_computer_folder, interval=vars.ai_type_speed)
                pyautogui.hotkey('enter')
            # BROWSER TAB
            elif helpers.check_for_keywords_from_list(cl.browserTabList,message) is not None and "Mozilla Firefox" in helpers.get_current_window_title():
                print(f"- - - {helpers.check_for_keywords_from_list(cl.browserTabList,message).upper()} - - -")
                pyautogui.hotkey('ctrl', 't')
            else:
                print(f"- - - NOTHING TO CREATE A TAB IN FOCUS - - -")
              
    # CLOSING
    elif helpers.check_for_keywords_from_list(cl.closingList,message) is not None:        
        # NEW TAB   
        if helpers.check_for_keywords_from_list(cl.tabList,message) is not None:
            print(f"- - - {helpers.check_for_keywords_from_list(cl.tabList,message).upper()} - - -")
            pyautogui.hotkey('ctrl', 'w')
        
        else:
            print(f"- - - {helpers.check_for_keywords_from_list(cl.closingList,message).upper()} - - -")
            pyautogui.hotkey('alt', 'f4')
            
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
            
    # MAXIMIZING
    elif helpers.check_for_keywords_from_list(cl.maximizingList,message) is not None:
        print(f"- - - {helpers.check_for_keywords_from_list(cl.maximizingList,message).upper()} - - -")
        pyautogui.hotkey('win', 'up')
            
        
    # if message contains word from list of words, trigger next function tree
        # Youtube
        # Close Tab
        # Open Tab
        # Close Window
        # Switch Tab
        
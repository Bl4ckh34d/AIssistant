import subprocess, os, pyautogui, re, json, keyboard, time
import command_list as cl, helpers as help, variables as vars

# LOCATIONS
home_folder = os.environ['USERPROFILE']
download_folder = "Downloads"
my_computer_folder = r"::{20D04FE0-3AEA-1069-A2D8-08002B30309D}"
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
discord_path = r"C:\Users\ROG\AppData\Local\Discord\app-1.0.9019\Discord.exe"
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

# FIREFOX EXTENSION
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

# CREATE PROCESS
def create_process(pid_collection, collection_name, word_list, message, path, params):
    print(f"- - - {help.check_for_keywords_from_list(word_list,message).upper()} - - -")
    help.gather_pids()
    if params is None:
        subprocess.Popen([path])    
    else:
        subprocess.Popen([path, params])
    help.find_pids(collection_name, pid_collection)

# EXECUTE COMMAND   
def check_for_command(message):
    action = []
    
    # FIND FIREFOX EXTENSION (WIP)
    if help.check_for_keywords_from_list(cl.findList,message) is not None:
        print(f"- - - {help.check_for_keywords_from_list(cl.findList,message).upper()} - - -")
        #asyncio.get_event_loop().run_until_complete(send_command(message))
        action.append(help.check_for_keywords_from_list(cl.findList,message).upper())
        
    # TYPE (WIP)
    if help.check_for_keywords_from_list(cl.typingList,message) is not None:
        print(f"- - - {help.check_for_keywords_from_list(cl.typingList,message).upper()} - - -")
        # pyautogui.typewrite(STRING, interval=0.2)
        action.append(help.check_for_keywords_from_list(cl.typingList,message).upper())
    
    # SCROLL
    if help.check_for_keywords_from_list(cl.scrollList,message) is not None:
        print(f"- - - {help.check_for_keywords_from_list(cl.scrollList,message).upper()} - - -")
        
        # UP
        if help.check_for_keywords_from_list(cl.upList,message) is not None:
            print(f"- - - {help.check_for_keywords_from_list(cl.upList,message).upper()} - - -")
            pyautogui.scroll(400)
            action.append(help.check_for_keywords_from_list(cl.scrollList,message).upper() + " " + help.check_for_keywords_from_list(cl.upList,message).upper())
            
        
        # DOWN
        if help.check_for_keywords_from_list(cl.downList,message) is not None:
            print(f"- - - {help.check_for_keywords_from_list(cl.downList,message).upper()} - - -")
            pyautogui.scroll(-400)
            action.append(help.check_for_keywords_from_list(cl.scrollList,message).upper() + " " + help.check_for_keywords_from_list(cl.downList,message))

    
    # GO TO
    if help.check_for_keywords_from_list(cl.gotoList,message) is not None:
        print(f"- - - {help.check_for_keywords_from_list(cl.gotoList,message).upper()} - - -")
        
        # DESKTOP
        if help.check_for_keywords_from_list(cl.desktopList,message) is not None and help.check_for_keywords_from_list(cl.tabList,message) is None:            
            print(f"- - - {help.check_for_keywords_from_list(cl.desktopList,message).upper()} - - -")
            pyautogui.hotkey('win', 'd')
            action.append(help.check_for_keywords_from_list(cl.gotoList,message).upper() + " " + help.check_for_keywords_from_list(cl.desktopList,message))

        
        # EXPLORER
        if help.check_for_keywords_from_list(cl.explorerList,message) is not None and help.check_for_keywords_from_list(cl.tabList,message) is None:            
            print(f"- - - {help.check_for_keywords_from_list(cl.explorerList,message).upper()} - - -")
            help.focus_pids(vars.folders, "Explorer")
            action.append(help.check_for_keywords_from_list(cl.gotoList,message).upper() + " " + help.check_for_keywords_from_list(cl.explorerList,message))

            
        # CHROME
        elif help.check_for_keywords_from_list(cl.chromeList,message) is not None:
            print(f"- - - {help.check_for_keywords_from_list(cl.chromeList,message).upper()} - - -")
            help.focus_pids(vars.chrome, "Chrome")
            action.append(help.check_for_keywords_from_list(cl.gotoList,message).upper() + " " + help.check_for_keywords_from_list(cl.chromeList,message))

            
        # FIREFOX
        elif help.check_for_keywords_from_list(cl.firefoxList,message) is not None:
            # FIREFOX INCOGNITO
            if help.check_for_keywords_from_list(cl.incognitoList,message) is not None:
                print(f"- - - {help.check_for_keywords_from_list(cl.incognitoList,message).upper()} - - -")
                help.focus_pids(vars.firefoxincognito, "Firefox")
                action.append(help.check_for_keywords_from_list(cl.gotoList,message).upper() + " " + help.check_for_keywords_from_list(cl.incognitoList,message))

            else:
                print(f"- - - {help.check_for_keywords_from_list(cl.firefoxList,message).upper()} - - -")
                help.focus_pids(vars.firefox, "Firefox")
                action.append(help.check_for_keywords_from_list(cl.gotoList,message).upper() + " " + help.check_for_keywords_from_list(cl.firefoxList,message))

                
        # VLC
        elif help.check_for_keywords_from_list(cl.vlcList,message) is not None:
            print(f"- - - {help.check_for_keywords_from_list(cl.vlcList,message).upper()} - - -")
            help.focus_pids(vars.vlc, "VLC")
            action.append(help.check_for_keywords_from_list(cl.gotoList,message).upper() + " " + help.check_for_keywords_from_list(cl.vlcList,message))

            
        # MEDIA PLAYER CLASSIC
        elif help.check_for_keywords_from_list(cl.mpcList,message) is not None:
            print(f"- - - {help.check_for_keywords_from_list(cl.mpcList,message).upper()} - - -")
            help.focus_pids(vars.mpc, "MPC")
            action.append(help.check_for_keywords_from_list(cl.gotoList,message).upper() + " " + help.check_for_keywords_from_list(cl.mpcList,message))
            
        # KEEPASS
        elif help.check_for_keywords_from_list(cl.keepassList,message) is not None:
            print(f"- - - {help.check_for_keywords_from_list(cl.keepassList,message).upper()} - - -")
            help.focus_pids(vars.keepass, "KeePass")
            action.append(help.check_for_keywords_from_list(cl.gotoList,message).upper() + " " + help.check_for_keywords_from_list(cl.keepassList,message))
            
        # STEAM
        elif help.check_for_keywords_from_list(cl.steamList,message) is not None:
            print(f"- - - {help.check_for_keywords_from_list(cl.steamList,message).upper()} - - -")
            help.focus_pids(vars.steam, "Steam")
            action.append(help.check_for_keywords_from_list(cl.gotoList,message).upper() + " " + help.check_for_keywords_from_list(cl.steamList,message))
            
        # DISCORD
        elif help.check_for_keywords_from_list(cl.discordList,message) is not None:
            print(f"- - - {help.check_for_keywords_from_list(cl.discordList,message).upper()} - - -")
            help.focus_pids(vars.discord, "Discord")
            action.append(help.check_for_keywords_from_list(cl.gotoList,message).upper() + " " + help.check_for_keywords_from_list(cl.discordList,message))

        # MS WORD
        elif help.check_for_keywords_from_list(cl.wordList,message) is not None:
            print(f"- - - {help.check_for_keywords_from_list(cl.wordList,message).upper()} - - -")
            help.focus_pids(vars.ms_word, "Winword")
            action.append(help.check_for_keywords_from_list(cl.gotoList,message).upper() + " " + help.check_for_keywords_from_list(cl.wordList,message))

        # MS EXCEL
        elif help.check_for_keywords_from_list(cl.excelList,message) is not None:
            print(f"- - - {help.check_for_keywords_from_list(cl.excelList,message).upper()} - - -")
            help.focus_pids(vars.ms_excel, "Excel")
            action.append(help.check_for_keywords_from_list(cl.gotoList,message).upper() + " " + help.check_for_keywords_from_list(cl.excelList,message))
            
        # MS POWERPOINT
        elif help.check_for_keywords_from_list(cl.powerpointList,message) is not None:
            print(f"- - - {help.check_for_keywords_from_list(cl.powerpointList,message).upper()} - - -")
            help.focus_pids(vars.ms_pp, "Powerpnt")
            action.append(help.check_for_keywords_from_list(cl.gotoList,message).upper() + " " + help.check_for_keywords_from_list(cl.powerpointList,message))
            
        # NOTEPAD++
        elif help.check_for_keywords_from_list(cl.notepadppList,message) is not None:
            print(f"- - - {help.check_for_keywords_from_list(cl.notepadppList,message).upper()} - - -")
            help.focus_pids(vars.npp, "Notepad++")
            action.append(help.check_for_keywords_from_list(cl.gotoList,message).upper() + " " + help.check_for_keywords_from_list(cl.notepadppList,message))
               
        # VISUAL STUDIO CODE
        elif help.check_for_keywords_from_list(cl.vscList,message) is not None:
            print(f"- - - {help.check_for_keywords_from_list(cl.vscList,message).upper()} - - -")
            help.focus_pids(vars.vsc, "Code.exe")
            action.append(help.check_for_keywords_from_list(cl.gotoList,message).upper() + " " + help.check_for_keywords_from_list(cl.vscList,message))
              
        # PUREREF
        elif help.check_for_keywords_from_list(cl.purerefList,message) is not None:
            print(f"- - - {help.check_for_keywords_from_list(cl.purerefList,message).upper()} - - -")
            help.focus_pids(vars.pureref, "PureRef")
            action.append(help.check_for_keywords_from_list(cl.gotoList,message).upper() + " " + help.check_for_keywords_from_list(cl.purerefList,message))
            
        # AUDACITY
        elif help.check_for_keywords_from_list(cl.audacityList,message) is not None:
            print(f"- - - {help.check_for_keywords_from_list(cl.audacityList,message).upper()} - - -")
            help.focus_pids(vars.audacity, "Audacity")
            action.append(help.check_for_keywords_from_list(cl.gotoList,message).upper() + " " + help.check_for_keywords_from_list(cl.audacityList,message))
        
        # BLENDER
        elif help.check_for_keywords_from_list(cl.blenderList,message) is not None:
            print(f"- - - {help.check_for_keywords_from_list(cl.blenderList,message).upper()} - - -")
            help.focus_pids(vars.blender, "Blender")
            action.append(help.check_for_keywords_from_list(cl.gotoList,message).upper() + " " + help.check_for_keywords_from_list(cl.blenderList,message))
            
        # STABLE DIFFUSION
        elif help.check_for_keywords_from_list(cl.stablediffusionList,message) is not None:
            print(f"- - - {help.check_for_keywords_from_list(cl.stablediffusionList,message).upper()} - - -")
            help.focus_pids(vars.stablediffusion, "Stable Diffusion")
            action.append(help.check_for_keywords_from_list(cl.gotoList,message).upper() + " " + help.check_for_keywords_from_list(cl.stablediffusionList,message))
            
        # CALCULATOR
        elif help.check_for_keywords_from_list(cl.calculatorList,message) is not None:
            print(f"- - - {help.check_for_keywords_from_list(cl.calculatorList,message).upper()} - - -")
            help.focus_pids(vars.calc, "Rechner")
            action.append(help.check_for_keywords_from_list(cl.gotoList,message).upper() + " " + help.check_for_keywords_from_list(cl.calculatorList,message))
              
    # OPENING
    if help.check_for_keywords_from_list(cl.openingList,message) is not None:
        print(f"- - - {help.check_for_keywords_from_list(cl.openingList,message).upper()} - - -")
        
        # EXPLORER
        if help.check_for_keywords_from_list(cl.explorerList,message) is not None and help.check_for_keywords_from_list(cl.tabList,message) is None:            
            # EXPLORER (C Drive)
            if help.check_for_keywords_from_list(cl.cDriveList,message) is not None:
                create_process(vars.folders, "Explorer", cl.cDriveList, message, explorer_path, r"C:")
                action.append(help.check_for_keywords_from_list(cl.openingList,message).upper() + " " + help.check_for_keywords_from_list(cl.explorerList,message) + " at " +help.check_for_keywords_from_list(cl.cDriveList,message))
            
            # EXPLORER (D Drive)
            elif help.check_for_keywords_from_list(cl.dDriveList,message) is not None:
                create_process(vars.folders, "Explorer", cl.dDriveList, message, explorer_path, r"D:")
                action.append(help.check_for_keywords_from_list(cl.openingList,message).upper() + " " + help.check_for_keywords_from_list(cl.explorerList,message) + " at " +help.check_for_keywords_from_list(cl.dDriveList,message))

                
            # EXPLORER (AppData)
            elif help.check_for_keywords_from_list(cl.appDataList,message) is not None:
                create_process(vars.folders, "Explorer", cl.appDataList, message, explorer_path, home_folder + r"\AppData")
                action.append(help.check_for_keywords_from_list(cl.openingList,message).upper() + " " + help.check_for_keywords_from_list(cl.explorerList,message) + " at " +help.check_for_keywords_from_list(cl.appDataList,message))
                
            # EXPLORER (Programs)
            elif help.check_for_keywords_from_list(cl.programsFolderList,message) is not None:
                # EXPLORER (Programs86)
                if help.check_for_keywords_from_list(cl.programs86FolderList,message) is not None:
                    create_process(vars.folders, "Explorer", cl.programs86FolderList, message, explorer_path, program_files_x86_folder)
                    action.append(help.check_for_keywords_from_list(cl.openingList,message).upper() + " " + help.check_for_keywords_from_list(cl.explorerList,message) + " at " +help.check_for_keywords_from_list(cl.programs86FolderList,message))
                else:
                    create_process(vars.folders, "Explorer", cl.programsFolderList, message, explorer_path, program_files_folder)
                    action.append(help.check_for_keywords_from_list(cl.openingList,message).upper() + " " + help.check_for_keywords_from_list(cl.explorerList,message) + " at " +help.check_for_keywords_from_list(cl.programsFolderList,message))
            # EXPLORER (Home)
            elif help.check_for_keywords_from_list(cl.homeFolderList,message) is not None:
                create_process(vars.folders, "Explorer", cl.homeFolderList, message, explorer_path, home_folder)
                action.append(help.check_for_keywords_from_list(cl.openingList,message).upper() + " " + help.check_for_keywords_from_list(cl.explorerList,message) + " at " +help.check_for_keywords_from_list(cl.homeFolderList,message))
                
            # EXPLORER (Downloads)
            elif help.check_for_keywords_from_list(cl.downloadFolderList,message) is not None:
                create_process(vars.folders, "Explorer", cl.downloadFolderList, message, explorer_path, download_folder)
                action.append(help.check_for_keywords_from_list(cl.openingList,message).upper() + " " + help.check_for_keywords_from_list(cl.explorerList,message) + " at " +help.check_for_keywords_from_list(cl.downloadFolderList,message))
            else:
                create_process(vars.folders, "Explorer", cl.explorerList, message, explorer_path, my_computer_folder)
                action.append(help.check_for_keywords_from_list(cl.openingList,message).upper() + " " + help.check_for_keywords_from_list(cl.explorerList,message) + " at " +help.check_for_keywords_from_list(cl.myComputerList,message))
            
        # CHROME
        elif help.check_for_keywords_from_list(cl.chromeList,message) is not None:
            create_process(vars.chrome, "Chrome", cl.chromeList, message, chrome_path, None)
            action.append(help.check_for_keywords_from_list(cl.openingList,message).upper() + " " + help.check_for_keywords_from_list(cl.chromeList,message))
        
        # FIREFOX
        elif help.check_for_keywords_from_list(cl.firefoxList,message) is not None:
            # FIREFOX INCOGNITO
            if help.check_for_keywords_from_list(cl.incognitoList,message) is not None:
                create_process(vars.firefoxincognito, "Firefox", cl.incognitoList, message, firefox_path, "-private-window")
                action.append(help.check_for_keywords_from_list(cl.openingList,message).upper() + " " + help.check_for_keywords_from_list(cl.incognitoList,message))

            else:
                create_process(vars.firefox, "Firefox", cl.firefoxList, message, firefox_path, None)   
                action.append(help.check_for_keywords_from_list(cl.openingList,message).upper() + " " + help.check_for_keywords_from_list(cl.firefoxList,message))
            
        # VLC
        elif help.check_for_keywords_from_list(cl.vlcList,message) is not None:
            create_process(vars.vlc, "VLC", cl.vlcList, message, vlc_path, None)
            action.append(help.check_for_keywords_from_list(cl.openingList,message).upper() + " " + help.check_for_keywords_from_list(cl.vlcList,message))
            
        # MEDIA PLAYER CLASSIC
        elif help.check_for_keywords_from_list(cl.mpcList,message) is not None:
            create_process(vars.mpc, "MPC", cl.mpcList, message, mpc_path, None)
            action.append(help.check_for_keywords_from_list(cl.openingList,message).upper() + " " + help.check_for_keywords_from_list(cl.mpcList,message))
            
        # KEEPASS
        elif help.check_for_keywords_from_list(cl.keepassList,message) is not None:
            create_process(vars.keepass, "KeePass", cl.keepassList, message, keepass_path, None)
            action.append(help.check_for_keywords_from_list(cl.openingList,message).upper() + " " + help.check_for_keywords_from_list(cl.keepassList,message))
            
        # STEAM
        elif help.check_for_keywords_from_list(cl.steamList,message) is not None:
            create_process(vars.steam, "Steam", cl.steamList, message, steam_path, None)
            action.append(help.check_for_keywords_from_list(cl.openingList,message).upper() + " " + help.check_for_keywords_from_list(cl.steamList,message))
        
        # DISCORD
        elif help.check_for_keywords_from_list(cl.discordList,message) is not None:
            create_process(vars.discord, "Discord", cl.discordList, message, discord_path, None)
            action.append(help.check_for_keywords_from_list(cl.openingList,message).upper() + " " + help.check_for_keywords_from_list(cl.discordList,message))
            
        # MS WORD
        elif help.check_for_keywords_from_list(cl.wordList,message) is not None:
            create_process(vars.ms_word, "Winword", cl.wordList, message, word_path, None)
            action.append(help.check_for_keywords_from_list(cl.openingList,message).upper() + " " + help.check_for_keywords_from_list(cl.wordList,message))
        
        # MS EXCEL
        elif help.check_for_keywords_from_list(cl.excelList,message) is not None:
            create_process(vars.ms_excel, "Excel", cl.excelList, message, excel_path, None)
            action.append(help.check_for_keywords_from_list(cl.openingList,message).upper() + " " + help.check_for_keywords_from_list(cl.excelList,message))
            
        # MS POWERPOINT
        elif help.check_for_keywords_from_list(cl.powerpointList,message) is not None:
            create_process(vars.ms_pp, "Powerpnt", cl.powerpointList, message, powerpoint_path, None)
            action.append(help.check_for_keywords_from_list(cl.openingList,message).upper() + " " + help.check_for_keywords_from_list(cl.powerpointList,message))
        
        # NOTEPAD++
        elif help.check_for_keywords_from_list(cl.notepadppList,message) is not None:
            create_process(vars.npp, "Notepad++", cl.notepadppList, message, notepadpp_path, None)
            action.append(help.check_for_keywords_from_list(cl.openingList,message).upper() + " " + help.check_for_keywords_from_list(cl.notepadppList,message))
            
        # VISUAL STUDIO CODE
        elif help.check_for_keywords_from_list(cl.vscList,message) is not None:
            create_process(vars.vsc, "Code.exe", cl.vscList, message, vsc_path, None)
            action.append(help.check_for_keywords_from_list(cl.openingList,message).upper() + " " + help.check_for_keywords_from_list(cl.vscList,message))
            
        # PUREREF
        elif help.check_for_keywords_from_list(cl.purerefList,message) is not None:
            create_process(vars.pureref, "PureRef", cl.purerefList, message, pureref_path, None)
            action.append(help.check_for_keywords_from_list(cl.openingList,message).upper() + " " + help.check_for_keywords_from_list(cl.purerefList,message))
        
        # AUDACITY
        elif help.check_for_keywords_from_list(cl.audacityList,message) is not None:
            create_process(vars.audacity, "Audacity", cl.audacityList, message, audacity_path, None)
            action.append(help.check_for_keywords_from_list(cl.openingList,message).upper() + " " + help.check_for_keywords_from_list(cl.audacityList,message))
        
        # BLENDER
        elif help.check_for_keywords_from_list(cl.blenderList,message) is not None:
            create_process(vars.blender, "Blender", cl.blenderList, message, blender_path, None)
            action.append(help.check_for_keywords_from_list(cl.openingList,message).upper() + " " + help.check_for_keywords_from_list(cl.blenderList,message))
            
        # STABLE DIFFUSION
        elif help.check_for_keywords_from_list(cl.stablediffusionList,message) is not None:
            create_process(vars.stablediffusion, "Stable Diffusion", cl.stablediffusionList, message, stablediffusion_path, None)
            action.append(help.check_for_keywords_from_list(cl.openingList,message).upper() + " " + help.check_for_keywords_from_list(cl.stablediffusionList,message))
            
        # CALCULATOR
        elif help.check_for_keywords_from_list(cl.calculatorList,message) is not None:
            create_process(vars.calc, "Rechner", cl.calculatorList, message, calculator_path, None)
            action.append(help.check_for_keywords_from_list(cl.openingList,message).upper() + " " + help.check_for_keywords_from_list(cl.calculatorList,message))
            
        # SYSTEM SETTINGS
        elif help.check_for_keywords_from_list(cl.controlList,message) is not None:
            print(f"- - - {help.check_for_keywords_from_list(cl.controlList,message).upper()} - - -")
            subprocess.Popen(["control.exe", "/name", "Microsoft.System"])
            action.append(help.check_for_keywords_from_list(cl.openingList,message).upper() + " " + help.check_for_keywords_from_list(cl.controlList,message))
            
        # AUDIO SETTINGS
        #elif help.check_for_keywords_from_list(cl.audioList,message) is not None:
            #create_process(cl.audioList, message, "control", "mmsys.cpl")
            #action.append(help.check_for_keywords_from_list(cl.openingList,message).upper() + " " + help.check_for_keywords_from_list(cl.audioList,message))
        
        # DISPLAY SETTINGS   
        #elif help.check_for_keywords_from_list(cl.videoList,message) is not None:
            #create_process(cl.videoList, message, "rundll32.exe", "shell32.dll,Control_RunDLL desk.cpl")
            #action.append(help.check_for_keywords_from_list(cl.openingList,message).upper() + " " + help.check_for_keywords_from_list(cl.videoList,message))
            
        # DESKTOP SETTINGS   
        #elif help.check_for_keywords_from_list(cl.desktopList,message) is not None:
            #create_process(cl.desktopList, message, "control", "desk.cpl")
            #action.append(help.check_for_keywords_from_list(cl.openingList,message).upper() + " " + help.check_for_keywords_from_list(cl.desktopList,message))
            
        # NEW TAB   
        elif help.check_for_keywords_from_list(cl.tabList,message) is not None:
            # FOLDER TAB
            if help.check_for_keywords_from_list(cl.folderList,message) is not None:
                print(f"- - - {help.check_for_keywords_from_list(cl.folderList,message).upper()} - - -")
                pyautogui.hotkey('ctrl', 't')
                pyautogui.hotkey('f4')
                time.sleep(0.1)
                if help.check_for_keywords_from_list(cl.downloadFolderList,message) is not None:
                    print(f"- - - {help.check_for_keywords_from_list(cl.downloadFolderList,message).upper()} - - -")
                    pyautogui.hotkey('ctrl', 'a')
                    pyautogui.hotkey('del')
                    pyautogui.typewrite(download_folder, interval=vars.llm_type_speed)
                    action.append(help.check_for_keywords_from_list(cl.openingList,message).upper() + " " + help.check_for_keywords_from_list(cl.folderList,message) + " " + help.check_for_keywords_from_list(cl.tabList,message) + " at " + help.check_for_keywords_from_list(cl.downloadFolderList,message))
                elif help.check_for_keywords_from_list(cl.homeFolderList,message) is not None:
                    print(f"- - - {help.check_for_keywords_from_list(cl.homeFolderList,message).upper()} - - -")
                    pyautogui.hotkey('ctrl', 'a')
                    pyautogui.hotkey('del')
                    pyautogui.typewrite(home_folder, interval=vars.llm_type_speed)
                    action.append(help.check_for_keywords_from_list(cl.openingList,message).upper() + " " + help.check_for_keywords_from_list(cl.folderList,message) + " " + help.check_for_keywords_from_list(cl.tabList,message) + " at " + help.check_for_keywords_from_list(cl.homeFolderList,message))
                elif help.check_for_keywords_from_list(cl.programs86FolderList,message) is not None:
                    print(f"- - - {help.check_for_keywords_from_list(cl.programs86FolderList,message).upper()} - - -")
                    pyautogui.hotkey('ctrl', 'a')
                    pyautogui.hotkey('del')
                    pyautogui.typewrite(program_files_x86_folder, interval=vars.llm_type_speed)
                    action.append(help.check_for_keywords_from_list(cl.openingList,message).upper() + " " + help.check_for_keywords_from_list(cl.folderList,message) + " " + help.check_for_keywords_from_list(cl.tabList,message) + " at " + help.check_for_keywords_from_list(cl.programs86FolderList,message))
                elif help.check_for_keywords_from_list(cl.programsFolderList,message) is not None:
                    print(f"- - - {help.check_for_keywords_from_list(cl.programsFolderList,message).upper()} - - -")
                    pyautogui.hotkey('ctrl', 'a')
                    pyautogui.hotkey('del')
                    pyautogui.typewrite(program_files_folder, interval=vars.llm_type_speed)
                    action.append(help.check_for_keywords_from_list(cl.openingList,message).upper() + " " + help.check_for_keywords_from_list(cl.folderList,message) + " " + help.check_for_keywords_from_list(cl.tabList,message) + " at " + help.check_for_keywords_from_list(cl.programsFolderList,message))
                elif help.check_for_keywords_from_list(cl.appDataList,message) is not None:
                    print(f"- - - {help.check_for_keywords_from_list(cl.appDataList,message).upper()} - - -")
                    pyautogui.hotkey('ctrl', 'a')
                    pyautogui.hotkey('del')
                    pyautogui.typewrite(home_folder + r"\AppData", interval=vars.llm_type_speed)
                    action.append(help.check_for_keywords_from_list(cl.openingList,message).upper() + " " + help.check_for_keywords_from_list(cl.folderList,message) + " " + help.check_for_keywords_from_list(cl.tabList,message) + " at " + help.check_for_keywords_from_list(cl.appDataList,message))
                elif help.check_for_keywords_from_list(cl.dDriveList,message) is not None:
                    print(f"- - - {help.check_for_keywords_from_list(cl.dDriveList,message).upper()} - - -")
                    pyautogui.hotkey('ctrl', 'a')
                    pyautogui.hotkey('del')
                    pyautogui.typewrite(r"D:", interval=vars.llm_type_speed)
                    action.append(help.check_for_keywords_from_list(cl.openingList,message).upper() + " " + help.check_for_keywords_from_list(cl.folderList,message) + " " + help.check_for_keywords_from_list(cl.tabList,message) + " at " + help.check_for_keywords_from_list(cl.dDriveList,message))
                elif help.check_for_keywords_from_list(cl.cDriveList,message) is not None:
                    print(f"- - - {help.check_for_keywords_from_list(cl.cDriveList,message).upper()} - - -")
                    pyautogui.hotkey('ctrl', 'a')
                    pyautogui.hotkey('del')
                    pyautogui.typewrite(r"C:", interval=vars.llm_type_speed)
                    action.append(help.check_for_keywords_from_list(cl.openingList,message).upper() + " " + help.check_for_keywords_from_list(cl.folderList,message) + " " + help.check_for_keywords_from_list(cl.tabList,message) + " at " + help.check_for_keywords_from_list(cl.cDriveList,message))
                elif help.check_for_keywords_from_list(cl.myComputerList,message) is not None:
                    print(f"- - - {help.check_for_keywords_from_list(cl.myComputerList,message).upper()} - - -")
                    pyautogui.hotkey('ctrl', 'a')
                    pyautogui.press('del')
                    keyboard.write(my_computer_folder)
                    action.append(help.check_for_keywords_from_list(cl.openingList,message).upper() + " " + help.check_for_keywords_from_list(cl.folderList,message) + " " + help.check_for_keywords_from_list(cl.tabList,message) + " at " + help.check_for_keywords_from_list(cl.myComputerList,message))
                else:
                    print(f"- - - MY COMPUTER: - - -")
                    pyautogui.hotkey('ctrl', 'a')
                    pyautogui.press('del')
                    keyboard.write(my_computer_folder)
                    action.append(help.check_for_keywords_from_list(cl.openingList,message).upper() + " " + help.check_for_keywords_from_list(cl.folderList,message) + " " + help.check_for_keywords_from_list(cl.tabList,message) + " at " + help.check_for_keywords_from_list(cl.myComputerList,message))
                pyautogui.hotkey('enter')
            # BROWSER TAB
            elif help.check_for_keywords_from_list(cl.browserTabList,message) is not None and "Mozilla Firefox" in help.get_current_window_title():
                print(f"- - - {help.check_for_keywords_from_list(cl.browserTabList,message).upper()} - - -")
                pyautogui.hotkey('ctrl', 't')
                action.append(help.check_for_keywords_from_list(cl.openingList,message).upper() + " " + help.check_for_keywords_from_list(cl.browserTabList,message))
            else:
                print(f"- - - NOTHING TO CREATE A TAB IN FOCUS - - -")
              
    # CLOSING
    elif help.check_for_keywords_from_list(cl.closingList,message) is not None:
        print(f"- - - {help.check_for_keywords_from_list(cl.closingList,message).upper()} - - -")
        # TAB   
        if help.check_for_keywords_from_list(cl.tabList,message) is not None:
            print(f"- - - {help.check_for_keywords_from_list(cl.tabList,message).upper()} - - -")
            pyautogui.hotkey('ctrl', 'w')
            action.append(help.check_for_keywords_from_list(cl.closingList,message).upper() + " " + help.check_for_keywords_from_list(cl.tabList,message))

        # EXPLORER
        elif help.check_for_keywords_from_list(cl.explorerList,message) is not None:
            print(f"- - - {help.check_for_keywords_from_list(cl.explorerList,message).upper()} - - -")
            help.close_pids(vars.folders, "Explorer")
            action.append(help.check_for_keywords_from_list(cl.closingList,message).upper() + " " + help.check_for_keywords_from_list(cl.explorerList,message))
        # CHROME
        elif help.check_for_keywords_from_list(cl.chromeList,message) is not None:
            print(f"- - - {help.check_for_keywords_from_list(cl.chromeList,message).upper()} - - -")
            help.close_pids(vars.chrome, "Chrome")
            action.append(help.check_for_keywords_from_list(cl.closingList,message).upper() + " " + help.check_for_keywords_from_list(cl.chromeList,message))
        # FIREFOX
        elif help.check_for_keywords_from_list(cl.firefoxList,message) is not None:
            print(f"- - - {help.check_for_keywords_from_list(cl.firefoxList,message).upper()} - - -")
            if help.check_for_keywords_from_list(cl.incognitoList,message) is not None:
                print(f"- - - {help.check_for_keywords_from_list(cl.incognitoList,message).upper()} - - -")
                help.close_pids(vars.firefoxincognito, "Firefox")
                action.append(help.check_for_keywords_from_list(cl.closingList,message).upper() + " " + help.check_for_keywords_from_list(cl.incognitoList,message))
            else:
                help.close_pids(vars.firefox, "Firefox")
                action.append(help.check_for_keywords_from_list(cl.closingList,message).upper() + " " + help.check_for_keywords_from_list(cl.firefoxList,message))
        # VLC
        elif help.check_for_keywords_from_list(cl.vlcList,message) is not None:
            print(f"- - - {help.check_for_keywords_from_list(cl.vlcList,message).upper()} - - -")
            help.close_pids(vars.vlc, "VLC")
            action.append(help.check_for_keywords_from_list(cl.closingList,message).upper() + " " + help.check_for_keywords_from_list(cl.vlcList,message))
        # MEDIA PLAYER CLASSIC
        elif help.check_for_keywords_from_list(cl.mpcList,message) is not None:
            print(f"- - - {help.check_for_keywords_from_list(cl.mpcList,message).upper()} - - -")
            help.close_pids(vars.mpc, "MPC")
            action.append(help.check_for_keywords_from_list(cl.closingList,message).upper() + " " + help.check_for_keywords_from_list(cl.mpcList,message))
        # KEEPASS
        elif help.check_for_keywords_from_list(cl.keepassList,message) is not None:
            print(f"- - - {help.check_for_keywords_from_list(cl.keepassList,message).upper()} - - -")
            help.close_pids(vars.keepass, "KeePass")
            action.append(help.check_for_keywords_from_list(cl.closingList,message).upper() + " " + help.check_for_keywords_from_list(cl.keepassList,message))
        # STEAM
        elif help.check_for_keywords_from_list(cl.steamList,message) is not None:
            print(f"- - - {help.check_for_keywords_from_list(cl.steamList,message).upper()} - - -")
            help.close_pids(vars.steam, "Steam")
            action.append(help.check_for_keywords_from_list(cl.closingList,message).upper() + " " + help.check_for_keywords_from_list(cl.steamList,message))
        # DISCORD
        elif help.check_for_keywords_from_list(cl.discordList,message) is not None:
            print(f"- - - {help.check_for_keywords_from_list(cl.discordList,message).upper()} - - -")
            help.close_pids(vars.discord, "Discord")
            action.append(help.check_for_keywords_from_list(cl.closingList,message).upper() + " " + help.check_for_keywords_from_list(cl.discordList,message))
        # MS WORD
        elif help.check_for_keywords_from_list(cl.wordList,message) is not None:
            print(f"- - - {help.check_for_keywords_from_list(cl.wordList,message).upper()} - - -")
            help.close_pids(vars.ms_word, "Winword")
            action.append(help.check_for_keywords_from_list(cl.closingList,message).upper() + " " + help.check_for_keywords_from_list(cl.wordList,message))
        # MS EXCEL
        elif help.check_for_keywords_from_list(cl.excelList,message) is not None:
            print(f"- - - {help.check_for_keywords_from_list(cl.excelList,message).upper()} - - -")
            help.close_pids(vars.ms_excel, "Excel")
            action.append(help.check_for_keywords_from_list(cl.closingList,message).upper() + " " + help.check_for_keywords_from_list(cl.excelList,message))
        # MS POWERPOINT
        elif help.check_for_keywords_from_list(cl.powerpointList,message) is not None:
            print(f"- - - {help.check_for_keywords_from_list(cl.powerpointList,message).upper()} - - -")
            help.close_pids(vars.ms_pp, "Powerpnt")
            action.append(help.check_for_keywords_from_list(cl.closingList,message).upper() + " " + help.check_for_keywords_from_list(cl.powerpointList,message))
        # NOTEPAD++
        elif help.check_for_keywords_from_list(cl.notepadppList,message) is not None:
            print(f"- - - {help.check_for_keywords_from_list(cl.notepadppList,message).upper()} - - -")
            help.close_pids(vars.npp, "Notepad++")
            action.append(help.check_for_keywords_from_list(cl.closingList,message).upper() + " " + help.check_for_keywords_from_list(cl.notepadppList,message))
        # VISUAL STUDIO CODE
        elif help.check_for_keywords_from_list(cl.vscList,message) is not None:
            print(f"- - - {help.check_for_keywords_from_list(cl.vscList,message).upper()} - - -")
            help.close_pids(vars.vsc, "Code.exe")
            action.append(help.check_for_keywords_from_list(cl.closingList,message).upper() + " " + help.check_for_keywords_from_list(cl.vscList,message))
        # PUREREF
        elif help.check_for_keywords_from_list(cl.purerefList,message) is not None:
            print(f"- - - {help.check_for_keywords_from_list(cl.purerefList,message).upper()} - - -")
            help.close_pids(vars.pureref, "PureRef")
            action.append(help.check_for_keywords_from_list(cl.closingList,message).upper() + " " + help.check_for_keywords_from_list(cl.purerefList,message))
        # AUDACITY
        elif help.check_for_keywords_from_list(cl.audacityList,message) is not None:
            print(f"- - - {help.check_for_keywords_from_list(cl.audacityList,message).upper()} - - -")
            help.close_pids(vars.audacity, "Audacity")
            action.append(help.check_for_keywords_from_list(cl.closingList,message).upper() + " " + help.check_for_keywords_from_list(cl.audacityList,message))
        # BLENDER
        elif help.check_for_keywords_from_list(cl.blenderList,message) is not None:
            print(f"- - - {help.check_for_keywords_from_list(cl.blenderList,message).upper()} - - -")
            help.close_pids(vars.blender, "Blender")
            action.append(help.check_for_keywords_from_list(cl.closingList,message).upper() + " " + help.check_for_keywords_from_list(cl.blenderList,message))
        # STABLE DIFFUSION
        elif help.check_for_keywords_from_list(cl.stablediffusionList,message) is not None:
            print(f"- - - {help.check_for_keywords_from_list(cl.stablediffusionList,message).upper()} - - -")
            help.close_pids(vars.stablediffusion, "Stable Diffusion")
            action.append(help.check_for_keywords_from_list(cl.closingList,message).upper() + " " + help.check_for_keywords_from_list(cl.stablediffusionList,message))
        # CALCULATOR
        elif help.check_for_keywords_from_list(cl.calculatorList,message) is not None:
            print(f"- - - {help.check_for_keywords_from_list(cl.calculatorList,message).upper()} - - -")
            help.close_pids(vars.calc, "Rechner")
            action.append(help.check_for_keywords_from_list(cl.closingList,message).upper() + " " + help.check_for_keywords_from_list(cl.calculatorList,message))
        # WINDOW
        elif help.check_for_keywords_from_list(cl.windowList,message) is not None:
            print(f"- - - {help.check_for_keywords_from_list(cl.windowList,message).upper()} - - -")
            pyautogui.hotkey('alt', 'f4')
            action.append(help.check_for_keywords_from_list(cl.closingList,message).upper() + " " + help.check_for_keywords_from_list(cl.windowList,message))
            
    # SWITCHING
    elif help.check_for_keywords_from_list(cl.switchingList,message) is not None and help.check_for_keywords_from_list(cl.gotoList,message) is None:
        print(f"- - - {help.check_for_keywords_from_list(cl.switchingList,message).upper()} - - -")
        if help.check_for_keywords_from_list(cl.tabList,message) is not None:
            print(f"- - - {help.check_for_keywords_from_list(cl.tabList,message).upper()} - - -")
            pyautogui.hotkey('ctrl', 'tab')
            action.append(help.check_for_keywords_from_list(cl.switchingList,message).upper() + " " + help.check_for_keywords_from_list(cl.tabList,message))
        else:
            print(f"- - - WINDOW - - -")
            pyautogui.hotkey('alt', 'tab')
            action.append(help.check_for_keywords_from_list(cl.switchingList,message).upper() + " " + help.check_for_keywords_from_list(cl.windowList,message))
            
    # MINIMIZING
    elif help.check_for_keywords_from_list(cl.minimizingList,message) is not None:
        print(f"- - - {help.check_for_keywords_from_list(cl.minimizingList,message).upper()} - - -")
        pyautogui.hotkey('win', 'down')
        action.append(help.check_for_keywords_from_list(cl.minimizingList,message).upper() + " WIWNDOW")

            
    # MAXIMIZING
    elif help.check_for_keywords_from_list(cl.maximizingList,message) is not None:
        print(f"- - - {help.check_for_keywords_from_list(cl.maximizingList,message).upper()} - - -")
        pyautogui.hotkey('win', 'up')
        action.append(help.check_for_keywords_from_list(cl.maximizingList,message).upper() + " WIWNDOW")
    
    return action     
        
    # Multisentence Analysis: Split reply into sentences, then find verbs in the sentences and object and formulate command chain.
    # Extension for Firefox to control browser tab content
    # Youtube API for outside browser access of youtube search
    # Google API for scraping information
    # ChatGPT API for complicated tasks
        
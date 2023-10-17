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
def create_process(pid_collection, collection_name, path, params):
    print(f"- - - OPENING - - -")
    help.gather_pids()
    if params is None:
        subprocess.Popen([path])    
    else:
        subprocess.Popen([path, params])
    help.find_pids(collection_name, pid_collection)

# EXECUTE COMMAND   
def check_for_command(message):
    
    init_commands = vars.executed_commands.copy()
    counter = 1
    
    # i wIlL dO iT f*CkINg aGAiN!
    if help.check_for_keywords_from_list(cl.againList,message) is not None and help.check_for_keywords_from_list(cl.allActionsButAgain,message) is None:
        if vars.executed_commands:
            if vars.silent is False:
                print(vars.executed_commands)
            print(f"- - - REPEATING LAST ACTION - - -")
            dict = help.check_for_keywords_from_list(cl.againList,message)
            counter = sum(dict.values())
            message = vars.executed_commands[-1]
        else:
            print("- - - NO LAST ACTION - - -")
           
    # REFRESH (TAB)
    if help.check_for_keywords_from_list(cl.refreshList,message) is not None:
        if vars.executed_commands: 
            print(f"- - - REFRESHING TAB - - -")
            for _ in range(counter):
                pyautogui.hotkey('f5')
            vars.executed_commands.append("REFRESHING")
    
    # GO BACK (TAB)
    if help.check_for_keywords_from_list(cl.backList,message) is not None and (help.check_for_keywords_from_list(cl.tabList,message) is not None or help.check_for_keywords_from_list(cl.browserTabList,message) is not None):
        if vars.executed_commands: 
            print(f"- - - GOING BACK BY ONE TAB - - -")
            pyautogui.keyDown('ctrl', 'shift')
            for _ in range(counter):
                pyautogui.hotkey('tab')
            pyautogui.keyUp('ctrl', 'shift')
            vars.executed_commands.append("GOING BACK BY ONE TAB")
    
    # FIND FIREFOX EXTENSION (WIP)
    #if help.check_for_keywords_from_list(cl.findList,message) is not None:
        #print(f"- - - FIND FIREFOX EXTENSION - - -")
        #asyncio.get_event_loop().run_until_complete(send_command(message))
        #vars.executed_commands.append("FIND FIREFOX EXTENSION")
        
    # TYPE (WIP)
    #if help.check_for_keywords_from_list(cl.typingList,message) is not None:
        #print(f"- - - TYPING - - -")
        #pyautogui.typewrite(STRING, interval=0.2)
        #vars.executed_commands.append("TYPING")
    
    # SCROLL
    if help.check_for_keywords_from_list(cl.scrollList,message) is not None:
        print(f"- - - SCROLLING - - -")
        
        # UP
        if help.check_for_keywords_from_list(cl.upList,message) is not None:
            print(f"- - - UP - - -")
            for _ in range(counter):
                pyautogui.scroll(400)
            vars.executed_commands.append("SCROLLING UP")            
        
        # DOWN
        if help.check_for_keywords_from_list(cl.downList,message) is not None:
            print(f"- - - DOWN - - -")
            for _ in range(counter):
                pyautogui.scroll(-400)
            vars.executed_commands.append("SCROLLING DOWN")
    
    # GO TO
    if help.check_for_keywords_from_list(cl.gotoList,message) is not None:
        print(f"- - - GO TO - - -")
        
        # DESKTOP
        if help.check_for_keywords_from_list(cl.desktopList,message) is not None and help.check_for_keywords_from_list(cl.tabList,message) is None:            
            print(f"- - - DESKTOP - - -")
            pyautogui.hotkey('win', 'd')
            vars.executed_commands.append("GOING TO DESKTOP")

        
        # EXPLORER
        elif help.check_for_keywords_from_list(cl.explorerList,message) is not None and help.check_for_keywords_from_list(cl.tabList,message) is None:            
            print(f"- - - EXPLORER - - -")
            help.focus_pids(vars.folders, "Explorer")
            vars.executed_commands.append("GOING TO EXPLORER")
          
        # CHROME
        elif help.check_for_keywords_from_list(cl.chromeList,message) is not None:
            print(f"- - - CHROME - - -")
            help.focus_pids(vars.chrome, "Chrome")
            vars.executed_commands.append("GOING TO CHROME")
            
        # FIREFOX
        elif help.check_for_keywords_from_list(cl.firefoxList,message) is not None:
            # FIREFOX INCOGNITO
            if help.check_for_keywords_from_list(cl.incognitoList,message) is not None:
                print(f"- - - FIREFOX INCOGNITO - - -")
                help.focus_pids(vars.firefoxincognito, "Firefox")
                vars.executed_commands.append("GOING TO FIREFOX")

            else:
                print(f"- - - FIREFOX - - -")
                help.focus_pids(vars.firefox, "Firefox")
                vars.executed_commands.append("GOING TO FIREFOX")
                
        # VLC
        elif help.check_for_keywords_from_list(cl.vlcList,message) is not None:
            print(f"- - - VLC - - -")
            help.focus_pids(vars.vlc, "VLC")
            vars.executed_commands.append("GOING TO VLC")
         
        # MEDIA PLAYER CLASSIC
        elif help.check_for_keywords_from_list(cl.mpcList,message) is not None:
            print(f"- - - MEDIA PLAYER CLASSIC - - -")
            help.focus_pids(vars.mpc, "MPC")
            vars.executed_commands.append("GOING TO MEDIA PLAYER CLASSIC")
            
        # KEEPASS
        elif help.check_for_keywords_from_list(cl.keepassList,message) is not None:
            print(f"- - - KEEPASS - - -")
            help.focus_pids(vars.keepass, "KeePass")
            vars.executed_commands.append("GOING TO KEEPASS")
            
        # STEAM
        elif help.check_for_keywords_from_list(cl.steamList,message) is not None:
            print(f"- - - STEAM - - -")
            help.focus_pids(vars.steam, "Steam")
            vars.executed_commands.append("GOING TO STEAM")
            
        # DISCORD
        elif help.check_for_keywords_from_list(cl.discordList,message) is not None:
            print(f"- - - DISCORD - - -")
            help.focus_pids(vars.discord, "Discord")
            vars.executed_commands.append("GOING TO DISCORD")

        # MS WORD
        elif help.check_for_keywords_from_list(cl.wordList,message) is not None:
            print(f"- - - WORD - - -")
            help.focus_pids(vars.ms_word, "Winword")
            vars.executed_commands.append("GOING TO WORD")

        # MS EXCEL
        elif help.check_for_keywords_from_list(cl.excelList,message) is not None:
            print(f"- - - EXCEL - - -")
            help.focus_pids(vars.ms_excel, "Excel")
            vars.executed_commands.append("GOING TO EXCEL")
            
        # MS POWERPOINT
        elif help.check_for_keywords_from_list(cl.powerpointList,message) is not None:
            print(f"- - - POWERPOINT - - -")
            help.focus_pids(vars.ms_pp, "Powerpnt")
            vars.executed_commands.append("GOING TO POWERPOINT")
            
        # NOTEPAD++
        elif help.check_for_keywords_from_list(cl.notepadppList,message) is not None:
            print(f"- - - NOTEPAD++ - - -")
            help.focus_pids(vars.npp, "Notepad++")
            vars.executed_commands.append("GOING TO NOTEPAD++")
            
        # VISUAL STUDIO CODE
        elif help.check_for_keywords_from_list(cl.vscList,message) is not None:
            print(f"- - - VISUAL STUDIO CODE - - -")
            help.focus_pids(vars.vsc, "Code.exe")
            vars.executed_commands.append("GOING TO VISUAL STUDIO CODE")
            
        # PUREREF
        elif help.check_for_keywords_from_list(cl.purerefList,message) is not None:
            print(f"- - - PUREREF - - -")
            help.focus_pids(vars.pureref, "PureRef")
            vars.executed_commands.append("GOING TO PUREREF")
            
        # AUDACITY
        elif help.check_for_keywords_from_list(cl.audacityList,message) is not None:
            print(f"- - - AUDACITY - - -")
            help.focus_pids(vars.audacity, "Audacity")
            vars.executed_commands.append("GOING TO AUDACITY")
        
        # BLENDER
        elif help.check_for_keywords_from_list(cl.blenderList,message) is not None:
            print(f"- - - BLENDER - - -")
            help.focus_pids(vars.blender, "Blender")
            vars.executed_commands.append("GOING TO BLENDER")
            
        # STABLE DIFFUSION
        elif help.check_for_keywords_from_list(cl.stablediffusionList,message) is not None:
            print(f"- - - STABLE DIFFUSION - - -")
            help.focus_pids(vars.stablediffusion, "Stable Diffusion")
            vars.executed_commands.append("GOING TO STABLE DIFFUSION")
            
        # CALCULATOR
        elif help.check_for_keywords_from_list(cl.calculatorList,message) is not None:
            print(f"- - - CALCULATOR - - -")
            help.focus_pids(vars.calc, "Rechner")
            vars.executed_commands.append("GOING TO CALCULATOR")
            
    # OPENING
    if help.check_for_keywords_from_list(cl.openingList,message) is not None:
        print(f"- - - OPENING - - -")
        
        # EXPLORER
        if help.check_for_keywords_from_list(cl.explorerList,message) and help.check_for_keywords_from_list(cl.tabList,message) is None:            
            # EXPLORER (C Drive)
            if help.check_for_keywords_from_list(cl.cDriveList,message) is not None:
                print(f"- - - C: DRIVE - - -")
                for _ in range(counter):
                    create_process(vars.folders, "Explorer", explorer_path, r"C:")
                vars.executed_commands.append("OPENING FOLDER AT C:")
            
            # EXPLORER (D Drive)
            elif help.check_for_keywords_from_list(cl.dDriveList,message) is not None:
                print(f"- - - D: DRIVE - - -")
                for _ in range(counter):
                    create_process(vars.folders, "Explorer", explorer_path, r"D:")
                vars.executed_commands.append("OPENING FOLDER AT D:")

                
            # EXPLORER (AppData)
            elif help.check_for_keywords_from_list(cl.appDataList,message) is not None:
                print(f"- - - APPDATA FOLDER - - -")
                for _ in range(counter):
                    create_process(vars.folders, "Explorer", explorer_path, home_folder + r"\AppData")
                vars.executed_commands.append("OPENING FOLDER AT APPDATA")
                
            # EXPLORER (Programs)
            elif help.check_for_keywords_from_list(cl.programsFolderList,message) is not None:
                # EXPLORER (Programs86)
                if help.check_for_keywords_from_list(cl.programs86FolderList,message) is not None:
                    print(f"- - - PROGRAMS 86 FOLDER - - -")
                    for _ in range(counter):
                        create_process(vars.folders, "Explorer", explorer_path, program_files_x86_folder)
                    vars.executed_commands.append("OPENING FOLDER AT PROGRAMS 86")
                else:
                    print(f"- - - PROGRAMS FOLDER - - -")
                    for _ in range(counter):
                        create_process(vars.folders, "Explorer", explorer_path, program_files_folder)
                    vars.executed_commands.append("OPENING FOLDER AT PROGRAMS")
            # EXPLORER (Home)
            elif help.check_for_keywords_from_list(cl.homeFolderList,message) is not None:
                print(f"- - - HOME FOLDER - - -")
                for _ in range(counter):
                    create_process(vars.folders, "Explorer", explorer_path, home_folder)
                vars.executed_commands.append("OPENING FOLDER AT HOME")
                
            # EXPLORER (Downloads)
            elif help.check_for_keywords_from_list(cl.downloadFolderList,message) is not None:
                print(f"- - - DOWNLOADS FOLDER - - -")
                for _ in range(counter):
                    create_process(vars.folders, "Explorer", explorer_path, download_folder)
                vars.executed_commands.append("OPENING FOLDER AT DOWNLOADS")
            else:
                print(f"- - - MY COMPUTER FOLDER - - -")
                for _ in range(counter):
                    create_process(vars.folders, "Explorer", explorer_path, my_computer_folder)
                vars.executed_commands.append("OPENING FOLDER AT MY COMPUTER")
            
        # CHROME
        elif help.check_for_keywords_from_list(cl.chromeList,message) is not None:
            print(f"- - - CHROME - - -")
            for _ in range(counter):
                create_process(vars.chrome, "Chrome", chrome_path, None)
            vars.executed_commands.append("OPENING CHROME")
        
        # FIREFOX
        elif help.check_for_keywords_from_list(cl.firefoxList,message) is not None:
            # FIREFOX INCOGNITO
            if help.check_for_keywords_from_list(cl.incognitoList,message) is not None:
                print(f"- - - FIREFOX INCOGNITO - - -")
                for _ in range(counter):
                    create_process(vars.firefoxincognito, "Firefox", firefox_path, "-private-window")
                vars.executed_commands.append("OPENING FIREFOX INCOGNITO")

            else:
                print(f"- - - FIREFOX - - -")
                for _ in range(counter):
                    create_process(vars.firefox, "Firefox", firefox_path, None)   
                vars.executed_commands.append("OPENING FIREFOX")
            
        # VLC
        elif help.check_for_keywords_from_list(cl.vlcList,message) is not None:
            print(f"- - - VLC - - -")
            for _ in range(counter):
                create_process(vars.vlc, "VLC", vlc_path, None)
            vars.executed_commands.append("OPENING VLC")
            
        # MEDIA PLAYER CLASSIC
        elif help.check_for_keywords_from_list(cl.mpcList,message) is not None:
            print(f"- - - MEDIA PLAYER CLASSIC - - -")
            for _ in range(counter):
                create_process(vars.mpc, "MPC", mpc_path, None)
            vars.executed_commands.append("OPENING MEDIA PLAYER CLASSIC")
            
        # KEEPASS
        elif help.check_for_keywords_from_list(cl.keepassList,message) is not None:
            print(f"- - - KEEPASS - - -")
            for _ in range(counter):
                create_process(vars.keepass, "KeePass", keepass_path, None)
            vars.executed_commands.append("OPENING KEEPASS")
            
        # STEAM
        elif help.check_for_keywords_from_list(cl.steamList,message) is not None:
            print(f"- - - STEAM - - -")
            for _ in range(counter):
                create_process(vars.steam, "Steam", steam_path, None)
            vars.executed_commands.append("OPENING STEAM")
        
        # DISCORD
        elif help.check_for_keywords_from_list(cl.discordList,message) is not None:
            print(f"- - - DISCORD - - -")
            for _ in range(counter):
                create_process(vars.discord, "Discord", discord_path, None)
            vars.executed_commands.append("OPENING DISCORD")
            
        # MS WORD
        elif help.check_for_keywords_from_list(cl.wordList,message) is not None:
            print(f"- - - WORD - - -")
            for _ in range(counter):
                create_process(vars.ms_word, "Winword", word_path, None)
            vars.executed_commands.append("OPENING WORD")
        
        # MS EXCEL
        elif help.check_for_keywords_from_list(cl.excelList,message) is not None:
            print(f"- - - EXCEL - - -")
            for _ in range(counter):
                create_process(vars.ms_excel, "Excel", excel_path, None)
            vars.executed_commands.append("OPENING EXCEL")
            
        # MS POWERPOINT
        elif help.check_for_keywords_from_list(cl.powerpointList,message) is not None:
            print(f"- - - POWERPOINT - - -")
            for _ in range(counter):
                create_process(vars.ms_pp, "Powerpnt", powerpoint_path, None)
            vars.executed_commands.append("OPENING POWERPOINT")
        
        # NOTEPAD++
        elif help.check_for_keywords_from_list(cl.notepadppList,message) is not None:
            print(f"- - - NOTEPAD++ - - -")
            for _ in range(counter):
                create_process(vars.npp, "Notepad++", notepadpp_path, None)
            vars.executed_commands.append("OPENING NOTEPAD++")
            
        # VISUAL STUDIO CODE
        elif help.check_for_keywords_from_list(cl.vscList,message) is not None:
            print(f"- - - VISUAL STUDIO CODE - - -")
            for _ in range(counter):
                create_process(vars.vsc, "Code.exe", vsc_path, None)
            vars.executed_commands.append("OPENING VISUAL STUDIO CODE")
            
        # PUREREF
        elif help.check_for_keywords_from_list(cl.purerefList,message) is not None:
            print(f"- - - PUREREF - - -")
            for _ in range(counter):
                create_process(vars.pureref, "PureRef", pureref_path, None)
            vars.executed_commands.append("OPENING PUREREF")
        
        # AUDACITY
        elif help.check_for_keywords_from_list(cl.audacityList,message) is not None:
            print(f"- - - AUDACITY - - -")
            for _ in range(counter):
                create_process(vars.audacity, "Audacity", audacity_path, None)
            vars.executed_commands.append("OPENING AUDACITY")
        
        # BLENDER
        elif help.check_for_keywords_from_list(cl.blenderList,message) is not None:
            print(f"- - - BLENDER - - -")
            for _ in range(counter):
                create_process(vars.blender, "Blender", blender_path, None)
            vars.executed_commands.append("OPENING BLENDER")
            
        # STABLE DIFFUSION
        elif help.check_for_keywords_from_list(cl.stablediffusionList,message) is not None:
            print(f"- - - STABLE DIFFUSION - - -")
            for _ in range(counter):
                create_process(vars.stablediffusion, "Stable Diffusion", stablediffusion_path, None)
            vars.executed_commands.append("OPENING STABLE DIFFUSION")
            
        # CALCULATOR
        elif help.check_for_keywords_from_list(cl.calculatorList,message) is not None:
            print(f"- - - CALCULATOR - - -")
            for _ in range(counter):
                create_process(vars.calc, "Rechner", calculator_path, None)
            vars.executed_commands.append("OPENING CALCULATOR")
            
        # SYSTEM SETTINGS
        elif help.check_for_keywords_from_list(cl.controlList,message) is not None:
            print(f"- - - SYSTEM SETTINGS - - -")
            subprocess.Popen(["control.exe", "/name", "Microsoft.System"])
            vars.executed_commands.append("OPENING SYSTEM SETTINGS")
            
        # AUDIO SETTINGS
        #elif help.check_for_keywords_from_list(cl.audioList,message) is not None:
            #print(f"- - - AUDIO SETTINGS - - -")
            #create_process(vars.audioSettings, "control", "mmsys.cpl", None)
            #vars.executed_commands.append("OPENING AUDIO SETTINGS")
        
        # DISPLAY SETTINGS   
        #elif help.check_for_keywords_from_list(cl.videoList,message) is not None:
            #print(f"- - - DISPLAY SETTINGS - - -")
            #create_process(vars.displaySettings, "rundll32.exe", "shell32.dll,Control_RunDLL desk.cpl", None)
            #vars.executed_commands.append("OPENING DISPLAY SETTINGS")
            
        # DESKTOP SETTINGS   
        #elif help.check_for_keywords_from_list(cl.desktopList,message) is not None:
            #print(f"- - - DESKTOP SETTINGS - - -")
            #create_process(vars.desktopSettings, "control", "desk.cpl", None)
            #vars.executed_commands.append("OPENING DESKTOP SETTINGS")
            
        # NEW TAB   
        elif help.check_for_keywords_from_list(cl.tabList,message) is not None:
            # FOLDER TAB
            if help.check_for_keywords_from_list(cl.folderList,message) is not None:
                print(f"- - - NEW FOLDER TAB - - -")
                pyautogui.hotkey('ctrl', 't')
                pyautogui.hotkey('f4')
                time.sleep(0.1)
                if help.check_for_keywords_from_list(cl.downloadFolderList,message) is not None:
                    print(f"- - - AT DOWNLOAD FOLDER - - -")
                    pyautogui.hotkey('ctrl', 'a')
                    pyautogui.hotkey('del')
                    pyautogui.typewrite(download_folder, interval=vars.llm_type_speed)
                    vars.executed_commands.append("OPENING NEW FOLDER TAB AT DOWNLOAD FOLDER")
                elif help.check_for_keywords_from_list(cl.homeFolderList,message) is not None:
                    print(f"- - - AT HOME FOLDER - - -")
                    pyautogui.hotkey('ctrl', 'a')
                    pyautogui.hotkey('del')
                    pyautogui.typewrite(home_folder, interval=vars.llm_type_speed)
                    vars.executed_commands.append("OPENING NEW FOLDER TAB AT HOME FOLDER")
                elif help.check_for_keywords_from_list(cl.programs86FolderList,message) is not None:
                    print(f"- - - AT PROGRAMS 86 FOLDER - - -")
                    pyautogui.hotkey('ctrl', 'a')
                    pyautogui.hotkey('del')
                    pyautogui.typewrite(program_files_x86_folder, interval=vars.llm_type_speed)
                    vars.executed_commands.append("OPENING NEW FOLDER TAB AT PROGRAMS 86 FOLDER")
                elif help.check_for_keywords_from_list(cl.programsFolderList,message) is not None:
                    print(f"- - - AT PROGRAMS FOLDER - - -")
                    pyautogui.hotkey('ctrl', 'a')
                    pyautogui.hotkey('del')
                    pyautogui.typewrite(program_files_folder, interval=vars.llm_type_speed)
                    vars.executed_commands.append("OPENING NEW FOLDER TAB AT PROGRAMS FOLDER")
                elif help.check_for_keywords_from_list(cl.appDataList,message) is not None:
                    print(f"- - - AT APPDATA FOLDER - - -")
                    pyautogui.hotkey('ctrl', 'a')
                    pyautogui.hotkey('del')
                    pyautogui.typewrite(home_folder + r"\AppData", interval=vars.llm_type_speed)
                    vars.executed_commands.append("OPENING NEW FOLDER TAB AT APPDATA FOLDER")
                elif help.check_for_keywords_from_list(cl.dDriveList,message) is not None:
                    print(f"- - - AT D: DRIVE - - -")
                    pyautogui.hotkey('ctrl', 'a')
                    pyautogui.hotkey('del')
                    pyautogui.typewrite(r"D:", interval=vars.llm_type_speed)
                    vars.executed_commands.append("OPENING NEW FOLDER TAB AT D: DRIVE")
                elif help.check_for_keywords_from_list(cl.cDriveList,message) is not None:
                    print(f"- - - AT C: DRIVE - - -")
                    pyautogui.hotkey('ctrl', 'a')
                    pyautogui.hotkey('del')
                    pyautogui.typewrite(r"C:", interval=vars.llm_type_speed)
                    vars.executed_commands.append("OPENING NEW FOLDER TAB AT C: DRIVE")
                elif help.check_for_keywords_from_list(cl.myComputerList,message) is not None:
                    print(f"- - - AT MY COMPUTER FOLDER - - -")
                    pyautogui.hotkey('ctrl', 'a')
                    pyautogui.press('del')
                    keyboard.write(my_computer_folder)
                    vars.executed_commands.append("OPENING NEW FOLDER TAB AT MY COMPUTER FOLDER")
                else:
                    print(f"- - - AT MY COMPUTER FOLDER - - -")
                    pyautogui.hotkey('ctrl', 'a')
                    pyautogui.press('del')
                    keyboard.write(my_computer_folder)
                    vars.executed_commands.append("OPENING NEW FOLDER TAB AT MY COMPUTER FOLDER")
                pyautogui.hotkey('enter')
            # BROWSER TAB
            elif help.check_for_keywords_from_list(cl.browserTabList,message) is not None and "Mozilla Firefox" in help.get_current_window_title():
                print(f"- - - NEW BROWSER TAB - - -")
                pyautogui.keyDown('ctrl')
                pyautogui.hotkey('t')
                pyautogui.keyUp('ctrl')
                vars.executed_commands.append("OPENING NEW BROWSER TAB")
            else:
                print(f"- - - NOTHING IN FOCUS TO CREATE A TAB IN - - -")
            
    # CLOSING
    if help.check_for_keywords_from_list(cl.closingList,message) is not None:
        print(f"- - - CLOSING - - -")
        
        # TAB   
        if help.check_for_keywords_from_list(cl.tabList,message) is not None:
            print(f"- - - TAB - - -")
            for _ in range(counter):
                pyautogui.hotkey('ctrl', 'w')
            vars.executed_commands.append("CLOSING TAB")

        # EXPLORER
        elif help.check_for_keywords_from_list(cl.explorerList,message) is not None:
            print(f"- - - EXPLORER - - -")
            help.close_pids(vars.folders, "Explorer")
            vars.executed_commands.append("CLOSING EXPLORER")

        # CHROME
        elif help.check_for_keywords_from_list(cl.chromeList,message) is not None:
            print(f"- - - CHROME - - -")
            help.close_pids(vars.chrome, "Chrome")
            vars.executed_commands.append("CLOSING CHROME")

        # FIREFOX
        elif help.check_for_keywords_from_list(cl.firefoxList,message) is not None:
            print(f"- - - FIREFOX - - -")
            if help.check_for_keywords_from_list(cl.incognitoList,message) is not None:
                print(f"- - - FIREFOX INCOGNITO - - -")
                help.close_pids(vars.firefoxincognito, "Firefox")
                vars.executed_commands.append("CLOSING FIREFOX INCOGNITO")
            else:
                help.close_pids(vars.firefox, "Firefox")
                vars.executed_commands.append("CLOSING FIREFOX")

        # VLC
        elif help.check_for_keywords_from_list(cl.vlcList,message) is not None:
            print(f"- - - VLC - - -")
            help.close_pids(vars.vlc, "VLC")
            vars.executed_commands.append("CLOSING VLC")
        
        # MEDIA PLAYER CLASSIC
        elif help.check_for_keywords_from_list(cl.mpcList,message) is not None:
            print(f"- - - MEDIA PLAYER CLASSIC - - -")
            help.close_pids(vars.mpc, "MPC")
            vars.executed_commands.append("CLOSING MEDIA PLAYER CLASSIC")
        
        # KEEPASS
        elif help.check_for_keywords_from_list(cl.keepassList,message) is not None:
            print(f"- - - KEEPASS - - -")
            help.close_pids(vars.keepass, "KeePass")
            vars.executed_commands.append("CLOSING KEEPASS")
        
        # STEAM
        elif help.check_for_keywords_from_list(cl.steamList,message) is not None:
            print(f"- - - STEAM - - -")
            help.close_pids(vars.steam, "Steam")
            vars.executed_commands.append("CLOSING STEAM")
        
        # DISCORD
        elif help.check_for_keywords_from_list(cl.discordList,message) is not None:
            print(f"- - - DISCORD - - -")
            help.close_pids(vars.discord, "Discord")
            vars.executed_commands.append("CLOSING DISCORD")
        
        # MS WORD
        elif help.check_for_keywords_from_list(cl.wordList,message) is not None:
            print(f"- - - WORD - - -")
            help.close_pids(vars.ms_word, "Winword")
            vars.executed_commands.append("CLOSING WORD")
        
        # MS EXCEL
        elif help.check_for_keywords_from_list(cl.excelList,message) is not None:
            print(f"- - - EXCEL - - -")
            help.close_pids(vars.ms_excel, "Excel")
            vars.executed_commands.append("CLOSING EXCEL")
        
        # MS POWERPOINT
        elif help.check_for_keywords_from_list(cl.powerpointList,message) is not None:
            print(f"- - - POWERPOINT - - -")
            help.close_pids(vars.ms_pp, "Powerpnt")
            vars.executed_commands.append("CLOSING POWERPOINT")
        
        # NOTEPAD++
        elif help.check_for_keywords_from_list(cl.notepadppList,message) is not None:
            print(f"- - - NOTEPAD++ - - -")
            help.close_pids(vars.npp, "Notepad++")
            vars.executed_commands.append("CLOSING NOTEPAD++")
        
        # VISUAL STUDIO CODE
        elif help.check_for_keywords_from_list(cl.vscList,message) is not None:
            print(f"- - - VISUAL STUDIO CODE - - -")
            help.close_pids(vars.vsc, "Code.exe")
            vars.executed_commands.append("CLOSING VISUAL STUDIO CODE")
        
        # PUREREF
        elif help.check_for_keywords_from_list(cl.purerefList,message) is not None:
            print(f"- - - PUREREF - - -")
            help.close_pids(vars.pureref, "PureRef")
            vars.executed_commands.append("CLOSING PUREREF")
        
        # AUDACITY
        elif help.check_for_keywords_from_list(cl.audacityList,message) is not None:
            print(f"- - - AUDACITY - - -")
            help.close_pids(vars.audacity, "Audacity")
            vars.executed_commands.append("CLOSING AUDACITY")
        
        # BLENDER
        elif help.check_for_keywords_from_list(cl.blenderList,message) is not None:
            print(f"- - - BLENDER - - -")
            help.close_pids(vars.blender, "Blender")
            vars.executed_commands.append("CLOSING BLENDER")
        
        # STABLE DIFFUSION
        elif help.check_for_keywords_from_list(cl.stablediffusionList,message) is not None:
            print(f"- - - STABLE DIFFUSION - - -")
            help.close_pids(vars.stablediffusion, "Stable Diffusion")
            vars.executed_commands.append("CLOSING STABLE DIFFUSION")
        
        # CALCULATOR
        elif help.check_for_keywords_from_list(cl.calculatorList,message) is not None:
            print(f"- - - CALCULATOR - - -")
            help.close_pids(vars.calc, "Rechner")
            vars.executed_commands.append("CLOSING CALCULATOR")
        
        # WINDOW
        elif help.check_for_keywords_from_list(cl.windowList,message) is not None:
            print(f"- - - WINDOW - - -")
            pyautogui.hotkey('alt', 'f4')
            vars.executed_commands.append("CLOSING WINDOW")
            
    # SWITCHING
    if help.check_for_keywords_from_list(cl.switchingList,message) is not None and help.check_for_keywords_from_list(cl.gotoList,message) is None and help.check_for_keywords_from_list(cl.backList,message) is None:
        print(f"- - - SWITCHING - - -")
        if help.check_for_keywords_from_list(cl.tabList,message) is not None:
            print(f"- - - TAB - - -")
            pyautogui.keyDown('ctrl')
            for _ in range(counter):
                pyautogui.hotkey('tab')
            pyautogui.keyUp('ctrl')
            vars.executed_commands.append("SWITCHING TAB")
        else:
            print(f"- - - WINDOW - - -")
            pyautogui.keyDown('alt')
            for _ in range(counter):
                pyautogui.hotkey('tab')
            pyautogui.keyUp('alt')
            vars.executed_commands.append("SWITCHING WINDOW")
            
    # MINIMIZING
    if help.check_for_keywords_from_list(cl.minimizingList,message) is not None:
        print(f"- - - MINIMIZING - - -")
        for _ in range(counter):
            pyautogui.hotkey('win', 'down')
        vars.executed_commands.append("MINIMIZING WINDOW")
        
    # MAXIMIZING
    if help.check_for_keywords_from_list(cl.maximizingList,message) is not None:
            print(f"- - - MAXIMIZING - - -")
            for _ in range(counter):
                pyautogui.hotkey('win', 'up')
            vars.executed_commands.append("MAXIMIZING WINDOW")
        
    if init_commands == vars.executed_commands:
        return False
    else:
        return True
            
    # Multisentence Analysis: Split reply into sentences, then find verbs in the sentences and object and formulate command chain.
    # Extension for Firefox to control browser tab content
    # Youtube API for outside browser access of youtube search
    # Google API for scraping information
    # ChatGPT API for complicated tasks
    
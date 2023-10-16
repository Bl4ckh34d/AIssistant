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
    init_commands = vars.executed_commands.copy()
    
    # i wIlL dO iT f*CkINg aGAiN!
    if help.check_for_keywords_from_list(cl.againList,message) and help.check_for_keywords_from_list(cl.allActionsButAgain,message) is None:
        if vars.executed_commands:
            print(f"- - - REPEATING LAST ACTION - - -")
            print(vars.executed_commands)
            message = vars.executed_commands[-1]
        else:
            print("- - - NO LAST ACTION - - -")
            
    # REFRESH (TAB)
    if help.check_for_keywords_from_list(cl.refreshList,message):
        if vars.executed_commands: 
            print(f"- - - {help.check_for_keywords_from_list(cl.refreshList,message).upper()} - - -")
            pyautogui.hotkey('f5')
            vars.executed_commands.append(help.check_for_keywords_from_list(cl.refreshList,message).upper())
    
    # GO BACK (TAB)
    if help.check_for_keywords_from_list(cl.backList,message) and (help.check_for_keywords_from_list(cl.tabList,message) or help.check_for_keywords_from_list(cl.browserTabList,message)):
        if vars.executed_commands: 
            print(f"- - - {help.check_for_keywords_from_list(cl.backList,message).upper()} BY ONE TAB - - -")
            pyautogui.hotkey('ctrl', 'shift', 'tab')
            vars.executed_commands.append(help.check_for_keywords_from_list(cl.backList,message).upper() + " BY ONE TAB")
    
    # FIND FIREFOX EXTENSION (WIP)
    #if help.check_for_keywords_from_list(cl.findList,message):
        #print(f"- - - {help.check_for_keywords_from_list(cl.findList,message).upper()} - - -")
        #asyncio.get_event_loop().run_until_complete(send_command(message))
        #vars.executed_commands.append(help.check_for_keywords_from_list(cl.findList,message).upper())
        
    # TYPE (WIP)
    #if help.check_for_keywords_from_list(cl.typingList,message):
        #print(f"- - - {help.check_for_keywords_from_list(cl.typingList,message).upper()} - - -")
        #pyautogui.typewrite(STRING, interval=0.2)
        #vars.executed_commands.append(help.check_for_keywords_from_list(cl.typingList,message).upper())
    
    # SCROLL
    if help.check_for_keywords_from_list(cl.scrollList,message):
        print(f"- - - {help.check_for_keywords_from_list(cl.scrollList,message).upper()} - - -")
        
        # UP
        if help.check_for_keywords_from_list(cl.upList,message):
            print(f"- - - {help.check_for_keywords_from_list(cl.upList,message).upper()} - - -")
            pyautogui.scroll(400)
            vars.executed_commands.append(help.check_for_keywords_from_list(cl.scrollList,message).upper() + " " + help.check_for_keywords_from_list(cl.upList,message).upper())            
        
        # DOWN
        if help.check_for_keywords_from_list(cl.downList,message):
            print(f"- - - {help.check_for_keywords_from_list(cl.downList,message).upper()} - - -")
            pyautogui.scroll(-400)
            vars.executed_commands.append(help.check_for_keywords_from_list(cl.scrollList,message).upper() + " " + help.check_for_keywords_from_list(cl.downList,message).upper())
    
    # GO TO
    if help.check_for_keywords_from_list(cl.gotoList,message):
        print(f"- - - {help.check_for_keywords_from_list(cl.gotoList,message).upper()} - - -")
        
        # DESKTOP
        if help.check_for_keywords_from_list(cl.desktopList,message) and help.check_for_keywords_from_list(cl.tabList,message) is None:            
            print(f"- - - {help.check_for_keywords_from_list(cl.desktopList,message).upper()} - - -")
            pyautogui.hotkey('win', 'd')
            vars.executed_commands.append(help.check_for_keywords_from_list(cl.gotoList,message).upper() + " " + help.check_for_keywords_from_list(cl.desktopList,message).upper())

        
        # EXPLORER
        elif help.check_for_keywords_from_list(cl.explorerList,message) and help.check_for_keywords_from_list(cl.tabList,message) is None:            
            print(f"- - - {help.check_for_keywords_from_list(cl.explorerList,message).upper()} - - -")
            help.focus_pids(vars.folders, "Explorer")
            vars.executed_commands.append(help.check_for_keywords_from_list(cl.gotoList,message).upper() + " " + help.check_for_keywords_from_list(cl.explorerList,message).upper())

            
        # CHROME
        elif help.check_for_keywords_from_list(cl.chromeList,message):
            print(f"- - - {help.check_for_keywords_from_list(cl.chromeList,message).upper()} - - -")
            help.focus_pids(vars.chrome, "Chrome")
            vars.executed_commands.append(help.check_for_keywords_from_list(cl.gotoList,message).upper() + " " + help.check_for_keywords_from_list(cl.chromeList,message).upper())

            
        # FIREFOX
        elif help.check_for_keywords_from_list(cl.firefoxList,message):
            # FIREFOX INCOGNITO
            if help.check_for_keywords_from_list(cl.incognitoList,message):
                print(f"- - - {help.check_for_keywords_from_list(cl.incognitoList,message).upper()} - - -")
                help.focus_pids(vars.firefoxincognito, "Firefox")
                vars.executed_commands.append(help.check_for_keywords_from_list(cl.gotoList,message).upper() + " " + help.check_for_keywords_from_list(cl.incognitoList,message).upper())

            else:
                print(f"- - - {help.check_for_keywords_from_list(cl.firefoxList,message).upper()} - - -")
                help.focus_pids(vars.firefox, "Firefox")
                vars.executed_commands.append(help.check_for_keywords_from_list(cl.gotoList,message).upper() + " " + help.check_for_keywords_from_list(cl.firefoxList,message).upper())

                
        # VLC
        elif help.check_for_keywords_from_list(cl.vlcList,message):
            print(f"- - - {help.check_for_keywords_from_list(cl.vlcList,message).upper()} - - -")
            help.focus_pids(vars.vlc, "VLC")
            vars.executed_commands.append(help.check_for_keywords_from_list(cl.gotoList,message).upper() + " " + help.check_for_keywords_from_list(cl.vlcList,message).upper())

            
        # MEDIA PLAYER CLASSIC
        elif help.check_for_keywords_from_list(cl.mpcList,message):
            print(f"- - - {help.check_for_keywords_from_list(cl.mpcList,message).upper()} - - -")
            help.focus_pids(vars.mpc, "MPC")
            vars.executed_commands.append(help.check_for_keywords_from_list(cl.gotoList,message).upper() + " " + help.check_for_keywords_from_list(cl.mpcList,message).upper())
            
        # KEEPASS
        elif help.check_for_keywords_from_list(cl.keepassList,message):
            print(f"- - - {help.check_for_keywords_from_list(cl.keepassList,message).upper()} - - -")
            help.focus_pids(vars.keepass, "KeePass")
            vars.executed_commands.append(help.check_for_keywords_from_list(cl.gotoList,message).upper() + " " + help.check_for_keywords_from_list(cl.keepassList,message).upper())
            
        # STEAM
        elif help.check_for_keywords_from_list(cl.steamList,message):
            print(f"- - - {help.check_for_keywords_from_list(cl.steamList,message).upper()} - - -")
            help.focus_pids(vars.steam, "Steam")
            vars.executed_commands.append(help.check_for_keywords_from_list(cl.gotoList,message).upper() + " " + help.check_for_keywords_from_list(cl.steamList,message).upper())
            
        # DISCORD
        elif help.check_for_keywords_from_list(cl.discordList,message):
            print(f"- - - {help.check_for_keywords_from_list(cl.discordList,message).upper()} - - -")
            help.focus_pids(vars.discord, "Discord")
            vars.executed_commands.append(help.check_for_keywords_from_list(cl.gotoList,message).upper() + " " + help.check_for_keywords_from_list(cl.discordList,message).upper())

        # MS WORD
        elif help.check_for_keywords_from_list(cl.wordList,message):
            print(f"- - - {help.check_for_keywords_from_list(cl.wordList,message).upper()} - - -")
            help.focus_pids(vars.ms_word, "Winword")
            vars.executed_commands.append(help.check_for_keywords_from_list(cl.gotoList,message).upper() + " " + help.check_for_keywords_from_list(cl.wordList,message).upper())

        # MS EXCEL
        elif help.check_for_keywords_from_list(cl.excelList,message):
            print(f"- - - {help.check_for_keywords_from_list(cl.excelList,message).upper()} - - -")
            help.focus_pids(vars.ms_excel, "Excel")
            vars.executed_commands.append(help.check_for_keywords_from_list(cl.gotoList,message).upper() + " " + help.check_for_keywords_from_list(cl.excelList,message).upper())
            
        # MS POWERPOINT
        elif help.check_for_keywords_from_list(cl.powerpointList,message):
            print(f"- - - {help.check_for_keywords_from_list(cl.powerpointList,message).upper()} - - -")
            help.focus_pids(vars.ms_pp, "Powerpnt")
            vars.executed_commands.append(help.check_for_keywords_from_list(cl.gotoList,message).upper() + " " + help.check_for_keywords_from_list(cl.powerpointList,message).upper())
            
        # NOTEPAD++
        elif help.check_for_keywords_from_list(cl.notepadppList,message):
            print(f"- - - {help.check_for_keywords_from_list(cl.notepadppList,message).upper()} - - -")
            help.focus_pids(vars.npp, "Notepad++")
            vars.executed_commands.append(help.check_for_keywords_from_list(cl.gotoList,message).upper() + " " + help.check_for_keywords_from_list(cl.notepadppList,message).upper())
               
        # VISUAL STUDIO CODE
        elif help.check_for_keywords_from_list(cl.vscList,message):
            print(f"- - - {help.check_for_keywords_from_list(cl.vscList,message).upper()} - - -")
            help.focus_pids(vars.vsc, "Code.exe")
            vars.executed_commands.append(help.check_for_keywords_from_list(cl.gotoList,message).upper() + " " + help.check_for_keywords_from_list(cl.vscList,message).upper())
              
        # PUREREF
        elif help.check_for_keywords_from_list(cl.purerefList,message):
            print(f"- - - {help.check_for_keywords_from_list(cl.purerefList,message).upper()} - - -")
            help.focus_pids(vars.pureref, "PureRef")
            vars.executed_commands.append(help.check_for_keywords_from_list(cl.gotoList,message).upper() + " " + help.check_for_keywords_from_list(cl.purerefList,message).upper())
            
        # AUDACITY
        elif help.check_for_keywords_from_list(cl.audacityList,message):
            print(f"- - - {help.check_for_keywords_from_list(cl.audacityList,message).upper()} - - -")
            help.focus_pids(vars.audacity, "Audacity")
            vars.executed_commands.append(help.check_for_keywords_from_list(cl.gotoList,message).upper() + " " + help.check_for_keywords_from_list(cl.audacityList,message).upper())
        
        # BLENDER
        elif help.check_for_keywords_from_list(cl.blenderList,message):
            print(f"- - - {help.check_for_keywords_from_list(cl.blenderList,message).upper()} - - -")
            help.focus_pids(vars.blender, "Blender")
            vars.executed_commands.append(help.check_for_keywords_from_list(cl.gotoList,message).upper() + " " + help.check_for_keywords_from_list(cl.blenderList,message).upper())
            
        # STABLE DIFFUSION
        elif help.check_for_keywords_from_list(cl.stablediffusionList,message):
            print(f"- - - {help.check_for_keywords_from_list(cl.stablediffusionList,message).upper()} - - -")
            help.focus_pids(vars.stablediffusion, "Stable Diffusion")
            vars.executed_commands.append(help.check_for_keywords_from_list(cl.gotoList,message).upper() + " " + help.check_for_keywords_from_list(cl.stablediffusionList,message).upper())
            
        # CALCULATOR
        elif help.check_for_keywords_from_list(cl.calculatorList,message):
            print(f"- - - {help.check_for_keywords_from_list(cl.calculatorList,message).upper()} - - -")
            help.focus_pids(vars.calc, "Rechner")
            vars.executed_commands.append(help.check_for_keywords_from_list(cl.gotoList,message).upper() + " " + help.check_for_keywords_from_list(cl.calculatorList,message).upper())
              
    # OPENING
    if help.check_for_keywords_from_list(cl.openingList,message):
        print(f"- - - {help.check_for_keywords_from_list(cl.openingList,message).upper()} - - -")
        
        # EXPLORER
        if help.check_for_keywords_from_list(cl.explorerList,message) and help.check_for_keywords_from_list(cl.tabList,message) is None:            
            # EXPLORER (C Drive)
            if help.check_for_keywords_from_list(cl.cDriveList,message):
                create_process(vars.folders, "Explorer", cl.cDriveList, message, explorer_path, r"C:")
                vars.executed_commands.append(help.check_for_keywords_from_list(cl.openingList,message).upper() + " " + help.check_for_keywords_from_list(cl.explorerList,message).upper() + " at " +help.check_for_keywords_from_list(cl.cDriveList,message).upper())
            
            # EXPLORER (D Drive)
            elif help.check_for_keywords_from_list(cl.dDriveList,message):
                create_process(vars.folders, "Explorer", cl.dDriveList, message, explorer_path, r"D:")
                vars.executed_commands.append(help.check_for_keywords_from_list(cl.openingList,message).upper() + " " + help.check_for_keywords_from_list(cl.explorerList,message).upper() + " at " +help.check_for_keywords_from_list(cl.dDriveList,message).upper())

                
            # EXPLORER (AppData)
            elif help.check_for_keywords_from_list(cl.appDataList,message):
                create_process(vars.folders, "Explorer", cl.appDataList, message, explorer_path, home_folder + r"\AppData")
                vars.executed_commands.append(help.check_for_keywords_from_list(cl.openingList,message).upper() + " " + help.check_for_keywords_from_list(cl.explorerList,message).upper() + " at " +help.check_for_keywords_from_list(cl.appDataList,message).upper())
                
            # EXPLORER (Programs)
            elif help.check_for_keywords_from_list(cl.programsFolderList,message):
                # EXPLORER (Programs86)
                if help.check_for_keywords_from_list(cl.programs86FolderList,message):
                    create_process(vars.folders, "Explorer", cl.programs86FolderList, message, explorer_path, program_files_x86_folder)
                    vars.executed_commands.append(help.check_for_keywords_from_list(cl.openingList,message).upper() + " " + help.check_for_keywords_from_list(cl.explorerList,message).upper() + " at " +help.check_for_keywords_from_list(cl.programs86FolderList,message).upper())
                else:
                    create_process(vars.folders, "Explorer", cl.programsFolderList, message, explorer_path, program_files_folder)
                    vars.executed_commands.append(help.check_for_keywords_from_list(cl.openingList,message).upper() + " " + help.check_for_keywords_from_list(cl.explorerList,message).upper() + " at " +help.check_for_keywords_from_list(cl.programsFolderList,message).upper())
            # EXPLORER (Home)
            elif help.check_for_keywords_from_list(cl.homeFolderList,message):
                create_process(vars.folders, "Explorer", cl.homeFolderList, message, explorer_path, home_folder)
                vars.executed_commands.append(help.check_for_keywords_from_list(cl.openingList,message).upper() + " " + help.check_for_keywords_from_list(cl.explorerList,message).upper() + " at " +help.check_for_keywords_from_list(cl.homeFolderList,message).upper())
                
            # EXPLORER (Downloads)
            elif help.check_for_keywords_from_list(cl.downloadFolderList,message):
                create_process(vars.folders, "Explorer", cl.downloadFolderList, message, explorer_path, download_folder)
                vars.executed_commands.append(help.check_for_keywords_from_list(cl.openingList,message).upper() + " " + help.check_for_keywords_from_list(cl.explorerList,message).upper() + " at " +help.check_for_keywords_from_list(cl.downloadFolderList,message).upper())
            else:
                create_process(vars.folders, "Explorer", cl.explorerList, message, explorer_path, my_computer_folder)
                vars.executed_commands.append(help.check_for_keywords_from_list(cl.openingList,message).upper() + " " + help.check_for_keywords_from_list(cl.explorerList,message).upper() + " at " +help.check_for_keywords_from_list(cl.myComputerList,message).upper())
            
        # CHROME
        elif help.check_for_keywords_from_list(cl.chromeList,message):
            create_process(vars.chrome, "Chrome", cl.chromeList, message, chrome_path, None)
            vars.executed_commands.append(help.check_for_keywords_from_list(cl.openingList,message).upper() + " " + help.check_for_keywords_from_list(cl.chromeList,message).upper())
        
        # FIREFOX
        elif help.check_for_keywords_from_list(cl.firefoxList,message):
            # FIREFOX INCOGNITO
            if help.check_for_keywords_from_list(cl.incognitoList,message):
                create_process(vars.firefoxincognito, "Firefox", cl.incognitoList, message, firefox_path, "-private-window")
                vars.executed_commands.append(help.check_for_keywords_from_list(cl.openingList,message).upper() + " " + help.check_for_keywords_from_list(cl.incognitoList,message).upper())

            else:
                create_process(vars.firefox, "Firefox", cl.firefoxList, message, firefox_path, None)   
                vars.executed_commands.append(help.check_for_keywords_from_list(cl.openingList,message).upper() + " " + help.check_for_keywords_from_list(cl.firefoxList,message).upper())
            
        # VLC
        elif help.check_for_keywords_from_list(cl.vlcList,message):
            create_process(vars.vlc, "VLC", cl.vlcList, message, vlc_path, None)
            vars.executed_commands.append(help.check_for_keywords_from_list(cl.openingList,message).upper() + " " + help.check_for_keywords_from_list(cl.vlcList,message).upper())
            
        # MEDIA PLAYER CLASSIC
        elif help.check_for_keywords_from_list(cl.mpcList,message):
            create_process(vars.mpc, "MPC", cl.mpcList, message, mpc_path, None)
            vars.executed_commands.append(help.check_for_keywords_from_list(cl.openingList,message).upper() + " " + help.check_for_keywords_from_list(cl.mpcList,message).upper())
            
        # KEEPASS
        elif help.check_for_keywords_from_list(cl.keepassList,message):
            create_process(vars.keepass, "KeePass", cl.keepassList, message, keepass_path, None)
            vars.executed_commands.append(help.check_for_keywords_from_list(cl.openingList,message).upper() + " " + help.check_for_keywords_from_list(cl.keepassList,message).upper())
            
        # STEAM
        elif help.check_for_keywords_from_list(cl.steamList,message):
            create_process(vars.steam, "Steam", cl.steamList, message, steam_path, None)
            vars.executed_commands.append(help.check_for_keywords_from_list(cl.openingList,message).upper() + " " + help.check_for_keywords_from_list(cl.steamList,message).upper())
        
        # DISCORD
        elif help.check_for_keywords_from_list(cl.discordList,message):
            create_process(vars.discord, "Discord", cl.discordList, message, discord_path, None)
            vars.executed_commands.append(help.check_for_keywords_from_list(cl.openingList,message).upper() + " " + help.check_for_keywords_from_list(cl.discordList,message).upper())
            
        # MS WORD
        elif help.check_for_keywords_from_list(cl.wordList,message):
            create_process(vars.ms_word, "Winword", cl.wordList, message, word_path, None)
            vars.executed_commands.append(help.check_for_keywords_from_list(cl.openingList,message).upper() + " " + help.check_for_keywords_from_list(cl.wordList,message).upper())
        
        # MS EXCEL
        elif help.check_for_keywords_from_list(cl.excelList,message):
            create_process(vars.ms_excel, "Excel", cl.excelList, message, excel_path, None)
            vars.executed_commands.append(help.check_for_keywords_from_list(cl.openingList,message).upper() + " " + help.check_for_keywords_from_list(cl.excelList,message).upper())
            
        # MS POWERPOINT
        elif help.check_for_keywords_from_list(cl.powerpointList,message):
            create_process(vars.ms_pp, "Powerpnt", cl.powerpointList, message, powerpoint_path, None)
            vars.executed_commands.append(help.check_for_keywords_from_list(cl.openingList,message).upper() + " " + help.check_for_keywords_from_list(cl.powerpointList,message).upper())
        
        # NOTEPAD++
        elif help.check_for_keywords_from_list(cl.notepadppList,message):
            create_process(vars.npp, "Notepad++", cl.notepadppList, message, notepadpp_path, None)
            vars.executed_commands.append(help.check_for_keywords_from_list(cl.openingList,message).upper() + " " + help.check_for_keywords_from_list(cl.notepadppList,message).upper())
            
        # VISUAL STUDIO CODE
        elif help.check_for_keywords_from_list(cl.vscList,message):
            create_process(vars.vsc, "Code.exe", cl.vscList, message, vsc_path, None)
            vars.executed_commands.append(help.check_for_keywords_from_list(cl.openingList,message).upper() + " " + help.check_for_keywords_from_list(cl.vscList,message).upper())
            
        # PUREREF
        elif help.check_for_keywords_from_list(cl.purerefList,message):
            create_process(vars.pureref, "PureRef", cl.purerefList, message, pureref_path, None)
            vars.executed_commands.append(help.check_for_keywords_from_list(cl.openingList,message).upper() + " " + help.check_for_keywords_from_list(cl.purerefList,message).upper())
        
        # AUDACITY
        elif help.check_for_keywords_from_list(cl.audacityList,message):
            create_process(vars.audacity, "Audacity", cl.audacityList, message, audacity_path, None)
            vars.executed_commands.append(help.check_for_keywords_from_list(cl.openingList,message).upper() + " " + help.check_for_keywords_from_list(cl.audacityList,message).upper())
        
        # BLENDER
        elif help.check_for_keywords_from_list(cl.blenderList,message):
            create_process(vars.blender, "Blender", cl.blenderList, message, blender_path, None)
            vars.executed_commands.append(help.check_for_keywords_from_list(cl.openingList,message).upper() + " " + help.check_for_keywords_from_list(cl.blenderList,message).upper())
            
        # STABLE DIFFUSION
        elif help.check_for_keywords_from_list(cl.stablediffusionList,message):
            create_process(vars.stablediffusion, "Stable Diffusion", cl.stablediffusionList, message, stablediffusion_path, None)
            vars.executed_commands.append(help.check_for_keywords_from_list(cl.openingList,message).upper() + " " + help.check_for_keywords_from_list(cl.stablediffusionList,message).upper())
            
        # CALCULATOR
        elif help.check_for_keywords_from_list(cl.calculatorList,message):
            create_process(vars.calc, "Rechner", cl.calculatorList, message, calculator_path, None)
            vars.executed_commands.append(help.check_for_keywords_from_list(cl.openingList,message).upper() + " " + help.check_for_keywords_from_list(cl.calculatorList,message).upper())
            
        # SYSTEM SETTINGS
        elif help.check_for_keywords_from_list(cl.controlList,message):
            print(f"- - - {help.check_for_keywords_from_list(cl.controlList,message).upper()} - - -")
            subprocess.Popen(["control.exe", "/name", "Microsoft.System"])
            vars.executed_commands.append(help.check_for_keywords_from_list(cl.openingList,message).upper() + " " + help.check_for_keywords_from_list(cl.controlList,message).upper())
            
        # AUDIO SETTINGS
        #elif help.check_for_keywords_from_list(cl.audioList,message):
            #create_process(cl.audioList, message, "control", "mmsys.cpl")
            #action.append(help.check_for_keywords_from_list(cl.openingList,message).upper() + " " + help.check_for_keywords_from_list(cl.audioList,message))
        
        # DISPLAY SETTINGS   
        #elif help.check_for_keywords_from_list(cl.videoList,message):
            #create_process(cl.videoList, message, "rundll32.exe", "shell32.dll,Control_RunDLL desk.cpl")
            #action.append(help.check_for_keywords_from_list(cl.openingList,message).upper() + " " + help.check_for_keywords_from_list(cl.videoList,message))
            
        # DESKTOP SETTINGS   
        #elif help.check_for_keywords_from_list(cl.desktopList,message):
            #create_process(cl.desktopList, message, "control", "desk.cpl")
            #action.append(help.check_for_keywords_from_list(cl.openingList,message).upper() + " " + help.check_for_keywords_from_list(cl.desktopList,message))
            
        # NEW TAB   
        elif help.check_for_keywords_from_list(cl.tabList,message):
            # FOLDER TAB
            if help.check_for_keywords_from_list(cl.folderList,message):
                print(f"- - - {help.check_for_keywords_from_list(cl.folderList,message).upper()} - - -")
                pyautogui.hotkey('ctrl', 't')
                pyautogui.hotkey('f4')
                time.sleep(0.1)
                if help.check_for_keywords_from_list(cl.downloadFolderList,message):
                    print(f"- - - {help.check_for_keywords_from_list(cl.downloadFolderList,message).upper()} - - -")
                    pyautogui.hotkey('ctrl', 'a')
                    pyautogui.hotkey('del')
                    pyautogui.typewrite(download_folder, interval=vars.llm_type_speed)
                    vars.executed_commands.append(help.check_for_keywords_from_list(cl.openingList,message).upper() + " " + help.check_for_keywords_from_list(cl.folderList,message).upper() + " " + help.check_for_keywords_from_list(cl.tabList,message).upper() + " at " + help.check_for_keywords_from_list(cl.downloadFolderList,message).upper())
                elif help.check_for_keywords_from_list(cl.homeFolderList,message):
                    print(f"- - - {help.check_for_keywords_from_list(cl.homeFolderList,message).upper()} - - -")
                    pyautogui.hotkey('ctrl', 'a')
                    pyautogui.hotkey('del')
                    pyautogui.typewrite(home_folder, interval=vars.llm_type_speed)
                    vars.executed_commands.append(help.check_for_keywords_from_list(cl.openingList,message).upper() + " " + help.check_for_keywords_from_list(cl.folderList,message).upper() + " " + help.check_for_keywords_from_list(cl.tabList,message).upper() + " at " + help.check_for_keywords_from_list(cl.homeFolderList,message).upper())
                elif help.check_for_keywords_from_list(cl.programs86FolderList,message):
                    print(f"- - - {help.check_for_keywords_from_list(cl.programs86FolderList,message).upper()} - - -")
                    pyautogui.hotkey('ctrl', 'a')
                    pyautogui.hotkey('del')
                    pyautogui.typewrite(program_files_x86_folder, interval=vars.llm_type_speed)
                    vars.executed_commands.append(help.check_for_keywords_from_list(cl.openingList,message).upper() + " " + help.check_for_keywords_from_list(cl.folderList,message).upper() + " " + help.check_for_keywords_from_list(cl.tabList,message).upper() + " at " + help.check_for_keywords_from_list(cl.programs86FolderList,message).upper())
                elif help.check_for_keywords_from_list(cl.programsFolderList,message):
                    print(f"- - - {help.check_for_keywords_from_list(cl.programsFolderList,message).upper()} - - -")
                    pyautogui.hotkey('ctrl', 'a')
                    pyautogui.hotkey('del')
                    pyautogui.typewrite(program_files_folder, interval=vars.llm_type_speed)
                    vars.executed_commands.append(help.check_for_keywords_from_list(cl.openingList,message).upper() + " " + help.check_for_keywords_from_list(cl.folderList,message).upper() + " " + help.check_for_keywords_from_list(cl.tabList,message).upper() + " at " + help.check_for_keywords_from_list(cl.programsFolderList,message).upper())
                elif help.check_for_keywords_from_list(cl.appDataList,message):
                    print(f"- - - {help.check_for_keywords_from_list(cl.appDataList,message).upper()} - - -")
                    pyautogui.hotkey('ctrl', 'a')
                    pyautogui.hotkey('del')
                    pyautogui.typewrite(home_folder + r"\AppData", interval=vars.llm_type_speed)
                    vars.executed_commands.append(help.check_for_keywords_from_list(cl.openingList,message).upper() + " " + help.check_for_keywords_from_list(cl.folderList,message).upper() + " " + help.check_for_keywords_from_list(cl.tabList,message).upper() + " at " + help.check_for_keywords_from_list(cl.appDataList,message).upper())
                elif help.check_for_keywords_from_list(cl.dDriveList,message):
                    print(f"- - - {help.check_for_keywords_from_list(cl.dDriveList,message).upper()} - - -")
                    pyautogui.hotkey('ctrl', 'a')
                    pyautogui.hotkey('del')
                    pyautogui.typewrite(r"D:", interval=vars.llm_type_speed)
                    vars.executed_commands.append(help.check_for_keywords_from_list(cl.openingList,message).upper() + " " + help.check_for_keywords_from_list(cl.folderList,message).upper() + " " + help.check_for_keywords_from_list(cl.tabList,message).upper() + " at " + help.check_for_keywords_from_list(cl.dDriveList,message).upper())
                elif help.check_for_keywords_from_list(cl.cDriveList,message):
                    print(f"- - - {help.check_for_keywords_from_list(cl.cDriveList,message).upper()} - - -")
                    pyautogui.hotkey('ctrl', 'a')
                    pyautogui.hotkey('del')
                    pyautogui.typewrite(r"C:", interval=vars.llm_type_speed)
                    vars.executed_commands.append(help.check_for_keywords_from_list(cl.openingList,message).upper() + " " + help.check_for_keywords_from_list(cl.folderList,message).upper() + " " + help.check_for_keywords_from_list(cl.tabList,message).upper() + " at " + help.check_for_keywords_from_list(cl.cDriveList,message).upper())
                elif help.check_for_keywords_from_list(cl.myComputerList,message):
                    print(f"- - - {help.check_for_keywords_from_list(cl.myComputerList,message).upper()} - - -")
                    pyautogui.hotkey('ctrl', 'a')
                    pyautogui.press('del')
                    keyboard.write(my_computer_folder)
                    vars.executed_commands.append(help.check_for_keywords_from_list(cl.openingList,message).upper() + " " + help.check_for_keywords_from_list(cl.folderList,message).upper() + " " + help.check_for_keywords_from_list(cl.tabList,message).upper() + " at " + help.check_for_keywords_from_list(cl.myComputerList,message).upper())
                else:
                    print(f"- - - MY COMPUTER: - - -")
                    pyautogui.hotkey('ctrl', 'a')
                    pyautogui.press('del')
                    keyboard.write(my_computer_folder)
                    vars.executed_commands.append(help.check_for_keywords_from_list(cl.openingList,message).upper() + " " + help.check_for_keywords_from_list(cl.folderList,message).upper() + " " + help.check_for_keywords_from_list(cl.tabList,message).upper() + " at " + help.check_for_keywords_from_list(cl.myComputerList,message).upper())
                pyautogui.hotkey('enter')
            # BROWSER TAB
            elif help.check_for_keywords_from_list(cl.browserTabList,message) and "Mozilla Firefox" in help.get_current_window_title():
                print(f"- - - {help.check_for_keywords_from_list(cl.browserTabList,message).upper()} - - -")
                pyautogui.hotkey('ctrl', 't')
                vars.executed_commands.append(help.check_for_keywords_from_list(cl.openingList,message).upper() + " " + help.check_for_keywords_from_list(cl.browserTabList,message).upper())
            else:
                print(f"- - - NOTHING TO CREATE A TAB IN FOCUS - - -")
              
    # CLOSING
    if help.check_for_keywords_from_list(cl.closingList,message):
        print(f"- - - {help.check_for_keywords_from_list(cl.closingList,message).upper()} - - -")
        # TAB   
        if help.check_for_keywords_from_list(cl.tabList,message):
            print(f"- - - {help.check_for_keywords_from_list(cl.tabList,message).upper()} - - -")
            pyautogui.hotkey('ctrl', 'w')
            vars.executed_commands.append(help.check_for_keywords_from_list(cl.closingList,message).upper() + " " + help.check_for_keywords_from_list(cl.tabList,message).upper())

        # EXPLORER
        elif help.check_for_keywords_from_list(cl.explorerList,message):
            print(f"- - - {help.check_for_keywords_from_list(cl.explorerList,message).upper()} - - -")
            help.close_pids(vars.folders, "Explorer")
            vars.executed_commands.append(help.check_for_keywords_from_list(cl.closingList,message).upper() + " " + help.check_for_keywords_from_list(cl.explorerList,message).upper())
        # CHROME
        elif help.check_for_keywords_from_list(cl.chromeList,message):
            print(f"- - - {help.check_for_keywords_from_list(cl.chromeList,message).upper()} - - -")
            help.close_pids(vars.chrome, "Chrome")
            vars.executed_commands.append(help.check_for_keywords_from_list(cl.closingList,message).upper() + " " + help.check_for_keywords_from_list(cl.chromeList,message).upper())
        # FIREFOX
        elif help.check_for_keywords_from_list(cl.firefoxList,message):
            print(f"- - - {help.check_for_keywords_from_list(cl.firefoxList,message).upper()} - - -")
            if help.check_for_keywords_from_list(cl.incognitoList,message):
                print(f"- - - {help.check_for_keywords_from_list(cl.incognitoList,message).upper()} - - -")
                help.close_pids(vars.firefoxincognito, "Firefox")
                vars.executed_commands.append(help.check_for_keywords_from_list(cl.closingList,message).upper() + " " + help.check_for_keywords_from_list(cl.incognitoList,message).upper())
            else:
                help.close_pids(vars.firefox, "Firefox")
                vars.executed_commands.append(help.check_for_keywords_from_list(cl.closingList,message).upper() + " " + help.check_for_keywords_from_list(cl.firefoxList,message).upper())
        # VLC
        elif help.check_for_keywords_from_list(cl.vlcList,message):
            print(f"- - - {help.check_for_keywords_from_list(cl.vlcList,message).upper()} - - -")
            help.close_pids(vars.vlc, "VLC")
            vars.executed_commands.append(help.check_for_keywords_from_list(cl.closingList,message).upper() + " " + help.check_for_keywords_from_list(cl.vlcList,message).upper())
        # MEDIA PLAYER CLASSIC
        elif help.check_for_keywords_from_list(cl.mpcList,message):
            print(f"- - - {help.check_for_keywords_from_list(cl.mpcList,message).upper()} - - -")
            help.close_pids(vars.mpc, "MPC")
            vars.executed_commands.append(help.check_for_keywords_from_list(cl.closingList,message).upper() + " " + help.check_for_keywords_from_list(cl.mpcList,message).upper())
        # KEEPASS
        elif help.check_for_keywords_from_list(cl.keepassList,message):
            print(f"- - - {help.check_for_keywords_from_list(cl.keepassList,message).upper()} - - -")
            help.close_pids(vars.keepass, "KeePass")
            vars.executed_commands.append(help.check_for_keywords_from_list(cl.closingList,message).upper() + " " + help.check_for_keywords_from_list(cl.keepassList,message).upper())
        # STEAM
        elif help.check_for_keywords_from_list(cl.steamList,message):
            print(f"- - - {help.check_for_keywords_from_list(cl.steamList,message).upper()} - - -")
            help.close_pids(vars.steam, "Steam")
            vars.executed_commands.append(help.check_for_keywords_from_list(cl.closingList,message).upper() + " " + help.check_for_keywords_from_list(cl.steamList,message).upper())
        # DISCORD
        elif help.check_for_keywords_from_list(cl.discordList,message):
            print(f"- - - {help.check_for_keywords_from_list(cl.discordList,message).upper()} - - -")
            help.close_pids(vars.discord, "Discord")
            vars.executed_commands.append(help.check_for_keywords_from_list(cl.closingList,message).upper() + " " + help.check_for_keywords_from_list(cl.discordList,message).upper())
        # MS WORD
        elif help.check_for_keywords_from_list(cl.wordList,message):
            print(f"- - - {help.check_for_keywords_from_list(cl.wordList,message).upper()} - - -")
            help.close_pids(vars.ms_word, "Winword")
            vars.executed_commands.append(help.check_for_keywords_from_list(cl.closingList,message).upper() + " " + help.check_for_keywords_from_list(cl.wordList,message).upper())
        # MS EXCEL
        elif help.check_for_keywords_from_list(cl.excelList,message):
            print(f"- - - {help.check_for_keywords_from_list(cl.excelList,message).upper()} - - -")
            help.close_pids(vars.ms_excel, "Excel")
            vars.executed_commands.append(help.check_for_keywords_from_list(cl.closingList,message).upper() + " " + help.check_for_keywords_from_list(cl.excelList,message).upper())
        # MS POWERPOINT
        elif help.check_for_keywords_from_list(cl.powerpointList,message):
            print(f"- - - {help.check_for_keywords_from_list(cl.powerpointList,message).upper()} - - -")
            help.close_pids(vars.ms_pp, "Powerpnt")
            vars.executed_commands.append(help.check_for_keywords_from_list(cl.closingList,message).upper() + " " + help.check_for_keywords_from_list(cl.powerpointList,message).upper())
        # NOTEPAD++
        elif help.check_for_keywords_from_list(cl.notepadppList,message):
            print(f"- - - {help.check_for_keywords_from_list(cl.notepadppList,message).upper()} - - -")
            help.close_pids(vars.npp, "Notepad++")
            vars.executed_commands.append(help.check_for_keywords_from_list(cl.closingList,message).upper() + " " + help.check_for_keywords_from_list(cl.notepadppList,message).upper())
        # VISUAL STUDIO CODE
        elif help.check_for_keywords_from_list(cl.vscList,message):
            print(f"- - - {help.check_for_keywords_from_list(cl.vscList,message).upper()} - - -")
            help.close_pids(vars.vsc, "Code.exe")
            vars.executed_commands.append(help.check_for_keywords_from_list(cl.closingList,message).upper() + " " + help.check_for_keywords_from_list(cl.vscList,message).upper())
        # PUREREF
        elif help.check_for_keywords_from_list(cl.purerefList,message):
            print(f"- - - {help.check_for_keywords_from_list(cl.purerefList,message).upper()} - - -")
            help.close_pids(vars.pureref, "PureRef")
            vars.executed_commands.append(help.check_for_keywords_from_list(cl.closingList,message).upper() + " " + help.check_for_keywords_from_list(cl.purerefList,message).upper())
        # AUDACITY
        elif help.check_for_keywords_from_list(cl.audacityList,message):
            print(f"- - - {help.check_for_keywords_from_list(cl.audacityList,message).upper()} - - -")
            help.close_pids(vars.audacity, "Audacity")
            vars.executed_commands.append(help.check_for_keywords_from_list(cl.closingList,message).upper() + " " + help.check_for_keywords_from_list(cl.audacityList,message).upper())
        # BLENDER
        elif help.check_for_keywords_from_list(cl.blenderList,message):
            print(f"- - - {help.check_for_keywords_from_list(cl.blenderList,message).upper()} - - -")
            help.close_pids(vars.blender, "Blender")
            vars.executed_commands.append(help.check_for_keywords_from_list(cl.closingList,message).upper() + " " + help.check_for_keywords_from_list(cl.blenderList,message).upper())
        # STABLE DIFFUSION
        elif help.check_for_keywords_from_list(cl.stablediffusionList,message):
            print(f"- - - {help.check_for_keywords_from_list(cl.stablediffusionList,message).upper()} - - -")
            help.close_pids(vars.stablediffusion, "Stable Diffusion")
            vars.executed_commands.append(help.check_for_keywords_from_list(cl.closingList,message).upper() + " " + help.check_for_keywords_from_list(cl.stablediffusionList,message).upper())
        # CALCULATOR
        elif help.check_for_keywords_from_list(cl.calculatorList,message):
            print(f"- - - {help.check_for_keywords_from_list(cl.calculatorList,message).upper()} - - -")
            help.close_pids(vars.calc, "Rechner")
            vars.executed_commands.append(help.check_for_keywords_from_list(cl.closingList,message).upper() + " " + help.check_for_keywords_from_list(cl.calculatorList,message).upper())
        # WINDOW
        elif help.check_for_keywords_from_list(cl.windowList,message):
            print(f"- - - {help.check_for_keywords_from_list(cl.windowList,message).upper()} - - -")
            pyautogui.hotkey('alt', 'f4')
            vars.executed_commands.append(help.check_for_keywords_from_list(cl.closingList,message).upper() + " " + help.check_for_keywords_from_list(cl.windowList,message).upper())
            
    # SWITCHING
    if help.check_for_keywords_from_list(cl.switchingList,message) and help.check_for_keywords_from_list(cl.gotoList,message) is None and help.check_for_keywords_from_list(cl.backList,message) is None:
        print(f"- - - {help.check_for_keywords_from_list(cl.switchingList,message).upper()} - - -")
        if help.check_for_keywords_from_list(cl.tabList,message):
            print(f"- - - {help.check_for_keywords_from_list(cl.tabList,message).upper()} - - -")
            pyautogui.hotkey('ctrl', 'tab')
            vars.executed_commands.append(help.check_for_keywords_from_list(cl.switchingList,message).upper() + " " + help.check_for_keywords_from_list(cl.tabList,message).upper())
        else:
            print(f"- - - WINDOW - - -")
            pyautogui.hotkey('alt', 'tab')
            vars.executed_commands.append(help.check_for_keywords_from_list(cl.switchingList,message).upper() + " " + help.check_for_keywords_from_list(cl.windowList,message).upper())
            
    # MINIMIZING
    if help.check_for_keywords_from_list(cl.minimizingList,message):
        print(f"- - - {help.check_for_keywords_from_list(cl.minimizingList,message).upper()} - - -")
        pyautogui.hotkey('win', 'down')
        vars.executed_commands.append(help.check_for_keywords_from_list(cl.minimizingList,message).upper() + " WIWNDOW")
         
    # MAXIMIZING
    if help.check_for_keywords_from_list(cl.maximizingList,message):
        print(f"- - - {help.check_for_keywords_from_list(cl.maximizingList,message).upper()} - - -")
        pyautogui.hotkey('win', 'up')
        vars.executed_commands.append(help.check_for_keywords_from_list(cl.maximizingList,message).upper() + " WIWNDOW")
    
    if init_commands == vars.executed_commands:
        return False
    else:
        return True
        
    # Multisentence Analysis: Split reply into sentences, then find verbs in the sentences and object and formulate command chain.
    # Extension for Firefox to control browser tab content
    # Youtube API for outside browser access of youtube search
    # Google API for scraping information
    # ChatGPT API for complicated tasks
        
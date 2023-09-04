import helpers
import command_list as cl
from pywinauto import Application, findwindows

# APPLICATIONS
firefox = Application(backend="uia")
firefox_incognito = Application(backend="uia")
firefox_path = r"C:\Program Files\Mozilla Firefox\firefox.exe"

explorer = Application(backend="uia")

def check_ai_for_command(message):
    # OPENING
    if helpers.check_for_keywords_from_list(cl.openingList,message) is not None:
        print(f"- - - {helpers.check_for_keywords_from_list(cl.openingList,message).upper()} - - -")
        
        # FIREFOX
        if helpers.check_for_keywords_from_list(cl.firefoxList,message) is not None:
            # Open Firefox
            firefox.start(firefox_path)
            # Wait for Firefox to open
            firefox.wait('ready')
            # Bring Firefox to the foreground
            firefox.set_focus()
        
        # FIREFOX INCOGNITO
        if helpers.check_for_keywords_from_list(cl.incognitoList,message) is not None:
            # Start Firefox in incognito (private browsing) mode
            firefox_incognito.start(f'{firefox_path} -private-window')
            # Wait for Firefox to open
            firefox_incognito.wait('ready')
            # Bring Firefox incognito to the foreground
            firefox_incognito.set_focus()
        
        # EXPLORER
        if helpers.check_for_keywords_from_list(cl.explorerList,message) is not None:
            # Start a new Windows Explorer window
            explorer.start("explorer.exe")
            # Wait for Explorer to open
            explorer.wait('ready')
            # Send the path to "My Computer" to the address bar
            explorer.window(title="File Explorer").type_keys('::{20D04FE0-3AEA-1069-A2D8-08002B30309D}')
            explorer.window(title="File Explorer").type_keys('{ENTER}')
            explorer.set_focus()
            
    # CLOSING
    elif helpers.check_for_keywords_from_list(cl.closingList,message) is not None:
        print(f"- - - {helpers.check_for_keywords_from_list(cl.closingList,message).upper()} - - -")
        # Close something like:
            # Program List
            # Folder List
            # Pretty much everyrhing
            # Tab
            
    # SWITCHING
    elif helpers.check_for_keywords_from_list(cl.switchingList,message) is not None:
        print(f"- - - {helpers.check_for_keywords_from_list(cl.switchingList,message).upper()} - - -")
        # Switch something like:
            # Program List
            # Folder List
            # Pretty much everyrhing
            # Tab
            
    # MINIMIZING
    elif helpers.check_for_keywords_from_list(cl.minimizingList,message) is not None:
        print(f"- - - {helpers.check_for_keywords_from_list(cl.minimizingList,message).upper()} - - -")
        # Minimize something like:
            # Program List
            # Folder List
            # Pretty much everyrhing
            # Tab
            
    # MAXIMIZING
    elif helpers.check_for_keywords_from_list(cl.maximizingList,message) is not None:
        print(f"- - - {helpers.check_for_keywords_from_list(cl.maximizingList,message).upper()} - - -")
        # Maximize something like:
            # Program List
            # Folder List
            # Pretty much everyrhing
            # Tab
            
        
    # if message contains word from list of words, trigger next function tree
        # Programs folder
        # My Computer folder
        # Programs86 folder
        # Discord
        # Firefox
        # Steam
        # Youtube
        # Close Tab
        # Open Tab
        # Close Window
        # Switch Tab
        # Microsoft Word
        # Microsoft Excel
        # Notepad++
        # Blender
        # Audacity
        
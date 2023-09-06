import helpers
import command_list as cl
import subprocess
import pyautogui
import time

# APPLICATIONS
# Define the paths to the applications
firefox_path = r"C:\Program Files\Mozilla Firefox\firefox.exe"
explorer_path = "explorer.exe"

def check_for_command(message):
    # OPENING
    if helpers.check_for_keywords_from_list(cl.openingList,message) is not None:
        print(f"- - - {helpers.check_for_keywords_from_list(cl.openingList,message).upper()} - - -")
        
        # FIREFOX
        if helpers.check_for_keywords_from_list(cl.firefoxList,message) is not None:
            # Open Firefox
            subprocess.Popen([firefox_path])
            # Wait for Firefox to open
            time.sleep(5)
            # Bring Firefox to the foreground
            pyautogui.click()
        
        # FIREFOX INCOGNITO
        if helpers.check_for_keywords_from_list(cl.incognitoList,message) is not None:
            # Start Firefox in incognito (private browsing) mode
            subprocess.Popen([firefox_path, "-private-window"])
            # Wait for Firefox to open
            time.sleep(5)
            # Bring Firefox incognito to the foreground
            pyautogui.click()
        
        # EXPLORER
        if helpers.check_for_keywords_from_list(cl.explorerList,message) is not None:
            # Start a new Windows Explorer window
            subprocess.Popen([explorer_path])
            # Wait for Explorer to open
            time.sleep(5)
            
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
        
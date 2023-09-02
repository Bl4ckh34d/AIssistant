import record_audio
import warnings
import AI_LLM

warnings.filterwarnings("ignore", message=".*The 'nopython' keyword.*")

def show_intro():
    print()
    print("====================================================================")
    print("\n     _      ___               _         _                     _   ")
    print("    / \    |_ _|  ___   ___  (_)  ___  | |_    __ _   _ __   | |_ ")
    print("   / _ \    | |  / __| / __| | | / __| | __|  / _` | | '_ \  | __|")
    print("  / ___ \   | |  \__ \ \__ \ | | \__ \ | |_  | (_| | | | | | | |_ ")
    print(" /_/   \_\ |___| |___/ |___/ |_| |___/  \__|  \__,_| |_| |_|  \__|\n")
    print("====================================================================")
    

show_intro() 

input("Press Enter to continue...")
print()
AI_LLM.invoke_tts(f"Alright, what do you need, {AI_LLM.user_name}?")

recording = record_audio.Recorder()
recording.listen()
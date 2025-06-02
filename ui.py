from decoder import decode_save_file
from encoder import encode_save_file
from utils import print_colored
from settings import CYAN, GREEN, YELLOW

def menu_loop():
    while True:
        print_colored("\n🌲 Cozy Grove Save Editor 🌲", CYAN)
        print("1️⃣  Decode save file")
        print("2️⃣  Encode save file")
        print("3️⃣  Exit")

        choice = input("\n👉 Choose an option (1-3): ").strip()

        if choice == "1":
            decode_save_file()
        elif choice == "2":
            encode_save_file()
        elif choice == "3":
            print_colored("👋 Goodbye!", YELLOW)
            break
        else:
            print_colored("❌ Invalid choice, try again.", "red")
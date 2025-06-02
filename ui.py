from decoder import decode_save_file
from encoder import encode_save_file
from save_manager import (
    load_save,
    write_save,
    list_inventory,
    set_item_amount,
    toggle_equip,
    remove_item,
    add_new_item,
)
from utils import print_colored, print_error
from settings import CYAN, GREEN, YELLOW, CONFIG_IDS
from autocomplete import autocomplete_prompt

def inventory_menu(data: dict) -> None:
    while True:
        print_colored("\n🎒 Inventory Management 🎒", CYAN)
        print("1.  List all items")
        print("2.  Change item amount")
        print("3.  Remove an item")
        print("4.  Add a new item")
        print("5.  Back to main menu")

        choice = input("\n👉 Choice [1-5]: ").strip()
        if choice == "1":
            list_inventory(data)

        elif choice == "2":
            cfg = input("→ Enter configID to modify (exact): ").strip()
            try:
                new_amt = int(input("→ New amount: ").strip())
            except ValueError:
                print_error("Amount must be an integer.")
                continue

            if set_item_amount(data, cfg, new_amt):
                write_save(data)

        elif choice == "3":
            cfg = input("→ Enter configID to remove (exact): ").strip()
            if remove_item(data, cfg):
                write_save(data)

        elif choice == "4":
            # ↪ Use autocomplete to select a configID
            result = autocomplete_prompt("→ Type item name: ", CONFIG_IDS)
            if not result:
                # User cancelled or ESC pressed
                print_error("Add‐item canceled.")
                continue

            # result is a valid configID
            cfg = result
            try:
                amt = int(input(f"→ How many '{cfg}'? ").strip())
            except ValueError:
                print_error("Amount must be an integer.")
                continue

            if add_new_item(data, cfg, amt):
                write_save(data)

        elif choice == "5":
            break

        else:
            print_error("Invalid choice. Please select 1–5.")


def menu_loop():
    from colorama import init as colorama_init
    colorama_init(autoreset=True)

    while True:
        print_colored("\n🌲 Cozy Grove Save Editor 🌲", CYAN)
        print(" 1️⃣  Decode save file")
        print(" 2️⃣  Encode save file")
        print(" 3️⃣  Modify Inventory")
        print(" 4️⃣  Exit")

        choice = input("\n👉 Choose (1-4): ").strip()
        if choice == "1":
            decode_save_file()

        elif choice == "2":
            encode_save_file()

        elif choice == "3":
            data = load_save()
            if data:
                inventory_menu(data)

        elif choice == "4":
            print_colored("👋 Goodbye!", YELLOW)
            break

        else:
            print_error("Invalid choice. Please select 1–4.")
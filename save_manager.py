# save_manager.py

from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
import json
import uuid

from settings import DECODED_JSON_PATH
from utils import print_success, print_error

SaveData = Dict[str, Any]
Slot = Dict[str, Any]


def load_save() -> Optional[SaveData]:
    """
    Load the decoded JSON (data/cg_save.json) into a Python dict.
    Returns None if the file does not exist or is invalid.
    """
    path = Path(DECODED_JSON_PATH)
    if not path.exists():
        print_error(f"Decoded file not found at {DECODED_JSON_PATH}. Run Decode first.")
        return None

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except Exception as e:
        print_error(f"Failed to load JSON: {e}")
        return None


def write_save(data: SaveData) -> bool:
    """
    Overwrite data/cg_save.json with the modified dict.
    """
    try:
        with open(DECODED_JSON_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        print_success(f"Changes written to {DECODED_JSON_PATH}")
        return True
    except Exception as e:
        print_error(f"Failed to write JSON: {e}")
        return False


def _get_slot_display_order(data: SaveData) -> List[Slot]:
    """
    Return the list of SlotDisplayOrder entries (skipping nulls).
    """
    inv = data.get("Player", {}).get("Inventory", {})
    raw_list = inv.get("SlotDisplayOrder", [])
    return [slot for slot in raw_list if slot is not None]


def list_inventory(data: SaveData) -> None:
    """
    Print each slot’s configID, amount, and instanceID.
    """
    slots = _get_slot_display_order(data)
    if not slots:
        print(" (Inventory is empty.)")
        return

    print("\nInventory Slots:")
    for idx, slot in enumerate(slots, start=1):
        item = slot.get("item", {})
        cfg = item.get("configID", "<unknown>")
        amt = slot.get("amount", 0)
        iid = item.get("instanceID", "<no-id>")
        equip = item.get("equipped", False)
        status = "🔹" if equip else " "
        print(f" {status} [{idx}] {cfg:30s} x{amt}   (id={iid})")
    print()


def find_slot_by_config(data: SaveData, config_id: str) -> Optional[Tuple[int, Slot]]:
    """
    Return (index_in_list, slot_dict) for the first matching configID in SlotDisplayOrder,
    or None if not found.
    """
    for idx, slot in enumerate(_get_slot_display_order(data)):
        item = slot.get("item", {})
        if item.get("configID") == config_id:
            return idx, slot
    return None


def set_item_amount(
    data: SaveData, config_id: str, new_amount: int
) -> bool:
    """
    Update the "amount" field for a given configID. Returns True if succeeded.
    """
    found = find_slot_by_config(data, config_id)
    if not found:
        print_error(f"Item '{config_id}' not in inventory.")
        return False

    idx, slot = found
    slot["amount"] = new_amount
    # Also update the nested item.amount to keep consistency
    slot.get("item", {})["amount"] = new_amount
    print_success(f"Set '{config_id}' amount to {new_amount}.")
    return True


def toggle_equip(data: SaveData, config_id: str) -> bool:
    """
    Flip the 'equipped' boolean for that item. Return True if succeeded.
    """
    found = find_slot_by_config(data, config_id)
    if not found:
        print_error(f"Item '{config_id}' not in inventory.")
        return False

    _, slot = found
    item = slot.get("item", {})
    current = bool(item.get("equipped", False))
    item["equipped"] = not current
    status = "equipped" if not current else "unequipped"
    print_success(f"{config_id} is now {status}.")
    return True


def remove_item(data: SaveData, config_id: str) -> bool:
    """
    Remove all references to this configID from SlotDisplayOrder.
    """
    inv = data.get("Player", {}).get("Inventory", {})
    sdo = inv.get("SlotDisplayOrder", [])
    changed = False

    for i, slot in enumerate(sdo):
        if slot and slot.get("item", {}).get("configID") == config_id:
            sdo[i] = None
            changed = True

    if changed:
        print_success(f"Removed all '{config_id}' entries from Inventory.")
        return True
    else:
        print_error(f"Item '{config_id}' not found; nothing removed.")
        return False


def add_new_item(data: SaveData, config_id: str, amount: int) -> bool:
    """
    Add a brand-new item into SlotDisplayOrder at the end. Generates a random instanceID.
    Returns True if successful.
    """
    inv = data.get("Player", {}).get("Inventory", {})
    sdo = inv.setdefault("SlotDisplayOrder", [])

    new_instance_id = f"item-{uuid.uuid4().hex[:16].upper()}"
    new_slot: Slot = {
        "item": {
            "configID": config_id,
            "type": "COLLECTABLE_ITEM",
            "state": None,
            "equipped": False,
            "acquired": True,
            "instanceID": new_instance_id,
            "amount": amount,
        },
        "amount": amount,
        "$id": str(uuid.uuid4().int)[:8],
    }
    sdo.append(new_slot)
    print_success(f"Added '{config_id}' x{amount} as instanceID={new_instance_id}.")
    return True
import os
import json
import time
from datetime import datetime
from typing import Dict, List, Any

HISTORY_DIR = os.path.join(os.path.dirname(__file__), "data_history")
os.makedirs(HISTORY_DIR, exist_ok=True)


def _get_safe_path(device_id: str) -> str:
    safe_id = "".join(c for c in device_id if c.isalnum() or c in ("-", "_"))
    if not safe_id:
        safe_id = "default_user"
    return os.path.join(HISTORY_DIR, f"{safe_id}.json")


def load_user_store(device_id: str) -> Dict[str, Any]:
    """Load the full dictionary of chats for this user/device."""
    path = _get_safe_path(device_id)
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict) and "chats" in data:
                    return data
        except Exception:
            pass

    # Default initial store with one empty chat
    initial_id = "chat_1"
    return {
        "active_chat_id": initial_id,
        "chats": {
            initial_id: {
                "id": initial_id,
                "title": "Новый диалог",
                "created_at": datetime.now().strftime("%d.%m %H:%M"),
                "messages": []
            }
        }
    }


def save_user_store(device_id: str, store: Dict[str, Any]):
    """Persist user store to JSON file."""
    path = _get_safe_path(device_id)
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(store, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


def create_new_chat(device_id: str, store: Dict[str, Any]) -> str:
    """Create a new chat in the store, set it active, and save."""
    new_id = f"chat_{int(time.time() * 1000)}"
    store["chats"][new_id] = {
        "id": new_id,
        "title": "Новый диалог",
        "created_at": datetime.now().strftime("%d.%m %H:%M"),
        "messages": []
    }
    store["active_chat_id"] = new_id
    save_user_store(device_id, store)
    return new_id


def delete_chat(device_id: str, store: Dict[str, Any], chat_id: str):
    """Delete a specific chat from the store."""
    if chat_id in store["chats"]:
        del store["chats"][chat_id]

    if not store["chats"]:
        # If no chats left, create a fresh one
        new_id = "chat_1"
        store["chats"][new_id] = {
            "id": new_id,
            "title": "Новый диалог",
            "created_at": datetime.now().strftime("%d.%m %H:%M"),
            "messages": []
        }
        store["active_chat_id"] = new_id
    elif store["active_chat_id"] == chat_id:
        store["active_chat_id"] = next(iter(store["chats"].keys()))

    save_user_store(device_id, store)


def update_active_messages(device_id: str, store: Dict[str, Any], messages: List[Dict[str, str]]):
    """Update messages of the active chat and auto-title if needed."""
    active_id = store.get("active_chat_id")
    if not active_id or active_id not in store["chats"]:
        active_id = next(iter(store["chats"].keys()))
        store["active_chat_id"] = active_id

    chat = store["chats"][active_id]
    chat["messages"] = messages

    # Auto-generate meaningful title from first user query if still default
    if chat.get("title") == "Новый диалог":
        for m in messages:
            if m.get("role") == "user" and m.get("content"):
                clean_text = m["content"].strip().replace("\n", " ")
                chat["title"] = clean_text[:28] + ("..." if len(clean_text) > 28 else "")
                break

    save_user_store(device_id, store)

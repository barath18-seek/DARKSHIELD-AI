import os
import time
import getpass
import hashlib
from datetime import datetime
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

# ============================================================
# DARKSHIELD - ADVANCED SECURE VAULT
# ============================================================

SAFE_DIR = "/storage/emulated/0/DARKSHIELD/SAFE"
LOCK_DIR = "/storage/emulated/0/DARKSHIELD/LOCKED"
EXPORT_DIR = "/storage/emulated/0/DARKSHIELD/EXPORT"

VAULT_PASSWORD = "falcon"
BLOCK_AFTER_TRIES = 3

LOG_FILE = "/storage/emulated/0/USB_GUARDIAN/activity_log.txt"

# ============================================================
# CREATE DIRECTORIES
# ============================================================

for d in [SAFE_DIR, LOCK_DIR, EXPORT_DIR]:
    os.makedirs(d, exist_ok=True)

# ============================================================
# AES UTILITIES
# ============================================================

def pad(data):
    return data + b" " * (16 - len(data) % 16)

def encrypt_file(path, password):
    key = hashlib.sha256(password.encode()).digest()
    iv = get_random_bytes(16)

    cipher = AES.new(key, AES.MODE_CBC, iv)

    with open(path, "rb") as f:
        data = f.read()

    encrypted = cipher.encrypt(pad(data))

    filename = os.path.basename(path)
    locked_file = os.path.join(LOCK_DIR, filename + ".lock")

    with open(locked_file, "wb") as f:
        f.write(iv + encrypted)

def decrypt_file(path, password, destination):
    key = hashlib.sha256(password.encode()).digest()

    with open(path, "rb") as f:
        iv = f.read(16)
        encrypted = f.read()

    cipher = AES.new(key, AES.MODE_CBC, iv)

    decrypted = cipher.decrypt(encrypted).rstrip(b" ")

    filename = os.path.basename(path).replace(".lock", "")

    output_file = os.path.join(destination, filename)

    with open(output_file, "wb") as f:
        f.write(decrypted)

    return output_file

# ============================================================
# TIMESTAMP FUNCTIONS
# ============================================================

def show_timestamps():

    now = datetime.now()

    print("\n===================================")
    print("📅 SECURITY TIMESTAMP")
    print("===================================")

    print("🕒 Normal Time  :", now.strftime("%I:%M:%S %p"))
    print("🚆 Railway Time :", now.strftime("%H:%M:%S"))
    print("📆 Date         :", now.strftime("%d-%m-%Y"))

    print("===================================\n")

# ============================================================
# LOGGING
# ============================================================

def write_log(action, filename):

    now = datetime.now()

    with open(LOG_FILE, "a") as log:
        log.write(
            f"{now.strftime('%Y-%m-%d %H:%M:%S')} | "
            f"{action} | "
            f"{filename}\n"
        )

# ============================================================
# XAI STYLE EXPLANATION
# ============================================================

def explain_action(action, filename):

    print("\n🤖 xAI SECURITY ANALYSIS")
    print("------------------------------------")

    print("📄 File :", filename)
    print("⚙️ Action :", action)

    explanations = {
        "COPY":
            "A duplicate of the selected file will be created.",

        "DELETE":
            "The selected file will be removed from storage.",

        "MOVE":
            "The selected file will be transferred to another location.",

        "EXPORT":
            "The file will be temporarily exported for use.",

        "SHARE":
            "The file is being prepared for external sharing.",

        "RENAME":
            "The filename metadata will be modified."
    }

    print("🧠 Explanation:")
    print(explanations.get(action, "Unknown operation selected."))

    print("------------------------------------\n")

# ============================================================
# FILE ACTION MENU
# ============================================================

def file_activity_menu():

    print("\n📂 FILE ACTIVITY MENU")
    print("1. COPY")
    print("2. DELETE")
    print("3. MOVE")
    print("4. EXPORT")
    print("5. SHARE")
    print("6. RENAME")

    choice = input("\nSelect activity: ")

    actions = {
        "1": "COPY",
        "2": "DELETE",
        "3": "MOVE",
        "4": "EXPORT",
        "5": "SHARE",
        "6": "RENAME"
    }

    return actions.get(choice, "EXPORT")

# ============================================================
# COUNTDOWN TIMER
# ============================================================

def countdown_timer():

    try:

        duration = int(
            input(
                "\n⏳ Enter file access duration (seconds): "
            )
        )

        print("\n🔓 Access Timer Started\n")

        for remaining in range(duration, 0, -1):

            print(f"⏱️ Remaining: {remaining} sec")

            if remaining == 5:
                print(
                    "⚠️ WARNING: File access expires in 5 seconds!"
                )

            time.sleep(1)

        print("\n🔒 Access Time Expired")

    except:
        print("❌ Invalid duration.")

# ============================================================
# LOCK FILES
# ============================================================

def lock_all_files():

    for fname in os.listdir(SAFE_DIR):

        path = os.path.join(SAFE_DIR, fname)

        if os.path.isfile(path):

            encrypt_file(path, VAULT_PASSWORD)
            os.remove(path)

    custom_file = "/storage/emulated/0/.acs/tcs.pdf"

    if os.path.exists(custom_file):

        encrypt_file(custom_file, VAULT_PASSWORD)

        try:
            os.remove(custom_file)
        except:
            pass

# ============================================================
# CLEAR EXPORT
# ============================================================

def clear_export():

    for f in os.listdir(EXPORT_DIR):

        path = os.path.join(EXPORT_DIR, f)

        try:
            if os.path.isfile(path):
                os.remove(path)
        except:
            pass

# ============================================================
# MAIN PROGRAM
# ============================================================

def main():

    print("""
=================================================
🛡️ DARKSHIELD AI -  ADVANCE FILE SYSTEM 🛡️
=================================================
""")

    show_timestamps()

    clear_export()
    lock_all_files()

    tries = 0

    while tries < BLOCK_AFTER_TRIES:

        password = getpass.getpass(
            "🔑 Enter Vault Password: "
        )

        if password == VAULT_PASSWORD:

            print("\n✅ ACCESS GRANTED")

            locked_files = os.listdir(LOCK_DIR)

            if not locked_files:
                print("📂 No locked files found.")
                return

            print("\n🔐 AVAILABLE FILES\n")

            for i, file in enumerate(locked_files):
                print(
                    f"{i + 1}. "
                    f"{file.replace('.lock','')}"
                )

            try:

                choice = int(
                    input("\nSelect file number: ")
                ) - 1

                selected_lock = os.path.join(
                    LOCK_DIR,
                    locked_files[choice]
                )

                action = file_activity_menu()

                explain_action(
                    action,
                    locked_files[choice].replace(".lock", "")
                )

                exported_file = decrypt_file(
                    selected_lock,
                    VAULT_PASSWORD,
                    EXPORT_DIR
                )

                print(
                    "\n📤 File Exported Successfully"
                )

                write_log(
                    action,
                    os.path.basename(exported_file)
                )

                countdown_timer()

                clear_export()

                print(
                    "\n🔒 File Removed From Export Area"
                )
                print(
                    "🛡️ Security Vault Relocked"
                )

                return

            except Exception as e:

                print(
                    "\n❌ Invalid Selection"
                )
                print("Error:", e)

                return

        else:

            tries += 1

            remaining = BLOCK_AFTER_TRIES - tries

            print(
                f"\n❌ Wrong Password "
                f"(Attempts Left: {remaining})"
            )

    print("\n💣 ACCESS DENIED")
    print("🔒 Vault Locked")

# ============================================================
# START
# ============================================================

if __name__ == "__main__":
    main()

from datetime import datetime
import subprocess
from config import settings

ADB_PATH = getattr(settings, "ADB_PATH", None)

def trigger_alert(user, message: str):
    """
    Trigger an emergency alert when suicide risk is detected.
    """
    print("ABD path : ",ADB_PATH)
    try:
        contact_name = user.emergency_contact_name
        contact_phone = user.emergency_contact_phone

        print("🚨 SUICIDE ALERT TRIGGERED")
        print("Time:", datetime.utcnow())
        print("User:", user.username)
        print("Message:", message)

        if contact_name and contact_phone:
            print(f"Contacting emergency person: {contact_name} ({contact_phone})")

            if not ADB_PATH:
                print("⚠ ADB_PATH not set. Skipping ADB emergency call trigger.")
                print("   (Uncomment / set ADB_PATH in backend/.env when ready.)")
                return

            # Trigger phone call through ADB (keep for later)
            subprocess.run(
                [
                    ADB_PATH,
                    "shell",
                    "am",
                    "start",
                    "-a",
                    "android.intent.action.CALL",
                    "-d",
                    f"tel:+91{contact_phone}",
                ],
                check=False,
            )

        else:
            print("⚠ No emergency contact found for this user")

    except Exception as e:
        print("ALERT SERVICE ERROR:", e)
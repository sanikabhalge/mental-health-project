from datetime import datetime
import subprocess
from config import settings

ADB_PATH=settings.ADB_PATH

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

            # Trigger phone call through ADB
            subprocess.run([
                        ADB_PATH,
                        "shell",
                        "am",
                        "start",
                        "-a",
                        "android.intent.action.CALL",
                        "-d",
                        f"tel:+91{contact_phone}"
                    ])

        else:
            print("⚠ No emergency contact found for this user")

    except Exception as e:
        print("ALERT SERVICE ERROR:", e)
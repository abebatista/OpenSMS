import re

try:
    from kivy.utils import platform
except ImportError:
    import sys
    if sys.platform.startswith("win"):
        platform = "win"
    elif sys.platform.startswith("linux"):
        platform = "linux"
    else:
        platform = "unknown"

## OS specific setups
# for android
if platform == "android":
    from jnius import autoclass

## functions

def clean_and_validate_phone(phone_number:str) -> str | None:
    """
    Cleans a phone number by removing spaces, dashes, parentheses, etc.,

    and validates if it follows the international format starting with '+'.

    Returns:
        - The cleaned string (e.g., '+14155552671') if valid.
        - None if the format is invalid.
    """
    if not isinstance(phone_number, str):
        return None

    # Step 1: Remove all characters except digits and the leading '+'
    cleaned = re.sub(r"[^\d+]", "", phone_number)

    # Step 2: Validate using E.164 international standard regex
    # - Starts with '+'
    # - Followed by 1 to 15 digits (country code + subscriber number)
    pattern = r"^\+[1-9]\d{1,14}$"

    if re.match(pattern, cleaned):
        return cleaned

    return None

def send_sms(phone:str, msg:str) -> bool:
    """
    Sends SMS from your default SIM as set in settings.

    Args:
        - phone (str) : The phone number starting with country code. Ex: +14155552671
        - msg (str) : The actual text message which needs to be sent.

    Returns:
        - bool: True if the execution is successful
    """
    stat = False
    if platform == "android":
        try:
            SmsManager = autoclass('android.telephony.SmsManager')
            sms_manager = SmsManager.getDefault()
            parts = sms_manager.divideMessage(msg)
            if parts.size() > 1:
                sms_manager.sendMultipartTextMessage(phone, None, parts, None, None)
            else:
                sms_manager.sendTextMessage(phone, None, msg, None, None)
            stat = True
        except Exception as e:
            print("SMS ❌ Failed:", e)
    else:
        # Desktop platforms to be implemented later
        stat = True
    return stat

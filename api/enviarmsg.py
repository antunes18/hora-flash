import pywhatkit

def send_whatsapp_message(phone_number: str, message: str):
    try:
        print(f"Sending message to {phone_number}...")
        pywhatkit.sendwhatmsg_instantly(phone_no=phone_number, message=message, wait_time=10, tab_close=True, close_time=5)
        print("Message sent successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    phone = input("Enter the phone number with country code (e.g. +5511999999999): ").strip()
    msg = input("Enter the message to send: ").strip()
    if phone and msg:
        send_whatsapp_message(phone, msg)
    else:
        print("Phone number and message cannot be empty.")

if __name__ == "__main__":
    main()

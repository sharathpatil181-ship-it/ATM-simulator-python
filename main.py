from database import get_connection
from user_account import UserAccount
from atm import ATM


def initialize_database() -> None:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS users (card_number VARCHAR(32) PRIMARY KEY, pin INT, balance DOUBLE)"
        )
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS transactions (id INT AUTO_INCREMENT PRIMARY KEY, card_number VARCHAR(32), description TEXT, date DATETIME)"
        )
        conn.commit()


def main() -> None:
    initialize_database()

    print("🏧 Welcome to the ATM Simulator")
    card_number = input("Enter your Card Number: ").strip()

    user = UserAccount.get_user(card_number)
    if user is None:
        print("❌ Card number not found.")
        return

    pin_text = input("Enter your 4-digit PIN: ").strip()
    if not pin_text.isdigit() or len(pin_text) != 4:
        print("❌ PIN must be a 4-digit number.")
        return

    pin = int(pin_text)
    if user.authenticate(card_number, pin):
        print("✅ Login successful!")
        atm = ATM(user)
        atm.start()
    else:
        print("❌ Incorrect PIN.")


if __name__ == "__main__":
    main()

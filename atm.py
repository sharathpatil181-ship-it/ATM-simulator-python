from user_account import UserAccount


class ATM:
    def __init__(self, user: UserAccount):
        self.user = user

    def start(self) -> None:
        while True:
            print("\n========= ATM Menu =========")
            print("1. 💰 Check Balance")
            print("2. ➕ Deposit")
            print("3. ➖ Withdraw")
            print("4. 📄 Transaction History")
            print("5. 🔒 Change PIN")
            print("6. 🚪 Exit")
            choice = input("Enter your choice (1-6): ").strip()

            if not choice.isdigit():
                print("❌ Invalid choice. Please try again.")
                continue

            choice = int(choice)

            if choice == 1:
                print(f"💳 Your Current Balance: ₹{self.user.get_balance():.2f}")
            elif choice == 2:
                amount = input("Enter amount to deposit: ₹").strip()
                try:
                    deposit_amt = float(amount)
                    self.user.deposit(deposit_amt)
                except ValueError:
                    print("❌ Invalid amount. Please enter a number.")
            elif choice == 3:
                amount = input("Enter amount to withdraw: ₹").strip()
                try:
                    withdraw_amt = float(amount)
                    self.user.withdraw(withdraw_amt)
                except ValueError:
                    print("❌ Invalid amount. Please enter a number.")
            elif choice == 4:
                self.user.show_transactions()
            elif choice == 5:
                new_pin = input("Enter new 4-digit PIN: ").strip()
                if not new_pin.isdigit() or len(new_pin) != 4:
                    print("❌ PIN must be a 4-digit number.")
                else:
                    self.user.change_pin(int(new_pin))
            elif choice == 6:
                print("👋 Thank you for using the ATM. Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please try again.")

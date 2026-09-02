from __future__ import annotations
import mysql.connector
from datetime import datetime
from database import get_connection


class UserAccount:
    def __init__(self, card_number: str, pin: int, balance: float):
        self.card_number = card_number
        self.pin = pin
        self.balance = balance

    @classmethod
    def get_user(cls, card_number: str) -> "UserAccount | None":
        try:
            with get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT pin, balance FROM users WHERE card_number = %s",
                    (card_number,),
                )
                row = cursor.fetchone()
                if row is None:
                    return None
                pin, balance = row
                return cls(card_number, pin, balance)
        except mysql.connector.Error as exc:
            print(f"Error retrieving user: {exc}")
            return None

    def authenticate(self, input_card: str, input_pin: int) -> bool:
        return self.card_number == input_card and self.pin == input_pin

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            print("❌ Invalid deposit amount.")
            return
        self.balance += amount
        self._update_balance()
        self._add_transaction(f"Deposited ₹{amount:.2f}")
        print(f"✅ ₹{amount:.2f} deposited.")

    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            print("❌ Invalid withdrawal amount.")
            return
        if amount > self.balance:
            print("❌ Insufficient balance.")
            return
        self.balance -= amount
        self._update_balance()
        self._add_transaction(f"Withdrew ₹{amount:.2f}")
        print(f"✅ ₹{amount:.2f} withdrawn.")

    def _update_balance(self) -> None:
        try:
            with get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE users SET balance = %s WHERE card_number = %s",
                    (self.balance, self.card_number),
                )
                conn.commit()
        except mysql.connector.Error as exc:
            print(f"Error updating balance: {exc}")

    def _add_transaction(self, description: str) -> None:
        try:
            with get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO transactions (card_number, description, date) VALUES (%s, %s, %s)",
                    (self.card_number, description, datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                )
                conn.commit()
        except mysql.connector.Error as exc:
            print(f"Error recording transaction: {exc}")

    def show_transactions(self) -> None:
        try:
            with get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT date, description FROM transactions WHERE card_number = %s ORDER BY date DESC",
                    (self.card_number,),
                )
                rows = cursor.fetchall()
                print("\n📜 Transaction History:")
                if not rows:
                    print("No transactions found.")
                    return
                for row in rows:
                    date, description = row
                    print(f"{date}: {description}")
        except mysql.connector.Error as exc:
            print(f"Error fetching transactions: {exc}")

    def change_pin(self, new_pin: int) -> None:
        if new_pin < 0 or new_pin > 9999:
            print("❌ PIN must be a 4-digit number.")
            return
        self.pin = new_pin
        try:
            with get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE users SET pin = %s WHERE card_number = %s",
                    (self.pin, self.card_number),
                )
                conn.commit()
                print("✅ PIN updated successfully.")
        except mysql.connector.Error as exc:
            print(f"Error updating PIN: {exc}")

    def get_balance(self) -> float:
        return self.balance

    def get_card_number(self) -> str:
        return self.card_number




#!/usr/bin/env python3
"""
Account manager for TikTok bot accounts.
"""

import json
import os
import random
from datetime import datetime, timedelta

class AccountManager:
    def __init__(self, accounts_dir='accounts'):
        self.accounts_dir = accounts_dir
        if not os.path.exists(accounts_dir):
            os.makedirs(accounts_dir)

    def load_account(self, filename):
        """Load an account from file."""
        filepath = os.path.join(self.accounts_dir, filename)
        with open(filepath, 'r') as f:
            return json.load(f)

    def save_account(self, account_data, filename=None):
        """Save account data to file."""
        if filename is None:
            filename = f"{account_data.get('username', 'new_account')}.json"
        filepath = os.path.join(self.accounts_dir, filename)
        with open(filepath, 'w') as f:
            json.dump(account_data, f, indent=4)

    def get_available_accounts(self):
        """Get list of available accounts."""
        accounts = []
        for filename in os.listdir(self.accounts_dir):
            if filename.endswith('.json'):
                try:
                    account = self.load_account(filename)
                    # Check if account is ready to be used (based on last_used timestamp)
                    last_used = datetime.fromisoformat(account.get('last_used', '2000-01-01').replace('Z', ''))
                    if datetime.now() - last_used > timedelta(hours=1):
                        accounts.append(account)
                except Exception as e:
                    print(f"[WARNING] Could not load account {filename}: {e}")
        return accounts

    def get_random_account(self):
        """Get a random available account."""
        accounts = self.get_available_accounts()
        if not accounts:
            raise Exception("No available accounts")
        return random.choice(accounts)

    def mark_used(self, account_data):
        """Mark an account as recently used."""
        account_data['last_used'] = datetime.now().isoformat() + 'Z'
        self.save_account(account_data)

if __name__ == "__main__":
    manager = AccountManager()

    # Example usage
    try:
        account = manager.get_random_account()
        print(f"Selected account: {account['username']}")
        manager.mark_used(account)
        print("Account marked as used")

    except Exception as e:
        print(f"Error: {e}")


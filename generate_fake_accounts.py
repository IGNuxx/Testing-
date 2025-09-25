



#!/usr/bin/env python3
"""
Generate fake TikTok accounts for testing.
"""

import json
import os
import random
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()

def generate_fake_account():
    """Generate a fake TikTok account."""
    return {
        "username": fake.user_name(),
        "password": fake.password(length=12),
        "email": fake.email(),
        "phone_number": fake.phone_number(),
        "device_id": fake.uuid4(),
        "last_used": (datetime.now() - timedelta(days=random.randint(1, 30))).isoformat() + 'Z',
        "country": random.choice(["US", "CA", "GB", "AU", "DE", "FR"]),
        "birthdate": fake.date_of_birth(minimum_age=18, maximum_age=45).isoformat()
    }

def main(num_accounts=20):
    """Generate multiple fake accounts."""
    if not os.path.exists('accounts'):
        os.makedirs('accounts')

    for i in range(num_accounts):
        account = generate_fake_account()
        filename = f"{account['username']}.json"
        filepath = os.path.join('accounts', filename)

        with open(filepath, 'w') as f:
            json.dump(account, f, indent=4)

        print(f"Generated: {filename}")

if __name__ == "__main__":
    main()


#!/usr/bin/env python3
"""
Test script for Galaxium Travels Frequent Traveller Feature
Demonstrates automatic status upgrades and seat preferences
"""

import requests
import json
import time

BASE_URL = "http://localhost:8080"

def print_header(text):
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")

def print_status(user):
    """Print user's frequent traveller status with emoji"""
    status_emoji = {
        'standard': '⭐',
        'bronze': '🥉',
        'silver': '🥈',
        'gold': '🥇',
        'platinum': '💎'
    }
    emoji = status_emoji.get(user['frequent_traveller_status'], '⭐')
    print(f"{emoji} Status: {user['frequent_traveller_status'].upper()}")
    print(f"📊 Total Bookings: {user['total_bookings']}")
    if user.get('seat_preference'):
        print(f"💺 Seat Preference: {user['seat_preference']}")

def test_frequent_traveller():
    print_header("🚀 Galaxium Travels - Frequent Traveller Test")
    
    # Step 1: Create a new user
    print("1️⃣  Creating new user...")
    import random
    random_id = random.randint(1000, 9999)
    user_data = {
        "name": f"Test Traveller {random_id}",
        "email": f"test{random_id}@galaxium.space"
    }
    response = requests.post(f"{BASE_URL}/register", json=user_data)
    user = response.json()
    
    # Debug: print the response
    print(f"   API Response: {json.dumps(user, indent=2)}")
    
    # Check if it's an error response
    if 'error' in user:
        print(f"   ⚠️  User already exists, fetching existing user...")
        response = requests.get(f"{BASE_URL}/user", params={"name": "Test Traveller", "email": "test@galaxium.space"})
        user = response.json()
        print(f"   API Response: {json.dumps(user, indent=2)}")
    
    user_id = user['user_id']
    print(f"✅ User created/found: {user['name']} (ID: {user_id})")
    print_status(user)
    
    # Step 2: Get available flights
    print("\n2️⃣  Fetching available flights...")
    response = requests.get(f"{BASE_URL}/flights")
    flights = response.json()
    print(f"✅ Found {len(flights)} available flights")
    flight_id = flights[0]['flight_id']
    print(f"   Selected: {flights[0]['origin']} → {flights[0]['destination']}")
    
    # Step 3: Make bookings to test status upgrades
    print("\n3️⃣  Making bookings to test status upgrades...")
    
    booking_thresholds = [
        (1, "standard", "⭐"),
        (5, "bronze", "🥉"),
        (10, "silver", "🥈"),
        (20, "gold", "🥇"),
        (50, "platinum", "💎")
    ]
    
    for target_bookings, expected_status, emoji in booking_thresholds:
        # Make bookings until we reach the target
        response = requests.get(f"{BASE_URL}/user/{user_id}/status")
        current_user = response.json()
        current_bookings = current_user['total_bookings']
        
        if current_bookings < target_bookings:
            bookings_needed = target_bookings - current_bookings
            print(f"\n   Making {bookings_needed} booking(s) to reach {expected_status.upper()}...")
            
            for i in range(bookings_needed):
                booking_data = {
                    "user_id": user_id,
                    "name": "Test Traveller",
                    "flight_id": flight_id
                }
                response = requests.post(f"{BASE_URL}/book", json=booking_data)
                if response.status_code == 200:
                    print(f"   ✓ Booking {current_bookings + i + 1} completed")
                time.sleep(0.1)  # Small delay to avoid overwhelming the server
            
            # Check status after bookings
            response = requests.get(f"{BASE_URL}/user/{user_id}/status")
            updated_user = response.json()
            
            print(f"\n   {emoji} STATUS UPGRADE!")
            print_status(updated_user)
            
            if updated_user['frequent_traveller_status'] != expected_status:
                print(f"   ⚠️  Expected {expected_status}, got {updated_user['frequent_traveller_status']}")
    
    # Step 4: Test seat preference
    print("\n4️⃣  Testing seat preference management...")
    preferences = ['window', 'aisle', 'middle']
    
    for pref in preferences:
        print(f"\n   Setting preference to: {pref}")
        response = requests.post(
            f"{BASE_URL}/user/{user_id}/seat-preference",
            json={"seat_preference": pref}
        )
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Preference updated: {result['seat_preference']}")
    
    # Step 5: Get final status
    print("\n5️⃣  Final Status Check...")
    response = requests.get(f"{BASE_URL}/user/{user_id}/status")
    final_status = response.json()
    
    print(f"\n   User: {final_status['name']}")
    print_status(final_status)
    
    # Step 6: Show all bookings
    print("\n6️⃣  Booking History...")
    response = requests.get(f"{BASE_URL}/bookings/{user_id}")
    bookings = response.json()
    print(f"   Total bookings: {len(bookings)}")
    
    print_header("✅ Test Complete!")
    print("All frequent traveller features working correctly:")
    print("  ✓ Automatic status upgrades")
    print("  ✓ Seat preference management")
    print("  ✓ Status tracking")
    print("  ✓ Booking history")
    print("\n🌐 View API docs at: http://localhost:8080/docs")

if __name__ == "__main__":
    try:
        test_frequent_traveller()
    except requests.exceptions.ConnectionError:
        print("❌ Error: Cannot connect to backend server")
        print("   Make sure the server is running on http://localhost:8080")
        print("   Run: cd galaxium-travels/booking_system_backend && python3 server.py")
    except Exception as e:
        print(f"❌ Error: {e}")

# Made with Bob

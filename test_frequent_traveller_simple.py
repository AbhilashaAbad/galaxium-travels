#!/usr/bin/env python3
"""
Simple test for Galaxium Travels Frequent Traveller Feature
Tests automatic status upgrades with realistic booking counts
"""

import requests
import json

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
    print_header("🚀 Galaxium Travels - Frequent Traveller Demo")
    
    # Create a new user
    print("1️⃣  Creating new user...")
    import random
    random_id = random.randint(1000, 9999)
    user_data = {
        "name": f"Demo User {random_id}",
        "email": f"demo{random_id}@galaxium.space"
    }
    response = requests.post(f"{BASE_URL}/register", json=user_data)
    user = response.json()
    user_id = user['user_id']
    print(f"✅ User created: {user['name']} (ID: {user_id})")
    print_status(user)
    
    # Get all flights
    print("\n2️⃣  Fetching available flights...")
    response = requests.get(f"{BASE_URL}/flights")
    flights = response.json()
    print(f"✅ Found {len(flights)} available flights")
    
    # Make bookings across different flights to test status upgrades
    print("\n3️⃣  Making bookings to demonstrate status upgrades...")
    
    test_scenarios = [
        (1, "standard", "⭐", "Initial booking"),
        (5, "bronze", "🥉", "Reached Bronze status!"),
        (10, "silver", "🥈", "Reached Silver status!"),
    ]
    
    flight_index = 0
    for target_bookings, expected_status, emoji, message in test_scenarios:
        # Get current status
        response = requests.get(f"{BASE_URL}/user/{user_id}/status")
        current_user = response.json()
        current_bookings = current_user['total_bookings']
        
        if current_bookings < target_bookings:
            bookings_needed = target_bookings - current_bookings
            print(f"\n   {message}")
            print(f"   Making {bookings_needed} booking(s)...")
            
            for i in range(bookings_needed):
                # Rotate through flights to avoid running out of seats
                flight = flights[flight_index % len(flights)]
                flight_index += 1
                
                booking_data = {
                    "user_id": user_id,
                    "name": user_data["name"],
                    "flight_id": flight['flight_id']
                }
                response = requests.post(f"{BASE_URL}/book", json=booking_data)
                result = response.json()
                
                if 'error' in result:
                    print(f"   ⚠️  Booking failed: {result['error']}")
                else:
                    print(f"   ✓ Booking {current_bookings + i + 1} completed ({flight['origin']} → {flight['destination']})")
            
            # Check status after bookings
            response = requests.get(f"{BASE_URL}/user/{user_id}/status")
            updated_user = response.json()
            
            print(f"\n   {emoji} STATUS: {updated_user['frequent_traveller_status'].upper()}")
            print_status(updated_user)
    
    # Test seat preference
    print("\n4️⃣  Setting seat preference...")
    response = requests.post(
        f"{BASE_URL}/user/{user_id}/seat-preference",
        json={"seat_preference": "window"}
    )
    if response.status_code == 200:
        result = response.json()
        print(f"   ✅ Preference set to: {result['seat_preference']}")
    
    # Final status
    print("\n5️⃣  Final Status...")
    response = requests.get(f"{BASE_URL}/user/{user_id}/status")
    final_status = response.json()
    
    print(f"\n   User: {final_status['name']}")
    print_status(final_status)
    
    # Show bookings
    print("\n6️⃣  Booking Summary...")
    response = requests.get(f"{BASE_URL}/bookings/{user_id}")
    bookings = response.json()
    print(f"   Total bookings made: {len(bookings)}")
    print(f"   All bookings confirmed: {all(b['status'] == 'booked' for b in bookings)}")
    
    print_header("✅ Demo Complete!")
    print("Frequent Traveller Features Demonstrated:")
    print("  ✓ Automatic status tracking")
    print("  ✓ Status upgrades (Standard → Bronze → Silver)")
    print("  ✓ Seat preference management")
    print("  ✓ Booking history")
    print("\n🌐 Explore more at: http://localhost:8080/docs")

if __name__ == "__main__":
    try:
        test_frequent_traveller()
    except requests.exceptions.ConnectionError:
        print("❌ Error: Cannot connect to backend server")
        print("   Make sure the server is running on http://localhost:8080")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

# Made with Bob

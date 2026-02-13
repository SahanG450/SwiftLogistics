"""
Simple MongoDB Connection Test for SwiftLogistics
This script shows exactly how Python connects to MongoDB through the API
"""

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime

# MongoDB connection details (from docker-compose.yml)
MONGODB_URI = "mongodb://admin:admin123@localhost:27017/swiftlogistics?authSource=admin"

async def test_mongodb_connection():
    """Test MongoDB connection and basic operations"""
    
    print("🔌 Step 1: Connecting to MongoDB...")
    print(f"   URI: {MONGODB_URI}")
    
    # Create MongoDB client
    client = AsyncIOMotorClient(MONGODB_URI)
    
    # Test connection
    try:
        await client.admin.command('ping')
        print("   ✅ Connected successfully!")
    except Exception as e:
        print(f"   ❌ Connection failed: {e}")
        return
    
    print("\n📊 Step 2: Getting database...")
    db = client['swiftlogistics']
    print(f"   Database: {db.name}")
    
    print("\n📝 Step 3: Creating a test order...")
    order = {
        "order_id": "TEST-ORDER-001",
        "client_id": "CLIENT-001",
        "pickup_location": "123 Main St, New York",
        "delivery_location": "456 Oak Ave, Boston",
        "package_details": "Test Package - Laptop",
        "status": "pending",
        "created_at": datetime.utcnow()
    }
    
    result = await db.orders.insert_one(order)
    print(f"   ✅ Order inserted with ID: {result.inserted_id}")
    
    print("\n🔍 Step 4: Retrieving the order...")
    found_order = await db.orders.find_one({"order_id": "TEST-ORDER-001"})
    if found_order:
        print(f"   ✅ Order found:")
        print(f"      Order ID: {found_order['order_id']}")
        print(f"      Client: {found_order['client_id']}")
        print(f"      From: {found_order['pickup_location']}")
        print(f"      To: {found_order['delivery_location']}")
        print(f"      Status: {found_order['status']}")
    
    print("\n📋 Step 5: Getting all orders...")
    cursor = db.orders.find({})
    orders = await cursor.to_list(length=100)
    print(f"   Total orders in database: {len(orders)}")
    
    print("\n🔄 Step 6: Updating order status...")
    update_result = await db.orders.update_one(
        {"order_id": "TEST-ORDER-001"},
        {"$set": {"status": "in-transit"}}
    )
    print(f"   ✅ Updated {update_result.modified_count} order(s)")
    
    print("\n🗑️  Step 7: Deleting test order...")
    delete_result = await db.orders.delete_one({"order_id": "TEST-ORDER-001"})
    print(f"   ✅ Deleted {delete_result.deleted_count} order(s)")
    
    print("\n✅ Test completed successfully!")
    print("\n" + "="*60)
    print("This is exactly how the API endpoints work:")
    print("1. Client sends HTTP request to API (port 3000)")
    print("2. API connects to MongoDB (port 27017)")
    print("3. API performs database operation (insert/find/update/delete)")
    print("4. API returns response to client")
    print("="*60)
    
    client.close()

if __name__ == "__main__":
    asyncio.run(test_mongodb_connection())

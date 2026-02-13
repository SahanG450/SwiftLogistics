"""
MongoDB Connection Test Script

This script tests the MongoDB connection and verifies that all repositories work correctly.
Run this to ensure your MongoDB setup is working.

Usage:
    python test_mongodb.py
"""
import asyncio
import os
import sys
from datetime import datetime

# Add shared directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from database import MongoDBClient, get_database, close_database_connection
from database.repositories import (
    OrderRepository,
    DriverRepository,
    ClientRepository,
    ShipmentRepository,
    ContractRepository,
    InvoiceRepository
)


async def test_connection():
    """Test basic MongoDB connection"""
    print("=" * 60)
    print("TESTING MONGODB CONNECTION")
    print("=" * 60)
    
    try:
        # Connect to MongoDB
        print("\n1. Connecting to MongoDB...")
        db = await get_database()
        print("   ✓ Connected successfully!")
        
        # Test ping
        print("\n2. Testing database ping...")
        result = await db.client.admin.command('ping')
        print(f"   ✓ Ping successful: {result}")
        
        # List collections
        print("\n3. Listing collections...")
        collections = await db.list_collection_names()
        print(f"   ✓ Found {len(collections)} collections: {collections}")
        
        return True
        
    except Exception as e:
        print(f"   ✗ Connection failed: {e}")
        return False


async def test_repositories():
    """Test all repository operations"""
    print("\n" + "=" * 60)
    print("TESTING REPOSITORIES")
    print("=" * 60)
    
    try:
        db = await get_database()
        
        # Test OrderRepository
        print("\n4. Testing OrderRepository...")
        order_repo = OrderRepository(db)
        
        # Create test order
        test_order = {
            "order_id": f"TEST-ORD-{int(datetime.utcnow().timestamp())}",
            "client_id": "TEST-CLIENT-001",
            "status": "pending",
            "pickup_address": "123 Test St",
            "delivery_address": "456 Test Ave",
            "items": [{"name": "Test Item", "weight": 10}],
            "total_amount": 100.00
        }
        
        order_id = await order_repo.create(test_order)
        print(f"   ✓ Created order: {order_id}")
        
        # Find order
        found_order = await order_repo.find_by_order_id(test_order["order_id"])
        print(f"   ✓ Found order: {found_order['order_id']}")
        
        # Update order
        updated = await order_repo.update_status(test_order["order_id"], "processing")
        print(f"   ✓ Updated order status: {updated}")
        
        # Count orders
        count = await order_repo.count()
        print(f"   ✓ Total orders in database: {count}")
        
        # Delete test order
        deleted = await order_repo.delete_one({"order_id": test_order["order_id"]})
        print(f"   ✓ Deleted test order: {deleted}")
        
        # Test DriverRepository
        print("\n5. Testing DriverRepository...")
        driver_repo = DriverRepository(db)
        
        test_driver = {
            "driver_id": f"TEST-DRV-{int(datetime.utcnow().timestamp())}",
            "name": "Test Driver",
            "email": f"test{int(datetime.utcnow().timestamp())}@example.com",
            "phone": "+1234567890",
            "license_number": "TEST-123",
            "vehicle_type": "Van",
            "status": "available"
        }
        
        driver_id = await driver_repo.create(test_driver)
        print(f"   ✓ Created driver: {driver_id}")
        
        # Find driver
        found_driver = await driver_repo.find_by_driver_id(test_driver["driver_id"])
        print(f"   ✓ Found driver: {found_driver['driver_id']}")
        
        # Update status
        updated = await driver_repo.update_status(test_driver["driver_id"], "busy")
        print(f"   ✓ Updated driver status: {updated}")
        
        # Clean up
        deleted = await driver_repo.delete_one({"driver_id": test_driver["driver_id"]})
        print(f"   ✓ Deleted test driver: {deleted}")
        
        # Test ClientRepository
        print("\n6. Testing ClientRepository...")
        client_repo = ClientRepository(db)
        count = await client_repo.count()
        print(f"   ✓ ClientRepository working - {count} clients")
        
        # Test ShipmentRepository
        print("\n7. Testing ShipmentRepository...")
        shipment_repo = ShipmentRepository(db)
        count = await shipment_repo.count()
        print(f"   ✓ ShipmentRepository working - {count} shipments")
        
        # Test ContractRepository
        print("\n8. Testing ContractRepository...")
        contract_repo = ContractRepository(db)
        count = await contract_repo.count()
        print(f"   ✓ ContractRepository working - {count} contracts")
        
        # Test InvoiceRepository
        print("\n9. Testing InvoiceRepository...")
        invoice_repo = InvoiceRepository(db)
        count = await invoice_repo.count()
        print(f"   ✓ InvoiceRepository working - {count} invoices")
        
        return True
        
    except Exception as e:
        print(f"   ✗ Repository test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_indexes():
    """Test that indexes are created"""
    print("\n" + "=" * 60)
    print("TESTING INDEXES")
    print("=" * 60)
    
    try:
        db = await get_database()
        
        print("\n10. Checking indexes...")
        
        # Check orders collection indexes
        orders_indexes = await db.orders.list_indexes().to_list(length=None)
        print(f"   ✓ Orders collection has {len(orders_indexes)} indexes")
        for idx in orders_indexes:
            print(f"      - {idx['name']}")
        
        # Check drivers collection indexes
        drivers_indexes = await db.drivers.list_indexes().to_list(length=None)
        print(f"   ✓ Drivers collection has {len(drivers_indexes)} indexes")
        for idx in drivers_indexes:
            print(f"      - {idx['name']}")
        
        return True
        
    except Exception as e:
        print(f"   ✗ Index test failed: {e}")
        return False


async def test_aggregation():
    """Test aggregation queries"""
    print("\n" + "=" * 60)
    print("TESTING AGGREGATION")
    print("=" * 60)
    
    try:
        db = await get_database()
        order_repo = OrderRepository(db)
        
        print("\n11. Testing aggregation pipeline...")
        
        # Create some test data
        test_orders = [
            {
                "order_id": f"TEST-AGG-{i}",
                "client_id": f"CLIENT-{i % 3}",
                "status": ["pending", "processing", "completed"][i % 3],
                "pickup_address": "123 Test St",
                "delivery_address": "456 Test Ave",
                "items": [],
                "total_amount": 100.00 * (i + 1)
            }
            for i in range(5)
        ]
        
        for order in test_orders:
            await order_repo.create(order)
        
        print("   ✓ Created test orders")
        
        # Aggregation: Count by status
        pipeline = [
            {
                "$match": {"order_id": {"$regex": "^TEST-AGG-"}}
            },
            {
                "$group": {
                    "_id": "$status",
                    "count": {"$sum": 1},
                    "total_amount": {"$sum": "$total_amount"}
                }
            }
        ]
        
        results = await order_repo.aggregate(pipeline)
        print(f"   ✓ Aggregation completed:")
        for result in results:
            print(f"      - {result['_id']}: {result['count']} orders, ${result['total_amount']:.2f}")
        
        # Clean up test data
        await order_repo.delete_many({"order_id": {"$regex": "^TEST-AGG-"}})
        print("   ✓ Cleaned up test data")
        
        return True
        
    except Exception as e:
        print(f"   ✗ Aggregation test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("MONGODB INTEGRATION TEST SUITE")
    print("=" * 60)
    print(f"Time: {datetime.utcnow().isoformat()}")
    print("=" * 60)
    
    results = {
        "connection": False,
        "repositories": False,
        "indexes": False,
        "aggregation": False
    }
    
    try:
        # Run tests
        results["connection"] = await test_connection()
        
        if results["connection"]:
            results["repositories"] = await test_repositories()
            results["indexes"] = await test_indexes()
            results["aggregation"] = await test_aggregation()
        
    except Exception as e:
        print(f"\n✗ Test suite failed: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Close connection
        await close_database_connection()
        print("\n" + "=" * 60)
        print("CLOSING CONNECTION")
        print("=" * 60)
        print("   ✓ MongoDB connection closed")
    
    # Print summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    total_tests = len(results)
    passed_tests = sum(1 for v in results.values() if v)
    
    for test_name, passed in results.items():
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"   {test_name.upper()}: {status}")
    
    print("\n" + "=" * 60)
    print(f"TOTAL: {passed_tests}/{total_tests} tests passed")
    print("=" * 60)
    
    # Exit with appropriate code
    exit_code = 0 if all(results.values()) else 1
    print(f"\nExiting with code: {exit_code}")
    
    return exit_code


if __name__ == "__main__":
    # Set MongoDB URI from environment or use default
    if "MONGODB_URI" not in os.environ:
        print("\nNote: Using default MongoDB URI (localhost)")
        print("Set MONGODB_URI environment variable to use a different connection\n")
        os.environ["MONGODB_URI"] = "mongodb://admin:admin123@localhost:27017/swiftlogistics?authSource=admin"
    
    # Run tests
    exit_code = asyncio.run(main())
    sys.exit(exit_code)

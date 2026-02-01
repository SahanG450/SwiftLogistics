# File-Based Storage for Python Mock Services

## Overview

All Python mock services now use **file-based storage** instead of in-memory storage. Data is persisted to JSON files in the `data/` directory, allowing data to survive service restarts.

## File Structure

```
services/mocks/
├── cms-mock/
│   ├── data/
│   │   ├── .gitkeep
│   │   └── customers.json    # Auto-generated, git-ignored
│   └── src/
│       └── utils/
│           └── file_storage.py
├── ros-mock/
│   ├── data/
│   │   ├── .gitkeep
│   │   └── routes.json        # Auto-generated, git-ignored
│   └── src/
│       └── utils/
│           └── file_storage.py
└── wms-mock/
    ├── data/
    │   ├── .gitkeep
    │   └── inventory.json     # Auto-generated, git-ignored
    └── src/
        └── utils/
            └── file_storage.py
```

## How It Works

### FileStorage Class

Each service uses a `FileStorage` utility class that provides:

- **Thread-safe operations** using locks
- **Automatic file creation** on first write
- **JSON serialization** for human-readable data
- **CRUD operations**: Create, Read, Update, Delete

### Data Persistence

1. **First Run**: If no data file exists, mock data is automatically initialized
2. **Subsequent Runs**: Data is loaded from existing JSON files
3. **All Operations**: Create, update, and delete operations immediately write to disk
4. **Data Survives**: Service restarts, container restarts, redeployments

### Storage Methods

```python
# Get all records
storage.get_all()  # Returns: Dict[str, Any]

# Get single record
storage.get(key)  # Returns: Optional[Any]

# Create new record
storage.create(key, value)  # Returns: Any

# Update existing record
storage.update(key, value)  # Returns: Optional[Any]

# Delete record
storage.delete(key)  # Returns: bool

# Check if exists
storage.exists(key)  # Returns: bool

# Clear all data
storage.clear()  # Returns: None
```

## Data Files

### CMS - customers.json

```json
{
  "uuid-1": {
    "id": "uuid-1",
    "name": "John Doe",
    "email": "john.doe@example.com",
    "phone": "+1-555-0101",
    "address": "123 Main St, New York, NY 10001",
    "company": "Tech Corp",
    "status": "active",
    "created_at": "2026-02-01T10:30:00",
    "updated_at": "2026-02-01T10:30:00"
  }
}
```

### ROS - routes.json

```json
{
  "uuid-1": {
    "id": "uuid-1",
    "origin": "New York, NY",
    "destination": "Boston, MA",
    "vehicle_id": "VEH-001",
    "driver_id": "DRV-001",
    "stops": [...],
    "status": "in_progress",
    "distance": 215.5,
    "estimated_duration": 240,
    "actual_duration": null,
    "created_at": "2026-02-01T10:30:00",
    "updated_at": "2026-02-01T10:30:00"
  }
}
```

### WMS - inventory.json

```json
{
  "uuid-1": {
    "id": "uuid-1",
    "sku": "PROD-001",
    "name": "Laptop Computer",
    "quantity": 50,
    "location": {
      "warehouse_id": "WH-001",
      "zone": "A",
      "aisle": "12",
      "rack": "3",
      "bin": "B"
    },
    "status": "available",
    "unit_price": 999.99,
    "reorder_level": 10,
    "created_at": "2026-02-01T10:30:00",
    "updated_at": "2026-02-01T10:30:00"
  }
}
```

## Benefits

✅ **Data Persistence**: Data survives service restarts  
✅ **No Database Required**: Simple file-based storage  
✅ **Human Readable**: JSON format for easy inspection  
✅ **Thread Safe**: Concurrent request handling  
✅ **Git Friendly**: Data files are git-ignored  
✅ **Easy Backup**: Just copy the JSON files  
✅ **Easy Reset**: Delete JSON files to reset to mock data

## Operations

### View Current Data

```bash
# CMS customers
cat services/mocks/cms-mock/data/customers.json | jq

# ROS routes
cat services/mocks/ros-mock/data/routes.json | jq

# WMS inventory
cat services/mocks/wms-mock/data/inventory.json | jq
```

### Reset to Mock Data

```bash
# Delete data files - they'll be recreated with mock data on next startup
rm services/mocks/cms-mock/data/customers.json
rm services/mocks/ros-mock/data/routes.json
rm services/mocks/wms-mock/data/inventory.json
```

### Backup Data

```bash
# Backup all data
tar -czf mock-data-backup-$(date +%Y%m%d).tar.gz services/mocks/*/data/*.json

# Restore data
tar -xzf mock-data-backup-YYYYMMDD.tar.gz
```

### Export/Import Data

```bash
# Export single service
cp services/mocks/cms-mock/data/customers.json ~/backup/

# Import data
cp ~/backup/customers.json services/mocks/cms-mock/data/
```

## Docker Volumes

For persistent storage in Docker, mount the data directory as a volume:

```yaml
services:
  cms-mock:
    volumes:
      - ./services/mocks/cms-mock/data:/app/data
  ros-mock:
    volumes:
      - ./services/mocks/ros-mock/data:/app/data
  wms-mock:
    volumes:
      - ./services/mocks/wms-mock/data:/app/data
```

## Thread Safety

The `FileStorage` class uses Python's `threading.Lock()` to ensure:

- **Concurrent reads** are safe
- **Write operations** are atomic
- **No race conditions** between requests
- **Data consistency** is maintained

## Error Handling

The storage system handles:

- **File not found**: Creates new file with empty data
- **JSON decode errors**: Returns empty dict and logs error
- **Write failures**: Logs error but doesn't crash service
- **Permission issues**: Logs error with clear message

## Performance Considerations

- **Small datasets**: Excellent performance (< 10,000 records)
- **Read operations**: Entire file is loaded into memory
- **Write operations**: Entire file is rewritten
- **File locking**: Brief locks ensure consistency
- **Not recommended**: For large-scale production use

## Migration Notes

### Changes from In-Memory Storage

**Before (In-Memory)**:

```python
self.customers: Dict[str, dict] = {}
```

**After (File-Based)**:

```python
self.storage = FileStorage(data_dir, 'customers')
```

### API Compatibility

✅ **No API changes required**  
✅ **Same endpoints and responses**  
✅ **Backward compatible**  
✅ **Drop-in replacement**

## Troubleshooting

### Data Not Persisting

1. Check file permissions on `data/` directory
2. Ensure directory exists: `mkdir -p services/mocks/*/data`
3. Check logs for write errors

### Data File Corrupted

1. Stop the service
2. Delete the JSON file
3. Restart service (will recreate with mock data)

### Need to Clear Data

```bash
# Clear all mock service data
rm services/mocks/cms-mock/data/*.json
rm services/mocks/ros-mock/data/*.json
rm services/mocks/wms-mock/data/*.json
```

## Summary

All three Python mock services now use file-based JSON storage:

- **CMS Mock**: `data/customers.json`
- **ROS Mock**: `data/routes.json`
- **WMS Mock**: `data/inventory.json`

Data persists across restarts, is human-readable, and requires no database setup!

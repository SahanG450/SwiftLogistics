"""File-based storage utility for mock services"""

import json
import os
from typing import Dict, List, Optional, Any
from pathlib import Path
import threading


class FileStorage:
    """Simple file-based storage using JSON files"""

    def __init__(self, data_dir: str, filename: str):
        """
        Initialize file storage

        Args:
            data_dir: Directory to store data files
            filename: Name of the JSON file (without extension)
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.filepath = self.data_dir / f"{filename}.json"
        self.lock = threading.Lock()

    def _read_file(self) -> Dict[str, Any]:
        """Read data from file"""
        try:
            if self.filepath.exists():
                with open(self.filepath, "r", encoding="utf-8") as f:
                    return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error reading file {self.filepath}: {e}")
        return {}

    def _write_file(self, data: Dict[str, Any]) -> None:
        """Write data to file"""
        try:
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except IOError as e:
            print(f"Error writing file {self.filepath}: {e}")

    def get_all(self) -> Dict[str, Any]:
        """Get all records"""
        with self.lock:
            return self._read_file()

    def get(self, key: str) -> Optional[Any]:
        """Get a single record by key"""
        with self.lock:
            data = self._read_file()
            return data.get(key)

    def create(self, key: str, value: Any) -> Any:
        """Create a new record"""
        with self.lock:
            data = self._read_file()
            data[key] = value
            self._write_file(data)
            return value

    def update(self, key: str, value: Any) -> Optional[Any]:
        """Update an existing record"""
        with self.lock:
            data = self._read_file()
            if key in data:
                data[key] = value
                self._write_file(data)
                return value
            return None

    def delete(self, key: str) -> bool:
        """Delete a record"""
        with self.lock:
            data = self._read_file()
            if key in data:
                del data[key]
                self._write_file(data)
                return True
            return False

    def exists(self, key: str) -> bool:
        """Check if a record exists"""
        with self.lock:
            data = self._read_file()
            return key in data

    def clear(self) -> None:
        """Clear all data"""
        with self.lock:
            self._write_file({})

    def initialize_with_data(self, initial_data: Dict[str, Any]) -> None:
        """Initialize file with data if it doesn't exist or is empty"""
        with self.lock:
            if not self.filepath.exists() or not self._read_file():
                self._write_file(initial_data)

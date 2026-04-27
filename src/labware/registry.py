#!/usr/bin/env python3
"""
====================================================================
Package: labware
====================================================================
Author:			Ragdata
Date:			19/04/2026
License:		MIT License
Repository:		https://github.com/Ragdata/.labware
Copyright:		Copyright © 2026 Redeyed Technologies
====================================================================
"""
from pathlib import Path
from typing import Any, Optional, Iterator, Dict
from sqlitedict import SqliteDict

from .logger import logger
from .config import config


#-------------------------------------------------------------------
# Module Variables
#-------------------------------------------------------------------
dbDir = Path.home() / config.get("dirs", "reg")
#-------------------------------------------------------------------
# Registry Class
#-------------------------------------------------------------------
class Registry:
	"""
	A persistent key/value and dictionary store using sqlitedict.

	Provides a live data storage mechanism for the labware package with
	automatic persistence to SQLite database. Supports all standard dictionary
	operations and context manager protocol.
	"""

	def __init__(self, db_name: str = "registry", db_dir: Path = dbDir, table: str = "default") -> None:
		"""
		Initialize a Registry instance.

		Args:
			db_name (str): Name of the database file (without extension). Defaults to "registry".
			db_dir (Optional[Path]): Directory to store the database. Defaults to ~/.labware/
			table (str): Name of the table/collection in the database. Defaults to "default".
		"""
		if not db_dir.exists():
			db_dir.mkdir(parents=True, exist_ok=True, mode=0o755)

		self.db_path = db_dir / f"{db_name}.db"
		self.table = table
		self._store: Optional[SqliteDict] = None

		logger.debug(f"Registry initialized: db_path={self.db_path}, table={table}")

	def __contains__(self, key: str) -> bool:
		"""Support membership testing: key in registry"""
		return self.exists(key)

	def __delitem__(self, key: str) -> None:
		"""Support dict-like deletion: del registry[key]"""
		self.delete(key)

	def __enter__(self):
		"""Context manager entry."""
		return self

	def __exit__(self, exc_type, exc_val, exc_tb):
		"""Context manager exit - commits and closes the registry."""
		self.commit()
		self.close()

	def __getitem__(self, key: str) -> Any:
		"""Support dict-like access: registry[key]"""
		return self.get(key)

	def __len__(self) -> int:
		"""Support len(): len(registry)"""
		return self.count()

	def __repr__(self) -> str:
		"""String representation of the registry."""
		try:
			return f"Registry(db_path={self.db_path}, table={self.table}, entries={self.count()})"
		except:
			return f"Registry(db_path={self.db_path}, table={self.table})"

	def __setitem__(self, key: str, value: Any) -> None:
		"""Support dict-like assignment: registry[key] = value"""
		self.set(key, value)

	def _get_store(self) -> SqliteDict:
		"""
		Lazily initialize and return the SqliteDict store.

		Returns:
			SqliteDict: The underlying storage dictionary.
		"""
		if self._store is None:
			try:
				self._store = SqliteDict(str(self.db_path), tablename=self.table)
				logger.debug(f"Opened registry database at {self.db_path}")
			except Exception as e:
				logger.error(f"Failed to initialize registry: {e}")
				raise
		# noinspection PyTypeChecker
		return self._store

	def commit(self) -> None:
		"""Commit pending changes to disk."""
		try:
			store = self._get_store()
			store.commit()
			logger.debug("Registry committed to disk")
		except Exception as e:
			logger.error(f"Failed to commit registry: {e}")
			raise

	def count(self) -> int:
		"""
		Get the number of entries in the registry.

		Returns:
			int: Number of key-value pairs stored.
		"""
		try:
			store = self._get_store()
			return len(store)
		except Exception as e:
			logger.error(f"Failed to count registry entries: {e}")
			raise

	def clear(self) -> None:
		"""Clear all entries from the registry."""
		try:
			store = self._get_store()
			store.clear()
			store.commit()
			logger.info(f"Registry cleared: {self.table}")
		except Exception as e:
			logger.error(f"Failed to clear registry: {e}")
			raise

	def close(self) -> None:
		"""Close the registry and release resources."""
		try:
			if self._store is not None:
				self._store.close()
				self._store = None
				logger.debug("Registry closed")
		except Exception as e:
			logger.error(f"Failed to close registry: {e}")
			raise

	def delete(self, key: str) -> None:
		"""
		Delete a key from the registry.

		Args:
			key (str): The key to delete.
		"""
		try:
			store = self._get_store()
			if key in store:
				del store[key]
				store.commit()
				logger.debug(f"Registry deleted: {key}")
			else:
				logger.warning(f"Registry key not found: {key}")
		except Exception as e:
			logger.error(f"Failed to delete registry key '{key}': {e}")
			raise

	def exists(self, key: str) -> bool:
		"""
		Check if a key exists in the registry.

		Args:
			key (str): The key to check.

		Returns:
			bool: True if key exists, False otherwise.
		"""
		try:
			store = self._get_store()
			return key in store
		except Exception as e:
			logger.error(f"Failed to check registry key '{key}': {e}")
			raise

	def get(self, key: str, default: Any = None) -> Any:
		"""
		Get a value from the registry.

		Args:
			key (str): The key to retrieve.
			default (Any): Default value if key not found. Defaults to None.

		Returns:
			Any: The stored value or default.
		"""
		try:
			store = self._get_store()
			return store.get(key, default)
		except Exception as e:
			logger.error(f"Failed to get registry key '{key}': {e}")
			raise

	def items(self) -> Iterator[tuple[str, Any]]:
		"""
		Get all key-value pairs in the registry.

		Returns:
			Iterator[tuple[str, Any]]: Iterator of (key, value) pairs.
		"""
		try:
			store = self._get_store()
			return iter(store.items())
		except Exception as e:
			logger.error(f"Failed to retrieve registry items: {e}")
			raise

	def keys(self) -> Iterator[str]:
		"""
		Get all keys in the registry.

		Returns:
			Iterator[str]: Iterator of registry keys.
		"""
		try:
			store = self._get_store()
			return iter(store.keys())
		except Exception as e:
			logger.error(f"Failed to retrieve registry keys: {e}")
			raise

	def set(self, key: str, value: Any) -> None:
		"""
		Set a key-value pair in the registry.

		Args:
			key (str): The key to set.
			value (Any): The value to store (must be JSON-serializable).
		"""
		try:
			store = self._get_store()
			store[key] = value
			store.commit()
			logger.debug(f"Registry set: {key}")
		except Exception as e:
			logger.error(f"Failed to set registry key '{key}': {e}")
			raise

	def to_dict(self) -> Dict[str, Any]:
		"""
		Convert registry to a standard dictionary.

		Returns:
			Dict[str, Any]: Dictionary representation of registry contents.
		"""
		try:
			store = self._get_store()
			return dict(store)
		except Exception as e:
			logger.error(f"Failed to convert registry to dictionary: {e}")
			raise

	def update(self, other: Dict[str, Any]) -> None:
		"""
		Update registry with key-value pairs from another dictionary.

		Args:
			other (Dict[str, Any]): Dictionary of key-value pairs to add.
		"""
		try:
			store = self._get_store()
			store.update(other)
			store.commit()
			logger.debug(f"Registry updated with {len(other)} entries")
		except Exception as e:
			logger.error(f"Failed to update registry: {e}")
			raise

	def values(self) -> Iterator[Any]:
		"""
		Get all values in the registry.

		Returns:
			Iterator[Any]: Iterator of registry values.
		"""
		try:
			store = self._get_store()
			return iter(store.values())
		except Exception as e:
			logger.error(f"Failed to retrieve registry values: {e}")
			raise

from typing import Any, Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class InMemoryStore(Generic[T]):
    def __init__(self, id_field: str = "id", max_items: int = 10000) -> None:
        self._data: dict[str, T] = {}
        self._id_field = id_field
        self._indices: dict[str, dict[Any, list[str]]] = {}
        self._max_items = max_items  # Memory limit

    def add(self, item: T) -> T:
        item_id = getattr(item, self._id_field)
        self._data[item_id] = item
        self._update_indices(item)
        self._check_memory_limit()
        return item

    def get(self, item_id: str) -> T | None:
        return self._data.get(item_id)

    def get_by_index(self, index_name: str, value: Any) -> list[T]:
        if index_name not in self._indices:
            return []

        item_ids = self._indices[index_name].get(value, [])
        return [self._data[item_id] for item_id in item_ids if item_id in self._data]

    def list(self, filters: dict[str, Any] | None = None) -> list[T]:
        items = list(self._data.values())

        if not filters:
            return items

        result = []
        for item in items:
            match = True
            for key, value in filters.items():
                if not hasattr(item, key) or getattr(item, key) != value:
                    match = False
                    break
            if match:
                result.append(item)

        return result

    def update(self, item_id: str, data: dict[str, Any]) -> T | None:
        if item_id not in self._data:
            return None

        item = self._data[item_id]

        # Remove from indices before update
        self._remove_from_indices(item)

        # Update item with new data
        for key, value in data.items():
            if hasattr(item, key):
                setattr(item, key, value)

        # Re-add to indices
        self._update_indices(item)
        return item

    def delete(self, item_id: str) -> bool:
        if item_id not in self._data:
            return False

        item = self._data[item_id]
        self._remove_from_indices(item)
        del self._data[item_id]
        return True

    def count(self) -> int:
        return len(self._data)

    def clear(self) -> None:
        self._data.clear()
        for index in self._indices.values():
            index.clear()

    def add_index(self, field_name: str) -> None:
        if field_name in self._indices:
            return

        self._indices[field_name] = {}

        # Populate the new index with existing data
        for item in self._data.values():
            if hasattr(item, field_name):
                value = getattr(item, field_name)
                if value not in self._indices[field_name]:
                    self._indices[field_name][value] = []

                item_id = getattr(item, self._id_field)
                if item_id not in self._indices[field_name][value]:
                    self._indices[field_name][value].append(item_id)

    def set_max_items(self, max_items: int) -> None:
        self._max_items = max_items
        self._check_memory_limit()

    def _update_indices(self, item: T) -> None:
        item_id = getattr(item, self._id_field)

        for field_name, index in self._indices.items():
            if hasattr(item, field_name):
                value = getattr(item, field_name)

                if value not in index:
                    index[value] = []

                if item_id not in index[value]:
                    index[value].append(item_id)

    def _remove_from_indices(self, item: T) -> None:
        item_id = getattr(item, self._id_field)

        for field_name, index in self._indices.items():
            if hasattr(item, field_name):
                value = getattr(item, field_name)

                if value in index and item_id in index[value]:
                    index[value].remove(item_id)

                    # Clean up empty lists
                    if not index[value]:
                        del index[value]

    def _check_memory_limit(self) -> None:
        if len(self._data) > self._max_items:
            # Simple strategy: remove oldest items (assuming ordered insertion)
            items_to_remove = len(self._data) - self._max_items
            for item_id in list(self._data.keys())[:items_to_remove]:
                self.delete(item_id)

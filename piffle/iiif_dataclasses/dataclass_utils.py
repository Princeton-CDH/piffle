from __future__ import annotations

from typing import Any


class GeoreferencingError(ValueError):
    pass


def parse_item(item: Any, dataclass: Any, raise_error: bool = True):
    if item is None:
        return item
    elif not isinstance(item, dataclass):
        try:
            return dataclass(**item)
        except GeoreferencingError:
            raise
        except TypeError:
            return item
        except ValueError:
            if raise_error:
                raise ValueError(f"Item {item} is not an {dataclass}")
    return item

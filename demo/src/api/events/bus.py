import logging
from collections import defaultdict
from collections.abc import Callable
from typing import Any

logger = logging.getLogger(__name__)

EventHandler = Callable[[Any], None]

_subscribers: dict[type, list[EventHandler]] = defaultdict(list)

def subscribe(event_type: type, handler: EventHandler) -> None:
    _subscribers[event_type].append(handler)

def publish(event: object) -> None:
    event_type = type(event)
    handlers = _subscribers.get(event_type, [])
    logger.info("Publicando evento %s para %d handlers", event_type.__name__, len(handlers))
    for handler in handlers:
        try:
            handler(event)
        except Exception:
            logger.exception("Erro no handler %s para evento %s", handler.__name__, event_type.__name__)

def clear() -> None:
    """Clear all subscribers. Used in tests."""
    _subscribers.clear()

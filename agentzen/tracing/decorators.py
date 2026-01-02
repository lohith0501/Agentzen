from functools import wraps
from typing import Callable, Awaitable
from .tracer import Tracer


def trace_async_step(tracer: Tracer, name: str):
    def decorator(fn: Callable[..., Awaitable]):
        @wraps(fn)
        async def wrapper(*args, **kwargs):
            span = tracer.start_span(name)
            try:
                result = await fn(*args, **kwargs)
                tracer.end_span(span, result)
                return result
            except Exception as e:
                tracer.record_exception(span, e)
                raise

        return wrapper

    return decorator

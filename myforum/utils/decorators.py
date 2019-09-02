import logging, functools

logger = logging.getLogger('myforum')

try:
    # Loads up
    from uwsgidecorators import spool, timer
except Exception as exc:
    logger.warning("uwsgi decorators not found, tasks are synchronous")

    # Create a synchronous version of the spooler
    def spool(pass_arguments=True):
        def outer(func):
            @functools.wraps(func)
            def inner(*args, **kwargs):
                result = func(*args, **kwargs)
                return result
            inner.spool = inner
            return inner
        # Gains an attribute called spool that
        # falls back to the same function
        return outer

    # Create a synchronous version of the timer
    def timer(secs, **kwargs):
        def outer(func):
            @functools.wraps(func)
            def inner(*args, **kwargs):
                result = func(*args, **kwargs)
                return result
            inner.timer = inner
            return inner
        # Gains an attribute called timer that
        # falls back to the same function
        return outer

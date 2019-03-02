from app import logger


def wrap_in_logs(before=None, after=None):
    def real_decorator(function):
        def wrapper(*args, **kwargs):
            if before is not None:
                logger.debug(before)

            result = function(*args, **kwargs)

            if after is not None:
                logger.debug(after)
            return result
        return wrapper
    return real_decorator

from functools import wraps

def disable_for_loaddata(signal_handler):
    """
    Decorator that turns off signal handlers when loading fixture data.
    https://docs.djangoproject.com/en/3.0/ref/django-admin/#what-s-a-fixture
    """
    @wraps(signal_handler)
    def wrapper(*args, **kwargs):
        if kwargs and kwargs.get('raw', False):
            return
        signal_handler(*args, **kwargs)
    return wrapper
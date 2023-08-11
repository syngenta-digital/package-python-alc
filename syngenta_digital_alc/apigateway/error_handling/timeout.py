import signal

from syngenta_digital_alc.apigateway.custom_exceptions import ApiTimeout

# maximum API gateway timeout at time of writing, remember this is configurable per endpoint
APIGATEWAY_MAXIMUM_RUNTIME_SECONDS = (
    30 - 2
)  # substract 2 to give us 2 seconds to cleanup


def timeout_after(seconds=APIGATEWAY_MAXIMUM_RUNTIME_SECONDS):
    """
    Decorator that raises an ApiTimeout exception if the decorated function does not return within the specified time.

    Args:
        seconds: int
    """

    def inner(func):
        def wrapper(*args, **kwargs):
            def buzzer(signum, frame):
                raise ApiTimeout()

            signal.signal(signal.SIGALRM, buzzer)
            signal.alarm(seconds)

            result = func(*args, **kwargs)

            signal.alarm(0)

            return result

        return wrapper

    return inner

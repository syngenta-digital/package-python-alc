import signal
import functools
from syngenta_digital_alc.apigateway.custom_exceptions import ApiTimeout
from syngenta_digital_alc.apigateway.response_client import ResponseClient


# maximum api gateway timeout at time of writing, remember this is configurable per endpoint
APIGATEWAY_MAXIMUM_RUNTIME_SECONDS = 30 - 2  # substract 2 to give us 2 seconds to cleanup


def timeout_after(seconds=APIGATEWAY_MAXIMUM_RUNTIME_SECONDS):
    def inner(func):
        def wrapper(*args, **kwargs):

            def handle_timeout(signum, frame):
                raise ApiTimeout()

            signal.signal(signal.SIGALRM, handle_timeout)
            signal.alarm(seconds)

            result = func(*args, **kwargs)

            signal.alarm(0)

            return result

        return wrapper
    return inner


def set_response_timeout_error(response: ResponseClient):
    response.set_error(key_path='Integration Timeout', message="This ")

from syngenta_digital_alc.apigateway.request_client import RequestClient
from syngenta_digital_alc.apigateway.response_client import ResponseClient
from syngenta_digital_alc.apigateway.request_validator import RequestValidator
from syngenta_digital_alc.apigateway.custom_exceptions import ApiTimeout
from syngenta_digital_alc.apigateway.error_handling.timeout import (
    timeout_after,
    APIGATEWAY_MAXIMUM_RUNTIME_SECONDS,
)
from syngenta_digital_alc.common import logger


def handler_requirements(timeout_seconds=APIGATEWAY_MAXIMUM_RUNTIME_SECONDS, **kwargs):
    def decorator_func(func):
        def wrapper(event, context, schema_path=""):
            request = RequestClient(event, context)
            response = ResponseClient()
            validator = RequestValidator(request, response, schema_path)
            validator.validate_request(**kwargs)
            if not response.has_errors:
                timeout_wrapper = timeout_after(seconds=timeout_seconds)
                timeout_wrapped = timeout_wrapper(func)

                try:
                    timeout_wrapped(request, response)
                except ApiTimeout:
                    response.code = 400
                    response.set_error(
                        key_path="Integration Timeout",
                        message="This API call timed out. Please try more, smaller queries, or reach out to our help-connect channel!",
                    )

                    logger.log(
                        level='ERROR',
                        log=f"{request.path_parameters} has timed out! Sending human readable message to user."
                    )

            return response.response

        return wrapper

    return decorator_func

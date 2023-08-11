import unittest
import time
from syngenta_digital_alc.apigateway.handler_requirements import handler_requirements
from tests.syngenta_digital_alc.apigateway.mock_data import apigateway_event


class TestTimeoutHandling(unittest.TestCase):
    def setUp(self):
        self.event = apigateway_event()
        self.context = {}

    def test_raises_api_timeout(self):
        def my_endpoint(request, response):
            time.sleep(30)

        wrapped = handler_requirements()(my_endpoint)

        result = wrapped(self.event, {})

        self.assertEqual(
            result["body"],
            '{"errors": [{"key_path": "Integration Timeout", "message": "This API call timed out. Please try more, smaller queries, or reach out to our help-connect channel!"}]}',
        )

    def test_not_raises_api_timeout(self):
        def my_endpoint(request, response):
            time.sleep(2)

        wrapped = handler_requirements()(my_endpoint)

        result = wrapped(self.event, {})

        self.assertEqual(result["body"], "{}")

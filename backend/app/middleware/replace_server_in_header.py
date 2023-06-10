"""
Middleware to replace the Server header in the response with a custom string
"""


class ReplaceServerHeaderMiddleware(object):
    # One-time configuration and initialization.
    def __init__(self, get_response):
        self.get_response = get_response

    # This call method is called once per request before the view is called
    def __call__(self, request):
        # Get the response for the request
        response = self.get_response(request)
        # Set the Server header to a custom string
        response.__setitem__('Server', 'Nothing to see here :)')
        # Return the response
        return response

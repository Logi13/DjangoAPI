# file: initialHeaderMiddleware/middleware.py

class HeaderTranslationMiddleware:
    def __init__(self, get_response):
        #one-time configurations and instance variables
        #print("---Init Header Translation [__init__]--->")
        self.get_response = get_response
        

    def __call__(self, request):
        #print("---Call Header Translation [__call__]---|")
        response = self.get_response(request)
        return response

    def process_template_response(self, request, response):
        #print("---[process_template_response] ---|")
        if 'image/webp' in request.headers['Accept'].split(','):
            response.context_data["imageType"] = '.webp'
        else:
            response.context_data["imageType"] = '.png'
        return response
        

class Request:

    def __init__(self, request):
        self.exists = bool(request)
        if self.exists:
            self.parse(request)

    def parse(self):
        

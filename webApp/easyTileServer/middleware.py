from django.contrib.sessions.middleware import SessionMiddleware
from django.conf import settings

class NoAnonymousCookiesMiddleware(SessionMiddleware):

    def process_request(self, request):
        """
        Disable CSRF otherwise login wont work, because the csrf cookie gets deleted for anonymous users
        """
        setattr(request, '_dont_enforce_csrf_checks', True)
    
    def process_response(self, request, response):
        """
        Delete all cookies for anonymous users
        """
        response = super(NoAnonymousCookiesMiddleware, self).process_response(request, response)
        try :
            if not request.user.is_authenticated():
                response.cookies.clear()
        except:
            pass
            
        return response

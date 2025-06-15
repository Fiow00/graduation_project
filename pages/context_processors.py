from craftsmen.models import Craftsman

def craftsman_context(request):
    craftsman = None
    if request.user.is_authenticated:
        try:
            craftsman = request.user.craftsman
        except (AttributeError, Craftsman.DoesNotExist):
            craftsman = None
    return {'craftsman': craftsman}
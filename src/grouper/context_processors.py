from django.conf import settings

def debug(request):
    """
    Return context variable indicating whether debug mode is active.
    This overrides the default Django behavior which requires INTERNAL_IPS match.
    """
    return {'debug': settings.DEBUG}

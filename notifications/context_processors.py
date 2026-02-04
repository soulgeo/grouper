from .models import Notification


def user_notifications(request):
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(
            user=request.user,
        ).order_by(
            '-created_at'
        )[:25]
    else:
        notifications = []

    return {'notifications': notifications}

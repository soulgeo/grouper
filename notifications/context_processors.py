from .models import Notification


def user_notifications(request):
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(
            user=request.user,
            is_active=True,
        ).order_by(
            '-created_at'
        )[:5]
    else:
        notifications = []

    return {'notifications': notifications}

from django.http import HttpResponse
from django.shortcuts import redirect, render

from .models import Notification


def clear_notification(request, id):
    if request.method != 'POST':
        return redirect('/account')  # TODO: Change Redirect

    notification = Notification.objects.get(id=id)
    if notification.user != request.user:
        return HttpResponse("Unauthorized", status=403)

    notification.delete()

    return HttpResponse("")


def clear_all_notifications(request):
    if request.method != 'POST':
        return redirect('/account')  # TODO: Change Redirect

    Notification.objects.filter(user=request.user).delete()

    return HttpResponse("")


def get_user_notifications(request):
    notifications = Notification.objects.filter(
        user=request.user,
    ).order_by('-created_at')[:25]

    context = {
        'notifications': notifications
    }
    return render(request, 'user_notifications.html', context)

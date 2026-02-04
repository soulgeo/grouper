from django.http import HttpResponse
from django.shortcuts import redirect, render

from .models import Notification


def clear_notification(request, id):
    notification = Notification.objects.get(id=id)
    if notification.user != request.user:
        return HttpResponse("Unauthorized", status=403)

    notification.is_active = False
    notification.save()

    return HttpResponse("OK", status=200)

def clear_all_notifications(request):
    if request.method != 'POST':
        return redirect('/account')  # TODO: Change Redirect

    Notification.objects.filter(
        user=request.user, is_active=True
    ).update(is_active=False)

    return render(request, 'empty.html', {})

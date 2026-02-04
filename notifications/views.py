from django.shortcuts import redirect, render

from .models import Notification


def clear_notifications(request):
    if request.method != 'POST':
        return redirect('/account')  # TODO: Change Redirect

    Notification.objects.filter(
        user=request.user, is_active=True
    ).update(is_active=False)

    return render(request, 'empty.html', {})

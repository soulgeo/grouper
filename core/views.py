from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Contact


def index(request):
    return render(request, 'index.html')


@login_required
def secret(request):
    return render(request, 'secret.html')


@login_required
def contacts(request):
    user = request.user
    contacts = Contact.objects.filter(user=user)
    context = {"contacts": contacts}
    return render(request, 'contacts.html', context=context)

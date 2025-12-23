from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render

from .models import Contact, Post


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
    template = 'contacts.html'
    return render(request, template, context)


def search_post(request):
    query = request.GET.get('query')
    visibility_filter = Q(visibility=Post.Visibility.PUBLIC)

    if request.user.is_authenticated:
        visibility_filter |= Q(visibility=Post.Visibility.CONTACTS_ONLY) & Q(
            user__in_contacts_of__user=request.user
        )

    results = Post.objects.filter(title__unaccent__icontains=query).filter(
        visibility_filter
    )
    context = {"query": query, "results": results}
    template = 'search_post.html'
    return render(request, template, context)

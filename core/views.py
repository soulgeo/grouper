from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from users.models import UserProfile

from .forms import PostContentForm, PostForm
from .models import Contact, Post


def index(request):
    visibility_filter = Q(visibility=Post.Visibility.PUBLIC)

    if request.user.is_authenticated:
        visibility_filter |= Q(user=request.user)
        visibility_filter |= Q(user__in_contacts_of__user=request.user)

    posts = Post.objects.filter(visibility_filter).order_by('-created_at')
    context = {
        "post_form": PostForm(),
        "post_content_form": PostContentForm(),
        "posts": posts,
    }
    template = 'index.html'
    return render(request, template, context)


def profile(request, username):
    profile = get_object_or_404(
        UserProfile.objects.select_related('user'), user__username=username
    )
    context = {"profile": profile}
    template = 'profile.html'
    return render(request, template, context)


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
        visibility_filter |= Q(user=request.user)
        visibility_filter |= Q(user__in_contacts_of__user=request.user)

    results = (
        Post.objects.filter(title__unaccent__icontains=query)
        .filter(visibility_filter)
        .order_by('-created_at')
    )
    context = {"query": query, "results": results}
    template = 'search_post.html'
    return render(request, template, context)


def create_post(request):
    if request.method == "POST":
        post_form = PostForm(request.POST)
        post_content_form = PostContentForm(request.POST)
        if post_form.is_valid() and post_content_form.is_valid():
            post_instance = post_form.save(commit=False)
            post_instance.user = request.user
            post_content_instance = post_content_form.save(commit=False)
            post_content_instance.post = post_instance
            post_instance.save()
            post_content_instance.save()
            return redirect("/")
        else:
            print("Form errors:", post_form.errors, post_content_form.errors)
            return redirect("/")  # Or render a template with errors
    else:
        return redirect("/accounts/")

from django.contrib.auth.decorators import login_required
from django.db.models import Q, QuerySet
from django.shortcuts import get_object_or_404, redirect, render

from users.forms import UserForm, UserProfileForm
from users.models import UserProfile

from .forms import PostContentForm, PostForm
from .models import Contact, Post


def filter_visible_posts(request, query_set: QuerySet) -> QuerySet:
    visibility_filter = Q(visibility=Post.Visibility.PUBLIC)

    if request.user.is_authenticated:
        visibility_filter |= Q(user=request.user)
        visibility_filter |= Q(user__in_contacts_of__user=request.user)

    return query_set.filter(visibility_filter)


def index(request):
    posts = filter_visible_posts(request, Post.objects.order_by('-created_at'))

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
    posts = filter_visible_posts(
        request,
        Post.objects.filter(user__username=request.username).order_by(
            '-created_at'
        ),
    )
    context = {"profile": profile, "posts": posts}
    template = 'profile.html'
    return render(request, template, context)


@login_required
def edit_profile(request):
    user = request.user
    profile = get_object_or_404(UserProfile, user=user)

    if request.method == "POST":
        user_form = UserForm(request.POST, instance=user)
        user_profile_form = UserProfileForm(
            request.POST, request.FILES, instance=profile
        )
        if user_form.is_valid() and user_profile_form.is_valid():
            user_form.save()
            user_profile_form.save()
            return redirect("profile", username=user.username)
    else:
        user_form = UserForm(instance=user)
        user_profile_form = UserProfileForm(instance=profile)

    context = {"user_form": user_form, "user_profile_form": user_profile_form}
    template = 'edit_profile.html'
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

    results = filter_visible_posts(
        request,
        Post.objects.filter(title__unaccent__icontains=query).order_by(
            '-created_at'
        ),
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

            context = {
                "post": post_instance,
            }
            partial = 'index.html#post_partial'
            return render(request, partial, context)
        else:
            print("Form errors:", post_form.errors, post_content_form.errors)
            return redirect("/")  # Or render a template with errors
    return redirect("/accounts/")

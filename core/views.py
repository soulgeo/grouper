from django.contrib.auth.decorators import login_required
from django.db.models import BooleanField, Exists, OuterRef, Q, QuerySet, Value
from django.shortcuts import get_object_or_404, redirect, render

from users.forms import UserForm, UserProfileForm
from users.models import User, UserProfile

from .forms import (
    PostContentForm,
    PostForm,
    UserProfileSearchForm,
    UserSearchForm,
)
from .models import Contact, FriendRequest, InterestCategory, Post


def filter_visible_posts(request, query_set: QuerySet) -> QuerySet:
    visibility_filter = Q(visibility=Post.Visibility.PUBLIC)

    if request.user.is_authenticated:
        visibility_filter |= Q(user=request.user)
        visibility_filter |= Q(user__in_contacts_of__user=request.user)

    return query_set.filter(visibility_filter).distinct()


def index(request):
    posts = filter_visible_posts(request, Post.objects.order_by('-created_at'))

    context = {
        'post_form': PostForm(),
        'post_content_form': PostContentForm(),
        'posts': posts,
    }
    template = 'index.html'
    return render(request, template, context)


def search_users(request):
    query = request.GET.get('query')

    in_contacts = request.GET.get('in_contacts')
    country = request.GET.get('country')
    interests = request.GET.getlist('interests')

    profiles = UserProfile.objects.filter(
        user__username__unaccent__icontains=query
    )

    if interests:
        profiles = profiles.filter(interests__in=interests)

    if country:
        profiles = profiles.filter(country=country)

    if in_contacts:
        profiles = profiles.filter(user__in_contacts_of__user=request.user)

    if request.user.is_authenticated:
        profiles = profiles.annotate(
            is_contact=Exists(
                Contact.objects.filter(
                    user=request.user, contact=OuterRef('user')
                )
            ),
            request_sent=Exists(
                FriendRequest.objects.filter(
                    sender=request.user,
                    receiver=OuterRef('user'),
                    status=FriendRequest.Status.PENDING,
                )
            ),
        )
    else:
        profiles = profiles.annotate(
            is_contact=Value(False, output_field=BooleanField()),
            request_sent=Value(False, output_field=BooleanField()),
        )

    interest_categories = InterestCategory.objects.prefetch_related(
        'interests'
    ).all()
    user_search_form = UserSearchForm(request.GET)
    user_profile_search_form = UserProfileSearchForm(request.GET)

    try:
        selected_interests = [int(i) for i in interests]
    except ValueError:
        selected_interests = []

    context = {
        "query": query,
        "in_contacts": in_contacts,
        "selected_interests": selected_interests,
        "country": country,
        "user_search_form": user_search_form,
        "user_profile_search_form": user_profile_search_form,
        "interest_categories": interest_categories,
        "profiles": profiles,
    }
    template = "search_users.html"
    return render(request, template, context)


def profile(request, username):
    qs = UserProfile.objects.select_related('user')
    if request.user.is_authenticated:
        qs = qs.annotate(
            is_contact=Exists(
                Contact.objects.filter(
                    user=request.user, contact=OuterRef('user')
                )
            ),
            request_sent=Exists(
                FriendRequest.objects.filter(
                    sender=request.user,
                    receiver=OuterRef('user'),
                    status=FriendRequest.Status.PENDING,
                )
            ),
        )
    else:
        qs = qs.annotate(
            is_contact=Value(False, output_field=BooleanField()),
            request_sent=Value(False, output_field=BooleanField()),
        )

    profile = get_object_or_404(qs, user__username=username)

    posts = filter_visible_posts(
        request,
        Post.objects.filter(user__username=username).order_by('-created_at'),
    )

    context = {
        'profile': profile,
        'posts': posts,
        'post_form': None,
        'post_content_form': None,
    }
    if request.user.username == username:
        context['post_form'] = PostForm()
        context['post_content_form'] = PostContentForm()
    template = 'profile.html'
    return render(request, template, context)


@login_required
def edit_profile(request):
    user = request.user
    profile = get_object_or_404(UserProfile, user=user)

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        user_profile_form = UserProfileForm(
            request.POST, request.FILES, instance=profile
        )
        if user_form.is_valid() and user_profile_form.is_valid():
            user_form.save()
            user_profile_form.save()
            return redirect('profile', username=user.username)
    else:
        user_form = UserForm(instance=user)
        user_profile_form = UserProfileForm(instance=profile)

    context = {'user_form': user_form, 'user_profile_form': user_profile_form}
    template = 'edit_profile.html'
    return render(request, template, context)


@login_required
def contacts(request):
    user = request.user
    contacts = Contact.objects.filter(user=user)
    context = {'contacts': contacts}
    template = 'contacts.html'
    return render(request, template, context)


@login_required
def friend_requests(request):
    friend_requests = request.user.received_friend_requests.filter(
        status=FriendRequest.Status.PENDING
    )
    context = {'friend_requests': friend_requests}
    template = 'friend_requests.html'
    return render(request, template, context)


@login_required
def send_friend_request(request, username):
    if not request.method == 'POST':
        return redirect('/')

    receiver = User.objects.get(username=username)
    friend_request = FriendRequest()
    friend_request.sender = request.user
    friend_request.receiver = receiver
    friend_request.save()

    profile = UserProfile.objects.annotate(
        is_contact=Value(False, output_field=BooleanField()),
        request_sent=Value(True, output_field=BooleanField()),
    ).get(user=receiver)

    context = {
        "friend_request": friend_request,
        "profile": profile,
    }
    partial = 'includes/friend_button.html#friend_button'
    return render(request, partial, context)


def accept_friend_request(request, id):
    if not request.method == 'POST':
        return redirect('/')

    friend_request = FriendRequest.objects.get(id=id)

    sender_contact = Contact()
    sender_contact.user = friend_request.sender
    sender_contact.contact = friend_request.receiver

    receiver_contact = Contact()
    receiver_contact.user = friend_request.receiver
    receiver_contact.contact = friend_request.sender

    friend_request.status = FriendRequest.Status.ACCEPTED

    sender_contact.save()
    receiver_contact.save()
    friend_request.save()

    context = {"friend_request": friend_request}
    partial = "friend_requests.html#friend_request"
    return render(request, partial, context)


def search_post(request):
    query = request.GET.get('query')

    results = filter_visible_posts(
        request,
        Post.objects.filter(title__unaccent__icontains=query).order_by(
            '-created_at'
        ),
    )
    context = {'query': query, 'results': results}
    template = 'search_post.html'
    return render(request, template, context)


@login_required
def like_post(request, post_id):
    if not request.method == 'POST':
        return redirect('/accounts/')

    post = Post.objects.get(id=post_id)

    if request.user in post.likes.all():
        post.likes.remove(request.user)

    else:
        post.likes.add(request.user)

    post.save()
    context = {'post': post}
    partial = 'includes/post.html#post_partial'
    return render(request, partial, context)


@login_required
def create_post(request):
    if not request.method == 'POST':
        return redirect('/accounts/')

    post_form = PostForm(request.POST)
    post_content_form = PostContentForm(request.POST)

    if not post_form.is_valid() or not post_content_form.is_valid():
        print('Form errors:', post_form.errors, post_content_form.errors)
        return redirect('/')  # Or render a template with errors

    post_instance = post_form.save(commit=False)
    post_instance.user = request.user

    post_content_instance = post_content_form.save(commit=False)
    post_content_instance.post = post_instance

    post_instance.save()
    post_content_instance.save()

    context = {
        'post': post_instance,
    }
    partial = 'includes/post.html#post_partial'
    return render(request, partial, context)

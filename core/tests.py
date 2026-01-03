from django.test import TestCase, RequestFactory
from users.models import User
from core.models import Post, Contact
from core.views import filter_visible_posts

class PostVisibilityTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='me', email='me@example.com', password='password')
        self.friend = User.objects.create_user(username='friend', email='friend@example.com', password='password')
        
        # Make friend a contact of user
        Contact.objects.create(user=self.user, contact=self.friend)
        
        self.factory = RequestFactory()

    def test_public_post_by_contact_no_duplicates(self):
        # Create a public post by friend
        # This matches:
        # 1. Visibility=PUBLIC
        # 2. user__in_contacts_of__user=request.user
        # Without distinct(), this would return duplicate.
        post = Post.objects.create(
            user=self.friend,
            title="Friend's Public Post",
            visibility=Post.Visibility.PUBLIC,
        )
        
        request = self.factory.get('/')
        request.user = self.user
        
        qs = Post.objects.all()
        filtered = filter_visible_posts(request, qs)
        
        self.assertEqual(filtered.count(), 1)
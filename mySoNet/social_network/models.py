# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser, Group, Permission 

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.core.validators import EmailValidator
from django.db import models
from django.utils import timezone

class UserManager(BaseUserManager):
    """
    Custom user manager to handle user creation with email and password.
    """

    def create_user(self, username, email, password, **extra_fields):
        """
        Creates and saves a User with the given email, password and other fields.

        Args:
            username (str): The username for the user.
            email (str): The email address of the user.
            password (str): The password for the user.
            extra_fields (dict, optional): A dictionary of other fields that should be saved on the user.

        Returns:
            User: The created user object.
        """

        if not username:
            raise ValueError('The username is required')

        if not email:
            raise ValueError('The email address is required')

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

class User(AbstractUser):
    ''' User information'''
    username = models.CharField(unique=True, max_length=225)
    email = models.CharField(max_length=50, unique=True, validators=[EmailValidator()])  # Ensures valid email format
    password = models.CharField(max_length=24, default="")  # This field is already hashed by AbstractUser
    bio = models.CharField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True)
    date_joined = models.DateTimeField(default=timezone.now)  # Auto-filled on creation
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='social_network_users',  # Different related_name here
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='social_network_users',  # Different related_name here
        blank=True
    )
    class Meta:
        db_table = 'user'


class Attachment(models.Model):
    ''' Stores information about uploaded files'''
    filename = models.CharField(max_length=225)
    content_type = models.CharField(max_length=255)
    size = models.IntegerField()
    attachment_file = models.FileField(upload_to='attachments/')

    class Meta:
        db_table = 'attachment'

class Post(models.Model):
    ''' Represents a user's post'''
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    attachment = models.ForeignKey(Attachment, on_delete = models.CASCADE, blank=True, null=True)

    class Meta:
        db_table = 'user_posts'
    
    def __str__(self):
        return f"{self.author.username} - {self.body[:20]}"


class PostAttachment(models.Model):
    '''Connects attachments to specific posts'''
    attachment = models.ForeignKey(Attachment, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        db_table = 'attachment_post'

class MessageThread(models.Model):
    '''Represents a conversation between two users '''
    participants = models.ManyToManyField(User, related_name='messagethreads')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'message_thread'


class Message(models.Model):
    '''Individual messages within a thread'''
    thread = models.ForeignKey(MessageThread, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField(max_length=1024)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=25, blank=True, null=True)

    class Meta:
        db_table = 'private_message'


class Comment(models.Model):
    '''Comments on user posts'''
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_comments'



class UserEngagement(models.Model):
    '''Stores post engagement metrics'''
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    views = models.IntegerField(blank=True, null=True)
    comments = models.IntegerField(blank=True, null=True)
    likes = models.IntegerField(blank=True, null=True)
    shares = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'user_engagement'


class Follow(models.Model):
  """Tracks user following relationships."""
  follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
  following = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)

  class Meta:
    unique_together = ('follower', 'following')  # Ensure a user can't follow the same user twice
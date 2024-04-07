# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import AbstractUser 

class User(AbstractUser):
    ''' User information'''
    username = models.CharField(unique=True, max_length=225)
    email = models.CharField(max_length=50, blank=True, null=True)
    password_hash = models.CharField(max_length=24)
    bio = models.CharField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True)
    date_joined = models.DateTimeField()

    class Meta:
        db_table = 'user_profile'

class Attachment(models.Model):
    ''' Stores information about uploaded files'''
    filename = models.CharField(max_length=225)
    content_type = models.CharField(max_length=255)
    size = models.IntegerField()
    attachment_file = models.FileField(upload_to='/attachments/')

    class Meta:
        db_table = 'attachment'

class Post(models.Model):
    ''' Represents a user's post'''
    user_profile = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    attachment = models.ForeignKey(Attachment, on_delete = models.CASCADE, blank=True, null=True)

    class Meta:
        db_table = 'user_posts'


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


class UserConnection(models.Model):
    '''Tracks user following relationships'''
    follower = models.ForeignKey(User, on_delete=models.CASCADE)
    following = models.ForeignKey(User,on_delete=models.CASCADE))
    status = models.CharField(blank=True, null=True)

    class Meta:
        db_table = 'user_connection'


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
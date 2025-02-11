"""Defines URL patterns for learning_logs."""

from django.urls import path
from . import views

app_name = 'learning_logs'
urlpatterns = [
    # Home page
    path('',views.index, name='index'),
    # Page that shows all topics
    path('topics/', views.topics, name='topics'),
    # Page that shows entries for one topic.
    path('topics/<int:topic_id>/', views.topic, name='topic'),
    # Page for a user to add a new topic
    path('new_topic/', views.new_topic, name='new_topic'),
    # Page for a new user Entry.
    path('new_entry/<int:topic_id>/', views.new_entry, name='new_entry'),
    # Delete a blog
    path('delete_blog/<int:topic_id>/', views.delete_topic, name="delete_topic"),
    # Delete an entry
    path('delete_entry/<int:entry_id>/', views.delete_entry, name="delete_entry"),
    # Edit an entry
    path('edit/<int:entry_id>/', views.edit_entry, name="edit_entry"),
]
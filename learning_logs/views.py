from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .models import Topic, Entry
from .forms import TopicForm, EntryForm

def index(request):
    """The home page for Learning Log."""
    return render(request, 'learning_logs/index.html')

@login_required
def topics(request):
    """Show all topics."""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics' : topics}
    return render(request, 'learning_logs/topics.html', context)

@login_required
def topic(request, topic_id):
    """Shows entries for a given topic."""
    # Load in the topic using the provided id.
    topic = Topic.objects.get(id=topic_id)
    # Make sure the topic belongs to the current user
    check_topic_owner(request, topic)
    
    # Populate name and entries variables for context.
    entries = topic.entry_set.order_by('-date_added')

    # Create dictionary context
    context = {
        'topic' : topic,
        'entries' : entries
    }
    # Return the context.
    return render(request, 'learning_logs/topic.html', context)

@login_required
def check_topic_owner(request, topic):
    """Helper function to check topic owner."""
    if request.user != topic.owner:
        raise Http404
    
@login_required
def new_topic(request):
    """Allows the entry of a new topic."""
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = TopicForm()
    else:
        # POST data submitted; process data.
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('learning_logs:topics')
        
    # Display a blank or invalid form.
    context = {'form' : form}
    return render(request, 'learning_logs/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    """View to add a new entry for a topic."""
    topic = Topic.objects.get(id=topic_id)
    check_topic_owner(request, topic)
    
    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('learning_logs:topic', topic_id=topic_id)
    
    context = {
        'form' : form,
        'topic' : topic,
    }

    return render(request, 'learning_logs/new_entry.html', context)

@login_required
def delete_topic(request, topic_id):
    """Deletes a topic."""
    topic = Topic.objects.get(id=topic_id)
    check_topic_owner(request, topic)
    topic.delete()
    return redirect("learning_logs:topics")


@login_required
def delete_entry(request, entry_id):
    """Deletes an entry."""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    check_topic_owner(request, topic)
    entry.delete()
    return redirect("learning_logs:topic", topic_id=topic.id)

@login_required
def edit_entry(request, entry_id):
    """View for the user to edit an existing entry."""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    check_topic_owner(request, topic)
    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        form = TopicForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("learning_logs:topic", topic_id = topic.id)
    context = {'form' : form, 'entry' : entry, 'topic' : topic}
    return render(request, "learning_logs/edit_entry.html", context)


from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from accounts.models import CustomUser as User
from django.db.models import Q
from .models import Relationship, FriendRequest, Relation, NotificationVerbs
from notifications.signals import notify
from django.db.models.signals import post_save
from django.contrib import messages
from django.urls import reverse
# import packages for network drawing
from pyvis.network import Network
import networkx
from bs4 import BeautifulSoup
import re


# Create your views here.


def home(request):
    def clean_network_html(html_content: str, del_html_by_pattern: list):
        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Define a regular expression pattern for "bootstrap"
        for pattern in del_html_by_pattern:
            bootstrap_pattern = re.compile(pattern, re.IGNORECASE)

            # Find all <link> tags and attributes containing "bootstrap" and remove them
            for link_element in soup.find_all('link', href=bootstrap_pattern):
                link_element.decompose()

            # Find all <script> tags and attributes containing "bootstrap" and remove them
            for script_element in soup.find_all('script', src=bootstrap_pattern):
                script_element.decompose()
        return str(soup)
    def single_target

    # Create a Network instance
    net = Network()
    G = networkx.Graph()
    # Get all users and their relationships
    users = User.objects.all()
    relationships = Relationship.objects.all()

    # Add nodes for users
    for user in users:
        G.add_node(user.id, label=user.username)

    # Add edges for relationships
    for relation in relationships:
        G.add_edge(relation.user.id, relation.friend.id, label=relation.relationship_type)
    if not user.is_superuser:
        G = G.path_graph(2)

    # Generate the HTML for the network
    net.from_nx(G)
    network_html = net.generate_html()
    network_html = clean_network_html(network_html, ['bootstrap'])
    return render(request, 'home.html', {'network': network_html})

def search_users(request):
    query = request.GET.get('q', '')
    
    # Perform the search based on the query.
    results = User.objects.filter(Q(username__icontains=query) | Q(first_name__icontains=query) | Q(last_name__icontains=query) | Q(nick_name__icontains=query) | Q(email__icontains=query))
    return render(request, 'search_results.html', {'results': results, 'query': query, 'choices': Relation.choices})

def send_friend_request(request, user_id):
    if request.method == 'POST':
        # Get the selected relationship type from the form
        relationship_type = request.POST.get('relationship')
        notification_desicription = {choice[0]: choice[1] for choice in NotificationVerbs.choices}
        notification_verbs = lambda relation_type: 'connection_request' if relationship_type in [notif[0] for notif in NotificationVerbs.choices[0:3]] else relationship_type
        if relationship_type:
            # Create a friend request with the selected relationship type
            # Get the sender and receiver users
            sender = request.user
            receiver = User.objects.get(id=user_id)

            # Check if a friend request already exists
            friend_request = FriendRequest.objects.filter(
                sender=sender, receiver=receiver, relationship_type=relationship_type
            ).first()
            if not friend_request:
                # Create a new friend request
                friend_request = FriendRequest(
                    sender=sender, receiver=receiver, relationship_type=relationship_type
                )
                friend_request.save()
                print(notification_verbs(relationship_type))
                notify.send(
                    sender, 
                    recipient=receiver, 
                    verb=f'{notification_verbs(relationship_type)}',
                    description=f'{sender} send you a {notification_desicription[relationship_type]}',
                    action_object=friend_request
                    )

    return redirect('home')

def confirm_request(request, notification_id):
    notification = request.user.notifications.get(id=notification_id)	
    notification.mark_as_read()	

    # Create a relationship using the instance of FriendRequest
    friend_request = FriendRequest.objects.get(id=notification.action_object.id)
    friend_request.status = 'confirm'  # Change status to "confirm"
    friend_request.save()  # Save the updated FriendRequest
    Relationship.objects.create(
        user=request.user,
        friend=friend_request.sender,
        relationship_type=friend_request.relationship_type,
    )


    # Display a success message
    messages.success(request, 'Friend request confirmed.')
    # Redirect to the desired page after confirmation

    return HttpResponseRedirect(request.path_info)

def ignore_request(request, notification_id):
    notification = request.user.notifications.get(id=notification_id)   
    notification.mark_as_read()
    return HttpResponseRedirect(request.path_info)

def mark_as_read(request, notification_id):
    notification = request.user.notifications.filter(verb__in=['update', 'confirm'])
    for notification in update_confirm_notifications:
        notification.mark_as_read()





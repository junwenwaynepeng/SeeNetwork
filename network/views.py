from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from accounts.models import CustomUser as User
from django.db.models import Q
from .models import Relationship, FriendRequest, NotificationVerbs
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
    def find_nodes_within_distance(source: set, relationships: set, edges:set, length: int):
        if length==0:
            return list(source), list(relationships)
        else:
            old_edges = set(edges)
            for edge in old_edges:
                if (edge[0], edge[1]) in source:
                    source.add((edge[2], edge[3]))
                    relationships.add(edge)
                    edges.remove(edge)
                if (edge[2], edge[3]) in source:
                    source.add((edge[0], edge[1]))
                    relationships.add(edge)
                    edges.remove(edge)
            return find_nodes_within_distance(source, relationships, edges, length-1)

    # Create a Network instance
    net = Network()
    G = networkx.Graph()
    # Get all users and their relationships
    users = User.objects.all()
    relationships = Relationship.objects.all()
    user = request.user

    if user.is_superuser:
        # Add nodes for users
        for user in users:
            G.add_node(user.id, label=user.username)

        # Add edges for relationships
        for relation in relationships:
            G.add_edge(relation.user.id, relation.friend.id)
    else:
        edges = {(relation.user.id, relation.user.username, relation.friend.id, relation.friend.username) for relation in relationships}
        source, local_relationships = find_nodes_within_distance({(user.id, user.username)}, set(), edges, 2)
        try:
            for node in source:
                G.add_node(node[0], label=node[1])
            for relation in local_relationships:
                G.add_edge(relation[0], relation[2])
        except Exception as e:
            print(e)

    # Generate the HTML for the network
    net.from_nx(G)
    network_html = net.generate_html()
    network_html = clean_network_html(network_html, ['bootstrap'])
    return render(request, 'home.html', {'network': network_html})

def search_users(request):
    query = request.GET.get('q', '')
    user=request.user
    # Perform the search based on the query.
    results = User.objects.filter(Q(username__icontains=query) | Q(first_name__icontains=query) | Q(last_name__icontains=query) | Q(nick_name__icontains=query) | Q(email__icontains=query) | Q(student_id__icontains=query)).exclude(id=user.id)
    request_has_sent = list()
    friends = list()
    for result in results:
        if FriendRequest.objects.filter(sender=user.id, receiver=result.id).first():
            request_has_sent.append(result)
        if Relationship.objects.filter(user=user.id, friend=result.id).first():
            friends.append(result)

    return render(
            request, 
            'search_results.html', 
            {
                'results': results, 
                'query': query, 
                'request_has_sent': request_has_sent,
                'friends': friends,
                })

def send_friend_request(request, user_id):
    if request.method=='POST':
        # Get the selected relationship type from the form
        # Create a friend request with the selected relationship type
        # Get the sender and receiver users
        sender = request.user
        receiver = User.objects.get(id=user_id)
        print(request)
        # Check if a friend request already exists
        friend_request = FriendRequest.objects.filter(
            sender=sender, receiver=receiver
        ).first()
        if not friend_request:
            # Create a new friend request
            friend_request = FriendRequest(
                sender=sender, receiver=receiver
            )
            friend_request.save()
            notify.send(
                sender, 
                recipient=receiver, 
                verb=f'following',
                description=f'{sender} send you a following request',
                action_object=friend_request
                )
        path = re.sub(f'/{user_id}','',request.path_info)
        response_data = {'message': 'Friend request sent successfully'}
    return JsonResponse(response_data)

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
    )
    # Redirect to the desired page after confirmation
    return redirect(request.path_info)

def ignore_request(request, notification_id):
    notification = request.user.notifications.get(id=notification_id)   
    notification.mark_as_read()
    return HttpResponseRedirect(request.path_info)

def mark_as_read(request, notification_id):
    notification = request.user.notifications.filter(verb__in=['update', 'confirm'])
    for notification in update_confirm_notifications:
        notification.mark_as_read()





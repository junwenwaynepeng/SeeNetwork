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
        if FriendRequest.objects.filter(sender=user.id, receiver=result.id, status="pending").first():
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
        try:
            sender = request.user
            receiver = User.objects.get(id=user_id)
            # Check if a friend request already exists
            friend_request = FriendRequest.objects.filter(
                sender=sender, receiver=receiver
            ).first()
            if not friend_request or (friend_request.status==None):
                # Create a new friend request
                if not friend_request:
                    friend_request = FriendRequest(
                        sender=sender, receiver=receiver, status='pending'
                    )
                    friend_request.save()
                else:
                    friend_request.status='pending'
                    friend_request.save()

                # check if the sender is in block list
                if not friend_request.block_sender:
                    notify.send(
                        sender, 
                        recipient=receiver, 
                        verb=NotificationVerbs.following,
                        description=f'{sender} send you a {NotificationVerbs.following.label}',
                        action_object=friend_request
                        )
            response_data = {'message': 'Friend request sent successfully'}
        except Exception as e:
            response_data = {'message': f'{e}'}
    else:
        response_data = {'message': "friend_request doesn't use POST method"}
    return JsonResponse(response_data)

def unsend_friend_request(request, user_id):
    if request.method=='POST':
        # setting up initial values
        sender = request.user
        receiver = User.objects.get(id=user_id)
        friend_request = FriendRequest.objects.get(sender=sender, receiver=receiver)

        # reset friend_request.status
        friend_request.status = None
        friend_request.save()
        notification = receiver.notifications.unread().filter(actor_object_id=sender.id, verb=NotificationVerbs.following)
        # Find the first friend unread notification, and delete it.
        if notification:
            notification.delete()
        relationship = Relationship.objects.filter(user=sender, friend=receiver).first()

        # Confirm -> delete friend request and friendship
        if relationship:
            relationship.delete()
        response_data = {'message': 'Friend request unsent successfully'}            

    else:
        response_data = {'message': "unsend_friend_request doesn't use POST method"}
    return JsonResponse(response_data)

def confirm_request(request, notification_id):
    try:
        notification = request.user.notifications.get(id=notification_id)	
        notification.mark_as_read()	

        # Create a relationship using the instance of FriendRequest
        friend_request = FriendRequest.objects.get(id=notification.action_object.id)
        friend_request.status = NotificationVerbs.confirm  # Change status to "confirm"
        friend_request.save()  # Save the updated FriendRequest
        Relationship.objects.create(
            user=request.user,
            friend=friend_request.sender,
        )
        # check if sender is in block list, otherwise, send notify
        if not friend_request.block_sender:
            notify.send(
                receiver,
                recipient=sender,
                verb=NotificationVerbs.confirm,
                description=f'{receiver} {NotificationVerbs.confirm}')
        response_data = {'messages': 'confirm request successfully'}
    except Exception as e:
        response_data = {'message': f'{e}'}
    # Redirect to the desired page after confirmation
    return JsonResponse(response_data)

def ignore_request(request, notification_id):
    notification = request.user.notifications.get(id=notification_id)   
    notification.mark_as_read()
    response_data = {'message': 'ignore a request'}
    return JsonResponse(response_data)

def block_unblock_user(request, user_id):
    pass
    # Read friend request
    # block user_id
    # unblock user_id




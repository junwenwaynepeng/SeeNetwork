from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from accounts.models import CustomUser as User
from django.db.models import Q, Case, When, Value, IntegerField
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


def graph(request, option):
    
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
            print(edges)
            for edge in old_edges:
                if (edge[0], edge[1]) in source:
                    source.add((edge[2], edge[3]))
                    relationships.add(edge)
                    edges.discard(edge)
                if (edge[2], edge[3]) in source:
                    source.add((edge[0], edge[1]))
                    relationships.add(edge)
                    edges.discard(edge)
            return find_nodes_within_distance(source, relationships, edges, length-1)

    def rgba_string_to_list(rgba:str):
        return list(eval(re.sub(r'rgba', '', rgba)))

    def rgba_list_to_string(rgba:list):
        return f'rgba({rgba[0]},{rgba[1]},{rgba[2]},{rgba[3]})'
    # Create a Network instance
    if option=='digraph':
        net = Network(directed=True)
    else:
        net = Network()

    me = request.user
    # Get all users and their relationships
    users = User.objects.all()
    relationships = Relationship.objects.all().order_by(
        Case(
            When(user__id=me.id, then=Value(0)),
            When(friend__id=me.id, then=Value(0)),
            default=Value(1),
            output_field=IntegerField(),
        )
    )
    net.add_node(me.id, label="Me", color="rgba(255, 99, 71, 1)")
    users = users.exclude(id=me.id)
    
    if me.is_superuser:
        # Add nodes for users
        for user in users:
            net.add_node(user.id, label=user.username, color="rgba(84, 99, 71, 0.1)")

        # Add edges for relationships
        for relation in relationships:
            net.add_edge(relation.user.id, relation.friend.id)
    else:
        nodes = [me.id] + [user.id for user in users]
        labels = ['Me'] + [user.username if user.privatesetting.display_name_on_network else '' for user in users]
        colors = [[255, 99, 71, 1]] + [[84, 99, 71, 0.1] for user in users]
        print(nodes)
        # edges = {(relation.user.id, relation.user.username, relation.friend.id, relation.friend.username) for relation in relationships}
        # source, local_relationships = find_nodes_within_distance({(user.id, user.username)}, set(), edges, 2)        
        for relation in relationships:
            user = relation.user
            user_index = nodes.index(user.id)
            user_rgba = colors[user_index]
            friend = relation.friend
            friend_index = nodes.index(friend.id)
            friend_rgba = colors[friend_index]
            if user.id==me.id:
                friend_rgba[3] = (1+friend_rgba[3])/2
                colors[friend_index] = friend_rgba
            elif friend.id==me.id:
                user_rgba[3] = (1+user_rgba[3])/2
                colors[user_index] = user_rgba
            elif user_rgba[3]>0.1 and friend_rgba[3]>0.1:
                friend_rgba[3] = (1+friend_rgba[3])/2
                colors[friend_index] = friend_rgba
                user_rgba[3] = (1+user_rgba[3])/2
                colors[user_index] = user_rgba
            else:
                pass
        colors = [rgba_list_to_string(c) for c in colors]
        print(colors)
        net.add_nodes(
            nodes,
            label=labels,
            color=colors
        )
        [net.add_edge(relation.user.id, relation.friend.id) for relation in relationships]

    # Generate the HTML for the network
    network_html = net.generate_html()
    network_html = clean_network_html(network_html, ['bootstrap'])
    return render(request, 'includes/graph.html', {'network': network_html})

def network(request):
    return render(request, 'network.html')

def home(request):
    return render(request, 'home.html')

def search_users(request):
    query = request.GET.get('search', '')
    user=request.user
    # Perform the search based on the query.
    print(query)
    print(';')
    results = User.objects.filter(Q(username__icontains=query) | Q(first_name__icontains=query) | Q(last_name__icontains=query) | Q(nick_name__icontains=query) | Q(email__icontains=query)).exclude(id=user.id)
    request_has_sent = list()
    friends = list()
    for result in results:
        friend_request = FriendRequest.objects.filter(sender=user.id, receiver=result.id).first()
        if friend_request and friend_request.status!=None:
            request_has_sent.append(result)

    return render(
            request, 
            'search_results.html', 
            {
                'results': results, 
                'query': query, 
                'request_has_sent': request_has_sent,
                })

def send_friend_request(request, user_id):
    if request.method=='POST':
        try:
            sender = request.user
            receiver = User.objects.get(id=user_id)
            # Check if a friend request already exists
            friend_request, created = FriendRequest.objects.get_or_create(
                sender=sender, receiver=receiver
            )
            if not created:
                friend_request.status='pending'

                # check if the sender is in block list
                if not friend_request.block_sender:
                    notify.send(
                        sender, 
                        recipient=receiver, 
                        verb=NotificationVerbs.following,
                        description=f'{sender} send you a {NotificationVerbs.following.label}',
                        action_object=friend_request
                        )
            friend_request.save()
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
        if friend_request.status=='pending':
            friend_request.status = NotificationVerbs.confirm  # Change status to "confirm"
            friend_request.save()  # Save the updated FriendRequest
            Relationship.objects.create(
                user=friend_request.sender,
                friend=request.user,
            )
            # check if sender is in block list, otherwise, send notify
            if not friend_request.block_sender:
                notify.send(
                    request.user,
                    recipient=friend_request.sender,
                    verb=NotificationVerbs.confirm,
                    description=f'{friend_request.sender} {NotificationVerbs.confirm} your friend_request')
            response_data = {'messages': 'confirm request successfully'}
        else:
            response_data = {'messages': 'Is confirmed already or the sender retreat this friend request'}
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
    # Set initial values
    user = request.user
    block_user = user_id
    # Read notification
    try:
        user.notifications.unread().mark_as_read()
    except:
        pass
    # find friend request
    friend_request = FriendRequest.objects.filter(
                sender=block_user, receiver=user
            ).first()
    if not friend_request:
        # create a FriendRequest obj and set block_sender=True
        friend_request =FriendRequest(sender=block_user, receiver=user, status=None, block_sender=True)
    else:
        # set block_sender attr False if block_sender is True else set True
        friend_request.block_sender = False if friend_request.block_sender else True

def mark_all_as_read(request):
    request.user.notifications.mark_all_as_read()
    return JsonResponse({'message': 'mark all notification as read'})

def notifications(request):
    return render(request, 'notifications.html')
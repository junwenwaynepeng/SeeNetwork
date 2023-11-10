from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from accounts.models import CustomUser as User
from django.db.models import Q
from .models import Relationship, FriendRequest, Relation
from notifications.signals import notify
from django.db.models.signals import post_save
from django.contrib import messages
from pyvis.network import Network
import networkx

# Create your views here.


def home(request):
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

    # Generate the HTML for the network
    net.from_nx(G)
    return render(request, 'home.html', {'network_html': net.generate_html()})

def search_users(request):
    query = request.GET.get('q', '')
    
    # Perform the search based on the query.
    results = User.objects.filter(Q(username__icontains=query) | Q(first_name__icontains=query) | Q(email__icontains=query))
    return render(request, 'home.html', {'results': results, 'query': query, 'choices': Relation.choices})

def send_friend_request(request, user_id):
    if request.method == 'POST':
        # Get the selected relationship type from the form
        relationship_type = request.POST.get('relationship')

        if relationship_type:
            # Create a friend request with the selected relationship type
            try:
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
                    notify.send(sender, recipient=receiver, verb=f'{sender} send you a {relationship_type} confirm request')
            except:
            	pass
    return redirect('home')

def confirm_request(request, notification_id):
    notification = request.user.notifications.get(id=notification_id)	
    notification.mark_as_read()	
    # Check if the notification is a friend request
    # Update the notification to "read"


    # Create a relationship using the instance of FriendRequest
    friend_request = FriendRequest.objects.get(id=notification.target.id)
    friend_request.status = 'confirm'  # Change status to "confirm"
    friend_request.save()  # Save the updated FriendRequest
    Relationship.objects.create(
        user=request.user,
        friend=friend_request.sender,
        relationship_type=friend_request.relationship_type,
    )


    # Display a success message
    messages.success(request, 'Friend request confirmed.')

    return redirect('home')  # Redirect to the desired page after confirmation







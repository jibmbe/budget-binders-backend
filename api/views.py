import json
from django.shortcuts import render,redirect

# Create your views here.
from rest_framework import viewsets
from .models import Book
from .serializers import BookSerializer
from .forms import RegistrationForm
from django.contrib.auth.decorators import login_required
from .models import Product, Purchase
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.core.paginator import Paginator

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()  # Save the user data
            return redirect('login')  # Redirect to login page
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

def profile(request):
    if request.user.is_authenticated:
        purchases = Purchase.objects.filter(user=request.user)
        return render(request, 'profile.html', {'user': request.user, 'purchases': purchases})
    else:
        return redirect('login')


@login_required
def purchase_product(request, product_id):
    product = Product.objects.get(id=product_id)
    if request.method == 'POST':
        # You can add logic to handle quantity and price here
        Purchase.objects.create(
            user=request.user,
            product=product,
            quantity=1,  # You can extend to take quantity from a form
        )
        return redirect('profile')  # After purchase, go back to profile
    return render(request, 'product_detail.html', {'product': product})


@csrf_exempt
def register_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')

            if not email or not password:
                return JsonResponse({'success': False, 'message': 'Email and password are required'}, status=400)

            # Create a new user
            user = User.objects.create_user(username=email, email=email, password=password)
            return JsonResponse({'success': True, 'message': 'User registered successfully'}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON'}, status=400)
    else:
        return JsonResponse({'success': False, 'message': 'Invalid method'}, status=405)
    
@csrf_exempt  # You may need this if you're using POST requests from non-Django clients like React
def login_view(request):
    if request.method == 'POST':
        try:
            # Parse the incoming JSON data
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')

            # Authenticate user
            user = authenticate(request, username=email, password=password)

            if user is not None:
                login(request, user)
                return JsonResponse({'success': True}, status=200)  # Respond with success message
            else:
                return JsonResponse({'success': False, 'message': 'Invalid credentials'}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON'}, status=400)
    else:
        return JsonResponse({'success': False, 'message': 'Invalid method'}, status=405)
    

def users_view(request):
    users = User.objects.all()  # Get all users from the database
    paginator = Paginator(users, 10)  # Show 10 users per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    users_data = [{'id': user.id, 'username': user.username, 'email': user.email} for user in page_obj]

    return JsonResponse({'users': users_data, 'total_pages': paginator.num_pages})
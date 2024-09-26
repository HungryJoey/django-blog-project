from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.utils import timezone
from .forms import ContactForm
from .models import ContactSubmission
from django.contrib import messages
from django.core.mail import send_mail
from .models import BlogPost, Profile
from .forms import BlogPostForm
from .forms import UserRegistrationForm, UserForm, ProfileForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserChangeForm
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .serializers import BlogPostSerializer
import random



def home(request):
    current_time = datetime.now()
    
    quotes = [
        "The best way to predict the future is to create it. - Peter Drucker",
        "Code is like humor. When you have to explain it, it's bad. - Cory House",
        "First, solve the problem. Then, write the code. - John Johnson",
        "The only way to learn a new programming language is by writing programs in it. - Dennis Ritchie",
        "The most disastrous thing that you can ever learn is your first programming language. - Alan Kay"
    ]
    random_quote = random.choice(quotes)
    
    context = {
        'current_time': current_time,
        'random_quote': random_quote
    }
    return render(request, 'index.html', context)

def about(request):
    return render(request, 'about.html')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            
            # Here you would typically send an email
            # For now, we'll just print the data
            print(f"Received message from {name} ({email}): {message}")
            
            messages.success(request, 'Your message has been sent!')
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})

def post_list(request):
    posts = BlogPost.objects.filter(published_date__isnull=False).order_by('-published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def post_new(request):
    if request.method == "POST":
        form = BlogPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.publish()
            return redirect('post_detail', pk=post.pk)
    else:
        form = BlogPostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if request.method == "POST":
        form = BlogPostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.publish()
            return redirect('post_detail', pk=post.pk)
    else:
        form = BlogPostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

def post_delete(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    post.delete()
    return redirect('post_list')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect('home')
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = UserRegistrationForm()
    return render(request, 'registration/register.html', {"form": form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect('home')
            else:
                messages.error(request,"Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.")
    form = AuthenticationForm()
    return render(request, 'registration/login.html', {"form": form})

def logout_view(request):
    logout(request)
    messages.info(request, "You have successfully logged out.") 
    return redirect('home')

@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

@login_required
def my_blog_posts(request):
    posts = BlogPost.objects.filter(author=request.user).order_by('-created_date')
    return render(request, 'myapp/my_posts.html', {'posts': posts})

class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all().order_by('-created_date')
    serializer_class = BlogPostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

def spa_view(request):
    return render(request, 'spa.html')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Save form data to the database
            ContactSubmission.objects.create(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                message=form.cleaned_data['message']
            )
            messages.success(request, 'Your message has been sent!')
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})

def view_submissions(request):
    submissions = ContactSubmission.objects.all().order_by('-submitted_at')
    return render(request, 'submissions.html', {'submissions': submissions})

def post_list(request):
    posts = BlogPost.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render

from .models import Post


def home(request):
	posts = Post.objects.select_related('author').order_by('-created_at')
	return render(request, 'home.html', {'posts': posts})


def login_view(request):
	if request.user.is_authenticated:
		return redirect('home')

	error = ''
	if request.method == 'POST':
		username = request.POST.get('username', '').strip()
		password = request.POST.get('password', '')
		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			next_page = request.GET.get('next') or request.POST.get('next') or 'home'
			return redirect(next_page)

		error = 'Invalid username or password.'

	return render(request, 'login.html', {'error': error})


def signup(request):
	error = ''
	if request.method == 'POST':
		username = request.POST.get('username', '').strip()
		email = request.POST.get('email', '').strip()
		password = request.POST.get('password', '')

		if not username or not email or not password:
			error = 'All fields are required.'
		elif User.objects.filter(username=username).exists():
			error = 'Username already exists.'
		else:
			User.objects.create_user(username=username, email=email, password=password)
			messages.success(request, 'Account created successfully. Please log in.')
			return redirect('login')

	return render(request, 'signup.html', {'error': error})


@login_required(login_url='login')
def create_post(request):
	error = ''
	if request.method == 'POST':
		title = request.POST.get('title', '').strip()
		content = request.POST.get('content', '').strip()
		image = request.FILES.get('image')

		if not title or not content:
			error = 'Title and content are required.'
		else:
			Post.objects.create(
				title=title,
				content=content,
				image=image,
				author=request.user,
			)
			messages.success(request, 'Post created successfully.')
			return redirect('home')

	return render(request, 'create_post.html', {'error': error})


def detail(request, id):
	post = get_object_or_404(Post, id=id)
	return render(request, 'detail.html', {'post': post})

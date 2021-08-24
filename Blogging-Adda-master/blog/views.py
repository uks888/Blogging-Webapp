from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

"""def home(request):
	context = {
		'posts' : Post.objects.all()
	}
	return render (request, 'blog/home.html', context)"""

class PostListView(ListView):
	model = Post
	template_name = 'blog/home.html'   # <app>/<model>_<viewtype>.html
	context_object_name = 'posts'
	ordering = ['-date_posted']		   # Date Posted ko Latest to Oldest m arrange kar dega
	paginate_by = 4					   # 4 posts per page ke hisab se paging kar raha hai

class UserPostListView(ListView):
	model = Post
	template_name = 'blog/user_posts.html'   # <app>/<model>_<viewtype>.html
	context_object_name = 'posts'
	paginate_by = 4			

	def get_queryset(self):
		user = get_object_or_404(User, username=self.kwargs.get('username'))		# Agar user exist nahi karega to error 404 aayega, or agar user exist kiya 
                                                                                  	# to wo "user" variable m store ho jayega, wo ki url se aayega
		return Post.objects.filter(author=user).order_by('-date_posted')			# Jo bhi author url se aayega uske posts ko paging ke sath limit kar rahe hai

class PostDetailView(DetailView):
	model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
	model = Post
	fields = ['title', 'content']

	def form_valid(self, form):					   	  # Blog likhne ke liye author jaruri hai to 
		form.instance.author = self.request.user	  # usi ko check karega
		return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Post
	fields = ['title', 'content']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

	def test_func(self):			  # Blog ka author hi update kar rha hai ya nahi, check karega
		post = self.get_object()	  # jo post ko udate karna chahte hai wo aa jayega aise m
		if self.request.user == post.author: 	# check karega if, access karne wala == author
			return True
		return False 

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Post			          # Similar to DetailView
	success_url = '/'				  # Post delete hone ke baad Home page m chala jayega

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False

def about(request):
	return render (request, 'blog/about.html', {'title' : 'About'})

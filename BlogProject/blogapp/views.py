from django.shortcuts import render, get_object_or_404
from .models import Post
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
# Create your views here.

def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blogapp/home.html', context)

class PostListView(ListView):
    model = Post
    template_name = "blogapp/home.html" #default=> <app>/<model>_<viewtype>.html
    context_object_name = "posts"
    ordering = ['-date_posted']
    paginate_by = 5

class UserPostListView(ListView):
    model = Post
    template_name = "blogapp/user_posts.html" #default=> <app>/<model>_<viewtype>.html
    context_object_name = "posts"
    ordering = ['-date_posted']
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username = self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

class PostDetailView(DetailView):
    model = Post
    #default template_name=> <app>/<model>_<viewtype>.html i.e. postapp/post_detail.html
    #default context_object_name = "object"

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title','content']
    #default template_name=> <app>/<model>_<form> i.e. postapp/post_form

    def form_valid(self,form): # for integrity error
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title','content']
    #default template_name=> <app>/<model>_<form> i.e. postapp/post_form

    def form_valid(self,form): # for integrity error
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self): #for update only current user posts not others
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = "/"

    def test_func(self): #for deleting only current user posts not others
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'blogapp/about.html', {'title': 'About'})

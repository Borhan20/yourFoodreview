from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (ListView,
                                  DetailView,
                                  CreateView,
                                  UpdateView,
                                  DeleteView
                                  )
from .models import Post
from django.db.models import Q
from django.urls import reverse
from django.http import HttpResponseRedirect



from django.core import serializers
from django.http import JsonResponse
from .models import Like

def like_post(request,pk):
    if request.method == 'POST':

        post_id = request.POST.get('post_id')
        user_id = request.POST.get('user_id')
        like = Like.objects.create(user_id=user_id, post_id=post_id)
        
        return HttpResponseRedirect(reverse('post-detail', args=[str(pk)]))

# Create your views here.

# posts = [
#     {
#         'author':'Borhan420',
#         'title': 'Blog Post1',
#         'content':'First Post content',
#         'date_posted':'March 27 2023'
#     },
#     {
#         'author':'Borhan420',
#         'title': 'Blog Post2',
#         'content':'Second post content',
#         'date_posted':'August March 28 2023'
#     }
# ]

def home(request):
    context = {
        'posts':Post.objects.all()
    }
    return render(request,'blog/home.html',context)

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    #<app>/<model>_<viewtype>.html
    context_object_name = 'posts' 
    ordering = ['-date_posted']
    paginate_by = 5

    
    

    # def get_context_data(self, **kwargs):
    #     context = super(PostListView, self).get_context_data(**kwargs)
    #     for post in context['posts']:
            
            
        
    #     return context

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            object_list = self.model.objects.filter(Q(title__icontains=query) | Q(content__icontains = query)).order_by('-date_posted')
        else:
            object_list = self.model.objects.filter().order_by('-date_posted')
        return object_list

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    #<app>/<model>_<viewtype>.html
    context_object_name = 'posts' 
    
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User,username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')



class PostDetailView(DetailView):
    model = Post
    #template_name = 'blog/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        liked_posts = []
        if self.request.user.is_authenticated:
            liked_posts = [like.post.id for like in Like.objects.filter(user=self.request.user)]
        context['liked_posts'] = liked_posts
        return context
    
class PostCreateView(LoginRequiredMixin,CreateView):
    model = Post
    fields = ['title','content','post_images']

    
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        post = form.save(commit=False)
        post.save()
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Post
    fields = ['title','content','post_images']
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Post
    success_url = '/'
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False




def about(request):
    return render(request,'blog/about.html',{'title':'About'})


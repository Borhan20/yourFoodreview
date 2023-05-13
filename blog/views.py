from django.shortcuts import render, get_object_or_404,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (ListView,
                                  DetailView,
                                  CreateView,
                                  UpdateView,
                                  DeleteView,
                                  FormView
                                  )
from .models import Post,About
from django.db.models import Q
from django.urls import reverse
from django.http import HttpResponseRedirect




from django.core import serializers
from django.http import JsonResponse
from .models import Like,Comment
from .forms import CommentForm


# def add_comment(request,pk):
    
    
#     post = get_object_or_404(Post, pk=pk)
    
#     if request.method == 'POST':
        
#         comment_form = CommentForm(data=request.POST)
#         if comment_form.is_valid():
#             new_comment = comment_form.save(commit=False)
#             new_comment.post = post
#             new_comment.save()
#             return redirect(reverse('post-detail',args=[str(pk)]))
#     else:
#         comment_form = CommentForm()
#         return render(request,'blog/comments.html',{'form':comment_form})
from django.contrib.auth.decorators import login_required   

@login_required
def like_post(request,pk):
    if request.method == 'POST':
        post = get_object_or_404(Post,pk=pk)
        post_id = request.POST.get('post_id')
        user_id = request.POST.get('user_id')
        print(post_id)
        print(user_id)
        like = Like.objects.create(user_id=user_id, post_id=post_id)
        likes_count = post.get_likes_count()

        # print(likes_count)

        data ={
            'likes_count':likes_count,
            'message':'(you have already liked it)',
        }

        return JsonResponse(data)

        #return HttpResponseRedirect(reverse('post-detail', args=[str(pk)]))

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
    #ordering = ['-date_posted']
    paginate_by = 5

    
    
    # return context
    def get_context_data(self,  **kwargs):
        posts = Post.objects.all()
        context = super().get_context_data(**kwargs)
        last_comments = [post.get_last_comment() for post in self.object_list]
        context['post_lastcomment']= zip(posts, last_comments)
        print(context)
        #context['last_comments'] = last_comments
        return context
            
            
        
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

        # return context
    def get_context_data(self,  **kwargs):
        posts = Post.objects.all()
        context = super().get_context_data(**kwargs)
        last_comments = [post.get_last_comment() for post in self.object_list]
        context['post_lastcomment']= zip(posts, last_comments)
        print(context)
        #context['last_comments'] = last_comments
        return context

    def get_queryset(self):
        user = get_object_or_404(User,username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')



class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        liked_posts = []
        if self.request.user.is_authenticated:
            liked_posts = [like.post.id for like in Like.objects.filter(user=self.request.user)]
        context['liked_posts'] = liked_posts
        context['comments'] = Comment.objects.filter(post=self.get_object(),parent = None)
        #context['replies'] = Comment.objects.filter(post=self.get_object()).exclude(parent=None)
        context['form'] = CommentForm()
        return context
    
    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.get_object()
            comment.user = self.request.user
            comment.save()
           
            url = reverse('reply_comment', args=[comment.id])
            
            data = {
                'bool': True,
                'user': comment.user.username,
                'body': comment.body,
                'date_added': comment.date_added.strftime('%b %d, %Y %I:%M %p'),
                'reply_url':url,
            }
            return JsonResponse(data)
            
            
            
            # return redirect('post-detail', pk=self.get_object().pk)
        
        else:

            # return JsonResponse({'message': 'Invalid request.'}, status=400)
            context = self.get_context_data(**kwargs)
            context['form'] = form
            return self.render_to_response(context)


     
                
    

    


class ReplyCommentView(FormView):
    form_class = CommentForm
    template_name = 'blog/reply_comment.html'

    def form_valid(self, form):
        parent_comment = get_object_or_404(Comment, pk=self.kwargs['pk'])
        comment = form.save(commit=False)
        comment.post = parent_comment.post
        comment.parent = parent_comment
        comment.user = self.request.user
        comment.save()
        return redirect('post-detail', pk=parent_comment.post.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['parent_comment'] = get_object_or_404(Comment, pk=self.kwargs['pk'])
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
    print(About.objects.first())
    return render(request,'blog/about.html',{'about_text':About.objects.first()})


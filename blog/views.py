from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from blog.models import Post, Comment
from django.utils import timezone
from blog.forms import PostForm, CommentForm

from django.views.generic import (TemplateView,ListView,
                                  DetailView,CreateView,
                                  UpdateView,DeleteView, FormView)

from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.db.models import F


class RegisterPage(FormView): #FormView is used to display the below defined view
    #cusomizing basic registration page
    template_name = './registration/register.html'
    form_class = UserCreationForm #UserCreationForm is the structure of registration form
    redirect_authenticated_user = True
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('post_list')
        return super(RegisterPage, self).get(*args, **kwargs)

class AboutView(LoginRequiredMixin, TemplateView):
    login_url = 'login'
    redirect_field_name = 'blog/post_list.html'

    template_name = 'about.html'

class PostListView(ListView):
    model = Post
    
    # running query to get all the post objects less than current timestamp ordered most recent to least
    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-claps')

class AuthorsListView(ListView):
    model = Post
    template_name = 'blog/post_authors_list.html'
    
    # running query to get all the post objects less than current timestamp ordered most recent to least
    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

class RecentListView(ListView):
    model = Post
    template_name = 'blog/post_recent_list.html'

    # running query to get all the post objects less than current timestamp ordered most recent to least
    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

class DraftListView(LoginRequiredMixin, ListView):
    login_url = 'login'
    redirect_field_name = 'blog/post_list.html'
    model = Post
    template_name = 'blog/post_draft_list.html'

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True, author = self.request.user).order_by('created_date')

class PostDetailView(LoginRequiredMixin, DetailView):
    login_url = 'login'
    redirect_field_name = 'blog/post_detail.html'

    model = Post


class CreatePostView(LoginRequiredMixin, CreateView):
    login_url = 'login'
    redirect_field_name = 'blog/post_detail.html'
    
    form_class = PostForm
    model = Post

    def post(self, request, *args, **kwargs):
        #getting post data from request
        form_title, form_text = request.POST.get("title", ""), request.POST.get("text", "")
        
        #creating 
        new_post = Post(author = request.user, title = form_title, text = form_text)
        new_post.save()
        return redirect('post_detail', pk = new_post.pk)




class PostUpdateView(LoginRequiredMixin, UpdateView):
    login_url = 'login'
    redirect_field_name = 'blog/post_detail.html'
    
    form_class = PostForm
    
    model = Post

    def post(self, request, *args, **kwargs):
        #getting post data from request
        form_title, form_text = request.POST.get("title", ""), request.POST.get("text", "")
        
        #updating 
        update_post = Post.objects.get(author = request.user, title = form_title)
        update_post.published_date = None
        update_post.text = form_text
        update_post.save()
        return redirect('post_detail', pk = update_post.pk)


class PostDeleteView(LoginRequiredMixin,DeleteView):
    model = Post
    #reverse_lazy() waits until the object is deleted from the model and then it redirects.
    success_url = reverse_lazy('post_list')

#######################################
## Functions that require a pk match ##
#######################################

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)

@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/comment_form.html', {'form': form})


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def add_clap_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    Post.objects.filter(title=post.title).update(claps=F('claps') + 1)
    return redirect('post_detail', pk=post.pk)


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail', pk=post_pk)

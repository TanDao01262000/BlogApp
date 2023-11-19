from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm, PostForm, ProfileUpdateForm
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from .models import Post, Like, Comment, CustomUser
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.db.models import Q
# Create your views here.

# Auth Views
def loginview(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username,password)
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('homeview')
        else:
            messages.error(request, 'Invalid credential')
    context = {}
    return render(request, template_name='main_app/login.html',context=context)


def logoutview(request):
    logout(request)
    return redirect('loginview')


def signupview(request):
    form = UserRegisterForm()

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {user}!')
            return redirect('loginview')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'Error in {field}: {error}')

    context = {'form': form}
    return render(request, 'main_app/signup.html', context)

# End Auth View

# User Profile CRUD View
@login_required
def profile_view(request, pk):
    custom_user = CustomUser.objects.get(id=pk)
    post_count = Post.objects.filter(author=custom_user).count()
    like_count = Like.objects.filter(user=custom_user).count()
    comment_count = Comment.objects.filter(user=custom_user).count()
    context ={
        'custom_user':custom_user,
        'post_count':post_count,
        'like_count':like_count,
        'comment_count':comment_count,
    }
    return render(request, 'main_app/profile.html', context=context)


@login_required
def update_profile(request, pk):
    if pk == request.user.id:

        cur_user_profile = {
            'bio': request.user.profile.bio,
            'linkedin_link': request.user.profile.linkedin_link,
        }

        if request.method == "POST":
            profile_update_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
            if profile_update_form.is_valid():
                profile = profile_update_form.save(commit=False)
                profile.user = request.user
                profile.save()
                messages.success(request, f'Profile updated successfully')
                return redirect('profileview', pk=request.user.id)
        else:
            profile_update_form = ProfileUpdateForm(initial=cur_user_profile)
        context = {
            'profile_update_form': profile_update_form,
        }
        return render(request, 'main_app/update.html', context=context)
    else:
        return render(request, 'main_app/error.html')
    
# End Profile Views 


def homeview(request):
    return render(request, 'main_app/home.html')


# CRUD operations for Post
class PostListView(ListView):
    context_object_name = 'posts'
    model = Post
    template_name = 'main_app/postlist.html'
    ordering = ['-published_date']


class PostDetailView(LoginRequiredMixin, DetailView):
    context_object_name = 'post'
    model = Post
    template_name = 'main_app/postdetail.html'


class AddPostView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'main_app/addpost.html'
    context_object_name = 'post'
    # fields = ['title', 'content']

    def form_valid(self, form):
        print(form.cleaned_data)
        form.instance.author = self.request.user
        return super().form_valid(form)
    
class UpdatePostView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'main_app/addpost.html'
    context_object_name = 'post'
    # fields = ['title', 'content']

    def form_valid(self, form):
        print(form.cleaned_data['title'])
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        return True if self.request.user == post.author else False
    
class DeletePostView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'main_app/deletepost.html'
    context_object_name = 'post'

    success_url = "/blog"
    
    def test_func(self):
        post = self.get_object()
        return True if self.request.user == post.author else False

# End Post CRUD

# Search
def search(request):
    query = request.GET.get('q')
    if query:
        results = Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query))

        if results:
            return render(request, 'main_app/search.html', {'results': results})

    return render(request, 'main_app/not_found_page.html')

# Add Comment View
@login_required
def add_comment_like(request, pk):
    if request.method == 'POST' :
        print(request.POST)
        if 'comment_button' in request.POST:
            post = get_object_or_404(Post, id=pk)
            comment_text = request.POST.get('comment_text')
            Comment.objects.create(post=post,user=request.user, content=comment_text)
            messages.success(request, 'Added Comment Successfully')

        elif 'like_button' in request.POST:
            post_obj = get_object_or_404(Post, id=pk)
            like_obj = Like.objects.filter(post=post_obj, user=request.user).first()
            if like_obj:
                like_obj.delete()
                messages.success(request, 'Like Removed')
            else:
                Like.objects.create(post=post_obj, user=request.user)
                messages.success(request, 'Like Successfully')
    
    return redirect('postdetailview', pk)
            
        






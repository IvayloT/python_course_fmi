from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category, Comment, Profile
from .forms import PostForm, EditForm, CommentForm, ProfileForm, ImportPostForm
from django.urls import reverse_lazy
from django.core.files.uploadedfile import UploadedFile
from .utils import determine_file_type

class Home(ListView):
    model = Post
    template_name = 'home.html'
    ordering = ['-created_at']

    def get_context_data(self, *args, **kwargs):
        categories = Category.objects.all()
        context = super(Home, self).get_context_data(*args, **kwargs)
        context["categories"] = categories
        return context

def CategoryView(request, pk):
    category_posts = Post.objects.filter(category=pk)
    category = Category.objects.get(pk=pk)
    categories = Category.objects.all()
    return render(request, 'category/show.html', { 'cats': category.name.title(), 'category_posts': category_posts, 'categories': categories})

class PostDetail(DetailView):
    model = Post
    template_name = 'post/details.html'

class CreatePost(CreateView):
    model = Post
    template_name = 'post/create.html'
    form_class = PostForm
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(CreatePost, self).form_valid(form)

class CreateCategory(CreateView):
    model = Category
    template_name = 'category/create.html'
    fields = '__all__'

class EditPost(UpdateView):
    model = Post
    template_name = 'post/edit.html'
    form_class = EditForm

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.kwargs['pk']})

class DeletePost(DeleteView):
    model = Post
    template_name = 'post/delete.html'
    success_url = reverse_lazy('home')

class CreateComment(CreateView):
    model = Comment
    template_name = 'comment/create.html'
    form_class = CommentForm

    def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']
        form.instance.name = self.request.user.first_name
        return super(CreateComment, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.kwargs['pk']})


class EditComment(UpdateView):
    model = Comment
    template_name = 'comment/edit.html'
    fields = ['body']

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.object.post.id})

class DeleteComment(DeleteView):
    model = Comment
    template_name = 'comment/delete.html'

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.object.post.id})

class EditProfile(UpdateView):
    model = Profile
    template_name = 'profile/edit.html'
    form_class = ProfileForm
    success_url = reverse_lazy('home')

class CreateProfile(CreateView):
    model = Profile
    template_name = 'profile/create.html'
    form_class = ProfileForm
    success_url = reverse_lazy('home')
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CreateProfile, self).form_valid(form)

class ImportPost(CreateView):
    model = Post
    template_name = 'post/import.html'
    form_class = ImportPostForm
    def form_valid(self, form):
        file = self.request.FILES['import_post']
        form.instance.body = determine_file_type(file)
        form.instance.author = self.request.user
        return super(ImportPost, self).form_valid(form)

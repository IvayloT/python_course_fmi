from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category
from .forms import PostForm, EditForm
from django.urls import reverse_lazy


class Home(ListView):
    model = Post
    template_name = 'home.html'
    ordering = ['-created_at']

    def get_context_data(self, *args, **kwargs):
        context = super(Home, self).get_context_data(*args, *kwargs)
        context["categories"] = Category.objects.all()
        return context

def CategoryView(request, pk):
    category_posts = Post.objects.filter(category=pk)
    category = Category.objects.get(pk=pk)
    return render(request, 'category/show.html', { 'cats': category.name.title(), 'category_posts': category_posts })

class PostDetail(DetailView):
    model = Post
    template_name = 'post/details.html'

class CreatePost(CreateView):
    model = Category
    template_name = 'post/create.html'
    form_class = PostForm

class CreateCategory(CreateView):
    model = Category
    template_name = 'category/create.html'
    fields = '__all__'

class EditPost(UpdateView):
    model = Post
    template_name = 'post/edit.html'
    form_class = EditForm

class DeletePost(DeleteView):
    model = Post
    template_name = 'post/delete.html'
    success_url = reverse_lazy('home')

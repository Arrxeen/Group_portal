from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, ListView, DeleteView, UpdateView, DetailView, View
from .forms import PostForm, CommentForm, PostFilterForm, CategoryForm
from .models import Post, Comment, Like, Dislike, Category
from django.urls import reverse_lazy, reverse
from .mixin import UserIsOwnerMixin
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin
)
from django.http import HttpResponseRedirect


class PostCreateViews(CreateView):
    model = Post
    form_class = PostForm

    def get_success_url(self):
        category_id = self.object.category_id
        return reverse_lazy('post-list', kwargs={'category_id': category_id})

    def form_valid(self, form):
        form.instance.creater = self.request.user
        return super().form_valid(form)

class PostDetailViews(DetailView):
    model = Post
    context_object_name = 'post'

    def form_valid(self, form):
        form.instance.creater = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["coment_form"] = CommentForm()
        return context
    
    def post(self, request, *args, **kwargs):
        coment_form = CommentForm(request.POST, request.FILES)
        if coment_form.is_valid():
            comment = coment_form.save(commit=False)
            comment.author = request.user
            comment.psot_id = self.get_object()
            comment.save()
            return redirect('post-detail', pk=comment.psot_id.pk)

class PostListViews(ListView):
    model = Post
    context_object_name = 'posts'
    paginate_by = 11
    
    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        if category_id:
            queryset = Post.objects.filter(category_id=category_id)
        else:
            queryset = Post.objects.all()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = PostFilterForm(self.request.GET)
        context["category"] = Category.objects.get(id=self.kwargs.get('category_id'))
        return context


class PostUpdateView(LoginRequiredMixin,UserIsOwnerMixin,UpdateView):
    model = Post
    form_class = PostForm

    def get_success_url(self):
        return super().get_success_url()

class TaskDeliteView(LoginRequiredMixin,UserIsOwnerMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('post-list')
    template_name = "forum/post_delete.html"


class PostLikeToggel(LoginRequiredMixin,View):
    def post(self, request, *args, **kwargs):
        comment = get_object_or_404(Post, pk=self.kwargs.get("pk"))
        likeq = Like.objects.filter(comment = comment, user = request.user)
        dislikeq = Dislike.objects.filter(comment = comment, user = request.user)
        if dislikeq.exists():
            dislikeq.delete()
            if not likeq.exists():
                Like.objects.create(comment = comment, user = request.user)
        else:
            if likeq.exists():
                likeq.delete()
            else:
                Like.objects.create(comment = comment, user = request.user)
        return HttpResponseRedirect(comment.get_absolute_url())


class PostDislikeToggel(LoginRequiredMixin,View):
    def post(self, request, *args, **kwargs):
        comment = get_object_or_404(Post, pk=self.kwargs.get("pk"))
        dislikeq = Dislike.objects.filter(comment = comment, user = request.user)
        likeq = Like.objects.filter(comment = comment, user = request.user)
        if likeq.exists():
            likeq.delete()
            if not dislikeq.exists():
                Dislike.objects.create(comment = comment, user = request.user)
        else:
            if dislikeq.exists():
                dislikeq.delete()
            else:
                Dislike.objects.create(comment = comment, user = request.user)
        return HttpResponseRedirect(comment.get_absolute_url())

class CategoryListView(ListView):
    model = Category
    context_object_name = 'categories'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

class CategoryCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    permission_required = 'forum.category_create'
    success_url = reverse_lazy('categories')

    def form_valid(self, form):
        return super().form_valid(form)
    
class CategoryUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    permission_required = 'forum.category_create'

    def get_success_url(self):
        return reverse_lazy('categories')

class CategoryDeleteView(LoginRequiredMixin,PermissionRequiredMixin, DeleteView):
    model = Category
    success_url = reverse_lazy('categories')
    permission_required = 'forum.category_create'
    template_name = "forum/category_delete.html"

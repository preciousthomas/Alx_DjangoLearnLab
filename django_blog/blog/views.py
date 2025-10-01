from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Auto-login after successful registration
            messages.success(request, 'Your account has been created successfully!')
            return redirect('profile')
    else:
        form = UserRegisterForm()
    return render(request, 'blog/register.html', {'form': form})
# blog/views.py (append only)

from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from .forms import PostForm


class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-published_date']
    paginate_by = 10


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.object.pk})


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.object.pk})


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog:post_list')
# inside PostDetailView class (append method)
from .forms import CommentForm
def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['comment_form'] = CommentForm()
    return context

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user
    # blog/views.py (append)

from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse

from .models import Post, Comment
from .forms import CommentForm

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.post = get_object_or_404(Post, pk=kwargs.get('post_pk'))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.post
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.post.pk})


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'

    def test_func(self):
        comment = self.get_object()
        return comment.author == self.request.user

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.get_object().post.pk})


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'

    def test_func(self):
        comment = self.get_object()
        return comment.author == self.request.user

    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.get_object().
                                                        # Append to blog/views.py

from django.views.generic import ListView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.db.models import Q

from .models import Tag, PostTag, Post
from .forms import ManageTagsForm

# 1) List all tags
class TagListView(ListView):
    model = Tag
    template_name = 'blog/tag_list.html'
    context_object_name = 'tags'


# 2) Posts by tag
class PostsByTagView(ListView):
    model = Post
    template_name = 'blog/posts_by_tag.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        tag_slug = self.kwargs.get('tag_slug')
        tag = get_object_or_404(Tag, slug=tag_slug)
        # follow relation: PostTag -> Tag
        post_ids = PostTag.objects.filter(tag=tag).values_list('post_id', flat=True)
        return Post.objects.filter(id__in=post_ids).order_by('-published_date')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['tag'] = get_object_or_404(Tag, slug=self.kwargs.get('tag_slug'))
        return ctx


# 3) Manage tags for a post (add/remove). Authenticated users only; author-only allowed
class ManagePostTagsView(LoginRequiredMixin, UserPassesTestMixin, FormView):
    form_class = ManageTagsForm
    template_name = 'blog/manage_tags.html'

    def dispatch(self, request, *args, **kwargs):
        self.post = get_object_or_404(Post, pk=kwargs.get('pk'))
        return super().dispatch(request, *args, **kwargs)

    def test_func(self):
        # Only post author may change tags. Change to allow staff if you want.
        return self.request.user == self.post.author

    def get_initial(self):
        initial = super().get_initial()
        existing = [pt.tag.name for pt in self.post.post_tags.select_related('tag').all()]
        initial['tags'] = ", ".join(existing)
        return initial

    def form_valid(self, form):
        raw = form.cleaned_data.get('tags', '')
        names = [t.strip() for t in raw.split(',') if t.strip()]
        # create or get Tag objects
        tags = []
        for name in names:
            tag_obj, _ = Tag.objects.get_or_create(name=name)
            tags.append(tag_obj)

        # Remove existing tags not in new list
        current_tags = [pt.tag for pt in self.post.post_tags.select_related('tag').all()]
        # remove those not present
        for ct in current_tags:
            if ct.name not in [t.name for t in tags]:
                PostTag.objects.filter(post=self.post, tag=ct).delete()
        # add new tags
        for t in tags:
            PostTag.objects.get_or_create(post=self.post, tag=t)

        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse('blog:post-detail', kwargs={'pk': self.post.pk})


# 4) Search view
class PostSearchView(ListView):
    model = Post
    template_name = 'blog/search_results.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        q = self.request.GET.get('q', '').strip()
        if not q:
            return Post.objects.none()

        # Search title/content
        qs = Post.objects.filter(
            Q(title__icontains=q) |
            Q(content__icontains=q)
        ).distinct()

        # Also search tags by name and gather related posts
        tag_matches = Tag.objects.filter(name__icontains=q)
        if tag_matches.exists():
            post_ids = PostTag.objects.filter(tag__in=tag_matches).values_list('post_id', flat=True)
            qs = qs | Post.objects.filter(id__in=post_ids)

        return qs.order_by('-published_date')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['query'] = self.request.GET.get('q', '')
        return ctx
post.pk})
    from django.db.models import Q
from django.shortcuts import render
from .models import Post


def search_posts(request):
    query = request.GET.get('q')
    results = Post.objects.all()

    if query:
        results = results.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(tags__name__icontains=query)   # ✅ search inside tags
        ).distinct()

    return render(request, 'blog/search_results.html', {'results': results, 'query': query})
from django.views.generic import ListView
from .models import Post

class PostByTagListView(ListView):
    model = Post
    template_name = "blog/posts_by_tag.html"
    context_object_name = "posts"

    def get_queryset(self):
        tag_name = self.kwargs.get("tag_name")
        return Post.objects.filter(tags__name=tag_name).distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tag_name"] = self.kwargs.get("tag_name")
        return context
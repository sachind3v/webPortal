from django.shortcuts import render, get_object_or_404, redirect
from .models import Board, Post, Topic
from django.contrib.auth.models import User
from .forms import NewTopicForm, PostForm, EditForm
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.views.generic import UpdateView,ListView
from django.utils import timezone
from django.http import HttpResponseForbidden
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.

# home view for the listing of boards
class BoardListView(ListView):
    model = Board
    context_object_name = 'boards'
    template_name = 'home.html'

def home(request):
    boards = Board.objects.all()
    # dir =os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # passing board as context
    return render(request, 'home.html', {'boards': boards})


# topic view for a particular board
@login_required
def board_topics(request, pk):
    board = get_object_or_404(Board, pk=pk)
    queryset = board.topics.order_by('last_updated').annotate(replies=Count('posts') - 1)

    page = request.GET.get('page', 1)

    paginator = Paginator(queryset, 20)

    try:
        topics = paginator.page(page)
    except PageNotAnInteger:
        # fallback to the first page
        topics = paginator.page(1)
    except EmptyPage:
        # probably the user tried to add a page number
        # in the url, so we fallback to the last page
        topics = paginator.page(paginator.num_pages)
    return render(request, 'topics.html', {'board': board, 'topics': topics})


# view for creating new topic
@login_required
def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)
    user = User.objects.first()  # TODO: get the currently logged in user

    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = request.user
            topic.save()
            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=request.user
            )
            return redirect('board_topics', pk=board.pk)  # TODO: redirect to the created topic page
    else:
        form = NewTopicForm()

    return render(request, 'new_topic.html', {'board': board, 'form': form})


def topic_posts(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    topic.views += 1
    topic.save()
    return render(request, 'topic_posts.html', {'topic': topic})


@login_required
def reply_topic(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()
            topic.last_updated = timezone.now()  # <- here
            topic.save() 
            return redirect('topic_posts', pk=pk, topic_pk=topic_pk)
    else:
        form = PostForm()
    return render(request, 'reply_topic.html', {'topic': topic, 'form': form})



# this view is made by sachin
@login_required
def EditPost(request, pk, topic_pk, post_pk):
    topic=get_object_or_404(Topic,board__pk=pk,pk=topic_pk)
    post = get_object_or_404(Post, topic=topic.id, pk=post_pk)
    if not post.created_by   == request.user:
        return HttpResponseForbidden("You can't make changes to this post cause its belong to others .There will be a page for this also!")
    if request.method == 'POST':
        form = EditForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.updated_by = request.user
            post.updated_at = timezone.now()
            post.save()
            return redirect('topic_posts', pk=pk, topic_pk=topic_pk)
    else:
        form = EditForm()
    return render(request, 'edit_post.html', {'post': post, 'form': form})

# belo is bcbv for above view
# class PostUpdateView(UpdateView):
#     model = Post
#     fields = ('message', )
#     template_name = 'edit_post.html'
#     pk_url_kwarg = 'post_pk'
#     context_object_name = 'post'

#     def form_valid(self, form):
#         post = form.save(commit=False)
#         post.updated_by = self.request.user
#         post.updated_at = timezone.now()
#         post.save()
#         return redirect('topic_posts', pk=post.topic.board.pk, topic_pk=post.topic.pk)

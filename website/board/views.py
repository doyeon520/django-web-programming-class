from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView, TemplateView, FormView
from django.views.generic.dates import ArchiveIndexView, YearArchiveView, MonthArchiveView
from django.views.generic.dates import DayArchiveView,TodayArchiveView

from board.models import Post

# 댓글
from django.conf import settings

# search
from board.forms import PostSearchForm
from django.db.models import Q
from django.shortcuts import render

class PostListView(ListView):
    model = Post
    template_name = 'board/post_all.html'
    context_object_name = 'posts'
    paginate_by = 2

class PostDetailView(DetailView):
    model = Post

    # 댓글
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['disqus_short'] = f"{settings.DISQUS_SHORTNAME}"
        context['disqus_id'] = f"post-{self.object.id}-{self.object.slug}"
        context['disqus_url'] = f"{settings.DISQUS_MY_DOMAIN}{self.object.get_absolute_url()}"
        context['disqus_title'] = f"{self.object.slug}"
        return context

class PostArchiveView(ArchiveIndexView):
    model = Post
    date_field = 'modify_dt'

class PostYearArchiveView(YearArchiveView) :
    model = Post
    date_field = 'modify_dt'

class PostMonthArchiveView(MonthArchiveView):
    model = Post
    date_field = 'modify_dt'

class PostDayArchiveView(DayArchiveView):
    model = Post
    date_field = 'modify_dt'

class PostTodayArchiveView(TodayArchiveView):
    model = Post
    date_field = 'modify_dt'

#Tag View
class TagCloudTV(TemplateView):
    template_name = 'taggit/taggit_cloud.html'

class TaggedObjectLV(ListView):
    template_name = 'taggit/taggit_post_list.html'
    model= Post

    def get_queryset(self):
        return Post.objects.filter(tags__name=self.kwargs.get('tag'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tagname'] = self.kwargs['tag']
        return context

#Search Form View
class SearchFormView(FormView):
    form_class = PostSearchForm
    template_name = 'board/post_search.html'

    def form_valid(self, form):
        searchWord = form.cleaned_data['search_word']
        post_list = Post.objects.filter(Q(title__icontains=searchWord)
                                        | Q(description__icontains=searchWord)
                                        | Q(content__icontains=searchWord)).distinct()

        context = {}
        context['form'] = form
        context['search_term'] = searchWord
        context['object_list'] = post_list

        #No redirection
        return render(self.request, self.template_name, context)

from django.forms import HiddenInput
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from app_news.forms import NewsForm, CommentForm
from app_news.models import News, Comment, Tag
from django.views import generic
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import Group
from .models import News
from django.contrib.auth.models import User


class NewsFormView(PermissionRequiredMixin, View):
    permission_required = 'app_news.add_news'

    def get(self, request):
        news_form = NewsForm()
        return render(request, template_name='news/create.html', context={'news_form': news_form})

    def post(self, request):
        news_form = NewsForm(request.POST)
        user = self.request.user

        if news_form.is_valid():
            news = News(
                name=news_form.cleaned_data['name'],
                content=news_form.cleaned_data['content'],
                news_author=user,
                tag=news_form.cleaned_data['tag']
            )
            news.save()
            # News.objects.create(**news_form.cleaned_data, news_author=user)
            return redirect(reverse('new-list-url'))
        return render(request, template_name='news/create.html', context={'news_form': news_form})


class NewsEditFormView(PermissionRequiredMixin, View):
    permission_required = 'app_news.change_news'

    def get(self, request, news_id):
        news = News.objects.get(id=news_id)
        if self.request.user != news.news_author:
            return self.handle_no_permission()
        news_form = NewsForm(instance=news)
        return render(request, template_name='news/edit.html',
                      context={'news_form': news_form, 'news_id': news_id})

    def post(self, request, news_id):
        news = News.objects.get(id=news_id)
        news_form = NewsForm(request.POST, instance=news)

        if news_form.is_valid():
            news.save()
            return redirect(reverse('new-list-url'))
        return render(request, template_name='news/edit.html',
                      context={'news_form': news_form, 'news_id': news_id})


class NewsListView(generic.ListView):
    model = News
    template_name = 'news/news_list.html'
    context_object_name = 'news_list'
    queryset = News.objects.order_by('created_at')


class NewsFilterTag(generic.ListView):
    model = News
    template_name = 'news/news_with_tag.html'
    context_object_name = 'news_with_tag'

    def get_context_data(self, **kwargs):
        context = super(NewsFilterTag, self).get_context_data(**kwargs)
        context['tag'] = self.kwargs['news_tag']
        return context

    def get_queryset(self):
        queryset = super(NewsFilterTag, self).get_queryset()
        tag = Tag.objects.get(title=self.kwargs['news_tag'])
        queryset = News.objects.order_by('created_at').filter(tag=tag)
        return queryset


@permission_required('app_users.can_activate_news')
def activate_news_view(request, **kwargs):
    news = News.objects.get(id=kwargs['pk'])
    news.active = True
    news.save()
    user = User.objects.get(id=news.news_author.id)
    user.profile.count_news += 1
    user.profile.save()
    return redirect('/news')


class NewsCommentsPageView(generic.edit.FormMixin, generic.DetailView):
    model = News
    context_object_name = 'one_news'
    template_name = 'news/news_and_comments.html'
    form_class = CommentForm

    def get_success_url(self):
        return reverse('news-comments-page', kwargs={'pk': self.get_object().id})

    def get_context_data(self, **kwargs):
        context = super(NewsCommentsPageView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['form'] = CommentForm(initial={'news': self.object, 'author': self.request.user})
            context['form'].fields['user_name'].required = False
            context['form'].fields['user_name'].widget = HiddenInput()
            context['form'].fields['user_name'].widget.attrs['required'] = False
        else:
            context['form'] = CommentForm(initial={'news': self.object})
            context['form'].fields['user_name'].widget.attrs['required'] = True
        # for comment in self.object.comments.all():
        #     context['form'].fields['user'].initial = (self.object.username or self.object.user_id and
        #                                           self.object.user.username or '')
        return context

    def get_form(self, form_class=form_class):
        form = super(NewsCommentsPageView, self).get_form(form_class)
        return form

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    # comment_form = CommentForm(request.POST)
    # new_comment = comment_form.save(commit=False)
    #
    # # user_name = comment_form.cleaned_data['user_name']
    # user_name = 'namepo'
    # comment_text = 'commento'
    #
    # new_comment.user_name = user_name
    # new_comment.comment_text = comment_text
    #
    # new_comment.save()

    def form_valid(self, form):
        # self.object = form.save(commit=False)
        # if self.request.user.is_authenticated:
        #     self.object.user = self.request.user
        # else:
        #     self.object.username = f"Anonym {self.request.POST['name']}"
        # self.object.save()
        form.save()
        return super(NewsCommentsPageView, self).form_valid(form)
        # self.object.user = self.request.user
        # self.object.save()
        # return super(NewsCommentsPageView, self).form_valid(form)

# class NewsCommentsPageView(generic.edit.FormMixin, generic.DetailView):
#     model = News
#     context_object_name = 'news'
#     template_name = 'news/news_and_comments.html'
#     form_class = CommentForm

# def post(self, request):
# comment_form = CommentForm(request.POST)
# if comment_form.is_valid():
#     Comment.objects.create(**comment_form.cleaned_data)
#     return HttpResponseRedirect('/')
# form = self.get_form()
# if form.is_valid():
#     return self.form_valid(form)
# else:
#     return self.form_invalid(form)

# def get_success_url(self, **kwargs):
#     return reverse_lazy('news-comments-page', kwargs={'pk': self.get_object().id})


# class NewsDetailView(generic.DetailView):
#     model = News
#     template_name = 'app_news/news_detail.html'
#
#     def get_context_data(self, *args, **kwargs):
#         news_id = self.kwargs.get('pk', None)
#         context = super().get_context_data(**kwargs)
#         context['comment_list'] = Comment.objects.filter(news_id=news_id)
#         context['comment_form'] = CommentForm()
#         return context
#
#     def post(self, request, *args, **kwargs):
#         news_id = self.kwargs.get('pk', None)
#         comment_form = CommentForm(request.POST)
#         if comment_form.is_valid():
#             Comment.objects.create(**comment_form.cleaned_data, news_id=news_id)
#             return HttpResponseRedirect(f'/news/{news_id}')
#         return render(request, 'app_news/news_detail.html', context={'comment_form': comment_form})

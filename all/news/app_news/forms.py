from django import forms
from .models import News, Comment


class NewsForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(NewsForm, self).__init__(*args, **kwargs)
        self.fields['tag'].required = True

    class Meta:
        model = News
        fields = ('name', 'content', 'tag')


class CommentForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['news'].widget = forms.HiddenInput()
        self.fields['author'].widget = forms.HiddenInput()

    class Meta:
        model = Comment
        fields = ('author', 'user_name', 'comment_text', 'news')


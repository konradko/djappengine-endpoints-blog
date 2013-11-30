from django import forms
from django.shortcuts import render
from django.template.defaultfilters import slugify

from blog.models import Article

class ArticleForm(forms.Form):

    class Meta:
        title = forms.CharField(required=True)
        content = forms.CharField(
            required=True,
            widget=forms.Textarea(attrs={
                'placeholder': 'Enter article',
            })
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title.error_messages['required'] = "Title can't be empty"
        self.content.error_messages['required'] = "Content can't be empty"


def home_page(request):
    articles = Article.all().order('-created')
    return render(request, 'home.html', {'articles': articles, "form": ArticleForm()})

def new_article(request):
    form = ArticleForm(request.POST or None)
    if form.is_valid():
        article = Article(
            title=form.cleaned_data['title'],
            content=form.cleaned_data['content'],
            # TODO: Validation needed to make slug unique
            slug=slugify(form.cleaned_data['title'])[:79])
        article.put()
    return render(request, 'article.html', {'article': article, "form": form})
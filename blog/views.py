from django import forms
from django.shortcuts import render
from django.template.defaultfilters import slugify

from blog.models import Article

DUPLICATE_TITLE_ERROR = "You've already got article with this title"
EMPTY_FIELD_ERROR = "You can't have an empty article"

class ArticleForm(forms.Form):
    title = forms.CharField(required=True)
    content = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={
            'placeholder': 'Enter article',
        })
    )

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
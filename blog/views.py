from django.shortcuts import render, redirect
from django.template.defaultfilters import slugify

from blog.forms import ArticleForm
from blog.models import Article


def home_page(request):
    articles = Article.all().order('-created').fetch(10)
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
        return redirect(article)
    return render(request, 'new_article.html', {'form': form})

def view_article(request, article_slug):
    article = Article.all().filter('slug', article_slug).get()
    return render(request, 'article.html', {'article': article})
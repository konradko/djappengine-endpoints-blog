from django.shortcuts import render, redirect
from django.template.defaultfilters import slugify
from django.http import Http404
from datetime import datetime

from blog.forms import ArticleForm, NewArticleForm
from blog.models import Article

def get_article(article_slug):
    article = Article.query(Article.slug == article_slug).get()
    if not article:
        raise Http404
    else:
        return article

def new_article(request):
    form = NewArticleForm(request.POST or None)
    if form.is_valid():
        article = Article(
            title=form.cleaned_data['title'],
            content=form.cleaned_data['content'],
            slug=slugify(form.cleaned_data['title'])[:79])
        article.put()
        return redirect('/')
    return render(request, 'new_article.html', {'form': form})

def edit_article(request, article_slug):
    article = get_article(article_slug)
    form = ArticleForm(request.POST or None, initial=article.to_dict())
    if form.is_valid():
        article.title = form.cleaned_data['title']
        article.content = form.cleaned_data['content']
        article.slug = slugify(form.cleaned_data['title'])[:79]
        article.last_update = datetime.now()
        article.put()
        return redirect('/')
    return render(request, 'edit_article.html', {'form': form})

def delete_article(request, article_slug):
    get_article(article_slug).key.delete()
    return redirect('/')

def home_page(request):
    articles = Article.query().order(-Article.created).fetch(10)
    return render(request, 'home.html', {'articles': articles})
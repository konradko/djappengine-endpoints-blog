from google.appengine.api import users
from django.shortcuts import render, redirect
from datetime import datetime

from blog.forms import EditArticleForm, ArticleForm
from blog.models import Article


def view_article(request, article_slug):
    article = Article.find(article_slug)
    return render(request, 'article.html', {'article': article})

def home_page(request):
    articles = Article.query().order(-Article.created).fetch()
    return render(request, 'home.html', {'articles': articles})

def new_article(request):
    form = ArticleForm(request.POST or None)
    if form.is_valid():
        Article.get_new(
            title=form.cleaned_data['title'],
            content=form.cleaned_data['content'],
        )
        return redirect('/')
    return render(request, 'form.html', {'form': form})

def edit_article(request, article_slug):
    article = Article.find(article_slug)
    form = EditArticleForm(request.POST or None, initial=article.to_dict())
    if request.POST.get('delete'):
        article.key.delete()
        return redirect('/')
    elif form.is_valid():
        article.title = form.cleaned_data['title']
        article.content = form.cleaned_data['content']
        article.last_update = datetime.now()
        article.put()
        return redirect('/')
    return render(request, 'form.html', {'form': form})

def admin(request):
    return redirect(users.create_login_url('/'))
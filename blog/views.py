from django.shortcuts import render, redirect
from django.template.defaultfilters import slugify
from datetime import datetime

from blog.forms import EditArticleForm, ArticleForm
from blog.models import Article

# Helper functions
def get_article(article_slug):
    return Article.query(Article.slug == article_slug).get()

def get_unique_slug(title):
    article_slug = slugify(title)[:79]
    if get_article(article_slug):
        original_slug = article_slug
        counter = 2
        while get_article(article_slug):
            article_slug = "%s-%i" % (original_slug, counter)
            counter += 1
    return article_slug

# Views
def new_article(request):
    form = ArticleForm(request.POST or None)
    if form.is_valid():
        article = Article(
            title=form.cleaned_data['title'],
            content=form.cleaned_data['content'],
            slug=get_unique_slug(form.cleaned_data['title'])
        )
        article.put()
        return redirect('/')
    return render(request, 'article.html', {'form': form})

def edit_article(request, article_slug):
    article = get_article(article_slug)
    form = EditArticleForm(request.POST or None, initial=article.to_dict())
    if form.is_valid():
        if form.cleaned_data['delete']:
            article.key.delete()
        else:
            article.title = form.cleaned_data['title']
            article.content = form.cleaned_data['content']
            article.last_update = datetime.now()
            article.put()
        return redirect('/')
    return render(request, 'article.html', {'form': form})

def home_page(request):
    articles = Article.query().order(-Article.created).fetch()
    return render(request, 'home.html', {'articles': articles})
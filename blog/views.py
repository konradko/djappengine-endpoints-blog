from django.shortcuts import render, redirect
from django.template.defaultfilters import slugify
from datetime import datetime

from blog.forms import EditArticleForm, ArticleForm
from blog.models import Article

# Helper functions
def find_article(article_slug):
    return Article.query(Article.slug == article_slug).get()

def get_unique_slug(title):
    article_slug = slugify(title)[:79]
    if not article_slug:
        article_slug = 's'
    if find_article(article_slug):
        original_slug = article_slug
        counter = 2
        while find_article(article_slug):
            article_slug = "%s-%i" % (original_slug, counter)
            counter += 1
    return article_slug

def get_new_article(title, content):
    article = Article(
        title=title,
        content=content,
        slug=get_unique_slug(title)
    )
    return article.put().get()

# Views
def new_article(request):
    form = ArticleForm(request.POST or None)
    if form.is_valid():
        get_new_article(
            title=form.cleaned_data['title'],
            content=form.cleaned_data['content'],
        )
        return redirect('/')
    return render(request, 'article.html', {'form': form})

def edit_article(request, article_slug):
    article = find_article(article_slug)
    form = EditArticleForm(request.POST or None, initial=article.to_dict())
    if request.POST.get('delete'):
        article.key.delete()
        return redirect('/')
    elif form.is_valid():
        article.title = form.cleaned_data['title']
        article.content = form.cleaned_data['content']
        article.last_update = datetime.now()
        article.slug = get_unique_slug(article.title)
        article.put()
        return redirect('/')
    return render(request, 'article.html', {'form': form})

def home_page(request):
    articles = Article.query().order(-Article.created).fetch()
    return render(request, 'home.html', {'articles': articles})
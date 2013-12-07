import unittest
from django.test.client import Client
from django.core.urlresolvers import reverse

from ndbtestcase import NdbTestCase

from blog.models import Article
from blog.forms import ArticleForm

class TestBase(NdbTestCase):

    def setUp(self):
        super(TestBase, self).setUp()
        self.client = Client()

    def create_article(self, title='Test title', content='Test content'):
        return Article.get_new(title=title, content=content)

class TestModel(TestBase):

    def test_article_creation(self):
        article = self.create_article()
        self.assertTrue(isinstance(article, Article))
        self.assertEqual(article.__unicode__(), article.title)

    def test_article_url_contains_slug(self):
        article = self.create_article()
        self.assertIn(article.slug, article.get_absolute_url())

class TestViews(TestBase):

    def test_home_contains_all_articles(self):
        articles = [self.create_article() for x in range(5)]
        url = reverse("blog.views.home_page")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(False, [a.title in response.content for a in articles])

    def test_slug_uniqueness(self):
        articles = [self.create_article() for x in range(5)]
        articles += [self.create_article(title='Title%s' % x) for x in ('!', '/', '@')]
        self.assertEqual(len(articles), len(set([a.slug for a in articles])))

    def test_add_article(self):
        self.client.post('/admin/new',
            {'title': 'New title', 'content': 'New content'}
        )
        self.assertTrue(Article.find('new-title'))

    def test_edit_article(self):
        article = self.create_article()
        self.client.post('/admin/edit/%s' % article.slug,
            {'title': 'Edited title', 'content': 'Edited content'}
        )
        self.assertEqual(article.title, 'Edited title')
        self.assertEqual(article.content, 'Edited content')

    def test_slug_changes_with_title(self):
        article = self.create_article()
        initial_slug = article.slug
        self.client.post('/admin/edit/%s' % article.slug,
            {'title': 'Edited title', 'content': 'Edited content'}
        )
        self.assertNotEqual(initial_slug, article.slug)

    def test_delete_article(self):
        article = self.create_article()
        self.client.post('/admin/edit/%s' % article.slug,
            {'delete': True}
        )
        self.assertFalse(Article.find(article.slug))

class TestForms(TestBase):

    def test_valid_article_form(self):
        data = {'title': 'Test form title', 'content': 'Test content'}
        form = ArticleForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_article_form(self):
        data = {'title': 'Test form title', 'content': ''}
        form = ArticleForm(data=data)
        self.assertFalse(form.is_valid())

    def test_invalid_article_html_content(self):
        data = {'title': 'Test form title', 'content': '<p>Test content</p>'}
        form = ArticleForm(data=data)
        self.assertFalse(form.is_valid())

if __name__ == '__main__':
    unittest.main()
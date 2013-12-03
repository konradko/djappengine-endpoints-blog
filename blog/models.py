from google.appengine.ext import ndb
from django.template.defaultfilters import slugify

class Article(ndb.Model):
    title = ndb.StringProperty(required=True)
    slug = ndb.StringProperty(required=True)
    content = ndb.TextProperty(required=True)
    created = ndb.DateTimeProperty(auto_now_add=True)
    last_update = ndb.DateTimeProperty(auto_now_add=True)

    def __unicode__(self):
        return self.title

    @classmethod
    def find(self, article_slug):
        return self.query(self.slug == article_slug).get()

    @classmethod
    def get_new(self, title, content):
        article = self(
            title=title,
            content=content,
        )
        return article.save().get()

    @classmethod
    def get_unique_slug(self, title):
        article_slug = slugify(title)[:79]
        if not article_slug:
            article_slug = 's'
        if self.find(article_slug):
            original_slug = article_slug
            counter = 2
            while self.find(article_slug):
                article_slug = "%s-%i" % (original_slug, counter)
                counter += 1
        return article_slug

    def save(self):
        self.slug = self.get_unique_slug(self.title)
        return self.put()

    def get_absolute_url(self):
        return "/edit/%s" % self.slug
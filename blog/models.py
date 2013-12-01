from google.appengine.ext import ndb

class Article(ndb.Model):
    title = ndb.StringProperty(required=True)
    slug = ndb.StringProperty(required=True)
    content = ndb.TextProperty(required=True)
    created = ndb.DateTimeProperty(auto_now_add=True)
    last_update = ndb.DateTimeProperty(auto_now_add=True)

    def get_absolute_url(self):
        return "/edit/%s/" % self.slug
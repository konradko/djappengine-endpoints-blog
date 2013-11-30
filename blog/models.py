from google.appengine.ext import db
# from django.shortcuts import resolve_url

class Article(db.Model):
    title = db.StringProperty(required=True)
    slug = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    # published = db.BooleanProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    last_update = db.DateTimeProperty(auto_now_add=True)

    def get_absolute_url(self):
        return "/%s" % self.slug

import endpoints
from protorpc import remote, message_types

from blog.models import Article

#TODO: Change with id generated for JS app on https://cloud.google.com/console
CLIENT_ID = endpoints.API_EXPLORER_CLIENT_ID

@endpoints.api(
    name='article_api',
    version='v1',
    description='API for articles',
    allowed_client_ids=[CLIENT_ID, ]
)
class ArticleApi(remote.Service):

    def check_if_exists(self, article):
        if not article.from_datastore:
            raise endpoints.NotFoundException('Article not found.')

    @Article.method(
        #TODO: Admin verification (user in model?)
        user_required=True,
        path='add',
        http_method='POST',
        name='article.insert')
    def add_article(self, article):
        article.put()
        return article

    @Article.method(
        user_required=True,
        request_fields=('id', 'title', 'content'),
        path='patch/{id}',
        http_method='PUT',
        name='article.patch'
    )
    def update_article(self, article):
        self.check_if_exists(article)
        article.put()
        return article

    @Article.method(
        user_required=True,
        request_fields=('id',),
        path='delete/{id}',
        response_message=message_types.VoidMessage,
        http_method='DELETE',
        name='article.delete'
    )
    def delete_article(self, article):
        self.check_if_exists(article)
        article.key.delete()
        return message_types.VoidMessage()

    @Article.method(
        user_required=True,
        request_fields=('id',),
        path='article/{id}',
        http_method='GET',
        name='article.get'
    )
    def get_article(self, article):
        self.check_if_exists(article)
        return article

    @Article.query_method(
        path='articles',
        name='article.list'
    )
    def list_articles(self, query):
        return query

application = endpoints.api_server([ArticleApi], restricted=False)
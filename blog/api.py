import endpoints
from protorpc import remote, message_types

from blog.models import Article

def check_if_exists(article):
    if not article.from_datastore:
        raise endpoints.NotFoundException('Article not found.')

@endpoints.api(name='article_api', version='v1', description='API for articles')
class ArticleApi(remote.Service):

    @Article.method(
        user_required=True,
        path='add',
        http_method='POST', name='article.insert')
    def ArticleInsert(self, article):
        article.put()
        return article

    @Article.method(
        user_required=True,
        request_fields=('id', 'title', 'content'),
        path='patch/{id}',
        http_method='PUT',
        name='article.patch'
    )
    def ArticleUpdate(self, article):
        check_if_exists(article)
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
    def ArticleDelete(self, article):
        check_if_exists(article)
        article.key.delete()
        return message_types.VoidMessage()

    @Article.method(
        request_fields=('id',),
        path='article/{id}',
        http_method='GET',
        name='article.get'
    )
    def ArticleGet(self, article):
        check_if_exists(article)
        return article

    @Article.query_method(
        path='articles',
        name='article.list'
    )
    def ArticleList(self, query):
        return query

application = endpoints.api_server([ArticleApi], restricted=False)
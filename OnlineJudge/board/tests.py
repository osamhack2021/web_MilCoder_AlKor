from logging import log
from utils.api.tests import APITestCase

from .models import Article


class ArticleTest(APITestCase):
    def setUp(self):
        self.create_super_admin(login=False)
        self.create_user(username = "user1", password = "useruser", login = False)
        self.create_user(username = "user2", password = "useruser", login = False)
        self.create_user(username = "user3", password = "useruser", login = True)
        self.url = self.reverse("board_api")

    def create_article(self):
        return self.client.post(self.url, data={"title": "test", "content": "test", "problem" : None})

    def test_create_article(self):
        resp = self.create_article()
        print(resp.data["data"])
        self.assertSuccess(resp)
        return resp

    def test_get_article_list(self):
        self.create_article()
        self.create_article()
        self.create_article()
        self.create_article()
        response = self.client.get(self.url)
        print(response.data["data"])
        self.assertSuccess(response)

    def test_get_article(self):
        id = self.create_article().data["data"]["id"]
        response = self.client.get("{}?id={}".format(self.url, id))
        print(response.data["data"])
        self.assertSuccess(response)
    '''
    def test_edit_article(self):
        data = {"id": self.create_article().data["data"]["id"], "title": "ahaha", "content": "test content"}
        resp = self.client.put(self.url, data=data)
        self.assertSuccess(resp)
        resp_data = resp.data["data"]
        self.assertEqual(resp_data["title"], "ahaha")
        self.assertEqual(resp_data["content"], "test content")
    '''

    def test_delete_article(self):
        id = self.create_article().data["data"]["id"]
        resp = self.client.delete(self.url + "?id=" + str(id))
        self.assertSuccess(resp)
        self.assertFalse(Article.objects.filter(id=id).exists())



class CommentTest(APITestCase):    
    def setUp(self):
        self.create_super_admin(login=False)
        self.create_user(username = "user1", password = "useruser", login = False)
        self.create_user(username = "user2", password = "useruser", login = False)
        self.create_user(username = "user3", password = "useruser", login = True)
        self.article_url = self.reverse("board_api")
        self.comment_url = self.reverse("board_comment_api")

    def create_article(self) :
        return self.client.post(self.article_url, data={"title": "test", "content": "test", "problem" : None})
    
    def create_comment(self, article_id) :
         return self.client.post(self.comment_url, data={"title": "test_comment", "content": "test_comment", "article_id" : article_id})

    def test_create_comment(self) :
        article_id = self.create_article().data["data"]["id"]
        resp = self.create_comment(article_id)
        print(resp.data["data"]) 
        self.assertSuccess(resp)

    def test_get_comments(self) :
        article_id = self.create_article().data["data"]["id"]
        self.create_comment(article_id)
        self.create_comment(article_id)
        self.create_comment(article_id)
        self.create_comment(article_id)
        self.create_comment(article_id)
        resp = self.client.get(self.comment_url + "?article_id=" + str(article_id))
        print(resp.data["data"]) 
        self.assertSuccess(resp)

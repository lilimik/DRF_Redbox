import json

from rest_framework import status
from rest_framework.test import APITestCase

from comments.models import Comment
from comments.serializers import CommentCreateSerializer
from posts.models import Post
from posts.serializers import PostsSerializer


class PostTests(APITestCase):

    def test_create_post(self):
        url = '/posts'
        data = {'name': 'test post name', 'content': 'test post content'}
        self.assertEquals(Post.objects.count(), 0)
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(Post.objects.count(), 1)
        self.assertEquals(Post.objects.get().name, 'test post name')
        self.assertEquals(Post.objects.get().content, 'test post content')

    def test_list_post(self):
        url = '/posts'
        data_set = [
            {'name': 'test post name 1', 'content': 'test post content 1'},
            {'name': 'test post name 2', 'content': 'test post content 2'},
            {'name': 'test post name 3', 'content': 'test post content 3'},
        ]
        self.assertEquals(Post.objects.count(), 0)
        saved_posts = []
        for data in data_set:
            serializer = PostsSerializer(data=data)
            serializer.is_valid()
            serializer.save()
            saved_posts.append(serializer.data)
        response = self.client.get(url)
        content = json.loads(response.content)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(Post.objects.count(), len(saved_posts))
        self.assertEquals(len(content), len(saved_posts))
        [self.assertTrue(data in content) for data in saved_posts]

    def test_get_post(self):
        url = '/posts/1'
        data = {'name': 'test post name 1', 'content': 'test post content 1'}
        post = Post.objects.create(name=data['name'], content=data['content'])
        comment = {'text': 'first comment', 'post': post.id}

        serializer = CommentCreateSerializer(data=comment)
        serializer.is_valid()
        post.comments.add(serializer.save())

        response = self.client.get(url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data['name'], data['name'])
        self.assertEquals(response.data['content'], data['content'])
        self.assertEquals(response.data['comments_count'], 1)

    def test_patch_post(self):
        url = '/posts/1'
        data = {'name': 'test post name 1', 'content': 'test post content 1'}
        new_data_name = {'name': 'test post new name 1'}
        new_data_content = {'content': 'test post new content 1'}

        serializer = PostsSerializer(data=data)
        serializer.is_valid()
        serializer.save()
        post = serializer.data
        new_post = post.copy()
        self.assertEquals(self.client.get(url).data, post)

        response = self.client.patch(url, new_data_name)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        new_post['name'] = new_data_name['name']
        self.assertNotEquals(self.client.get(url).data, post)
        self.assertEquals(self.client.get(url).data, new_post)

        response = self.client.patch(url, new_data_content)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertNotEquals(self.client.get(url).data, new_post)
        new_post['content'] = new_data_content['content']
        self.assertEquals(self.client.get(url).data, new_post)

    def test_put_post(self):
        url = '/posts/1'
        data = {'name': 'test post name 1', 'content': 'test post content 1'}
        serializer = PostsSerializer(data=data)
        serializer.is_valid()
        serializer.save()
        post = serializer.data
        new_post = post.copy()

        self.assertEquals(self.client.get(url).data, post)
        new_data = {'name': 'test post new name 1', 'content': 'test post new content 1'}
        response = self.client.put(url, new_data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

        new_post['name'] = new_data['name']
        new_post['content'] = new_data['content']

        self.assertNotEquals(self.client.get(url).data, post)
        self.assertEquals(self.client.get(url).data, new_post)

    def test_delete_post(self):
        url = '/posts/1'
        data = {'name': 'test post name 1', 'content': 'test post content 1'}
        self.assertEquals(Post.objects.count(), 0)
        Post.objects.create(name=data['name'], content=data['content'])
        self.assertEquals(Post.objects.count(), 1)

        response = self.client.delete(url)
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEquals(Post.objects.count(), 0)

    def test_get_post_with_comments(self):
        url = '/posts/1/comments'
        data = {'name': 'test post name 1', 'content': 'test post content 1'}
        post = Post.objects.create(name=data['name'], content=data['content'])
        comments = [
            {'text': 'first comment', 'post': post.id},
            {'text': 'second comment', 'post': post.id},
        ]

        created_comments = []
        for comment in comments:
            serializer = CommentCreateSerializer(data=comment)
            serializer.is_valid()
            post.comments.add(serializer.save())
            created_comments.append(serializer.data)

        response = self.client.get(url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data['name'], data['name'])
        self.assertEquals(response.data['content'], data['content'])
        response_comments = [dict(comment)['text'] for comment in response.data['comments']]
        self.assertEquals(response.data['comments_count'], len(response_comments))
        self.assertEquals(len(response_comments), len(created_comments))

        [self.assertTrue(data['text'] in response_comments) for data in created_comments]


class CommentTest(APITestCase):

    def test_create_comment(self):
        url = '/comments'
        post_data = {'name': 'test post name 1', 'content': 'test post content 1'}
        post = Post.objects.create(name=post_data['name'], content=post_data['content'])
        comment_data = {'text': 'first comment', 'post': post.id}
        self.assertEquals(Comment.objects.count(), 0)

        response = self.client.post(url, comment_data)

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(Comment.objects.count(), 1)
        self.assertEquals(response.data['text'], comment_data['text'])
        self.assertEquals(Comment.objects.get().text, comment_data['text'])

    def test_list_comment(self):
        url = '/comments'
        data = {'name': 'test post name 1', 'content': 'test post content 1'}
        post = Post.objects.create(name=data['name'], content=data['content'])
        comments = [
            {'text': 'first comment', 'post': post.id},
            {'text': 'second comment', 'post': post.id},
        ]

        self.assertEquals(Comment.objects.count(), 0)
        created_comments = []
        for comment in comments:
            serializer = CommentCreateSerializer(data=comment)
            serializer.is_valid()
            serializer.save()
            created_comments.append(serializer.data)
        self.assertEquals(Comment.objects.count(), len(created_comments))

        response = self.client.get(url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(Comment.objects.count(), len(response.data))

        comments = list(Comment.objects.all().values('id', 'text'))
        response_comments = [dict(comment) for comment in response.data]
        [self.assertTrue(comment in comments) for comment in response_comments]

    def test_patch_comment(self):
        url = '/comments/1'
        post_data = {'name': 'test post name 1', 'content': 'test post content 1'}
        post = Post.objects.create(name=post_data['name'], content=post_data['content'])
        comment_data = {'text': 'first comment text'}
        self.assertEquals(Comment.objects.count(), 0)

        Comment.objects.create(text=comment_data['text'], post=post)

        self.assertEquals(Comment.objects.count(), 1)
        self.assertEquals(Comment.objects.get().text, comment_data['text'])

        new_comment_data = {'text': 'first comment new text'}
        response = self.client.patch(url, new_comment_data)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertNotEquals(Comment.objects.get().text, comment_data['text'])
        self.assertEquals(Comment.objects.get().text, new_comment_data['text'])

    def test_put_comment(self):
        url = '/comments/1'
        post_data = {'name': 'test post name 1', 'content': 'test post content 1'}
        post = Post.objects.create(name=post_data['name'], content=post_data['content'])
        comment_data = {'text': 'first comment text'}
        self.assertEquals(Comment.objects.count(), 0)

        Comment.objects.create(text=comment_data['text'], post=post)

        self.assertEquals(Comment.objects.count(), 1)
        self.assertEquals(Comment.objects.get().text, comment_data['text'])

        new_comment_data = {'text': 'first comment new text'}
        response = self.client.put(url, new_comment_data)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertNotEquals(Comment.objects.get().text, comment_data['text'])
        self.assertEquals(Comment.objects.get().text, new_comment_data['text'])

    def test_delete_comment(self):
        url = '/comments/1'
        post_data = {'name': 'test post name 1', 'content': 'test post content 1'}
        post = Post.objects.create(name=post_data['name'], content=post_data['content'])
        comment_data = {'text': 'first comment text'}
        self.assertEquals(Comment.objects.count(), 0)

        Comment.objects.create(text=comment_data['text'], post=post)

        self.assertEquals(Comment.objects.count(), 1)
        response = self.client.delete(url)
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEquals(Comment.objects.count(), 0)

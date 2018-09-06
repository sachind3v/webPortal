from django.test import TestCase
from django.urls import reverse, resolve
from .. views import home, board_topics,new_topic
from django.contrib.auth.models import User
from .. models import Board ,Topic, Post
from ..forms import NewTopicForm
# Create your tests here.

class HomeTests(TestCase):
    def setUp(self):
        self.board = Board.objects.create(name='DjangoHOME', description='Django ABDsboard.')
        url = reverse('home')
        self.response = self.client.get(url)

    def test_home_view_status_code(self):
        # url = reverse('home')
        # response = self.client.get(url)
        self.assertEqual(self.response.status_code, 200)

    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEqual(view.func, home)

    def test_home_view_contains_link_to_topics_page(self):
        board_topics_url = reverse('board_topics', kwargs={'pk': self.board.pk})
        self.assertContains(self.response, 'href="{0}"'.format(board_topics_url))


class BoardTopicsTests(TestCase):
    def setUp(self):
# creating a dummy instance for the testing purpose

        self.board=Board.objects.create(name='machinehh learning', description='futuhhtre')

# do not use same board as already inside database 
# always use self
#there is a problem with this test case response.status_code=404


# The test_board_topics_view_success_status_code method: 
# is testing if Django is returning a status code 200 (success) for an existing Board.

    def test_board_topics_view_success_status_code(self):
        url = reverse('board_topics', kwargs={'pk':self.board.pk})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

# The test_board_topics_view_not_found_status_code method: is testing if Django is 
# returning a status code 404 (page not found) for a Board that doesn’t exist in the database.

    def test_board_topics_view_not_found_status_code(self):
        url = reverse('board_topics', kwargs={'pk': 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

# The test_board_topics_url_resolves_board_topics_view method: is testing if Django is
 # using the correct view function to render the topics.

    def test_board_topics_url_resolves_board_topics_view(self):
        view = resolve('/boards/1/')
        self.assertEquals(view.func, board_topics)        


    # def test_board_topics_view_contains_link_back_to_homepage(self):
    #     board_topics_url = reverse('board_topics', kwargs={'pk': self.board.pk})
    #     self.response = self.client.get(board_topics_url)
    #     homepage_url = reverse('home')
    #     self.assertContains(self.response, 'href="{0}"'.format(homepage_url))

    def test_board_topics_view_contains_navigation_links(self):
            board_topics_url = reverse('board_topics', kwargs={'pk': self.board.pk})
            homepage_url = reverse('home')
            new_topic_url = reverse('new_topic', kwargs={'pk': self.board.pk})

            self.response = self.client.get(board_topics_url)

            self.assertContains(self.response, 'href="{0}"'.format(homepage_url))
            self.assertContains(self.response, 'href="{0}"'.format(new_topic_url))
            


class NewTopicTests(TestCase):
    def setUp(self):
        self.board=Board.objects.create(name='Djangoojj', description='Django boaprd.')
        self.user=User.objects.create_user(username='johnff', email='john@doe.com', password='123')  # <- included this line here

    def test_new_topic_view_success_status_code(self):
        url = reverse('new_topic', kwargs={'pk': self.board.pk})
        self.response = self.client.get(url)
        self.assertEqual(self.response.status_code, 200)

    def test_new_topic_view_not_found_status_code(self):
        url = reverse('new_topic', kwargs={'pk': 99})
        self.response = self.client.get(url)
        self.assertEqual(self.response.status_code, 404)

    def test_new_topic_url_resolves_new_topic_view(self):
        view = resolve('/boards/1/new/')
        self.assertEqual(view.func, new_topic)

    def test_new_topic_view_contains_link_back_to_board_topics_view(self):
        new_topic_url = reverse('new_topic', kwargs={'pk': self.board.pk})
        board_topics_url = reverse('board_topics', kwargs={'pk': self.board.pk})
        response = self.client.get(new_topic_url)
        self.assertContains(response, 'href="{0}"'.format(board_topics_url))   



# here is the test case for form data 
##############################
##############################
    def test_csrf(self):
        url = reverse('new_topic', kwargs={'pk':self.board.pk})
        self.response = self.client.get(url)
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_new_topic_valid_post_data(self):
        url = reverse('new_topic', kwargs={'pk': self.board.pk})
        data = {
            'subject': 'Test title',
            'message': 'Lorem ipsum dolor sit amet'
        }
        self.response = self.client.post(url, data)
        self.assertTrue(Topic.objects.exists())
        self.assertTrue(Post.objects.exists())

    def test_new_topic_invalid_post_data(self):
        '''
        Invalid post data should not redirect
        The expected behavior is to show the form again with validation errors
        '''
        url = reverse('new_topic', kwargs={'pk': self.board.pk})
        self.response = self.client.post(url, {})
        self.assertEquals(self.response.status_code, 200)

    def test_new_topic_invalid_post_data_empty_fields(self):
        '''
        Invalid post data should not redirect
        The expected behavior is to show the form again with validation errors
        '''
        url = reverse('new_topic', kwargs={'pk': self.board.pk})
        data = {
            'subject': '',
            'message': ''
        }
        self.response = self.client.post(url, data)
        self.assertEquals(self.response.status_code, 200)
        self.assertFalse(Topic.objects.exists())
        self.assertFalse(Post.objects.exists())


#################################
#################################

    def test_contains_form(self):  # <- new test
        url = reverse('new_topic', kwargs={'pk': self.board.pk})
        self.response = self.client.get(url)
        form = self.response.context.get('form')
        self.assertIsInstance(form, NewTopicForm)

    def test_new_topic_invalid_post_data(self):  # <- updated this one
        '''
        Invalid post data should not redirect
        The expected behavior is to show the form again with validation errors
        '''
        url = reverse('new_topic', kwargs={'pk': self.board.pk})
        self.response = self.client.post(url, {})
        form = self.response.context.get('form')
        self.assertEquals(self.response.status_code, 200)
        self.assertTrue(form.errors)
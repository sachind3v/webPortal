from django.test import TestCase
from django.urls import reverse, resolve
from .. views import home, board_topics,new_topic
from django.contrib.auth.models import User
from .. models import Board ,Topic, Post
from ..forms import NewTopicForm
# Create your tests here.

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
            
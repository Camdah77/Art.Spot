from django.test import TestCase
from .models import Artwork

class TestModels(TestCase):

    def test_done_defaults_to_false(self):
        artwork = Artwork.objects.create(name='Test Artwork Model')
        self.assertFalse(artwork.done)
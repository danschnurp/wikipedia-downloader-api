from django.test import TestCase

from rest_framework.test import APIClient

from rest_framework import status


class TestCS(TestCase):

    def setUp(self):
        self.client = APIClient(HTTP_ACCEPT_LANGUAGE="cs")

    def testHappy(self):
        response = self.client.get('/wiki/birell')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["result"][:69], "Birell (dříve Radegast Birell) je českou značkou "
                                                       "nealkoholického piva")

    def testRumInsideString(self):
        response = self.client.get('/wiki/RumbEllion')
        self.assertEqual(response.status_code, status.HTTP_303_SEE_OTHER)


    def testNonsense(self):
        response = self.client.get('/wiki/abcdedfgh')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def testEmpty(self):
        response = self.client.get('/wiki/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def testCharles(self):
        response = self.client.get('/wiki/Karel%20IV')
        self.assertEqual(response.status_code, status.HTTP_300_MULTIPLE_CHOICES)
        self.assertEqual(response.data["result"][:50], "Karel IV. (14. května 1316, Praha – 29. listopadu ")


class TestEN(TestCase):

    def setUp(self):
        self.client = APIClient(HTTP_ACCEPT_LANGUAGE="en")

    def testCountry(self):
        response = self.client.get('/wiki/Czech%20Republic')
        self.assertEqual(response.data["result"][:50], "The Czech Republic,[c][12] also known as Czechia,[")

    def testRumInsideString(self):
        response = self.client.get('/wiki/RumbEllion')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def testRum(self):
        response = self.client.get('/wiki/Rum')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["result"][:35], "Rum is a liquor made by fermenting ")

    def testNonsense(self):
        response = self.client.get('/wiki/abcdxdfdxfedfgh')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

import requests

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import bs4


class FirstParagraph(APIView):

    @staticmethod
    def get_data_from_wiki(prompt="rum", site=f"https://cs.wikipedia.org/wiki/"):
        """
        retrieves data from a specified Wikipedia page and returns a cleaned-up version of the first non-empty
        paragraph as a string.
        """
        result = requests.get(url=f"{site}{prompt.lower()}")
        if result.status_code == 200:
            filtered = [i.text for i in bs4.BeautifulSoup(result.text, features='html.parser').find_all('p')
                        if len(i.text) > 1][0].split()
            return f"{' '.join(filtered)}"
        else:
            return None

    @staticmethod
    def get_data_from_search(prompt, site=f"https://cs.wikipedia.org/w/index.php?search="):
        """"
        tries to search similar queries
        """
        result = requests.get(url=f"{site}{prompt.lower()}")
        result = bs4.BeautifulSoup(result.text, features='html.parser').find("div", "mw-search-results-container")
        if result is None:
            return None
        result = result.find("a").attrs["title"]
        result = requests.get(url=f"{site}{result.lower()}")
        return f"{' '.join(bs4.BeautifulSoup(result.text, features='html.parser').find('p').text.split())}"

    def get(self, request, query):
        """
        main endpoint
        """
        lang = "cs"
        if 'Accept-Language' in request.headers:
            lang = request.headers['Accept-Language']

        result = self.get_data_from_wiki(query, site=f"https://{lang}.wikipedia.org/wiki/")
        if result is not None:
            return Response(data={"result": f"{result}"}, status=status.HTTP_200_OK)

        result = self.get_data_from_search(query, site=f"https://{lang}.wikipedia.org/w/index.php?search=")
        if result is not None:
            return Response(data={"result": f"{result}"}, status=status.HTTP_303_SEE_OTHER)

        return Response(data={"result": "null"}, status=status.HTTP_404_NOT_FOUND)

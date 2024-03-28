import requests

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import bs4


def find_paragraph(result: Response) -> str | None:
    """
    This function finds and returns the first paragraph of text from a web page response, excluding certain types of
    content.

    :param result: The `result` parameter in the `find_paragraph` function is expected to be an object of type `Response`,
    which likely contains the text content of a web page. The function uses BeautifulSoup to parse this text and extract
    relevant information from it
    :type result: Response
    :return: The function `find_paragraph` is returning a string that contains the text content of the first paragraph found
    in the provided `Response` object after filtering out paragraphs with less than 100 characters. If no suitable paragraph
    is found based on the conditions specified in the function, it returns `None`.
    """
    # looking if site even exists
    if len(bs4.BeautifulSoup(result.text, features='html.parser').find_all("p", 'mw-search-nonefound')) > 0:
        return None
    # found but not exactly
    if bs4.BeautifulSoup(result.text, features='html.parser').find("div", "mw-search-results-container") is not None:
        return None

    filtered = [i.text for i in bs4.BeautifulSoup(result.text, features='html.parser').find_all('p')
                # iterates over <p> and skips info in sidebar table by setting min len of paragraph as 100
                # todo could be improved
                if len(i.text) > 100][0].split()
    return f"{' '.join(filtered)}"


def get_data_from_wiki(prompt="rum", site=f"https://cs.wikipedia.org/wiki/") -> str:
    """
    retrieves data from a specified Wikipedia page and returns a cleaned-up version of the first non-empty
    paragraph as a string.
    """

    result = requests.get(url=site + prompt)
    if result.status_code == 200:
        return find_paragraph(result)


def get_data_from_search(prompt: str, site=f"https://cs.wikipedia.org") -> list | str | None:
    """
    This function takes a search prompt and retrieves data from a specified website, returning the found information or None
    if no results are found.

    :param prompt: The `prompt` parameter is a string that represents the search query you want to look up on the specified
    website (in this case, the Czech Wikipedia). It is used to search for information on the website and retrieve relevant
    data based on the search query
    :type prompt: str
    :param site: The `site` parameter in the `get_data_from_search` function is the base URL of the website from which you
    want to retrieve data. In this case, the default value is set to "https://cs.wikipedia.org", which is the Czech version
    of Wikipedia. You can specify a different website, defaults to f"https://cs.wikipedia.org" (optional)
    :return: The function `get_data_from_search` returns a string containing the data found from the search prompt on the
    specified website (default is Czech Wikipedia). If no data is found, it returns `None`.
    """
    result = requests.get(url=f"{site}/w/index.php?search={prompt}")
    found = find_paragraph(result)
    if found is not None:
        return found
    # gets first possible result
    result = bs4.BeautifulSoup(result.text, features='html.parser').find("ul", "mw-search-results")
    if result is None:
        return None
    # gets hrefs of the results
    result = result.find_all("a")
    return list(set(site[:-1] + i.attrs["href"] for i in result))


class FirstParagraph(APIView):

    def get(self, request, query):
        """
        The function retrieves data from Wikipedia based on a query and language preference provided in the request.

        :param request: The `request` parameter in the `get` method is typically an HTTP request object that contains
        information about the incoming request, such as headers, method type, and request data. In this specific code
        snippet, the `request` parameter is used to access the headers of the incoming request, specifically the
        :param query: The `query` parameter in the `get` method represents the search query or term that the user wants to
        look up on Wikipedia. This query is processed and used to retrieve information from Wikipedia in the specified
        language (English or Czech). The query is then formatted to be used in the Wikipedia URL for
        :return: The `get` method in the provided code snippet returns a response based on the query and language specified
        in the request. If the language is not 'en' or 'cs', it returns a 404 Not Found response with data {"result":
        "null"}.
        """
        lang = "cs"
        if 'Accept-Language' in request.headers:
            lang = request.headers['Accept-Language']

        # lang validation, but it can limit the functionality...
        if lang not in ["en", "cs"]:
            Response(data={"result": "null"}, status=status.HTTP_404_NOT_FOUND)

        query = query.lower().replace(" ", "_")

        result = get_data_from_wiki(query, site=f"https://{lang}.wikipedia.org/wiki/")
        if result is not None:
            return Response(data={"result": f"{result}"}, status=status.HTTP_200_OK)

        result = get_data_from_search(query, site=f"https://{lang}.wikipedia.org/")
        if type(result) is str:
            return Response(data={"result": f"{result}"}, status=status.HTTP_300_MULTIPLE_CHOICES)
        elif result is not None:
            return Response(data={"result": "null", "articles": f"{result}"}, status=status.HTTP_303_SEE_OTHER)

        return Response(data={"result": "null"}, status=status.HTTP_404_NOT_FOUND)

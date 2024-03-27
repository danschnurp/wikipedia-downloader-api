# simple-wikipedia-api

- rest api for downloading first paragraph from wikipedia
- headers:
  - Accept-Language: <your_language>
- endpoint
  - /wiki/<your_search_phrase>


### how to start
```
pip install -r requirements.txt
python simple_api/manage.py test wiki
python simple_api/manage.py runserver localhost:8000
```
### how to use
```
curl -H "Accept-Language: en" -w ", %{http_code}\n" http://localhost:8000/wiki/rum 
```
- result:
```
{"result":"Rum is a liquor made by fermenting and then distilling sugarcane molasses or sugarcane juice. The distillate, a clear liquid, is often aged in barrels of oak. While associated with the Caribbean due to its Barbadian origin, rum is nowadays produced in nearly every major sugar-producing region of the world, such as the Philippines, where Tanduay Distillers, the largest producer of rum worldwide, has its headquarters.[1][2][3]"}, 200
```
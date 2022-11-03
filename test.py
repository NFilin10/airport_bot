import json
import requests

url = "https://www.estravel.ee/wp-json/flights/v1/flight-results?lang=et&search_id=11774539&calendar_id=false"

r = requests.get(url)


my_json = r.content.decode('utf8').replace("'", '"')

js = json.loads(my_json)

for i in range(0, len(js["flights"]["flights"])):
    if js["flights"]["flights"][i]["isFastest"] == True:
        print(js["flights"]["flights"][i]["priceInfo"]["total"])




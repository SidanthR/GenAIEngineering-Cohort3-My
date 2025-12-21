import requests
import json

url = "https://open-weather13.p.rapidapi.com/city"

querystring = {"city":"new delhi","lang":"EN"}

headers = {
	"x-rapidapi-key": "7018ce2f00msh6c1c9369fe4d0aap190cdejsn7aeb5f8aec3e",
	"x-rapidapi-host": "open-weather13.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(json.dumps(response.json(), indent=4))
import urllib
from geopy.geocoders import Nominatim
import certifi
def uo(args, **kwargs):
    return urllib.request.urlopen(args, cafile=certifi.where(), **kwargs)
from datetime import datetime,timedelta
import sys, requests

DARK_SKY_API_KEY = "07f42ebfb8fe9f47c357781f1ba974b7"
option_list = "exclude=currently,minutely,hourly,alerts&amp;units=si"

geolocator = Nominatim()
geolocator.urlopen = uo
location = geolocator.geocode(sys.argv[1], language='en_US')

#location = Nominatim().geocode(sys.argv[1], language='en_US')
d_from_date = datetime.strptime(sys.argv[2] , '%Y-%m-%d')
d_to_date = datetime.strptime(sys.argv[3] , '%Y-%m-%d')
delta = d_to_date - d_from_date

latitude = str(location.latitude)

longitude = str(location.longitude)


print("\nLocation: "+ location.address)
for i in range(delta.days+1):
  new_date = (d_from_date + timedelta(days=i)).strftime('%Y-%m-%d')
  search_date = new_date+"T00:00:00"
  response = requests.get("https://api.darksky.net/forecast/"+DARK_SKY_API_KEY+"/"+latitude+","+longitude+","+search_date+"?"+option_list)
  json_res = response.json()
  print("\n"+(d_from_date + timedelta(days=i)).strftime('%Y-%m-%d %A'))
  unit_type = '°F' if json_res['flags']['units'] == 'us' else '°C'
  print("Min temperature: "+str(json_res['daily']['data'][0]['apparentTemperatureMin'])+unit_type)
  print("Max temperature: "+str(json_res['daily']['data'][0]['apparentTemperatureMax'])+unit_type)
  print("Summary: " + json_res['daily']['data'][0]['summary'])
  precip_type = None
  precip_prob = None
  if'precipProbability' in json_res['daily']['data'][0] and 'precipType' in json_res['daily']['data'][0]:
    precip_type = json_res['daily']['data'][0]['precipType']
    precip_prob = json_res['daily']['data'][0]['precipProbability']
  if (precip_type == 'rain' and precip_prob != None):
    precip_prob *= 100
    print("Chance of rain: %.2f%%" % (precip_prob))

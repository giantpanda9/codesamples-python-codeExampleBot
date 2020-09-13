from configparser import ConfigParser
from datetime import date
from os.path import dirname, abspath
from random import randint
import requests
class parseNASA:
	def __init__(self):
		configParser = ConfigParser()
		configPath = dirname(dirname(abspath(__file__))) + "/config/NASAAPI_config.ini"
		configParser.read(configPath)
		self._APIKey = configParser.get('NASAAPI','NASAAPI_Key')
		self._todayDate = date.today()
	def _getURL(self):
		return f"https://api.nasa.gov/neo/rest/v1/feed?start_date={self._todayDate}&end_date={self._todayDate}&api_key={self._APIKey}"
	def getResponse(self):
		APIUrl = self._getURL();
		response = requests.get(APIUrl)
		returned = []
		if response.status_code != 200:
			return []
		responseJSON = response.json()
		
		currentDate = self._todayDate
		responseJSONCurrent = responseJSON["near_earth_objects"][str(currentDate)]
		for nasaItem in responseJSONCurrent:
			returnedItem = {}
			returnedItem["name"] = nasaItem["name"]
			returnedItem["fromDate"] = str(currentDate)
			returnedItem["diameterEstMin"] = nasaItem["estimated_diameter"]["kilometers"]["estimated_diameter_min"] or 0
			returnedItem["diameterEstMax"] = nasaItem["estimated_diameter"]["kilometers"]["estimated_diameter_max"] or 0
			returnedItem["hazardous"] = "Yes" if nasaItem["is_potentially_hazardous_asteroid"] else "No"
			returnedItem["cameCloser"] = nasaItem["close_approach_data"][0]["close_approach_date"]
			returnedItem["details"] = nasaItem["nasa_jpl_url"]
			returned.append(returnedItem)		
		return returned
	def getOneAsteroid(self):
		APIResponse = self.getResponse()
		returned = {}
		#If NASA returned more than one object - then get random one
		if (len(APIResponse) > 1):
			maxNum = len(APIResponse) - 1
			APICount = randint(0,maxNum)
			returned = APIResponse[APICount]
		else:
			#Otherwise use the single one returned - potentially impossible
			returned = APIResponse[0]
		return returned
	def getDescription(self):
		returnedText = "";
		APIResponse = self.getOneAsteroid();
		if (len(APIResponse) > 0):
			returnedText += "Asteroid Name: " + str(APIResponse["name"]) + "\n"
			returnedText += "Report Date: " + str(APIResponse["fromDate"]) + "\n"
			returnedText += "Diameter Min (Km: " + str(APIResponse["diameterEstMin"]) + "\n"
			returnedText += "Diameter Max (Km: " + str(APIResponse["diameterEstMax"]) + "\n"
			returnedText += "Hazardous?: " + str(APIResponse["hazardous"]) + "\n"
			returnedText += "Close Encounter Date: " + str(APIResponse["cameCloser"]) + "\n"
			returnedText += "Details: " + str(APIResponse["details"]) + "\n"
		else:
			returnedText = "Nothing returned from NASA API \n";
		return returnedText;

from configparser import ConfigParser
from os.path import dirname, abspath
from urllib.parse import quote_plus
import requests
class codeExampleBot:
	def __init__(self):
		configParser = ConfigParser()
		configPath = dirname(dirname(abspath(__file__))) + "/config/codeExampleBot_config.ini"
		configParser.read(configPath)
		self._token = configParser.get('Telegram API','codeExampleBot_token')
		self._chatid = configParser.get('Telegram API','chat_id')
		self._message = ""
	def _setMessage(self,msg):
		self._message = msg;
	def _getURL(self):
		returned = "";
		if (self._message != ""):
			chatid = self._chatid;
			token = self._token;
			outMessage = self._message;
			returned = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chatid}&parse_mode=html&text={quote_plus(outMessage)}"
		else: 
			print("Telegram Bot: Message must be set.\n")
		return returned;

	def sendMessage(self):
		APIUrl = self._getURL();
		if (APIUrl == ""):
			return 0;
		response = requests.get(APIUrl)
		if response.status_code == 200:
			print("Message has been sent")
		return 1;


from classes.parseNASA import parseNASA
from classes.codeExampleBot import codeExampleBot
def main():
	parseNASAInstance = parseNASA()
	message = parseNASAInstance.getDescription()
	codeExampleBotInstance = codeExampleBot()
	codeExampleBotInstance._setMessage(message)
	codeExampleBotInstance.sendMessage()
if __name__=='__main__': main()





'''
Base on https://www.geeksforgeeks.org/twitter-sentiment-analysis-using-python/
https://python-hue-client.readthedocs.io/en/latest/
https://pypi.org/project/python-hue/
https://github.com/studioimaginaire/phue
This code records conversations in the room and determines the mood based on the words used

Step: pip install textblob
'''

from textblob import TextBlob
import speech_recognition as sr 
import RPi.GPIO as GPIO

#Remote GPIO libraries
from gpiozero import LED
from gpiozero.pins.pigpio import PiGPIOFactory
  
def listener():
    # Record Audio
	r = sr.Recognizer()
	r.energy_threshold = 800
	with sr.Microphone(sample_rate = 44100) as source:
		print("Say something!")
		audio = r.listen(source,None, 6)

		data = ""
		try:
			print("processing")
			data = r.recognize_google(audio)
			print("Google Speech Recognition " + data)
              
		except sr.UnknownValueError:
			print("Google Speech Recognition could not understand your audio")
		except sr.RequestError as e:
			print("Could not request results from Google Speech Recognition service; {0}".format(e))
		return data 
  
def mood(conversation, phrase): 
	''' 
	Utility function to classify sentiment of  phrase
	using textblob's sentiment method 
	'''

	analysis = TextBlob(phrase) 
	# set sentiment 
	print(analysis.sentiment.polarity)
	if analysis.sentiment.polarity > 0: 
		print('That sounded positive.')
	elif analysis.sentiment.polarity == 0: 
		print('That sounded neutral.')
	else: 
		print('That sounded negative.')
	del conversation[0]
	conversation.append(phrase)
	sentiment = 0
	for i in conversation:
		analysis = TextBlob(i)
		sentiment += analysis.sentiment.polarity	
	sentiment = sentiment/10
	print('Mood = ' + sentiment)
	if sentiment < -0.5:
		ledcontrol('red')
	elif sentiment < -0.8:
		ledcontrol('orange')
	elif sentiment < 0:
		ledcontrol('green')
	elif sentiment < 0.2:
		ledcontrol('teal')
	elif sentiment < 0.6:
		ledcontrol('blue')
	elif sentiment <= 1:
		ledcontrol('pink')
	
	return conversation
 
#LED Control
#Resistors needed at GPIO to LED, RED= 330 Ohm, Green=165 ohm, Blue=110 ohm.
def ledcontrol(color):
    print('Turning on LED to ' + color)
    factory = PiGPIOFactory('192.168.1.101')#Ip adress of Pi zero

    pin1 = 13
	pin2 = 19
	pin3 = 26
	Redled = LED(pin1, pin_factory=factory) # remote pin
	Greenled = LED(pin2, pin_factory=factory) 
	Blueled = LED(pin3, pin_factory=factory) 
    if color == 'red':
		Redled.on()
		Greenled.off()
		Blueled.off()
	if color == 'green':
		Redled.off()
		Greenled.on()
		Blueled.off()
	if color == 'blue':
		Redled.off()
		Greenled.off()
		Blueled.on()
	if color == 'orange':
		Redled.on()
		Greenled.on()
		Blueled.off()
	if color == 'pink':
		Redled.on()
		Greenled.off()
		Blueled.on()
	if color == 'teal':
		Redled.off()
		Greenled.on()
		Blueled.on()
   
conversation = ['hi','youtube','how','are','you','feeling','today?','we','love','learning!']
while 1:
	# calling main function 
	phrase = listener()
	print(conversation)
	conversation = mood(conversation, phrase)

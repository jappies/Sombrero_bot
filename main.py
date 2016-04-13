import cv2
import sys
import telebot
import requests
import urllib
import PIL
from PIL import Image

overlay = Image.open("somb.png")
cascPath = "haarcascade_frontalface_default.xml"
token = ""
bot = telebot.TeleBot(token)
faceCascade = cv2.CascadeClassifier(cascPath) 

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Paste image, and in caption type: /sombrero")


@bot.message_handler(content_types=['photo'])
def handle_image(message):
	#print(message.from_user.username)
	if message.caption == "/sombrero":
		file_info = bot.get_file(message.photo[1].file_id)
		urllib.urlretrieve('https://api.telegram.org/file/bot{0}/{1}'.format(token, file_info.file_path), "background.png")
		image = cv2.imread('background.png')
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

		# Detect faces in the image
		faces = faceCascade.detectMultiScale(
			gray,
			scaleFactor=1.1,
			minNeighbors=5,
			minSize=(30, 30),
			flags = cv2.cv.CV_HAAR_SCALE_IMAGE
		)

		background = Image.open('background.png')

		for (x, y, w, h) in faces:
			somres = overlay.resize((w+(w/5),h), PIL.Image.ANTIALIAS)
			background.paste(somres, (x-(w/10), y-(h-(h/5))), somres)


		background.save('background.png','png')

		photo = open('background.png', 'rb')
		bot.send_photo(message.chat.id, photo)

	  
def main():
	bot.polling()

if __name__ == '__main__':
	main()
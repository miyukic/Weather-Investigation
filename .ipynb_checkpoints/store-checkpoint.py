from bs4 import BeautifulSoup
from urllib.parse import urlparse
import requests
import time

URL = "https://weather.goo.ne.jp/past/412/20200500/"
#URL = "https://weather.goo.ne.jp"

def main():
	crawling = Crawling(URL)
	crawling.storeHTML(fileName="sapporo", directory="./HTML/")
	while crawling.isNextURL():
		crawling.generateNextURL()
		crawling.storeHTML(fileName="sapporo", directory="./HTML/")
		time.sleep(0.5)

	if not crawling.isNextURL():
		print(f"総ファイル数: {crawling.fileNameNumber + 1}")
		print("-----------------COMPLETE!-----------------")
		return

class Crawling:
	def __init__(self, url):
		self.__url = url
		self.__fileNameNumber = 0
		self.urlToSoup(url)
		up = urlparse(url)
		self.__domain = f"{up.scheme}://{up.netloc}" 
	
	@property
	def fileNameNumber(self):
		return self.__fileNameNumber

	def isNextURL(self) -> bool:
		self.__tags = self.__soup.select("li.next.mb0 a")
		if self.__tags:
			return True
		return False

	def generateNextURL(self):
		if not self.isNextURL():
			print("URLの生成に失敗しました。")
		for tag in self.__tags:
			self.__url = f"{self.__domain}{tag.get('href')}"
		self.urlToSoup(self.__url)
		self.__fileNameNumber += 1
		print("URL=", self.__url)	
		print("self.__fileNameNumbers=", self.__fileNameNumber)

	def urlToSoup(self, URL):
		response = requests.get(URL)
		self.__soup = BeautifulSoup(response.text, "lxml")
f"{str.capitalize(key)}HTML"
	def storeHTML(self, fileName: str = None, directory: str = ""):
        if directory == "":
            directory = fileName
		if fileName is None:
			fileName = f"{self.__soup.title.text} No.{self.__fileNameNumber}"
		else:
			fileName += (" No." + str(self.__fileNameNumber))
        if directory == "":
            directory = str.capitalize(fileName)
		try:
			with open(directory + fileName + '.html', "w", encoding="UTF-8") as f:
				f.write(Crawling.getHTML(self.__url))
				print(fileName, "でファイルを保存しました。")
		except OSError as e:
			print(e)
			fileName = f"no-name No.{self.__fileNameNumber}"
			with open(directory + fileName + '.html', "w", encoding="UTF-8") as f:
				f.write(Crawling.getHTML(self.__url))
				print(fileName, "でファイルを保存しました。")

	@staticmethod
	def getHTML(URL):
		res = requests.get(URL)
		html = res.text
		return html

if __name__ == "__main__":
	main() 
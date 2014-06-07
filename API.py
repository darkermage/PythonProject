 # -*- coding: utf-8 -*-
#from imp import load_source
import Book
import xml.etree.ElementTree as ET
from urllib2 import urlopen
from urllib import quote_plus as encode # za querry search string TODO

class goodReads():
	def __init__(self):
		self.key = "oib8AhZCRYiJ8k3Lmlpfag"
	
	def parseBook(self,child):
		book = Book.book()
		book.setGoodreadsID(child[0].text)
		book.setTittle(child[1].text)
		book.setIsbn(child[2].text)
		book.setIsbn13(child[3].text)
		book.setImageURL(child[5].text)
		book.setSmallImageURL(child[6].text)
		book.setPublicationYear(child[7].text)
		book.setPublicationMonth(child[8].text)
		book.setPublicationDay(child[9].text)
		book.setPublisher(child[10].text)
		book.setLanguageCode(child[11].text)
		book.setIsEbook(child[12].text)
		book.setDescription(child[13].text)
		for bl in child.find("book_links").findall("book_link"):
			if bl[1].text == "Amazon":
				book.setAmazonUrl(bl[2].text+"?book_id="+child[0].text)
		return book
		
	def showBookByID(self,ID):
		url = "https://www.goodreads.com/book/show/"+str(ID)+"?format=xml&key="+self.key
		responce = urlopen(url)
		data = responce.read()
		if ( data[:15] != "<!DOCTYPE html>"):   # Proverka dali sushtestvuva IDto
			root = ET.fromstring(data)
			return self.parseBook(root[1])
		else:
			return None
	def showBookByISBN(self,ISBN):
		url = "https://www.goodreads.com/book/isbn?isbn="+str(ISBN)+"&key="+self.key
		responce = urlopen(url)
		data = responce.read()
		if ( data != "<error>book not found</error>"):   # Proverka dali sushtestvuva ISBN
			root = ET.fromstring(data)
			return self.parseBook(root[1])
		else:
			return None 
	def showBookByTitle(self,title):
		url = "https://www.goodreads.com/book/title.xml?title="+encode(str(title))+"&key="+self.key
		responce = urlopen(url)
		data = responce.read()
		if ( data[:15] != "<!DOCTYPE html>"):   # Proverka dali sushtestvuva IDto
			root = ET.fromstring(data)
			return self.parseBook(root[1])
		else:
			return None

	
if __name__ == "__main__":
	g = goodReads()
	b1 = g.showBookByID(53732)
	b2 = g.showBookByISBN(1)
	b3 = g.showBookByID(50)
	b4 = g.showBookByTitle("Hatchet")
	print b1
	print b2.getAmazonUrl()
	print b2
	print b3
	print b4
	b4.AmazonLookup()
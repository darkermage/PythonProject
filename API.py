 # -*- coding: utf-8 -*-
import Book
import xml.etree.ElementTree as ET
from urllib2 import urlopen
from urllib import quote_plus as encode

class goodReads():
	"""A class used to comunicate with goodreads API"""
	def __init__(self):
		self.key = "oib8AhZCRYiJ8k3Lmlpfag" # API key need to connect to the API
	
	def parseBook(self,child):
		"""Parses the xml data received from the API returns a Book object"""
		book = Book.Book()
		book.setGoodreadsID(child[0].text)
		book.setTitle(child[1].text)
		for author in child.find("authors").findall("author"):
			book.setAuthor(author[1].text)
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
		book.setRating(child[15].text)
		book.setNbPages(child[16].text)
		for bl in child.find("book_links").findall("book_link"):
			book.setLink(bl[1].text,bl[2].text)
		return book
		
	def showBookByID(self,ID):
		"""Searches for a book by its goodreads ID returns Book object if the book a result is found or None if there is an error"""
		url = "https://www.goodreads.com/book/show/"+str(ID)+"?format=xml&key="+self.key
		responce = urlopen(url)
		data = responce.read()
		if ( data[:15] != "<!DOCTYPE html>"):   # Checks if book exists if book does not exist the API returns the home web page
			root = ET.fromstring(data)
			return self.parseBook(root[1])
		else:
			return None

	def showBookByISBN(self,ISBN):
		"""Searches for a book by its ISBN returns Book object if the book a result is found or None if there is an error"""
		url = "https://www.goodreads.com/book/isbn?isbn="+str(ISBN)+"&key="+self.key
		responce = urlopen(url)
		data = responce.read()
		if ( data != "<error>book not found</error>"):   # Checks if book exists if book does not exist the API returns book not found error
			root = ET.fromstring(data)
			return self.parseBook(root[1])
		else:
			return None 

	def showBookByTitle(self,title):
		"""Searches for a book by its tittle returns Book object if the book a result is found or None if there is an error
		goodreads API returns a book even if ISBN is passed"""
		url = "https://www.goodreads.com/book/title.xml?title="+encode(str(title))+"&key="+self.key
		responce = urlopen(url)
		data = responce.read()
		if ( data != "<error>book not found</error>"):   # Checks if book exists if book does not exist the API returns book not found error
			root = ET.fromstring(data)
			return self.parseBook(root[1])
		else:
			return None

if __name__ == "__main__":
	#TESTS:
	g = goodReads()
	#b1 = g.showBookByID(53732) #20168816
	#b2 = g.showBookByISBN(9780441172719)
	#b3 = g.showBookByID(50)
	b4 = g.showBookByTitle(300)
	#print b1
	#print b2
	#print b3
	print b4
	#b4.AmazonLookup()
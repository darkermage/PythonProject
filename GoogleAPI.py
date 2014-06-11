# -*- coding: utf-8 -*-

import Book
import json
import errno
import urllib
from urllib2 import urlopen
from urllib import quote_plus as encode

class GoogleAPI():
	
	# The function makes a list of books objects with the data contained in the JSON object - parsedData
	def parseBook(self, parsedData):
		books = []
		items = parsedData['items']
		
		# If the search is by ISBN this list will always contain 1 book. If the search is by title
		# there might be multiple books in the result
		for item in items:
			
			book = Book.Book()
		
			book.setGoogleBooksID(item['id'])
			book.setIsEbook(item['saleInfo']['isEbook'])
			
			volumeInfo = item['volumeInfo']
			
			book.setTitle(volumeInfo['title'])
			
			for author in volumeInfo['authors']:
				book.setAuthor(author)
				
			if ('categories' in volumeInfo):
				for category in volumeInfo['categories']:
					book.setGenre(category)
					
			if ('averageRating' in volumeInfo):
				book.setRating(volumeInfo['averageRating'])
					
			# For some old books there isn't ISBN10 and ISBN13. For those books the default value
			# of None is left
			if ('industryIdentifiers' in volumeInfo and len(volumeInfo['industryIdentifiers']) == 2):	
				book.setIsbn(self.getShorterISBN(volumeInfo['industryIdentifiers']))
				book.setIsbn13(self.getLongerISBN(volumeInfo['industryIdentifiers']))
			
			if ('publishedDate' in volumeInfo):	
				book.setPublicationDate(volumeInfo['publishedDate'])
			
			# Some old books might not have a 'publisher' key
			if ('publisher' in volumeInfo):
				book.setPublisher(volumeInfo['publisher'])	
			
			# volumeInfo['description'] have a type 'unicode' and it must be parsed to ascii to prevent
			# UnicodeEncodeError when printing the content of the Book object.
			# For some books there is no description
			if ('description' in volumeInfo):
				u = volumeInfo['description']
				description = u.encode('ascii', 'ignore')
				book.setDescription(description)
			
			#if ('imageLinks' in volumeInfo):
				#book.setImageURL(volumeInfo['imageLinks']['thumbnail'])
				#book.setSmallImageURL(volumeInfo['imageLinks']['smallThumbnail'])
			
			if ('language' in volumeInfo):	
				book.setLanguageCode(volumeInfo['language'])	
			
			if ('pageCount' in volumeInfo):
				book.setNbPages(volumeInfo['pageCount'])
			
			books.append(book)
			
		return books	
	
	# The function searches in Google Book for a book with the specified ISBN. The search by ISBN returns a unique result
	# (if a book with this ISBN is found)
	def searchBookByISBN(self, ISBN):
		url = "https://www.googleapis.com/books/v1/volumes?q=isbn:"+ISBN+"&key=AIzaSyB3zv7o9a9Dqk5DFH8L_0PRRhU00UVXypE"
		response = urlopen(url)
		data = response.read()
		parsedData = json.loads(data)
		
		# If there isn't a book with this ISBN - None is returned
		if (parsedData['totalItems'] == 0):
			return None
		else:
			return self.parseBook(parsedData)
		
	# The function searches in Google Books for a book that contains the specified search string in its title. Multiple books might be
	# returned in one search.
	def seearchBookByTitle(self, title):
		url = "https://www.googleapis.com/books/v1/volumes?q=intitle:"+encode(str(title))+"&key=AIzaSyB3zv7o9a9Dqk5DFH8L_0PRRhU00UVXypE"
		response = urlopen(url)
		data = response.read()
		parsedData = json.loads(data)
		
		# If there isn't any books with this title - None is returned
		if (parsedData['totalItems'] == 0):
			return None
		else:
			return self.parseBook(parsedData)
	
	# The list provided as a parameter contains 2 values and the function is used to find which one of the two is ISBN10.
	# The second function - getLongerISBN is used to get ISBN13 out of the list.
	def getShorterISBN(self, list):
		if (len(list[0]['identifier']) < len(list[1]['identifier'])):
			return list[0]['identifier']
		else:
			return list[1]['identifier']
	
	def getLongerISBN(self, list):
		if (len(list[0]['identifier']) > len(list[1]['identifier'])):
			return list[0]['identifier']
		else:
			return list[1]['identifier']
	
		
if __name__ == "__main__":
	obj = GoogleAPI()
	books1 = obj.searchBookByISBN("0062228242")
	books2 = obj.seearchBookByTitle("Vortex")
	
	if (books1 == None):
		print None
	else:
		for book in books1:
			print book
			
	if (books2 == None):
		print None
	else:
		for book in books2:
			print book	
	
	#obj.downloadPicturebyURL("http://www.digimouth.com/news/media/2011/09/google-logo.jpg")
	#obj.downloadPicturebyURL("http://www.digimouth.com/news/media/2012/04/mashable_crowd_360x225.png")

import Book
import json
import urllib
from urllib2 import urlopen

class GoogleAPI():

	def parseBook(self, parsedData):
		books = []
		items = parsedData['items']
		
		# If the search is by ISBN this list will always contain 1 book. If the search is by title
		# there might be multiple books in the result
		for item in items:
			
			book = Book.book()
		
			book.setGoogleBooksID(item['id'])
			book.setIsEbook(item['saleInfo']['isEbook'])
			
			volumeInfo = item['volumeInfo']
			
			book.setTittle(volumeInfo['title'])
			
			# For some books there isn't ISBN10 and ISBN13. For those books the default value
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
			
			if ('imageLinks' in volumeInfo):
				book.setImageURL(volumeInfo['imageLinks']['thumbnail'])
				book.setSmallImageURL(volumeInfo['imageLinks']['smallThumbnail'])
			
			if ('language' in volumeInfo):	
				book.setLanguageCode(volumeInfo['language'])	
			
			books.append(book)
			
		return books	
	
	def searchBookByISBN(self, ISBN):
		url = "https://www.googleapis.com/books/v1/volumes?q=isbn:"+ISBN+"&key=AIzaSyB3zv7o9a9Dqk5DFH8L_0PRRhU00UVXypE"
		response = urlopen(url)
		data = response.read()
		parsedData = json.loads(data)
		return self.parseBook(parsedData)
		
	def seearchBookByTitle(self, title):
		url = "https://www.googleapis.com/books/v1/volumes?q=intitle:"+title+"&key=AIzaSyB3zv7o9a9Dqk5DFH8L_0PRRhU00UVXypE"
		response = urlopen(url)
		data = response.read()
		parsedData = json.loads(data)
		return self.parseBook(parsedData)
	
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
	
	def downloadPicturebyURL(self, url):
		urllib.urlretrieve(url, "picture.jpg")
		
if __name__ == "__main__":
	obj = GoogleAPI()
	books1 = obj.searchBookByISBN("0062228242")
	books2 = obj.seearchBookByTitle("Vortex")
	
	for book in books1:
		print book
	
	for book in books2:
		print book
	
	obj.downloadPicturebyURL("http://www.digimouth.com/news/media/2011/09/google-logo.jpg")
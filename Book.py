import webbrowser

class book:
	def __init__(self):
		self.goodreadsID = None
		self.GoogleBooksId = None
		self.tittle = None
		self.isbn = None
		self.isbn13 = None
		self.imageURL = None
		self.smallImageURL = None
		self.publicationDay = None
		self.publicationYear = None
		self.publicationMonth = None
		self.publicationDate = None
		self.publisher = None
		self.languageCode = None
		self.isEbook = None
		self.description = None
<<<<<<< HEAD
		self.links = {} #TODO add more stores
=======
		self.originalPanguageId = None
		self.originalPublicationDay = None
		self.originalPublicationMonth = None
		self.originalPublicationYear = None
		self.originalTitle = None
		self.amazonUrl = None
>>>>>>> 520c9c285cfbce1d89c92de69a95168a6e30e971
		
	def setGoodreadsID(self,tmp):
		self.goodreadsID = tmp
	def getGoodreadsID(self):
		return self.goodreadsID
		
	def setGoogleBooksID(self,tmp):
		self.GoogleBooksId = tmp
	def getGoogleBooksID(self):
		return self.GoogleBooksId
		
	def setTittle(self,tmp):
		self.tittle = tmp
	def getTittle(self):
		return self.tittle
		
	def setIsbn(self,tmp):
		self.isbn = tmp
	def getIsbn(self):
		return self.isbn
		
	def setIsbn13(self,tmp):
		self.isbn13 = tmp
	def getIsbn13(self):
		return self.isbn13
		
	def setImageURL(self,tmp):
		self.imageURL = tmp
	def getImageURL(self):
		return self.imageURL
		
	def setSmallImageURL(self,tmp):
		self.smallImageURL = tmp
	def getSmallImageURL(self):
		return self.smallImageURL
		
	def setPublicationDay(self,tmp):
		self.publicationDay = tmp
	def getPublicationDay(self):
		return self.publicationDay
		
	def setPublicationYear(self,tmp):
		self.publicationYear = tmp
	def getPublicationYear(self):
		return self.publicationYear
		
	def setPublicationMonth(self,tmp):
		self.publicationMonth = tmp
	def getPublicationMonth(self):
		return self.publicationMonth
	
	def setPublicationDate(self,tmp):
		self.publicationDate = tmp
	def getPublicationDate(self):
		return self.publicationDate
	
	def setPublisher(self,tmp):
		self.publisher = tmp
	def getPublisher(self):
		return self.publisher
		
	def setLanguageCode(self,tmp):
		self.languageCode = tmp
	def getLanguageCode(self):
		return self.languageCode
		
	def setIsEbook(self,tmp):
		self.isEbook = tmp
	def getIsEbook(self):
		return self.isEbook
		
	def setDescription(self,tmp):
		self.description = tmp
	def getDescription(self):
		return self.description
		
	def setLink(self,name,url):
		self.links[name] = url
	def getLinks(self):
		return self.links
	def clearLinks(self):
		self.links.clear()
	
	def AmazonLookup(self):
		if (self.getAmazonUrl() != None):
			webbrowser.open(self.getAmazonUrl())
		
		
	def getLinksStr(self):
		keys = self.links.keys()
		ret = ""
		for i in keys:
			ret += i+" = "+self.links[i]+"\n"
		return ret
	def __str__(self):
		return ("*"*10+"BOOK"+"*"*10+"\n"+
			"Goodreads ID = "+str(self.goodreadsID)+"\n"+
			"Google Books ID = "+str(self.GoogleBooksId)+"\n"+
			"Tittle = "+str(self.tittle)+"\n"+
			"ISBN = "+str(self.isbn)+"\n"+
			"ISBN 13 = "+str(self.isbn13)+"\n"+
			"Image URL = "+str(self.imageURL)+"\n"+
			"Small Image URL = "+str(self.smallImageURL)+"\n"+
		        "Publication Date = "+str(self.publicationDate)+"\n"+
			"Publication Day = "+str(self.publicationDay)+"\n"+
			"Publication Month = "+str(self.publicationMonth)+"\n"+
			"Publication Year = "+str(self.publicationYear)+"\n"+
			"Publisher = "+str(self.publisher)+"\n"+
			"Language Code = "+str(self.languageCode)+"\n"+
			"Is Ebook = "+str(self.isEbook)+"\n"+
			"Description = "+str(self.description)+"\n"+
			self.getLinksStr()+
			"*"*24)
			
if __name__ == "__main__":
	b = book()
	b.setTittle("TEST")
	print(b)

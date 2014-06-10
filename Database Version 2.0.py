# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import sessionmaker
from Book import Book

engine = create_engine('mysql://user1:123@localhost:3306/test', encoding='utf-8', echo = True)

Base = declarative_base()

class BookModel(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100))
    authors = Column(String(100))
    ISBN = Column(String(50), unique=True)
    pages = Column(Integer)
    genre = Column(String(100))
    publisher = Column(String(50))    
    imageURL = Column(String(50))   
    grade = Column(Integer)
    location = Column(String(50))
    tenant = Column(String(50))
    dateBorrow = Column(String(50))
    dateReturned = Column(String(50))
    
    def __init__(self, title, authors, ISBN, pages, tenant = "", dateBorrow = "", dateReturned = "", genre = "", publisher = "", imageURL = "", grade = 0, location = ""):
        self.title = title
        self.authors = authors
        self.ISBN = ISBN
        self.pages = pages
	self.tenant = tenant
	self.dateBorrow = dateBorrow
	self.dateReturned = dateReturned
        self.genre = genre
        self.publisher = publisher   
        self.imageURL = imageURL     
        self.grade = grade
        self.location = location

    def ConvertToBook(self):
        book = Book()
        book.setTitle(self.title)
        book.setAuthor(self.authors)
        book.setIsbn(self.ISBN)
        book.setNbPages(self.pages)
	book.getTenant()
	book.getDateBorrow()
	book.getDateReturned()
        book.setPublisher(self.publisher)     
        book.setImageURL(self.imageURL)

        return book
       
def saveBook(book):
    bookModel = BookModel(book.getTitle(), book.getAuthorsStr(), book.getIsbn(), book.getNbPages(), book.getTenant(), book.getDateBorrow(), book.getDateReturned(), "", book.getPublisher(), book.getImageURL(), 0, "")

    Session = sessionmaker(bind = engine)
    session = Session()
    session.add(bookModel)
    session.commit()
    
def deleteBook(ISBN):
    Session = sessionmaker(bind = engine)
    session = Session()
    session.query(BookModel).filter(BookModel.ISBN == ISBN).delete()
    session.commit()

def updateBook(id, book):
    Session = sessionmaker(bind = engine)
    session = Session()
    
    bookModel = session.query(BookModel).filter(BookModel.id == id).first()
    bookModel.title = book.getTitle()
    bookModel.authors = book.getAuthorsStr()
    bookModel.ISBN = book.getIsbn()
    bookModel.pages = book.getNbPages()
    bookModel.tenant = book.getTenant()
    bookModel.dateBorrow = book.getDateBorrow()
    bookModel.dateReturned = book.getDateReturned()
    bookModel.genre = "" # book.genre
    bookModel.publisher = book.getPublisher()
    bookModel.imageURL = book.getImageURL()
    bookModel.grade = 0 # book.grade
    bookModel.location = "" # book.location

    session.commit()
    
def getAllBooks():
    Session = sessionmaker(bind = engine)
    session = Session()
    listOfBooks = []
        
    for book in session.query(BookModel).all():
        listOfBooks.append(book.ConvertToBook())

    return listOfBooks

def getSingleBook(ISBN):
    Session = sessionmaker(bind = engine)
    session = Session()
    bookModel = session.query(BookModel).filter(BookModel.ISBN == ISBN).first()
    
    book = bookModel.ConvertToBook()
    return book

Base.metadata.create_all(engine)

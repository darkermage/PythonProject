# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Table, Date
from sqlalchemy.orm import sessionmaker
from Book import Book

engine = create_engine('mysql://root:password@127.0.0.1:3306/bookstore', encoding='utf-8', echo = True)

Base = declarative_base()

class BookModel(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255))
    authors = Column(String(255))
    ISBN = Column(String(255), unique=True)
    pages = Column(Integer)
    genre = Column(String(255))
    publisher = Column(String(255))
    image = Column(String(255))
    grade = Column(Integer)
    location = Column(String(255))
    tenant = Column(String(255))
    dateBorrow = Column(Date)
    dateReturned = Column(Date)
    
    def __init__(self, title, authors, ISBN, pages, genre = None, publisher = None, image = None, grade = 0, location = None, tenant = None, dateBorrow = None, dateReturned = None):
        self.title = title
        self.authors = authors
        self.ISBN = ISBN
        self.pages = pages
        self.genre = genre
        self.publisher = publisher
        self.image = image
        self.grade = grade
        self.location = location
        self.tenant = tenant
        self.dateBorrow = dateBorrow
        self.dateReturned = dateReturned

    def ConvertToBook(self):
        book = Book()
        book.setID(self.id)
        book.setTitle(self.title)
        book.setAuthor(self.authors)
        book.setIsbn(self.ISBN)
        book.setNbPages(self.pages)
        book.setGenre(self.genre)
        book.setPublisher(self.publisher)     
        book.setImage(self.image)
        book.setRating(self.grade)
        book.setLocation(self.location)
        book.setTenant(self.tenant)
        book.setDateBorrow(self.dateBorrow)
        book.setDateReturned(self.dateReturned)

        return book
       
def saveBook(book):
    bookModel = BookModel(book.getTitle(),
                          book.getAuthorsStr(),
                          book.getIsbn(),
                          book.getNbPages(),
                          book.getGenresStr(),
                          book.getPublisher(),
                          book.getImage(),
                          book.getRating(),
                          book.getLocation(),
                          book.getTenant(),
                          book.getDateBorrow(),
                          book.getDateReturned())

    Session = sessionmaker(bind = engine)
    session = Session()
    session.add(bookModel)
    session.commit()
    
def deleteBook(book):
    Session = sessionmaker(bind = engine)
    session = Session()
    session.query(BookModel).filter(BookModel.id == book.getID()).delete()
    session.commit()

def updateBook(id, book):
    Session = sessionmaker(bind = engine)
    session = Session()
    
    bookModel = session.query(BookModel).filter(BookModel.id == id).first()
    bookModel.title = book.getTitle()
    bookModel.authors = book.getAuthorsStr()
    bookModel.ISBN = book.getIsbn()
    bookModel.pages = book.getNbPages()
    bookModel.genre = book.getGenresStr()
    bookModel.publisher = book.getPublisher()
    bookModel.image = book.getImage()
    bookModel.grade = book.getRating()
    bookModel.location = book.getLocation()
    bookModel.tenant = book.getTenant()
    bookModel.dateBorrow = book.getDateBorrow()
    bookModel.dateReturned = book.getDateReturned()

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

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import sessionmaker

engine = create_engine('mysql://root:123@localhost/test', encoding='utf-8', echo=True)

Base = declarative_base()

class Book(Base):
    __tablename__ = 'book'
    id = Column(Integer, primary_key=True, autoincrement=True)
    fullName = Column(String(50))
    author = Column(String(50))
    genre = Column(String(50))
    publisher = Column(String(50))
    pages = Column(Integer)
    cover = Column(String(50))
    ISBN = Column(String(50), unique=True)
    grade = Column(Integer)
    location = Column(String(50))
    
    def __init__(self, fullName, author, genre, publisher, pages, cover, ISBN, grade, location):
        self.fullName = fullName
        self.author = author
        self.publisher = publisher
        self.pages = pages
        self.cover = cover
        self.ISBN = ISBN
        self.grade = grade
        self.location = location
        
def saveBook(book):
    Session = sessionmaker(bind=engine)
    session = Session()
    session.add(book)
    session.commit()
    
def deleteBook(ISBN):
    Session = sessionmaker(bind=engine)
    session = Session()
    session.query(Book).filter(Book.ISBN==ISBN).delete()
    session.commit()

def updateBook(id, book):
    Session = sessionmaker(bind=engine)
    session = Session()
    
    temporaryBook = session.query(Book).filter(Book.id==id).first()
    temporaryBook.fullName = book.fullName
    temporaryBook.ISBN = book.ISBN
    temporaryBook.genre = book.genre
    temporaryBook.publisher = book.publisher
    temporaryBook.cover = book.cover
    temporaryBook.grade = book.grade
    temporaryBook.location = book.location
    temporaryBook.author = book.author
    temporaryBook.pages = book.pages
    
    session.commit()
    
def getAllBooks():
    Session = sessionmaker(bind=engine)
    session = Session()
    listOfBooks = []
        
    for i in session.query(Book).all():
        listOfBooks.append(i.__dict__)

    return listOfBooks

def getSingleBook(ISBN):
    Session = sessionmaker(bind=engine)
    session = Session()
    book = session.query(Book).filter(Book.ISBN==Book.ISBN).first()
        
    return book

Base.metadata.create_all(engine)
 # -*- coding: utf-8 -*-

import wx
from Book import Book
from Images import ImageManager
import Database

window = None
imageManager = ImageManager()

class ManageBooksWindow(wx.Window):
    """The Collection window"""
    def __init__(self, parent):
        wx.Window.__init__(self, parent)

        self.sizer = wx.BoxSizer(wx.VERTICAL);
        self.splitter = wx.SplitterWindow(self)
        self.splitter.SetSashGravity(1);
        self.splitter.SetMinimumPaneSize(400);
        self.splitter.SetSashSize(15)
        self.sizer.Add(self.splitter, 1, wx.EXPAND);
 
        self.leftPane = LeftPane(self.splitter);
        self.rightPane = RightPane(self.splitter);
        self.splitter.SplitVertically(self.leftPane, self.rightPane, 600);
 
        self.SetSizer(self.sizer);
        self.sizer.SetSizeHints(self)

        global window
        window = self

    def OnAddNewBook(self):
        """Opens the Add new book window"""
        self.rightPane.ShowAddNewBook()

    def OnShowBookDetails(self, book):
        """Open Book details window"""
        self.rightPane.ShowBookDetails(book)

class LeftPane(wx.Panel):
    """The left pane of the Collection window - here is the collection of books"""
    def __init__(self, parent):
        super(LeftPane, self).__init__(parent)
        self.SetBackgroundColour("#FFFFFF")

        self.sizer = wx.BoxSizer(wx.VERTICAL)

        self.paneLabel = wx.StaticText(self, label = "Collection", style = wx.ALIGN_CENTER_HORIZONTAL)
        font = wx.Font(18, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        self.paneLabel.SetFont(font)

        self.bookList = BookListView(self)
        self.sizer.Add(self.paneLabel, 0, wx.EXPAND)
        self.sizer.Add(self.bookList, 1, wx.EXPAND)

        self.SetSizer(self.sizer)

    def RefreshBooks(self):
        """Refreshes the collection of books"""
        self.bookList.RefreshBooks()

class RightPane(wx.Window):
    """The right pane of the Collection window - here is the Book details view"""
    def __init__(self, parent):
        super(RightPane, self).__init__(parent)
        self.SetBackgroundColour("#FFFFFF")

        self.sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.noSelectionText = wx.StaticText(self, wx.ID_ANY, "No book selected", style = wx.ALIGN_CENTER_HORIZONTAL)      
        font = wx.Font(18, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        self.noSelectionText.SetFont(font)
        self.sizer.Add(self.noSelectionText, 1, wx.ALIGN_CENTER)

        self.bookDetailsView = BookDetailsView(self)
        self.sizer.Add(self.bookDetailsView, 1, wx.ALIGN_CENTER)
        self.sizer.Hide(self.bookDetailsView)

        self.addNewBookView = None

        self.SetSizer(self.sizer);

        self.ShowNoSelectionText()

    def ShowNoSelectionText(self):
        """Shows a message 'No selection'"""
        if self.addNewBookView is not None and self.addNewBookView.IsShown():
            self.sizer.Hide(self.addNewBookView)
        elif self.bookDetailsView.IsShown():
            self.sizer.Hide(self.bookDetailsView)
       
        self.sizer.Show(self.noSelectionText)
        self.sizer.Layout()

    def ShowAddNewBook(self):
        """Opens the add new book window"""
        if self.noSelectionText.IsShown():
            self.sizer.Hide(self.noSelectionText)
        elif self.bookDetailsView.IsShown():
            self.sizer.Hide(self.bookDetailsView)
        
        if self.addNewBookView is not None:
            self.addNewBookView.Destroy()

        self.addNewBookView = NewBookView(self)
        self.sizer.Add(self.addNewBookView, 1, wx.ALIGN_CENTER)
        self.sizer.Layout()

    def ShowBookDetails(self, book):
        """Opens Book details window"""
        if self.noSelectionText.IsShown():
            self.sizer.Hide(self.noSelectionText)
        elif self.addNewBookView is not None and self.addNewBookView.IsShown():
            self.sizer.Hide(self.addNewBookView)
       
        self.bookDetailsView.ShowBook(book)
        self.sizer.Show(self.bookDetailsView)
        self.sizer.Layout()

class BookListView(wx.Panel):
    """Shows a list of books in a grid"""

    def __init__(self, parent):
        super(BookListView, self).__init__(parent)

        self.RefreshBooks()

    def RefreshBooks(self):
        """Refreshes the list of books"""
        self.sizer = wx.GridSizer(cols = 3, vgap = 10, hgap = 10)
        
        self.DestroyChildren()

        allBooks = Database.getAllBooks()

        for book in allBooks:
            self.sizer.Add(SingleBookView(self, book))

        self.SetSizer(self.sizer)
        self.Layout()

class SingleBookView(wx.Panel):
    """Used to show a single book in BookListView"""
    def __init__(self, parent, book):
        super(SingleBookView, self).__init__(parent)
        self.SetSizeHints(200, 240, 200, 240)

        self.book = book

        sizer = wx.BoxSizer(wx.VERTICAL)

        img = wx.EmptyImage(120, 180)
        self.imageCtrl = wx.StaticBitmap(self, wx.ID_ANY, wx.BitmapFromImage(img))
        sizer.Add(self.imageCtrl, 0, wx.ALIGN_CENTER_HORIZONTAL)

        self.titleCtrl = wx.StaticText(self, label = book.getTitle(), style = wx.ALIGN_CENTER_HORIZONTAL)
        sizer.Add(self.titleCtrl, 1, wx.EXPAND | wx.ALL, border = 10)

        self.SetSizer(sizer)

        self.imageCtrl.Bind(wx.EVT_LEFT_UP, self.OnSingleBookSelected)
        self.titleCtrl.Bind(wx.EVT_LEFT_UP, self.OnSingleBookSelected)

        self._onView()

    def OnSingleBookSelected(self, e):
        window.OnShowBookDetails(self.book)

    def _onView(self):
        filepath = self.book.getImage()
        
        if filepath is not None:
            filepath = imageManager.getPicturePath(filepath)
            img = wx.Image(filepath, wx.BITMAP_TYPE_ANY)

            img = img.Scale(120, 180)
 
            self.imageCtrl.SetBitmap(wx.BitmapFromImage(img))
            self.Refresh()

class BookViewBase(wx.Panel):
    """description of class"""

    def _setBorrowerRow(self):
        borrowedLabel = wx.StaticText(self, wx.ID_ANY, "Borrowed:")
        borrowSizer = wx.BoxSizer()
        
        self.borrower = wx.TextCtrl(self, wx.ID_ANY, size = (220, 22))
        borrowSizer.Add(self.borrower)

        self.sizer.Add(borrowedLabel, 1, wx.ALIGN_RIGHT)
        self.sizer.Add(borrowSizer, 1)

    def _setBorrowDatesRow(self):
        returnedLabel = wx.StaticText(self, wx.ID_ANY, "")
        returnSizer = wx.BoxSizer()
        
        self.borrowDate = wx.DatePickerCtrl(self, size = (105, 22), style = wx.DP_DROPDOWN)
        returnSizer.Add(self.borrowDate)
        self.returnDate = wx.DatePickerCtrl(self, size = (105, 22), style = wx.DP_DROPDOWN)
        returnSizer.Add(self.returnDate, flag=wx.LEFT, border = 10)
        
        self.sizer.Add(returnedLabel, 1, wx.ALIGN_RIGHT)
        self.sizer.Add(returnSizer, 1)

    def __init__(self, parent):    
        self.book = None
          
        super(BookViewBase, self).__init__(parent) 
        self.SetSizeHints(400, 700)
        self.boxSizer = wx.BoxSizer(wx.VERTICAL)

        self.imagePath = None
        img = wx.EmptyImage(120, 180)
        self.emptyImage = wx.BitmapFromImage(img)
        self.imageCtrl = wx.StaticBitmap(self, wx.ID_ANY, self.emptyImage)
        self.boxSizer.Add(self.imageCtrl, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.BOTTOM, border = 30)
        self.imageCtrl.Bind(wx.EVT_LEFT_UP, self._pickImage)

        self.sizer = wx.FlexGridSizer(rows = 11, cols = 2, vgap = 5, hgap = 10)

        self.sizer.AddGrowableCol(0, 1)
        self.sizer.AddGrowableCol(1, 2)

        titleLabel = wx.StaticText(self, wx.ID_ANY, "Title:")
        authorLabel = wx.StaticText(self, wx.ID_ANY, "Authors:")
        genresLabel = wx.StaticText(self, wx.ID_ANY, "Genres:")
        publisherLabel = wx.StaticText(self, wx.ID_ANY, "Publisher:")
        pagesLabel = wx.StaticText(self, wx.ID_ANY, "Pages:")
        isbnLabel = wx.StaticText(self, wx.ID_ANY, "ISBN:")
        placeLabel = wx.StaticText(self, wx.ID_ANY, "Place:")
        grade = wx.StaticText(self, wx.ID_ANY, "Grade:")

        # TODO: Add validators
        defCtrlSize = wx.Size(220, 22) 
        self.titleCtrl = wx.TextCtrl(self, wx.ID_ANY, size = defCtrlSize)
        self.authorsCtrl = wx.TextCtrl(self, wx.ID_ANY, size = defCtrlSize)
        self.genresCtrl = wx.TextCtrl(self, wx.ID_ANY, size = defCtrlSize)
        self.publisherCtrl = wx.TextCtrl(self, wx.ID_ANY, size = defCtrlSize)
        self.pagesCtrl = wx.TextCtrl(self, wx.ID_ANY, size = defCtrlSize)
        self.isbnCtrl = wx.TextCtrl(self, wx.ID_ANY, size = defCtrlSize)
        self.placeCtrl = wx.TextCtrl(self, wx.ID_ANY, size = defCtrlSize)
        self.gradeCtrl = wx.SpinCtrl(self, min = 0, max = 5, size = (80, 22))

        self.sizer.Add(titleLabel, 1, wx.ALIGN_RIGHT)
        self.sizer.Add(self.titleCtrl, 2)
        self.sizer.Add(authorLabel, 1, wx.ALIGN_RIGHT)
        self.sizer.Add(self.authorsCtrl, 2)
        self.sizer.Add(genresLabel, 1, wx.ALIGN_RIGHT)
        self.sizer.Add(self.genresCtrl, 2)
        self.sizer.Add(publisherLabel, 1, wx.ALIGN_RIGHT)
        self.sizer.Add(self.publisherCtrl, 2)
        self.sizer.Add(pagesLabel, 1, wx.ALIGN_RIGHT)
        self.sizer.Add(self.pagesCtrl, 2)
        self.sizer.Add(isbnLabel, 1, wx.ALIGN_RIGHT)
        self.sizer.Add(self.isbnCtrl, 2)
        self.sizer.Add(placeLabel, 1, wx.ALIGN_RIGHT)
        self.sizer.Add(self.placeCtrl, 2)
        self.sizer.Add(grade, 1, wx.ALIGN_RIGHT)
        self.sizer.Add(self.gradeCtrl, 2)

        self._setBorrowerRow()
        self._setBorrowDatesRow()

    def _pickImage(self, e):
        wildcard = "pictures (*.jpeg,*jpg,*.png,*.gif)|*.jpeg;*jpg;*.png;*.gif"
        dialog = wx.FileDialog(None, "Choose a file",
                               wildcard=wildcard,
                               style=wx.OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            fullPath = dialog.GetPath().split('\\')
            length = len(fullPath)
            filePath = str(fullPath[length - 1])
            self.imagePath = filePath
        dialog.Destroy() 
        self._onTempView()

    def _onView(self):
        filepath = self.book.getImage()
        
        if filepath is not None:
            filepath = imageManager.getPicturePath(filepath)
            img = wx.Image(filepath, wx.BITMAP_TYPE_ANY)

            img = img.Scale(120, 180)
 
            self.imageCtrl.SetBitmap(wx.BitmapFromImage(img))
            self.Refresh()
        else:
            self.imageCtrl.SetBitmap(self.emptyImage)
            self.Refresh()

    def _onTempView(self):
        filepath = self.imagePath
        
        if filepath is not None:
            filepath = imageManager.getPicturePath(filepath)
            img = wx.Image(filepath, wx.BITMAP_TYPE_ANY)

            img = img.Scale(120, 180)
 
            self.imageCtrl.SetBitmap(wx.BitmapFromImage(img))
            self.Refresh()
        else:
            self.imageCtrl.SetBitmap(self.emptyImage)
            self.Refresh()

    def CollectData(self):
        book = Book()

        if self.imagePath is not None:
            book.setImage(self.imagePath)
        elif self.book is not None:
            book.setImage(self.book.getImage())

        book.setTitle(str(self.titleCtrl.GetValue()))
        book.setAuthor(str(self.authorsCtrl.GetValue()))
        book.setGenre(str(self.genresCtrl.GetValue()))
        book.setPublisher(str(self.publisherCtrl.GetValue()))
        book.setNbPages(int(self.pagesCtrl.GetValue()))
        book.setIsbn(str(self.isbnCtrl.GetValue()))
        book.setLocation(str(self.placeCtrl.GetValue()))
        book.setRating(self.gradeCtrl.GetValue())
        
        borrower = str(self.borrower.GetValue()).strip()
        
        if borrower != "":
            book.setTenant(borrower)
            book.setDateBorrow(_wxdate2pydate(self.borrowDate.GetValue()))
            book.setDateReturned(_wxdate2pydate(self.returnDate.GetValue()))

        return book

class BookDetailsView(BookViewBase):
    """description of class"""

    def __init__(self, parent): 
        super(BookDetailsView, self).__init__(parent) 

        self.buttonsSizer = wx.BoxSizer()

        btn1 = wx.Button(self, label='Save', size=(70, 30))
        self.buttonsSizer.Add(btn1, flag = wx.LEFT, border = 75)
        btn2 = wx.Button(self, label='Delete', size=(70, 30))
        self.buttonsSizer.Add(btn2, flag=wx.LEFT, border=5)

        self.sizer.Add(wx.StaticText(self, label = ""))
        self.sizer.Add(self.buttonsSizer, 1)

        self.boxSizer.Add(self.sizer, 1, wx.EXPAND)  
        self.SetSizerAndFit(self.boxSizer)

        self.Bind(wx.EVT_BUTTON, self.SaveChanges, btn1)
        self.Bind(wx.EVT_BUTTON, self.Delete, btn2)
        
    def ShowBook(self, book):
        self.book = book

        self.titleCtrl.SetValue(book.getTitle())
        self.authorsCtrl.SetValue(book.getAuthorsStr())

        self.genresCtrl.SetValue(book.getGenresStr())

        if book.getPublisher() is not None:
            self.publisherCtrl.SetLabelText(book.getPublisher())

        self.pagesCtrl.SetValue(str(book.getNbPages()))

        if book.getIsbn() is not None:
            self.isbnCtrl.SetValue(book.getIsbn())

        if book.getLocation() is not None:
            self.placeCtrl.SetValue(book.getLocation())

        self.gradeCtrl.SetValue(book.getRating())

        if book.getTenant() is not None:
            self.borrower.SetValue(book.getTenant())
            self.borrowDate.SetValue(_pydate2wxdate(book.getDateBorrow()))
            self.returnDate.SetValue(_pydate2wxdate(book.getDateReturned()))

        self._onView()

    def SaveChanges(self, e):
        dlg = wx.MessageDialog(self, "Are you sure you want to update the book?", "Update Book", wx.YES_NO)
        returnCode = dlg.ShowModal()
        dlg.Destroy()

        if returnCode == wx.ID_YES:
            book = self.CollectData()

            Database.updateBook(self.book.getID(), book)
            #dlg2 = wx.MessageDialog(self, "The book has been updated!", "Success", wx.OK)
            #dlg2.ShowModal()
            #dlg2.Destroy()

            window.rightPane.ShowNoSelectionText()
            window.leftPane.RefreshBooks()

    def Delete(self, e):
        dlg = wx.MessageDialog(self, "Are you sure you want to delete the book?", "Delete Book", wx.YES_NO)
        returnCode = dlg.ShowModal()
        dlg.Destroy()

        if returnCode == wx.ID_YES:
            Database.deleteBook(self.book)
            #dlg2 = wx.MessageDialog(self, "The book has been deleted!", "Success", wx.OK)
            #dlg2.ShowModal()
            #dlg2.Destroy()

            window.rightPane.ShowNoSelectionText()
            window.leftPane.RefreshBooks()

class NewBookView(BookViewBase):
    """description of class"""

    def __init__(self, parent):      
        super(NewBookView, self).__init__(parent) 

        self.buttonsSizer = wx.BoxSizer()

        btn1 = wx.Button(self, label='Save', size=(70, 30))
        self.buttonsSizer.Add(btn1, flag = wx.LEFT, border = 75)
        btn2 = wx.Button(self, label='Cancel', size=(70, 30))
        self.buttonsSizer.Add(btn2, flag=wx.LEFT, border=5)

        self.sizer.Add(wx.StaticText(self, label = ""))
        self.sizer.Add(self.buttonsSizer, 1)

        self.boxSizer.Add(self.sizer, 1, wx.EXPAND)  
        self.SetSizerAndFit(self.boxSizer)

        self.Bind(wx.EVT_BUTTON, self.Save, btn1)
        self.Bind(wx.EVT_BUTTON, self.Cancel, btn2)

    def Save(self, e):
        book = self.CollectData()

        Database.saveBook(book)

        dlg = wx.MessageDialog(self, "A new book is added to your colection!", "Success", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()

        window.rightPane.ShowNoSelectionText()
        window.leftPane.RefreshBooks()

    def Cancel(self, e):
        window.rightPane.ShowNoSelectionText()


def _pydate2wxdate(date): 
     import datetime 
     assert isinstance(date, (datetime.datetime, datetime.date)) 
     tt = date.timetuple() 
     dmy = (tt[2], tt[1]-1, tt[0]) 
     return wx.DateTimeFromDMY(*dmy) 

def _wxdate2pydate(date): 
     import datetime 
     assert isinstance(date, wx.DateTime) 
     if date.IsValid(): 
         ymd = map(int, date.FormatISODate().split('-')) 
         return datetime.date(*ymd) 
     else: 
         return None 
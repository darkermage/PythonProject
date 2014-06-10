 # -*- coding: utf-8 -*-

import wx
from Book import Book
from Database import *

class ManageBooksWindow(wx.Window):
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

        #allBooks = getAllBooks()

        #self.OnShowBookDetails(allBooks[0])

    def OnAddNewBook(self):
        self.rightPane.ShowAddNewBook()

    def OnShowBookDetails(self, book):
        self.rightPane.ShowBookDetails(book)

class LeftPane(wx.Panel):
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

    def OnSingleBookSelected(self, book):
        self.GetParent().GetParent().OnShowBookDetails(book)

class RightPane(wx.Window):
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
        if self.addNewBookView is not None and self.addNewBookView.IsShown():
            self.sizer.Hide(self.addNewBookView)
        elif self.bookDetailsView.IsShown():
            self.sizer.Hide(self.bookDetailsView)
       
        self.sizer.Show(self.noSelectionText)
        self.sizer.Layout()

    def ShowAddNewBook(self):
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
        if self.noSelectionText.IsShown():
            self.sizer.Hide(self.noSelectionText)
        elif self.addNewBookView is not None and self.addNewBookView.IsShown():
            self.sizer.Hide(self.addNewBookView)
       
        self.bookDetailsView.ShowBook(book)
        self.sizer.Show(self.bookDetailsView)
        self.sizer.Layout()

class BookListView(wx.Panel):
    """description of class"""

    def __init__(self, parent):
        super(BookListView, self).__init__(parent)

        self.sizer = wx.GridSizer(vgap = 10, hgap = 10)
        b = Book()
        b.setTitle("Count Monte Cristo Count Monte Cristo Count Monte Cristo")

        self.sizer.Add(SingleBookView(self, b))

        self.SetSizer(self.sizer)

    def OnSingleBookSelected(self, book):
        self.GetParent().OnSingleBookSelected(book)

class SingleBookView(wx.Panel):
    def __init__(self, parent, book):
        super(SingleBookView, self).__init__(parent)
        self.SetSizeHints(200, 240, 200, 240)
        self.SetBackgroundColour("#483D8B")

        self.book = book

        sizer = wx.BoxSizer(wx.VERTICAL)

        img = wx.EmptyImage(120, 180)
        self.imageCtrl = wx.StaticBitmap(self, wx.ID_ANY, wx.BitmapFromImage(img))
        sizer.Add(self.imageCtrl, 0, wx.ALIGN_CENTER_HORIZONTAL)

        sizer.Add(wx.StaticText(self, label = book.getTitle(), style = wx.ALIGN_CENTER_HORIZONTAL), 1, wx.EXPAND | wx.ALL, border = 10)

        self.SetSizer(sizer)

        self.Bind(wx.EVT_LEFT_UP, self.OnSingleBookSelected, self)

    def OnSingleBookSelected(self, e):
        self.GetParent().OnSingleBookSelected(self.book)

class BookViewBase(wx.Panel):
    """description of class"""

    def _setBorrowedRow(self):
        borrowedLabel = wx.StaticText(self, wx.ID_ANY, "Borrowed:")
        borrowSizer = wx.BoxSizer()
        
        self.borrower = wx.TextCtrl(self, wx.ID_ANY, size = (135, 22))
        borrowSizer.Add(self.borrower)
        self.borrowDate = wx.DatePickerCtrl(self, size = (80, 22), style = wx.DP_DROPDOWN)
        borrowSizer.Add(self.borrowDate, flag=wx.LEFT, border = 5)
        
        self.sizer.Add(borrowedLabel, 1, wx.ALIGN_RIGHT)
        self.sizer.Add(borrowSizer, 1)

    def _setReturnedRow(self):
        returnedLabel = wx.StaticText(self, wx.ID_ANY, "Returned:")
        returnSizer = wx.BoxSizer()
        
        self.returner = wx.TextCtrl(self, wx.ID_ANY, size = (135, 22))
        returnSizer.Add(self.returner)
        returnDate = wx.DatePickerCtrl(self, size = (80, 22), style = wx.DP_DROPDOWN)
        returnSizer.Add(returnDate, flag=wx.LEFT, border = 5)
        
        self.sizer.Add(returnedLabel, 1, wx.ALIGN_RIGHT)
        self.sizer.Add(returnSizer, 1)

    def __init__(self, parent):      
        super(BookViewBase, self).__init__(parent) 
        self.SetSizeHints(400, 700)
        self.boxSizer = wx.BoxSizer(wx.VERTICAL)

        img = wx.EmptyImage(150, 220)
        self.imageCtrl = wx.StaticBitmap(self, wx.ID_ANY, wx.BitmapFromImage(img))
        self.boxSizer.Add(self.imageCtrl, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.BOTTOM, border = 30)

        self.sizer = wx.FlexGridSizer(rows = 10, cols = 2, vgap = 5, hgap = 10)

        self.sizer.AddGrowableCol(0, 1)
        self.sizer.AddGrowableCol(1, 2)

        titleLabel = wx.StaticText(self, wx.ID_ANY, "Title:")
        authorLabel = wx.StaticText(self, wx.ID_ANY, "Authors:")
        genresLabel = wx.StaticText(self, wx.ID_ANY, "Genres:")
        publisherLabel = wx.StaticText(self, wx.ID_ANY, "Publisher:")
        pagesLabel = wx.StaticText(self, wx.ID_ANY, "Pages:")
        isbnLabel = wx.StaticText(self, wx.ID_ANY, "ISBN:")
        placeLabel = wx.StaticText(self, wx.ID_ANY, "Place:")

        # TODO: Add validators
        defCtrlSize = wx.Size(220, 22) 
        self.titleCtrl = wx.TextCtrl(self, wx.ID_ANY, size = defCtrlSize)
        self.authorsCtrl = wx.TextCtrl(self, wx.ID_ANY, size = defCtrlSize)
        self.genresCtrl = wx.TextCtrl(self, wx.ID_ANY, size = defCtrlSize)
        self.publisherCtrl = wx.TextCtrl(self, wx.ID_ANY, size = defCtrlSize)
        self.pagesCtrl = wx.TextCtrl(self, wx.ID_ANY, size = defCtrlSize)
        self.isbnCtrl = wx.TextCtrl(self, wx.ID_ANY, size = defCtrlSize)
        self.placeCtrl = wx.TextCtrl(self, wx.ID_ANY, size = defCtrlSize)

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

        self._setBorrowedRow()
        self._setReturnedRow()

        #self.boxSizer.Add(self.sizer, 1, wx.EXPAND)  
        #self.SetSizerAndFit(self.boxSizer)

class BookDetailsView(BookViewBase):
    """description of class"""

    def __init__(self, parent): 
        super(BookDetailsView, self).__init__(parent) 

        self.currentBook = None

        self.buttonsSizer = wx.BoxSizer()

        btn1 = wx.Button(self, label='Save', size=(70, 30))
        self.buttonsSizer.Add(btn1, flag = wx.LEFT, border = 150)
        #btn2 = wx.Button(self, label='Close', size=(70, 30))
        #self.buttonsSizer.Add(btn2, flag=wx.LEFT, border=5)

        self.sizer.Add(wx.StaticText(self, label = ""))
        self.sizer.Add(self.buttonsSizer, 1)

        self.boxSizer.Add(self.sizer, 1, wx.EXPAND)  
        self.SetSizerAndFit(self.boxSizer)

        self.Bind(wx.EVT_BUTTON, self.SaveChanges, btn1)
        #self.Bind(wx.EVT_BUTTON, self.SaveChanges, btn1)
        
    def ShowBook(self, book):
        self.currentBook = book

        self.titleCtrl.SetLabelText(book.getTitle())
        self.authorsCtrl.SetLabelText(book.getAuthorsStr())
        self.publisherCtrl.SetLabelText(book.getPublisher())
        self.pagesCtrl.SetLabelText(str(book.getNbPages()))
        self.isbnCtrl.SetLabelText(book.getIsbn())

    def SaveChanges(self, e):
        # TODO: Save the changes
        dlg = wx.MessageDialog(self, "Bookah is a simple collection manager for books.", "About Bookah", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()

class NewBookView(BookViewBase):
    """description of class"""

    def __init__(self, parent):      
        super(NewBookView, self).__init__(parent) 

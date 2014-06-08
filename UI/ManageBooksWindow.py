import wx

class ManageBooksWindow(wx.Window):

    def __init__(self, parent):
        wx.Window.__init__(self, parent)

        self.sizer = wx.BoxSizer(wx.VERTICAL);
        self.splitter = wx.SplitterWindow(self)
        self.splitter.SetSashGravity(0.5);
        self.splitter.SetMinimumPaneSize(300);
        self.splitter.SetSashSize(15)
        self.sizer.Add(self.splitter, 1, wx.EXPAND, 0);
 
        self.leftPane = LeftPane(self.splitter);
        self.rightPane = RightPane(self.splitter);
        self.splitter.SplitVertically(self.leftPane, self.rightPane);
 
        self.SetSizer(self.sizer);
        self.sizer.SetSizeHints(self)

    def OnAddNewBook(self):
        NewBookView(self.rightPane)

class LeftPane(wx.Panel):
    def __init__(self, parent):
        super(LeftPane, self).__init__(parent)
        self.SetBackgroundColour("#FFE4C4")

        sizer = wx.BoxSizer(wx.VERTICAL)

        paneLabel = wx.StaticText(self, label = "Collection", style = wx.ALIGN_CENTER_HORIZONTAL)
        self.bookList = BookListView(self)
        sizer.Add(paneLabel, 0, wx.EXPAND)
        sizer.Add(self.bookList, 1, wx.EXPAND)

        self.SetSizer(sizer)

class RightPane(wx.Panel):
    def __init__(self, parent):
        super(RightPane, self).__init__(parent)
        self.SetBackgroundColour("#A52A2A")

class BookListView(wx.Panel):
    """description of class"""

    def __init__(self, parent):
        super(BookListView, self).__init__(parent)

        # Layout
        self.sizer = wx.GridSizer()

        #Layout sizers
        self.SetSizer(self.sizer)
        # self.SetAutoLayout(1)
        self.sizer.Fit(parent)

class BookDetailsView(wx.Panel):
    """description of class"""

    def __init__(self, parent): 
        super(BookDetailsView, self).__init__(parent) 

        self.control = wx.TextCtrl(self);
        self.control.WriteText("Hello World")

class NewBookView(wx.Panel):
    """description of class"""

    def __init__(self, parent):      
        super(NewBookView, self).__init__(parent) 

        self.sizer = wx.GridSizer(1, 2)
        self.sizer.Add(wx.TextCtrl(self, value = "Title:"), 0)
        self.sizer.Add(wx.TextCtrl(self), 1)

        self.SetSizer(self.sizer)
        self.SetAutoLayout(True)
        self.sizer.Fit(parent)


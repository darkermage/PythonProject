 # -*- coding: utf-8 -*-

import wx
from UI import ManageBooksWindow
from UI import ImportWindow

class MainFrame(wx.Frame):
    """The main frame of the application"""

    def __init__(self):
        frameTitle = "Bookah - Collection Manager"
        super(MainFrame, self).__init__(None, title = frameTitle, size = (1000, 700))
        self.SetMinSize((1000, 700))
        self.Center()

        self._initMenu()

        self.mainWindow = MainWindow(self)

        self.Show(True)

    def _initMenu(self):
        self.CreateStatusBar()

        # Menu
        self.filemenu = wx.Menu()
        self.menuManageCollection = wx.MenuItem(None, wx.ID_ANY, "&Manage Collection", "Manage Collection") # Not attached at first
        self.menuAddNewBook = self.filemenu.Append(wx.ID_ANY, "&Add New Book", "Add a new book")
        self.menuImportBook = self.filemenu.Append(wx.ID_ANY, "&Import Book", "Import a book")  
        self.menuExit = self.filemenu.Append(wx.ID_EXIT, "E&xit", "Terminate the program")

        self.aboutmenu = wx.Menu();
        self.menuAbout = self.aboutmenu.Append(wx.ID_ABOUT, "&About", "About this program")

        self.menuBar = wx.MenuBar()
        self.menuBar.Append(self.filemenu, "&File")
        self.menuBar.Append(self.aboutmenu, "&Help");
        self.SetMenuBar(self.menuBar)    

        # Event binding       
        self.Bind(wx.EVT_MENU, self.OnManageColletion, self.menuManageCollection)
        self.Bind(wx.EVT_MENU, self.OnAddNewBook, self.menuAddNewBook)
        self.Bind(wx.EVT_MENU, self.OnImportBook, self.menuImportBook)
        self.Bind(wx.EVT_MENU, self.OnExit, self.menuExit)
        self.Bind(wx.EVT_MENU, self.OnAbout, self.menuAbout)

    def OnManageColletion(self, e):
        """Opens the Collection window"""
        self.mainWindow.ShowManageBooksWindow()
        self.filemenu.RemoveItem(self.menuManageCollection)

        self.filemenu.InsertItem(0, self.menuAddNewBook)
        self.filemenu.InsertItem(1, self.menuImportBook)

    def OnAddNewBook(self, e):
        """Opens the Add new book window"""
        self.mainWindow.OnAddNewBook()

    def OnImportBook(self, e):
        """Opens the Search and import book window"""
        self.mainWindow.ShowImportBookWindow()
        self.filemenu.RemoveItem(self.menuAddNewBook)
        self.filemenu.RemoveItem(self.menuImportBook)

        self.filemenu.InsertItem(0, self.menuManageCollection)

    def OnAbout(self,e):
        """Opens the About window"""
        dlg = wx.MessageDialog(self, "Bookah is a simple collection manager for books.", "About Bookah", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()

    def OnExit(self,e):
        """Exits from the application"""
        self.Close(True)

class MainWindow(wx.Window):
    """The Main window of the application"""
    def __init__(self, parent):
        super(MainWindow, self).__init__(parent)

        self.manageBooksWindow = ManageBooksWindow.ManageBooksWindow(self)
        self.importBookWindow = ImportWindow.ImportWindow(self)

        self.sizer = wx.BoxSizer()
        self.sizer.Add(self.manageBooksWindow, 1, wx.EXPAND)
        self.sizer.Add(self.importBookWindow, 1, wx.EXPAND)
        self.sizer.Hide(self.importBookWindow)

        self.SetSizer(self.sizer);

    def ShowManageBooksWindow(self):
        """Opens the Collection window"""
        self.sizer.Hide(self.importBookWindow)
        self.sizer.Show(self.manageBooksWindow)
        self.manageBooksWindow.leftPane.RefreshBooks()

        self.sizer.Layout()

    def ShowImportBookWindow(self):
        """Opens the Search and Import book window"""
        self.sizer.Hide(self.manageBooksWindow)
        self.sizer.Show(self.importBookWindow)

        self.sizer.Layout()

    def OnAddNewBook(self):
        """Opens the Add new book window"""
        self.manageBooksWindow.OnAddNewBook()
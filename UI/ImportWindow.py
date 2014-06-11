import wx
from GoogleAPI import GoogleAPI
from API import goodReads
import Book
import Database

class ImportWindow(wx.Panel):
        
    def __init__(self, parent):
        super(ImportWindow, self).__init__(parent)
            
        self.InitUI()
        self.Centre()
        self.bookGoodReads = None
        self.bookGoogleBooks = None
        
    def InitUI(self):
        self.sizer = wx.GridBagSizer(4, 4)
        
        self.searchTextField = wx.TextCtrl(self, size=(180, 20))
        self.sizer.Add(self.searchTextField, pos=(0, 0), flag=wx.TOP|wx.LEFT, border = 10)
        
        self.searchButton = wx.Button(self, label="Search")
        self.searchButton.Bind(wx.EVT_BUTTON, self.searchButtonClicked)
        self.sizer.Add(self.searchButton, pos=(0, 1), flag=wx.TOP|wx.LEFT, border = 10)

        sampleList = ['Google books', 'Goodreads']
        self.chooseSite = wx.ComboBox(self, -1, "Goodreads", (30, 30), wx.DefaultSize, sampleList, wx.CB_DROPDOWN)
        self.chooseSite.SetEditable(False)
        self.sizer.Add(self.chooseSite, pos=(1, 0), span = (1, 1), flag=wx.LEFT|wx.TOP|wx.EXPAND, border = 10)

        self.importButton = wx.Button(self, label="Import book")
        self.importButton.Bind(wx.EVT_BUTTON, self.importButtonClicked)
        self.sizer.Add(self.importButton, pos=(1, 1), flag = wx.TOP|wx.LEFT, border = 10)

        sb = wx.StaticBox(self, label = "Goodreads")
        boxsizer = wx.StaticBoxSizer(sb, wx.VERTICAL)
        
        self.titleLabel = wx.StaticText(self, label = "Title: ")
        boxsizer.Add(self.titleLabel, flag = wx.LEFT|wx.TOP, border = 5)

        self.authorLabel = wx.StaticText(self, label = "Author: ") 
        boxsizer.Add(self.authorLabel, flag = wx.LEFT|wx.TOP, border = 5)
        self.sizer.Add(boxsizer, pos=(2, 0), span = (1, 2), flag = wx.EXPAND|wx.TOP|wx.LEFT, border = 10)

        goodreads = wx.StaticBox(self, label = "Google books")
        boxsizerGoodreads = wx.StaticBoxSizer(goodreads, wx.VERTICAL)
        
        self.titleLabelGoodreads = wx.StaticText(self, label = "Title: ")
        boxsizerGoodreads.Add(self.titleLabelGoodreads, flag = wx.LEFT|wx.TOP, border = 5)

        self.authorLabelGoodreads = wx.StaticText(self, label = "Author: ") 
        boxsizerGoodreads.Add(self.authorLabelGoodreads, flag = wx.LEFT|wx.TOP, border = 5)
        
        self.sizer.Add(boxsizerGoodreads, pos=(3, 0), span = (1, 2), flag = wx.EXPAND|wx.TOP|wx.LEFT, border = 10)

        self.SetSizer(self.sizer)

    def searchButtonClicked(self, event):
        api = GoogleAPI()
        api2 = goodReads()
        
        text = self.searchTextField.GetValue().strip()
        
        self.bookGoogleBooks = api.seearchBookByTitle(text)
        self.bookGoodReads = api2.showBookByTitle(text)
       
        self.titleLabel.SetLabel("Title: " + self.bookGoodReads.getTitle())
        self.authorLabel.SetLabel("Author: " + str(self.bookGoodReads.getAuthors()))

        if self.bookGoogleBooks != None:
            self.titleLabelGoodreads.SetLabel("Title: " + self.bookGoogleBooks[0].title)
            self.authorLabelGoodreads.SetLabel("Author: " + str(self.bookGoogleBooks[0].authors[0]))
        else:
            self.titleLabelGoodreads.SetLabel("Title: ")
            self.authorLabelGoodreads.SetLabel("Author: ")  
        
    def importButtonClicked(self, event):
        if self.chooseSite.GetValue() == "Goodreads":
            Database.saveBook(self.bookGoodReads)
        else:
            Database.saveBook(self.bookGoogleBooks[0])
        dlg = wx.MessageDialog(self, "Book imported successfully!", "Success", wx.OK)
        returnCode = dlg.ShowModal()
        dlg.Destroy()
        
if __name__ == '__main__':
    app = wx.App()
    ImportWindow(None, title='Book imports')
    app.MainLoop()

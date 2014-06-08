from wx import App
from UI.MainFrame import MainFrame

class BookLibraryApp(App):

    def OnInit(self):
        frame = MainFrame()
        self.SetTopWindow(frame)
        return True

app = BookLibraryApp(False)
app.MainLoop()
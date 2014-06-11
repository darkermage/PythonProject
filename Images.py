import os
import urllib

class ImageManager(object):
    """description of class"""

    def requireDir(self, path):	
        """The function creates the directory specified in (path) variable if it doesn't exist already"""
        if (not os.path.exists(path)):
            os.makedirs(path)
    
    def downloadPicturebyURL(self, url):
        """The function dowloads the picture that resides on the specified url. The name of the picture is taken from
        the last token of the url and it is saved in the (images) folder"""
        directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images")
        self.requireDir(directory)
        fileName = url.split('/')[-1]
        filePath = os.path.join(directory, fileName)
        
        if not os.path.exists(filePath):
            urllib.urlretrieve(url, filePath)

        return fileName

    def getPicturePath(self, fileName):
        directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images")
        self.requireDir(directory)
        filePath = os.path.join(directory, fileName)

        if os.path.exists(filePath):
            return filePath
        else:
            return None





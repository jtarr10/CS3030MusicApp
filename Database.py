import shelve
import os

class Database:
    ''' Database format - songs
    {'location': '', 'lastID': '0',
     'songs': { 'song/path' : {'id': '', 'title': 'string', 'artist' : 'string', 'album': 'string'}}}
    '''

    ''' Database format - statistics 
    {'id' : {keys to be decided}}
    '''

    def __init__(self, path):
        self.location = path
        self.data = os.path.abspath(self.location + os.sep + 'songs')
        self.stats = os.path.abspath(self.location + os.sep + 'statistics')
        self.dataFile, self.statsFile = self.loadDatabase()
        self.lastID = self.dataFile['lastID']

    # loads the database from file or initializes it if does not exist
    def loadDatabase(self):
        try:
            dataFile = shelve.open(self.data)
            statsFile = shelve.open(self.stats)
            dataFile['lastID']
        except Exception as e:
            dataFile['lastID'] = 0
            dataFile['location'] = self.location
            dataFile['songs'] = {}

        return dataFile, statsFile

    # adds a song to the database using the path as a unique identifier
    def addSongToDatabase(self, songObj):
        if not songObj.path in self.dataFile['songs']:
            load = self.dataFile['songs']
            dataDict = songObj.songToDict()
            dataDict['id'] = self.lastID + 1
            load[songObj.path] = dataDict
            self.dataFile['songs'] = load
            load = self.dataFile['lastID']
            load = self.lastID + 1
            self.dataFile['lastID'] = load

    # removes a song from the database given a songs identifier (path)
    def removeFromDatabase(self, path):
        data = self.dataFile['songs']
        if path in data:
            del data[path]
            self.dataFile['songs'] = data

    # closes the database files
    def closeDatabase(self):
        self.dataFile.close()
        self.statsFile.close()

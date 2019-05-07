import shelve
import os

""" Database format - songs
    {'location': string,
     'lastID': int,
     'totalSongs: int',
     'songs': {
        'song/path' : {
            'id': '',
            'title': 'string',
            'artist' : 'string',
            'album': 'string',
            'stats': {
                rating : int,
                plays : int,
                favorite : bool
                }
            }
        }
     }
"""

""" Database format - playlist
{playlistname : id}
"""

class Database:

    def __init__(self, path):

        try:
            mlmConfig = open('mlm.config', 'r')
            self.location = mlmConfig.readline()
            self.data = os.path.abspath(self.location + os.sep + 'mlm_song_data')
            self.pList = os.path.abspath(self.location + os.sep + 'mlm_play_lists')
        except Exception as e:
            mlmConfig = open('mlm.config', 'w')
            mlmConfig.write(path)
            self.location = path
            self.data = os.path.abspath(self.location + os.sep + 'mlm_song_data')
            self.pList = os.path.abspath(self.location + os.sep + 'mlm_play_lists')
        finally:
            mlmConfig.close()

        self.dataFile, self.playLists = self.loadDatabase()
        #self.lastID = self.dataFile['lastID']

    # loads the database from file or initializes it if does not exist
    def loadDatabase(self):

        try:
            dataFile = shelve.open(self.data)
            playLists = shelve.open(self.pList)
            throwAway = dataFile['lastID']
        except Exception as e:
            dataFile['lastID'] = 0
            dataFile['location'] = self.location
            dataFile['songs'] = {}

        return dataFile, playLists

    # adds a song to the database using the path as a unique identifier
    def addSongToDatabase(self, songObj):
        updateUntaged = self.location + os.sep + 'Unlabeled Files' + os.sep + songObj.path.split(os.sep)[-1]
        if updateUntaged in self.dataFile['songs']:
            update = self.dataFile['songs']
            if songObj.path != updateUntaged:
                update[songObj.path] = update[updateUntaged]
                self.dataFile['songs'] = update
                self.removeFromDatabase(updateUntaged)
                self.updateEntry(songObj)

        if songObj.path not in self.dataFile['songs']:
            nextID = self.dataFile['lastID'] + 1
            dataDict = songObj.songToDict()
            dataDict['id'] = nextID

            update = self.dataFile['songs']
            update[songObj.path] = dataDict
            self.dataFile['songs'] = update

            # Update lastID in database
            update = self.dataFile['lastID']
            update = nextID
            self.dataFile['lastID'] = update
        else:
            self.updateEntry(songObj)
        self.dataFile.sync()

    def updateEntry(self,songObj):
        update = self.dataFile['songs']
        dataDict = songObj.songToDict()
        dataDict['id'] = update[songObj.path]['id']
        update[songObj.path] = dataDict
        self.dataFile['songs'] = update
        self.dataFile.sync()
        self.playLists.sync()

    # removes a song from the database given a songs identifier (path)
    def removeFromDatabase(self, path):
        data = self.dataFile['songs']
        if path in data:
            del data[path]
            self.dataFile['songs'] = data

    def searchDatabase(self, term, key=''):
        pass


    def listData(self, key='songs', dataFilter='title', key2='title'):
        if key == 'songs':
            data = self.dataFile[key]
            for song in data:
                print(data[song][dataFilter])
        if key == 'location':
            data = self.dataFile[key]
            print(data)

    def returnData(self, key='songs', dataFilter='title', key2='title'):
        dataList = []
        if key == 'songs':
            data = self.dataFile[key]
            for song in data:
                dataList.append(data[song][dataFilter])
                dataList.sort()
            return dataList
        if key == 'location':
            data = self.dataFile[key]
            print(data)


    # closes the database files
    def closeDatabase(self):
        self.dataFile.close()
        self.playLists.close()

    # TODO add way to update songs in database
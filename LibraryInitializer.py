'''
Final Project: Music Library Manager
Contributors: Jason Tarr, Mitchel Walker


Resources:
mutagen - audio file metadata library
'https://musicbrainz.org/search' - Database for album artworks


Planned Features:
1. File organization - Renaming, Categorizing, Directory manipulation
    a. Organizing the File directory and saving the final location
    b. File Parsing/ Dictionary Population
2. Web scraping - Album artwork, Lyrics, Artist information
3. File launching 
4. Listening statistics - Other usage information
5. Playlist creation 
6. Play options - Shuffle, Random, By genre, By Artist

Features Implemented:
1. File Organizer: The Library class has an organize function that will organize the file directory given as the home with the artist and albums.
    a. Organizing the File directory and saving the final location
    b. Library Stat Database Created
2.Interface with Music Brainz Database
    a. getAlbumArtwork method populates all possible album folders with available online album artwork files
    b. getMusicBrainzReleaseID method will search Music Brainz database for the correct album id. This is stored in song object's MBID attribute and used to look up the album using MB functions.
'''


import mutagen
import os
import re
import shutil
import shelve
import json
import bs4
import musicbrainzngs
import pyacoustid


acousticAPIKey = 'FCX67RczyA'

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

#The song object holds the metadata of each individual song file scanned
class Song:
    #When a song is created, mutagen fills in the meta data information
    def __init__(self, root, file):

        #we create a mutagen file object for the file
        self.ms = mutagen.File(open(os.path.join(root, file), 'rb'), easy=True)
        
        #we attempt to read metaData from the file
        try:
            self.title = self.ms['title'][0]
        except:
            self.title = file
        try:
            self.artist = self.ms['artist'][0]
        except:
            self.artist = ''
        try:
            self.album = self.ms['album'][0]
        except:
            self.album = ''

        self.path = os.path.join(root, file)
        self.filename = file
        #the following two attributes are only used if the user looks for album artwork, and MBID will only happen on the first song of every album.
        self.MBID = None
        self.artworkPath = ''
        #self.identifier = re.sub(r'[^A-Za-z0-9]', '', self.title + self.artist + self.album, )

    # returns the songs meta data as a dictionary
    def songToDict(self):
        return {'title' : self.title, 'artist' : self.artist, 'album' : self.album, 'id': 0}

    #returns the musicbrainz song id for further use in data lookups
    def getMusicBrainzReleaseID(self):
        #Here we setup our useragent for the webqueries 
        musicbrainzngs.set_useragent('CS3030MusicApp', 'V0.2')

        #we construct a query string from existing metadata
        if(self.album != '' and self.artist != ''):
            temp = '{0} AND artist:{1}'.format(self.album, self.artist)
        elif(self.album != ''):
            temp = '"{}"'.format(self.album)
        else:
            print('Insufficient MetaData for {}'.format(self.filename))
            return ''

        #if there is enough information to create a viable query string, we search the musicBrainz database
        results = musicbrainzngs.search_releases(query=temp, limit=50)
        
        #if any of the results are produced by the same artist, the id is saved
        for release in results['release-list']:
            #we try to get a succesful response from the database without any HTTP errors
            try:
                musicbrainzngs.get_image_front(release['id'])
                hasImage = True
            #if it doesn't work we move on to the next result
            except:
                hasImage = False

            if(release['artist-credit-phrase'] == self.artist and hasImage):
                print('Image match found!')
                return release['id']

        #if nothing is returned we print to a notification to console
        print('No viable database results available for {}'.format(self.album))
        return ''
    



#The library houses all the data and methods needed for manipulating the library
class Library:

    def __init__(self, homeDir, filePattern='(.*)(.mp3|.flac|.wav|.ogg|.m4a|.m4b|.m4p|.mp4)$'):
        self.homeDirectory = homeDir
        self.songFileRE = re.compile(filePattern)
        self.songs = []
        print('Scanning Files in Library...')
        self.update()
        

    #The update method looks through the home directory and populates a dictionary of contents
    def update(self):
        self.songs = []

        #We walk through the directories and parse through each file
        for root, dirs, files in os.walk(self.homeDirectory):
            for file in files:
                temp = self.songFileRE.search(file)
                #if the file is of the proper type, we create a new song object and append it to the contents of the library
                if(temp != None):
                    self.songs.append(Song(root, file))


    #The organize method will move all files into a typical artist based directory organization
    #DO NOT RUN THIS AFTER ALBUM ARTWORK DIRECTORIES HAVE BEEN CREATED
    def organize(self):
        print('Reorganizing library directories')

        data = Database(self.homeDirectory)
        
        #move all files to the root directory
        for song in self.songs:
            shutil.move(song.path, os.path.join(self.homeDirectory, song.filename))

        #delete all the child directories
        for root, dirs, files in os.walk(self.homeDirectory):
            for dir in dirs:
                shutil.rmtree(os.path.join(root, dir))
                
                
        #we update the song list
        self.update()

        #increment through all songs and organize them
        for song in self.songs:
            #Initialize the directories needed to build the organization tree

            artistDir = os.path.join(self.homeDirectory, song.artist)
            albumDir = os.path.join(artistDir, song.album)
            songDir = os.path.join(albumDir, song.filename)

            #if there is no directories available to sort the song, one is created
            if(not os.path.exists(artistDir)):
                os.mkdir(artistDir)
            if(not os.path.exists(albumDir)):
                    os.mkdir(albumDir)

            #move the song to the proper location and move on to the next song
            shutil.move(song.path, songDir)
            # add song to database
            data.addSongToDatabase(song)
        
        #Finally update the song list to reflect the final directory layout
        self.update()

        # release the database
        data.closeDatabase()

        print('Finished Reoganization...')

    #This method will look up the album artwork for each of the folders without an existing photo from the MB database
    def getAlbumArtwork(self):
        #notifying the user
        print('Searching Music Brainz database for album artwork\n This could take several minutes...')
        for song in self.songs:
           
            artworkFolder = os.path.join(song.path.rstrip(song.filename), 'artwork')
            song.artworkPath = os.path.join(artworkFolder, song.album + '.jpg')

            #if album artwork already exists, we continue to the next song
            if(not os.path.exists(artworkFolder)):
                os.mkdir(artworkFolder)
            
            if(not os.path.exists(song.artworkPath)):
                print('Searching: {}'.format(song.album))
                #we first initiate a search query to find the database id for the album in question
                song.MBID = song.getMusicBrainzReleaseID()
                if(song.MBID != ''):
                    #then we lookup the artwork using the song's release id and download the raw data
                    try:
                        print('Downloading the image file to {}'.format(song.artworkPath))
                        rawAlbumArt = musicbrainzngs.get_image_front(song.MBID)
                        #we open a .jpg file and write the binary data to the file
                        file = open(song.artworkPath, 'wb')
                        file.write(rawAlbumArt)
                        file.close()
                    except Exception as ex:
                        print('Problems downloading artwork: {}'.format(ex))
                        continue
                

        






#Temporary user input through the command line
directoryInput = input('Please enter the absolute pathway to your music library: ')
myLibrary = Library(directoryInput)

print('Library Contains: {} songs'.format(len(myLibrary.songs)))
print('Would you like to organize your library?  Y or N')
answer = input()
if(answer == 'Y' or answer == 'y'):
    myLibrary.organize()
    answer = ''

print('Would you like to search for album artwork online? Y or N')
answer = input()
if(answer == 'Y' or answer == 'y'):
    myLibrary.getAlbumArtwork()
    answer = ''
else:
    print('Program Finished...')
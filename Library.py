import re
import os
import shutil
import musicbrainzngs
from Database import Database
from Song import Song



#The library houses all the data and methods needed for manipulating the library
class Library:

    def __init__(self, homeDir, filePattern='(.*)(.mp3|.flac|.wav|.ogg|.m4a|.m4b|.m4p|.mp4)$'):
        self.dataBase = Database(homeDir)
        self.homeDirectory = self.dataBase.dataFile['location']
        self.songFileRE = re.compile(filePattern)
        self.artworkDirRE = re.compile('^(.*)--$')
        self.songs = []

        print('Scanning Files in Library...')
        self.update()
        

    #The update method looks through the home directory and populates a dictionary of contents
    def update(self, trgtdatabase=False):
        self.songs = []

        #We walk through the directories and parse through each file
        for root, dirs, files in os.walk(self.homeDirectory):
            for file in files:
                temp = self.songFileRE.search(file)
                #if the file is of the proper type, we create a new song object and append it to the contents of the library
                if(temp != None):
                    if trgtdatabase:
                        self.dataBase.addSongToDatabase(Song(root, file))
                    
                    self.songs.append(Song(root, file))


    #The organize method will move all files into a typical artist based directory organization
    def organize(self):
        print('Reorganizing library directories')
        
        #move all files to the root directory
        for song in self.songs:
            shutil.move(song.path, os.path.join(self.homeDirectory, song.filename))

        #delete all the child directories except the folder holding album artwork
        for root, dirs, files in os.walk(self.homeDirectory):
            for dir in dirs:
                temp = self.artworkDirRE.search(os.path.join(root, dir))
                if(temp == None):
                    shutil.rmtree(os.path.join(root, dir))
                
                
        #we update the song list
        self.update()

        #increment through all songs and organize them
        for song in self.songs:
            #if the file doesn't have complete metadata, the file will be sorted into a directory called Unlabeled Files
            if(song.artist == '' or song.album == ''):
                artistDir = os.path.join(self.homeDirectory, 'Unlabeled Files')
                albumDir = artistDir
            else:
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

        #Finally update the song list and database to reflect the final directory layout
        self.update()
        self.update(True)


        print('Finished Reoganization...')

    #This method will look up the album artwork for each of the folders without an existing photo from the MB database
    def getAlbumArtwork(self):
        #notifying the user
        print('Searching Music Brainz database for album artwork\n This could take several minutes...')
        for song in self.songs:
            #we should skip any files that don't have the appropriate metadata
            if(song.artist == '' or song.album == ''):
                print('Skipping {}'.format(song.filename))
                continue
           
            artworkFolder = os.path.join(self.homeDirectory, 'Album Artwork--')
            artistFolder = os.path.join(artworkFolder, song.artist + '--')
            song.artworkPath = os.path.join(artistFolder, song.album + '.jpg')

            #if album artwork already exists, we continue to the next song
            if(not os.path.exists(artworkFolder)):
                os.mkdir(artworkFolder)
            if(not os.path.exists(artistFolder)):
                os.mkdir(artistFolder)
            
            if(not os.path.exists(song.artworkPath)):
                print('Searching: {}'.format(song.album))
                #we first initiate a search query to find the database id for the album in question
                song.MBID = song.getMusicBrainzReleaseID(imageSearch=True)
                #If the song search comes back with an ID we continue
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
                #else we create a placeholder file that prevents further search attempts
                else:
                    file = open(song.artworkPath, 'wb')
                    file.write(b'NO ARTWORK FOUND')
                    file.close()
            self.dataBase.updateEntry(song)
                

    #this method will go through all songs in the scanned library and try to find metadata, if there is not enough information to find anything the user will be prompted to enter it
    def updateUnlabeledFiles(self):
        #we go through the library and look for all songs that are missing information
        for song in self.songs:
            #if the song is missing critical information we first ask the user if they know it or not
            if(song.artist == '' or song.album == ''):
                print('Attempting to update info for file: {}'.format(song.filename))
                print('The more info you can provide. The more accurate the information found will be.')
                song.title = input('What is the song name for filename <{}> (Hit enter if name is unknown):'.format(song.filename))
                if(song.artist == ''):
                    song.artist = input('If possible, please enter the artist for {} (Hit enter if no artist is known): '.format(song.title))
                if(song.album == ''):
                    song.album = input('Please enter the album name for {} (Required): '.format(song.title))
               
                song.MBID = song.getMusicBrainzReleaseID()
                try:
                    if(song.MBID != ''):
                        song.updateMetaData(song.MBID)
                except Exception as ex:
                    print('Problem finding metadata: {}'.format(ex))
            else:
                continue
        #finally we try to organize the new files and update the database with information
        self.organize()

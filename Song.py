import mutagen
import os, stat
import musicbrainzngs
from re import sub
from mutagen.mp4 import MP4
from pprint import pprint as pp




#The song object holds the metadata of each individual song file scanned
class Song:
    #When a song is created, mutagen fills in the meta data information
    def __init__(self, root, file):
        # if file is read-only allow writes
        filePerm = os.path.join(root, file)
        if not os.access(filePerm, os.W_OK):
            os.chmod(filePerm, stat.S_IWRITE)
        #we create a mutagen file object for the file
        ms = mutagen.File(os.path.join(root, file), easy=True)
        #we attempt to read metaData from the file
        try:
            self.title = ms['title'][0]
        except:
            self.title = file
        try:
            self.artist = sub(r'[<>\\:/"|?*]', '_', ms['artist'][0])
        except:
            self.artist = ''
        try:
            self.album = sub(r'[<>\\:/"|?*]', '', ms['album'][0])
        except:
            self.album = ''
        
        ms.save()

        self.path = os.path.join(root, file)
        self.filename = file
        #the following two attributes are only used if the user looks for album artwork, and MBID will only happen on the first song of every album.
        self.MBID = ''
        self.artworkPath = ''
        #self.identifier = re.sub(r'[^A-Za-z0-9]', '', self.title + self.artist + self.album, )

    # returns the songs meta data as a dictionary
    # add the song attributes that you want in the data base here
    def songToDict(self):
        return {'title': self.title, 'artist' : self.artist, 'album' : self.album, 'id': 0, 'artwork': self.artworkPath}

    def setMetaData(self, newTitle='', newArtist='', newAlbum=''):
        #if any of the parameters are not used in the function call, we set them to what they already are
        if(newTitle == ''):
            newTitle = self.title
        if(newArtist == ''):
            newArtist == self.artist
        if(newAlbum == ''):
            newAlbum == self.album

        #we open a mutagen version of the song object
        ms = mutagen.File(self.path, easy=True)

        if(not isinstance(ms, MP4)):
            ms['title'] = newTitle
            ms['artist'] = newArtist
            ms['album'] = newAlbum
            self.album = newAlbum
            self.artist = newArtist
            self.title = newTitle
        else:
            print('Itunes overlord does not approve of you messing with their files: {}'.format(self.path))

        ms.save(self.path)
        print('File info updated...')
        

    #this function will lookup the musicbrainz id of a recording and update the file's metadata
    def updateMetaData(self, musicBrainzId):
        #we look up the song and download the dictionary of recording stats
        musicbrainzngs.set_useragent('CS3030MusicApp', 'V0.5')
        result = musicbrainzngs.get_release_by_id(musicBrainzId, includes=['artist-credits', 'release-rels'])
        #then we call the metadata update function to complete the process
        self.setMetaData(self.title, result['release']['artist-credit-phrase'], result['release']['title'])

    # this function will present the user a choice of recordings from which to extract metadata
    def updateMetaDataInteractive(self):

        print('Last try. Is the file in this list.')

        #we look up the song and download the dictionary of recording stats
        musicbrainzngs.set_useragent('CS3030MusicApp', 'V0.5')

        if (self.artist != '' or self.title != ''):
            temp = '{0} AND artist:{1}'.format(self.title.replace(' ', '_'), self.artist)

        results = musicbrainzngs.search_recordings(query=temp, limit=25)
        lineNum = 1
        releaseList = []
        for release in results['recording-list']:
            try:
                print(str(lineNum) + '\tTitle: ' + release['title'],
                      'Artist: ' + release['artist-credit'][0]['artist']['name'], 'ID: ' + release['id'],
                      'Album: ' + release['release-list'][0]['title'])
                lineNum += 1
                releaseList.append(release)
            except Exception as e:
                pass

        userInput = input("Which song matches your file? ")
        try:
            userInput = int(userInput)
            result = releaseList[int(userInput) - 1]
            self.setMetaData(result['title'], result['artist-credit-phrase'], result['release-list'][0]['title'])
        except Exception as e:
            print('Choice not found.')

    #returns the musicbrainz song id for further use in data lookups
    def getMusicBrainzReleaseID(self, imageSearch=False):
        #Here we setup our useragent for the webqueries 
        musicbrainzngs.set_useragent('CS3030MusicApp', 'V0.5')

        #we construct a query string from existing metadata
        if(self.album != '' and self.artist != ''):
            temp = '{0} AND artist:{1}'.format(self.album, self.artist)
        elif(self.album != ''):
            temp = '"{}"'.format(self.album)
        elif(self.artist != '' and self.title != ''):
            temp = '{0} AND artist:{1}'.format(self.title.replace(' ', '_'), self.artist)
        else:
            print('Insufficient MetaData for {}'.format(self.filename))
            return ''
        
        print('Looking for online profile for {}'.format(self.title))
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

            if(release['title'] == self.album and hasImage):
                print('Release match found!')
                return release['id']

        # If nothing is found in releases try recordings but not if the function is called for album art
        if not imageSearch:
            self.updateMetaDataInteractive()
            return ''
        else:
            #if nothing is returned we print a notification to console
            print('No viable database results available for {}'.format(self.album))
            return ''

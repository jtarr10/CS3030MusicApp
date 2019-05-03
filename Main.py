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
    b. getMusicBrainzReleaseID method will search Music Brainz database for the correct album id and returns it
    c. updateMetaData metod will lookup a recording id given and change the file's metadata to the database stats (it is required that at least the album name is set)
    d. updateUnlabeledFiles method from the library object will look through all songs and attempt to fill in the title, artist, and release name with the help of the user and the internet
'''





from Song import Song
from Library import Library
from Database import Database


#Temporary user input through the command line
directoryInput = input('Please enter the absolute pathway to your music library: ')
myLibrary = Library(directoryInput)

print('Library Contains: {} songs'.format(len(myLibrary.songs)))
print('Would you like to organize your library?  Y or N')
answer = input()
if(answer == 'Y' or answer == 'y'):
    myLibrary.organize()
    answer = ''
print('Would you like to look up information for your unlabled files? (Y or N): ')
answer = input()
if(answer == 'Y' or answer == 'y'):
    myLibrary.updateUnlabeledFiles()
    answer = ''
print('Would you like to look up album artwork for your library? (Y or N)')
answer = input()
if(answer == 'Y' or answer == 'y'):
    myLibrary.getAlbumArtwork()
    answer = ''
    print('Program Finished...')
else:
    print('Program Finished...')

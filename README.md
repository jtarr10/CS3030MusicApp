# CS3030MusicApp
Music organizer for python

Welcome to our music library manager. To run this program please assure that you have all of the following dependencies installed in your python package directory: mutagen, musicbrainzngs, pyglet, Command, python-docx. 

To run this program, simply run the Main.py file and the cmd interface will start. By using the command help followed by the name of the command, you can learn more information of command usage. 



Resources:
mutagen - audio file metadata
'https://musicbrainz.org/search' - Database for album artwork


Game Plan:

1. File organization - Renaming, Categorizing, Directory manipulation
    a. Organizing the File directory and saving the final location
    b. File Parsing/ Dictionary Population
2. Web scraping - Album artwork, Lyrics, Artist information
3. File launching 
4. Listening statistics - Other usage information
5. Playlist creation 
6. Play options - Shuffle, Random, By genre, By Artist


Implemented Features:
1. File Organization 
2. Database Populated with song information and listening statistics
3. MusicBrainz interface
    a. getAlbumArtwork will get relavent album cover art for library's albums
    b. updateMetaData will get metadata from the musicbrainz profile of a song and update the metadata of the file
    c. updateMetaDataInteractive gets a list of 25 results based off of known information and asks user for clarrification
        (automatically runs after an unsuccesful search by updateMetaData)
4. Song Player: play, stop, pause, resume commands
5. Directory Printer
    a. printDirectory <path> will print a directory word file in the given path that will contain a sorted list of songs from the library
    
    
    


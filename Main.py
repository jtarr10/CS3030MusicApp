'''
Final Project: Music Library Manager
Contributors: Jason Tarr, Mitchel Walker


Resources:
mutagen - audio file metadata library
'https://musicbrainz.org/search' - Database for album artworks


Planned Features:
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
    b. Library Database Created
2.Interface with Music Brainz Database
    a. getAlbumArtwork method populates all possible album folders with available online album artwork files
    b. getMusicBrainzReleaseID method will search Music Brainz database for the correct album id and returns it
    c. updateMetaData metod will lookup a recording id given and change the file's metadata to the database stats (it is required that at least the album name is set)
    d. updateUnlabeledFiles method from the library object will look through all songs and attempt to fill in the title, artist, and release name with the help of the user and the internet
'''


from Command import MLMPrompt


# startup message
print("Enter commands into the command-line interpreter to get started.")
print("Use the 'help' command if you run into problems.")
print("Use the 'setup' command to run the default library setup")

# command line shell interaction
if __name__ == '__main__':
    prompt = MLMPrompt()
    prompt.prompt = '[MLM] >> '
    prompt.cmdloop('Starting Music Library Manager (MLM)')

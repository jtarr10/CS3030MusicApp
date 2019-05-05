from cmd import Cmd
import json
import sys
import musicbrainzngs
import shelve
import pprint

from Song import Song
from Library import Library
from Database import Database


class MLMPrompt(Cmd):
    """command functions"""
    def do_help(self,args):
        arguments = args.split()
        helpFile = open("mlm_help.json", 'r')
        helpDict = json.load(helpFile)
        validHelp = helpDict['help_text']
        if not args:
            print('all cmds')
        elif arguments[0] in validHelp:
            print(helpDict['help_text'][arguments[0]])
        else:
            print('\"{}\" is not a valid help topic'.format(arguments[0]))

    def do_commands(self,args):
        # TODO create list of commands
        print('''help\ncommand\nimport\nlist\nls\nquit''')


    def do_import(self, args):
        # TODO import commands
        print('imports song into the music library manager')

    def do_quit(self, args):
        """Quits the program."""
        print("Quitting.")
        raise SystemExit


    def do_list(self, args):
        # TODO add list command logic
        """Lists the library structure"""
        """Options: artist, album"""
        print('this will print your library structure')

    def do_ls(self, args):
        """Alias for list command"""
        self.do_list(args)

    def do_library(self, args):
        # TODO add library command logic
        # status
        # label
        # print - songs, albums, artist
        # Here we setup our useragent for the webqueries
        musicbrainzngs.set_useragent('CS3030MusicApp', 'V0.5')

        temp = '{0} AND artist:{1}'.format('Birnie Bouzle / When Will We Be Married Molly', 'Darby O\'Gill')

        # if there is enough information to create a viable query string, we search the musicBrainz database
        results = musicbrainzngs.search_recordings(query=temp, limit=50)

        # if any of the results are produced by the same artist, the id is saved
        for release in results['recording-list']:
            print(release)

    def do_setup(self, args):
        # Temporary user input through the command line
        directoryInput = input('Please enter the absolute pathway to your music library: ')
        myLibrary = Library(directoryInput)

        print('Library Contains: {} songs'.format(len(myLibrary.songs)))
        print('Would you like to organize your library?  Y or N')
        answer = input()
        if (answer == 'Y' or answer == 'y'):
            myLibrary.organize()
            answer = ''
        print('Would you like to look up information for your unlabled files? (Y or N): ')
        answer = input()
        if (answer == 'Y' or answer == 'y'):
            myLibrary.updateUnlabeledFiles()
            answer = ''
        print('Would you like to look up album artwork for your library? (Y or N)')
        answer = input()
        if (answer == 'Y' or answer == 'y'):
            myLibrary.getAlbumArtwork()
            answer = ''
            print('Program Finished...')
        else:
            print('Program Finished...')
        myLibrary.dataBase.closeDatabase()

    def do_db(self, args):
        """Temporary full database print"""
        dataPath = input("Enter database location:")
        dataPath = r'C:\Users\Mitchell\Music\test' if not dataPath else dataPath
        data = Database(dataPath)
        pprint.pprint(data.dataFile['songs'])
        a = data.returnData()
        pprint.pprint(a)


    """helper functions"""


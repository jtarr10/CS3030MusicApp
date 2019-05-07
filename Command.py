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

    def __init__(self):
        super(MLMPrompt, self).__init__()
        self.do_setup('')

    """command functions"""
    def do_help(self,args):
        arguments = args.split()
        helpFile = open("mlm_help.json", 'r')
        helpDict = json.load(helpFile)
        validHelp = helpDict['help_text']
        if not args:
            self.do_commands(args)
        elif arguments[0] in validHelp:
            print(helpDict['help_text'][arguments[0]])
        else:
            print('\"{}\" is not a valid help topic'.format(arguments[0]))


    def do_commands(self,args):
        # TODO create list of commands
        print('''help\ncommands\norganize\ngetMetaData\ngetAlbumArtwork\nlist\nls\nquit''')

    def do_organize(self, args):
        self.myLibrary.organize()

    def do_getMetaData(self, args):
        self.myLibrary.updateUnlabeledFiles()

    def do_getAlbumArtwork(self, args):
        self.myLibrary.getAlbumArtwork()

    def do_quit(self, args):
        """Quits the program."""
        print("Quitting.")
        self.myLibrary.database.closeDatabase()
        sys.exit(0)


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
        pass

    def do_setup(self, args):
        # Temporary user input through the command line
        try:
            dirFile = open('mlm.config', 'r')
            dir = dirFile.readline()
            self.myLibrary = Library(dir)
        except:
            directoryInput = input('Please enter the absolute pathway to your music library: ')
            self.myLibrary = Library(directoryInput)
        
        

        print('Library Contains: {} songs'.format(len(self.myLibrary.songs)))

    def do_db(self, args):
        """Temporary full database print"""
        dataPath = input("Enter database location:")
        dataPath = r'C:\Users\Mitchell\Music\test' if not dataPath else dataPath
        data = Database(dataPath)
        pprint.pprint(data.dataFile['songs'])
        a = data.returnData()
        pprint.pprint(a)


    """helper functions"""


from cmd import Cmd
import json
import sys
from Library import Library
from Player import mlmPlayer
from Directory import Directory


class MLMPrompt(Cmd):

    def __init__(self):
        super(MLMPrompt, self).__init__()
        self.setup('')
        self.player = None
        try:
            helpFile = open("mlm_help.json", 'r')
            self.helpDict = json.load(helpFile)
        except:
            print("Help file not found. Please redownload \"mlm_help.json\"")
            self.helpDict = None

    def setup(self, args):
        try:
            dirFile = open('mlm.config', 'r')
            dir = dirFile.readline()
            self.myLibrary = Library(dir)
        except:
            directoryInput = input('Please enter the absolute pathway to your music library: ')
            self.myLibrary = Library(directoryInput)

    def do_help(self,args):
        # This command function helps the user understand the various features of the program
        if self.helpDict:
            arguments = args.split()
            validHelp = self.helpDict['help_text'].keys()
            print(validHelp)
            if not args:
                self.do_commands(args)
            elif arguments[0] in validHelp:
                print(self.helpDict['help_text'][arguments[0]])
            else:
                print('\"{}\" is not a valid help topic'.format(arguments[0]))
        else:
            print("Help not currently available.")

    def do_commands(self,args):
        # displays a list of commands
        for item in self.helpDict['help_text'].keys():
            print(item)

    def do_organize(self, args):
        # initiates the library's organize feature
        self.myLibrary.organize()

    def do_getMetaData(self, args):
        # initiates the library's find metadata feature
        self.myLibrary.updateUnlabeledFiles()

    def do_getAlbumArtwork(self, args):
        # initiates the library's find artwork feature
        self.myLibrary.getAlbumArtwork()

    #use this function by calling printDirectory <savePath>
    def do_printDirectory(self, args):
        
        myDir = Directory(self.myLibrary.songs)
        myDir.print(args)

    def do_quit(self, args):
        # quits the program.
        print("Closing MLM.")
        self.myLibrary.dataBase.closeDatabase()
        sys.exit(0)

    def do_list(self, args):
        print('this will print your library structure')

    def do_ls(self, args):
        # alias for list command
        self.do_list(args)

    def do_play(self, args):
        songDict = self.myLibrary.dataBase.searchDatabase(args)
        print('Match Found at: ', songDict['path'])
        print(songDict['title'], 'Is now playing.')

        if self.player:
            self.do_stop('')
            self.player = None

        self.player = mlmPlayer(songDict['path'], 1)
        self.player.play_song()

    # def do_skip(self, args):
    #     # FIXME have not figured out how skip works
    #     if self.player:
    #         seek = int(args)
    #         self.player.jump(seek)

    def do_stop(self, args):
        # stops the currently playing song
        self.player.stop()

    def do_pause(self, args):
        # stops the currently playing song
        self.player.pause()

    def do_resume(self, args):
        # stops the currently playing song
        self.player.resume()
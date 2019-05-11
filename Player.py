import pyglet.media as media

class mlmPlayer:
    def __init__(self, path, volume):
        # Song Playing Song
        self.path = path
        # Song Volume Update
        self.volume = volume
        # pyglet Media Player
        self.player = media.Player()
        self.player.volume = volume

    def jump(self, time):
        try:
            self.player.seek(time)
            return
        except:
            print('Jump is Not Possible')
            return

    def pause(self):
        self.player.pause()
        return

    def play(self):
        self.player.play()
        return

    def stop(self):
        self.reset_player()
        return

    def volume_(self, *args, **kwargs):
        try:
            volume = self.volume.get()
            self.player.volume = volume
        except:
            pass
        return


    def reset_player(self):
        self.player.pause()
        self.player.delete()
        return

    def play_song(self, *args, **kwargs):
        if self.path:
            try:
                self.reset_player()
                try:
                    src = media.load(self.path)
                    self.player.queue(src)
                    self.play()
                    return
                except Exception as e:
                    print("Something went wrong when playing song", e)
                    return
            except Exception as e:
                print('Please Check Your File Path', self.path)
                print('Error: Problem On Playing \n ', e)
                return
        else:
            print('Please Check Your File Path', self.path)
        return


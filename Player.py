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
        self.songPosition = 0

    def jump(self, time):
        try:
            self.player.seek(time)
            return
        except:
            print('Jump is Not Possible')
            return

    def pause(self):
        self.player.pause()
        self.songPosition = self.player.time
        return

    def play(self):
        self.player.play()
        return

    def resume(self):
        if self.songPosition != 0:
            self.play()
            self.player.seek(self.songPosition)
        return

    def stop(self):
        self.reset_player()
        self.songPosition = 0
        return

    def volume(self, volume):
        self.player.volume = volume
        return

    def reset_player(self):
        self.player.pause()
        self.player.delete()
        return

    def play_song(self):
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


import requests
from pytube import YouTube


class InputVideo:
    def __init__(self, location):
        self.location = location
        self.isYoutube = self.check_video_url()

    def check_video_url(self):
        checker_url = "https://www.youtube.com/oembed?url="
        video_url = checker_url + self.location
        request = requests.get(video_url)
        if request.status_code == 200:
            yt = YouTube(self.location)
            self.location = yt.streams.get_by_itag(137).url
            return True
        return False

    def get_location(self):
        return self.location

    def is_youtube_video(self):
        return self.isYoutube

import webbrowser

class Movie():
    """ This class provies a way to store movie related information """

    VALID_RATINGS = ["G", "PG", "PG-13", "R"]

    def __init__(self, title, story_line, poster_url, trailer_url):
        self.title = title
        self.story_line = story_line
        self.poster_url = poster_url
        self.trailer_url = trailer_url

    def __str__(self):
        text = ""
        text = text + self.title + " | "
        text = text + self.story_line + " | "
        text = text + self.poster_url + " | "
        text = text + self.trailer_url + " | "
        return text

    def show_trailer(self):
        webbrowser.open(self.trailer_url)

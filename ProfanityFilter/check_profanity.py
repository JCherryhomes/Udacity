from os import path
import urllib

def read_text():
    dir_path = path.dirname(__file__)
    quotes = open(dir_path + "\\movie_quotes.txt")
    
    contents = quotes.read()
    quotes.close()
    speak_pirate(contents)

def speak_pirate(text):
    response = urllib.urlopen("http://postlikeapirate.com/AJAXtranslate.php?typing=" + text)
    output = response.read()
    print(output)
    response.close()

read_text()
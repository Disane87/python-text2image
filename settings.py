import os 
import json
from json import JSONEncoder
from collections import defaultdict

class Settings:

    txt_color = ""
    fontfile = ""
    border = True
    border_color = "" 
    border_size = 0
    output_dir = ""
    text_alignment = ""
    preview_mode = True

    # debug mode 
    debug = True

    # wordpress settings
    wp_auto_upload = True # only valid if preview_mode is true
    wp_user = ""
    wp_url = ""
    wp_auth_key = ""
    # portion of image width you want text width to be
    img_fraction = 1

    _settings = None

    def __init__(self, settings_file):

        self.txt_color = "white"
        self.fontfile = "font/LuckiestGuy.ttf"
        self.border = True
        self.border_color = "black" 
        self.border_size = 5
        self.output_dir = "output"
        self.text_alignment = "center"
        self.preview_mode = True

        # debug mode 
        self.debug = True

        # wordpress settings
        self.wp_auto_upload = True # only valid if preview_mode is true
        self.wp_user = "Disane"
        self.wp_url = "https://[YOUR URL]/wp-json/wp/v2"
        self.wp_auth_key = "[YOUR API KEY]"
        # portion of image width you want text width to be
        self.img_fraction = 1

        
        if(os.path.getsize(settings_file) > 0):
            sets = json.loads(open(settings_file, 'r', encoding='utf-8').read())
            for key, value in sets.items():
                # s = defaultdict(self)
                self[key] = value
        else:
            with open(settings_file, 'w+') as outfile:
                print("Class encoded: "+ MyEncoder().encode(self))
                json.dump(self, outfile, cls=MyEncoder) #cls=MyEncoder

    def getSetting(name):
        return _setting[name]

    def __getitem__(self, key):
        return self.__dict__[key]
    
    def __setitem__ (self, key, value):
        if key in self.__dict__:
            self.__dict__[key] = value

class MyEncoder(JSONEncoder):
        def default(self, o):
            return o.__dict__ 
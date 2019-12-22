#/usr/bin/env python

import os
import sys
import zipfile
import difflib
import subprocess
from pathlib import Path

import PTN
import pyperclip

thunar_window_name = 'Menedżer plików' # Set it for your language

class MovieFiles:
    extensions = ('.avi', '.mkv', '.mp4', '.ogv', '.mpg', '.mov' )
    def __init__(self, path):
        self.path = os.path.dirname(path)
        os.chdir(self.path)
        self.p = Path('.')
        self.files = self.filelist()
        self.movies = self.moviesinfo()
        self.title = self.movietitle()

    def filelist(self):
        self.files = [str(x) for x in self.p.iterdir() if x.is_file() and str(x).endswith(self.extensions)]
        if len(self.files) < 1:
            print_error('Did not find any files with extensions: ' + str(self.extensions))
            exit(3)
        return self.files

    def moviesinfo(self):
        self.movies = [ PTN.parse(x) for x in self.files ]
        if len(self.files) < 1:
            print_error('PTN module have not found any files. Strange.')
            exit(4)
        return self.movies

    def movietitle(self):
        self.title = set([ x['title'] for x in self.movies ])
        if len(self.title) == 1:
            self.title = self.title.pop()
            return self.title
        if len(self.title) == 0:
            print_error("PTN module found movies but there were no titles." )
            exit(4)
        if len(self.title) > 1:
            self.title = user_choice(self.title)
            if self.title == 'None of the above':
                self.title = user_input()
            return self.title

class SubtitleFiles:
    extensions = ('.srt', '.txt', '.sub')
    zip_extensions = ('.zip', '.ZIP')
    def __init__(self, path):
        self.path = os.path.dirname(path)
        os.chdir(self.path)
        self.p = Path('.')
        self.unpack()
        self.files = self.filelist()
        self.subs = self.subsinfo()

    def unpack(self):
        self.zips = [ str(x) for x in self.p.iterdir() if x.is_file() and str(x).endswith(self.zip_extensions) ]
        for zip in self.zips:
            with zipfile.ZipFile (zip, 'r') as zip_ref:
                zip_ref.extractall('.')

    def filelist(self):
        self.files = [str(x) for x in self.p.iterdir() if x.is_file() and str(x).endswith(self.extensions)]
        return self.files

    def subsinfo(self):
        self.subs = [ PTN.parse(x) for x in self.files ]
        if len(self.files) < 1:
            print_error('PTN module found no subtitles. Strange.')
            exit(4)
        return self.subs

class Renamer:
    def __init__(self, mov, sub):
        self.mov = mov
        self.sub = sub
        self.episodes = self.find_episodes()

    def find_episodes(self):
        self.series = [ x for x in self.mov.movies if 'season' in x and 'episode' in x ]
        for e in self.series:
            possible_subs = [ sub for sub in enumerate(self.sub.subs) if sub[1]["season"] == e["season"] and sub[1]["episode"] == e["episode"] ]
            if len(possible_subs) > 1:
                best_match = Renamer.compare_names(e, possible_subs)
            elif len(possible_subs) == 1:
                best_match = possible_subs[0][0]
            elif len(possible_subs) == 0:
                continue
            self.rename_subtitle(best_match, e)

    def rename_subtitle(self, subid, e):
        # print(mov.files[mov.movies.index(e)] + '\n' + sub.files[subid] )
        os.rename(sub.files[subid], os.path.splitext(mov.files[mov.movies.index(e)])[0] + '.srt' )

    @staticmethod
    def compare_names(episode, possible_subs):
        best_match = (0, None)
        for sub in possible_subs:
            diff = difflib.SequenceMatcher(None, str( episode.values() ), str( sub[1].values() )  )
            if best_match[0] < diff.ratio():
                best_match = ( diff.ratio(), sub[0] )
        return best_match[1]





def user_choice(titles):
    title =  subprocess.run( ['zenity', '--title', 'Select correct title:',
            '--list', '--column', 'Title', 'None of the above', *titles],
            capture_output=True )
    return title.stdout.decode("utf-8").strip()

def user_input():
    title = subprocess.run( ['zenity', '--title', 'Provide a title',
        '--entry', '--text', 'Provide movie title:' ], capture_output=True )
    return title.stdout.decode("utf-8").strip()

def print_error(error):
    subprocess.run(['zenity', '--width', '200', '--error', '--text',
                   error])

def find_directory():
    try:
        return sys.argv[1] #if there is some argument, just use it as a path!
    except: pass

    cmd = subprocess.run(['xdotool', 'search', '--name', thunar_window_name,
                'windowfocus', 'key', '--clearmodifiers', 'ctrl+l', 'ctrl+c'])
    if cmd.returncode != 0:
        print_error('Thunar file manager not found. ' +
        'Check if you have a single filemanager window opened in movie directory.')
        exit(1)

    try:
        path = pyperclip.paste()
    except:
        print_error('Could not get data from pastebin.')
        exit(2)

    return path


def rename_subtitles(mov, sub):
    pass


if __name__ == '__main__':
    path = find_directory()
    mov = MovieFiles(path)
    sub = SubtitleFiles(path)
    ren = Renamer(mov, sub)

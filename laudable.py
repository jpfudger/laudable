import os
import sys
import glob, fnmatch
import re
import time
import datetime
import math
import pickle
import subprocess
import string
import matplotlib.pyplot as plt
from gigproc import gigproc
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from laudable.design import Ui_MainWindow
from PyQt4.phonon import Phonon

class LAUD_song():
    def __init__(self,fname,album,artist):
        self.fname  = fname
        self.album  = album
        self.artist = artist
        self.title  = self.extract_title(fname)
        self.searchtitle = self.extract_search_title(self.title)
        self.path   = album.path + os.sep + fname
    def extract_title(self,path):
        title = path.split('/')[-1]
        title = re.sub('\.\w+$','',title)
        return title
    def extract_search_title(self,title):
        search_title = re.sub('\s+','',title)
        punctuation = [ '\.', ',', "'", '"', '-', '_' ]
        for p in punctuation:
            search_title = re.sub(p,'',title)
        #print(title + " ==> " + search_title)
        return search_title
    def play(self):
        if os.path.exists(self.path):
            os.system( 'mplayer "' + self.path + '"')
        else:
            print("Not found: " + self.path)

class LAUD_album():
    def __init__(self,artist,name,songs,path,bootleg,mydates,opts):
        self.artist = artist
        self.name = name
        self.songs = songs
        self.path = path
        self.playlist = self.find_playlist()
        self.psongs = self.process_songs()
        self.bootleg = bootleg
        self.year = 0 # how?
        self.image = None
        self.date = None
        self.mine = False
        self.live = 'live' in name.lower() # path.lower()
        self.studio = False
        self.order = 999
        self.last = False
        self.videos = self.find_videos()
        
        if self.bootleg:
            keywords = [ 'studio', 'rehears', 'demo', 'outtake', 'session', 'acetate', 'radio', 'bbc' ]
            for k in keywords:
                if k in path.lower():
                    self.studio = True
                    break

        m_date = re.match( '.*(\d\d\d\d\.\d\d\.\d\d).*', path )
        if m_date and '.00' not in path:
            self.date = datetime.datetime.strptime( m_date.group(1), '%Y.%m.%d')
            if self.date:
                m_venue = re.match( '.*\[(.*)\].*', path )
                if m_venue:
                    for m in mydates:
                        if m['ordinal'] == self.date.toordinal():
                            for x in m['venue'].split():
                                if x in m_venue.group(1):
                                    self.mine = True
                                    break

        images = self.myglob(path + '/*.jpg')
        if images:
            self.image = images[0]
        else:
            self.image = opts.root + '/_Interface_/blank.jpg'
            #self.image = '/home/jpf/Music/Music/_Interface_/blank.jpg'

        if self.artist.info:
            try:
                self.order = 1 + self.artist.info[0].index(self.name)
                self.year  = self.artist.info[1][self.order-1]
                self.last  = self.order == len(self.artist.info[0]) or self.artist.info[0][self.order] == ''
            except:
                pass
    def find_videos(self):
        matches = []
        video_exts = ('.mp4','.mpg','.flv','.avi','.wmv','.m4v','.mov','.webm')
        for root, dirnames, filenames in os.walk(self.path):
            for filename in fnmatch.filter(filenames, '*.*'):
                if filename.endswith(video_exts):
                    matches.append(os.path.join(root, filename))
                # elif filename.endswith( ('.mp3','.m3u','.png','.jpg','.txt','.pdf','.wav','.WAV') ):
                #     pass
                # else:
                #     print(os.path.join(root,filename))
        matches.sort()
        return matches
    def find_playlist(self):
        playlists = self.myglob(self.path + '/*.m3u')
        if playlists:
            return playlists[0]
        return None
    def myglob(self,pattern):
        new_pattern = pattern.replace('[', 'XXXXXX')
        new_pattern = new_pattern.replace(']', 'YYYYYY')
        new_pattern = new_pattern.replace('XXXXXX', '[[]')
        new_pattern = new_pattern.replace('YYYYYY', '[]]')
        return glob.glob(new_pattern)
    def __str__(self):
        return '"' + self.name + '" by ' + self.artist.name + '.'
    def process_songs(self):
        songs = []
        psongs = []
        if self.playlist and os.path.exists(self.playlist):
            with open(self.playlist) as f:
                lines = f.readlines()
                for line in lines:
                    l = line.strip()
                    if len(l) == 0 or l[0] == '#':
                        pass
                    else:
                        psongs.append(LAUD_song(l,self,self.artist))
                        songs.append(l)
            self.songs = songs
        else:
            for path in self.songs:
                psongs.append(LAUD_song(path,self,self.artist))
        return psongs
    def play(self):
        if self.playlist:
            print(self.playlist)
            os.system( 'mplayer -playlist "' + self.playlist + '"')
            #subprocess.Popen( ['mplayer','-playlist',self.playlist] )
        else:
            print("No playlist in " + self.path)
    def html_img_link(self):
        string = ''
        if self.playlist and self.image:
            title = 'title="%s"' % self.name
            if self.year:
                title = 'title="%s, %d"' % ( self.name, self.year )
            string = '<a href="' + self.playlist + '" ' + title + ' >' \
                   + '<img class=cover src="' + self.image + '">' \
                   + '</a>'
        return string
    def split_boot_name(self):
        # separates a boot path into a date and name
        date = ''
        name = self.name
        m = re.match( '(.*)\s+[[](.*)[]].*', self.name )
        if m:
            date = m.group(1) + ' '
            name = m.group(2)
            m_full_date = re.match( '.*(\d\d\d\d.\d\d.\d\d).*', date.strip() )
            try:
                if not m_full_date:
                    m_partial_date = re.match( '.*(\d\d\d\d.\d\d).*', date.strip() )
                    if m_partial_date:
                        # format 1962.01
                        dummy_date = m_partial_date.group(1) + '.01'
                        d = datetime.datetime.strptime(dummy_date, '%Y.%m.%d')
                        if d:
                            date = d.strftime('%Y %b')
                elif m_full_date.group(1)[-5:] == '00.00':
                    # format 1962.00.00
                    date = m_full_date.group(1)[0:4]
                elif m_full_date.group(1)[-2:] == '00':
                    # format 1962.01.00
                    dummy_date = m_full_date.group(1)[:-2] + '01'
                    d = datetime.datetime.strptime(dummy_date, '%Y.%m.%d')
                    if d:
                        date = d.strftime('%Y %b')
                else:
                    # format 1962.01.01
                    d = datetime.datetime.strptime(m_full_date.group(1), '%Y.%m.%d')
                    if d:
                        date = d.strftime('%Y %b %d ')
            except:
                pass
        return date, name
    def boot_link(self):
        link = ''
        if self.bootleg and self.playlist:
            date, name = self.split_boot_name()
            n_tracks = ''
            if self.songs:
                n_tracks = '<div class=date>%s</div>' % str(len(self.songs))
            if self.playlist and self.name:
                link = '<div class=date>' + date + '</div>  ' + '<a '
                if self.mine:
                    link += 'class=mine '
                elif self.studio:
                    link += 'class=stud '
                else:
                    link += 'class=boot '
                link += 'href="' + self.playlist + '">' + name + '</a> ' + n_tracks
        return link

class LAUD_artist():
    def __init__(self,name,path):
        self.name = name
        self.alt_name = self.getAltName()
        self.index = None
        self.albums = []
        self.info = [[],[]]
        self.rank = 0
        self.process_info(path)
    def getAltName(self):
        if ' and ' in self.name.lower():
            pass
        elif ' & ' in self.name:
            pass
        elif ', ' in self.name:
            splits = self.name.split(', ')
            splits.reverse()
            return ' '.join(splits)
        return self.name
    def discog_fname(self):
        return self.name[0].upper() + str(self.index).zfill(3) + '.html'
    def discog_fname_b(self, decade=''):
        post = 'b.html'
        if decade != '':
            post = 'b_' + decade + '.html'
        return self.name[0].upper() + str(self.index).zfill(3) + post
    def process_info(self,path):
        info_path = path + os.sep + 'info'
        if os.path.exists(info_path):
            lines = []
            with open(info_path) as f:
                lines = f.readlines()
            for line in lines:
                splits = line.split('#')
                name = splits[0].strip()
                year = None
                if len(splits) == 2:
                    year_str = splits[1].strip()
                    if year_str:
                        year = int(year_str)
                self.info[0].append( name )
                self.info[1].append( year )
    def __str__(self):
        return self.name + '  :  %d albums' % len(self.albums) 
    def is_number(self,s):
        try:
            float(s)
            return True
        except ValueError:
            return False
    def div_albums(self,linkback=None):
        lines = []
        #albums = [ a for a in self.albums if not a.bootleg and not a.live ]
        albums = [ a for a in self.albums if not a.bootleg ]
        live = [ a for a in self.albums if not a.bootleg and a.live ]
        albums.sort(key = lambda x: x.name)
        albums.sort(key = lambda x: x.order)
        if albums:
            lines.append( '<div id=discography>' )
            name = self.alt_name
            if linkback:
                name += ' <a class=boot href="%s">+</a>' % linkback
            #lines.append( '<h1>' + name + '</h1>' )
            lines.append( '<h1><div class=rank title="Rank: %s">%s</div></h1>' % ( self.rank, name ) )
            n_albums = 0
            for a in albums:
                link = a.html_img_link()
                if link:
                    n_albums += 1
                    lines.append( link )
                    if a.last:
                        lines.append( '<br> <br>' )
                        n_albums = 0
                    elif n_albums % 12 == 0:
                        lines.append( '<br>' )
                        n_albums = 0

            if False:
                if n_albums > 10:
                    new_lines = []
                    #square = int(math.sqrt(n_albums)) + 1
                    square = 10
                    for i,l in enumerate(lines):
                        new_lines.append(l)
                        if i > 0 and i % square == 1:
                            new_lines.append( '<br>' )
                    lines = new_lines

                # add live albums after a gap
                if live:
                    lines.append( '<br> <br>' )
                    for a in live:
                        link = a.html_img_link()
                        if link:
                            lines.append( link )

            lines.append( '</div>' )
        else:
            lines.append( '<div id=discography>' )
            name = self.alt_name
            if linkback:
                name += ' <a class=boot href="%s">+</a>' % linkback
            lines.append( '<h1>' + name + '</h1>' )
            lines.append( '</div>' )

        return lines
    def div_boots(self,linkback=None):
        lines = []
        decades = []
        years = []
        boots = [ a for a in self.albums if a.bootleg ]
        boots.sort(key = lambda x: x.name)
        if len(boots) > 50:
            last_year = None
            last_decade = None
            lines.append( '<div id=discography>' )
            name = self.alt_name
            if linkback:
                name += ' <a class=boot href="%s">+</a>' % linkback
            lines.append( '<h1>' + name + '</h1>' )
            n_columns = 0
            max_col_length = 20
            cur_col_length = 0

            earliest_boot_year = boots[0].name[0:4]
            if earliest_boot_year[3] != 0:
                this_year = int(earliest_boot_year[0:3] + '0')
                while this_year < int(earliest_boot_year):
                    lines.append( str(this_year) )
                    this_year += 1
                last_year = None
                last_decade = earliest_boot_year[0:3] + '0'

            bootyears = [ a.name[0:4] for a in boots ]
            bootyears = list(set(bootyears))
            bootyears.sort()

            for i, a in enumerate(boots):
                cur_col_length += 1
                this_year = a.name[0:4]
                this_decade = a.name[0:3] + '0'

                if last_year != this_year:

                    try:
                        if int(this_year) != int(last_year) + 1:
                            difference = int(this_year) - int(last_year)
                            tmp_year = int(last_year) + 1
                            tmp_decade = str(tmp_year)[0:3] + '0'

                            while tmp_year != int(this_year):
                                if tmp_decade != last_decade:
                                    lines.append( '<br>' )
                                lines.append( str(tmp_year) )
                                tmp_year += 1
                                last_decade = tmp_decade
                    except:
                        pass
                    
                    year_link = self.discog_fname_b(this_year)
                    year_link_string = '<a href="%s">%s</a>' % ( year_link, this_year)
                    if this_decade != last_decade:
                        year_link_string = '<br> ' + year_link_string
                    lines.append( year_link_string )
                    if last_year != None:
                        years[-1]['lines'].append( '</div>' ) # close bootcol
                        years[-1]['lines'].append( '</div>' ) # close discog
                    years.append({'name': this_year, 'lines': []})
                    years[-1]['lines'].append( '<div id=discography>' )
                    years[-1]['lines'].append( '<h1>' + name + '</h1>' )
                    try:
                        pre = linkback.replace( '.html', 'b_' )
                        years[-1]['lines'].append( '<a href="%s">&lt;</a>' % ( pre + last_year + '.html' ) )
                        years[-1]['lines'].append( this_year )
                        next_year_index = bootyears.index(this_year) + 1
                        next_year = bootyears[next_year_index] 
                        years[-1]['lines'].append( '<a href="%s">&gt;</a>' % ( pre + next_year + '.html' ) )
                    except:
                        pass
                    n_columns = 0
                    cur_col_length = 0
                    last_year = this_year
                    last_decade = this_decade

                if cur_col_length % max_col_length == 0:
                    if n_columns > 0:
                        years[-1]['lines'].append( '</div>' )
                    n_columns += 1
                    years[-1]['lines'].append( '<div class=bootcol%d>' % n_columns )

                years[-1]['lines'].append( '<br> ' + ' ' + a.boot_link() )

            years[-1]['lines'].append( '</div>' )

            decades = years

            # Still need to add non-link strings for missing years (e.g. "1968")
            # Still need to break the playlist links into columns for each year.
        elif boots:
            lines.append( '<div id=discography>' )
            name = self.alt_name
            if linkback:
                name += ' <a class=boot href="%s">+</a>' % linkback
            lines.append( '<h1>' + name + '</h1>' )
            album_lines = []
            n_albums = 0
            decade = None
            for a in boots:
                if a.playlist and a.name:
                    this_decade = a.name[0:3]
                    if decade and this_decade != decade and self.is_number(decade): 
                        album_lines.append('<br>')
                    decade = this_decade
                    n_albums += 1
                    album_lines.append( '<br> ' + a.boot_link() )

            if n_albums > 40:
                new_lines = []
                col_length = 30
                if n_albums > 40 * 5:
                    col_length = int(n_albums/5)+2
                n_cols = 1
                for i,l in enumerate(album_lines):
                    new_lines.append(l)
                    if i > 0 and i % col_length == 0:
                        n_cols += 1
                        new_lines.append( '</div>' )
                        new_lines.append( '<div class=bootcol%d>' % n_cols )
                album_lines = new_lines

            lines += [ '<div class=bootcol1>' ] + album_lines + [ '</div>' ]
            lines.append( '</div>' )
            if n_albums == 0:
                lines = []
        return lines, decades
    def getAlbums(self):
        albums = [ a for a in self.albums if not a.bootleg ]
        albums.sort(key = lambda x: x.name)
        albums.sort(key = lambda x: x.order)
        return albums
    def getBoots(self):
        boots = [ a for a in self.albums if a.bootleg ]
        boots.sort(key = lambda x: x.name)
        return boots
    def getVideos(self):
        videos = [ a for a in self.albums if a.videos ]
        videos.sort(key = lambda x: x.name)
        return videos

class LAUD_data():
    def __init__(self,options):
        self.artists = []
        self.sort = True    # whether to do sorted traverse
        self.opts = options
        self.time = time.clock()
        self.mydates = self.my_dates()
        self.load_data()
        #self.build_song_data()
        self.time = time.clock() - self.time
        self.albums_by_year = []
        self.my_gigs = []
    def __str__(self):
        counts = [ 0, 0, 0, 0 ] # albums, artists, mine, songs
        for x in self.artists:
            counts[0] += 1
            for y in x.albums:
                counts[1] += 1
                if y.mine:
                    counts[2] += 1
                for z in y.songs:
                    counts[3] += 1
        return "%d artists, %d albums (%d gigproc) and %d songs in %.2f seconds." % \
                    ( counts[0], counts[1], counts[2], counts[3], self.time )
    def ignore_path(self,path):
        if 'PENDING' in path:
            return True
        if '_Cl' in path:
            return True
        if '_Interface_' in path:
            return True
        if '_Misc' in path:
            return True
        if 'Dylan/Interface' in path:
            return True
        if 'Dylan/Stuff' in path:
            return True
        if 'Dylan/XM-Radio' in path:
            return True
        return False
    def get_artist(self,name,path):
        for a in self.artists:
            if a.name == name:
                return a
        a = LAUD_artist(name,path)
        self.artists.append(a)
        return a
    def myglob(self,pattern):
        new_pattern = pattern.replace('[', 'XXXXXX')
        new_pattern = new_pattern.replace(']', 'YYYYYY')
        new_pattern = new_pattern.replace('XXXXXX', '[[]')
        new_pattern = new_pattern.replace('YYYYYY', '[]]')
        return glob.glob(new_pattern)
    def process_album(self,path):
        if self.ignore_path(path):
            return
        subpath = path[ (len(self.opts.root) + 1) : ]
        splits = subpath.split('/')
        artist_name = splits[1]
        album_name = splits[-1]
        mp3s = self.myglob( path + '/*mp3' )
        bootleg = ( '/bootlegs/' in path.lower() ) or ( '/boots/' in path.lower() )
        if True: #len(mp3s) > 0:
            # Some albums have no mp3s because the playlist links elsewhere
            if self.sort:
                mp3s.sort()
            art_path = os.path.sep.join( [ self.opts.root, splits[0], splits[1] ] )
            a = self.get_artist(artist_name,art_path)
            mp3list = [ x.split('/')[-1] for x in mp3s ]
            album = LAUD_album(a,album_name,mp3list,path,bootleg,self.mydates,self.opts)
            if album.playlist:
                a.albums.append(album)
    def load_data(self):
        if self.opts.update:
            if os.path.exists(self.opts.pickle_file):
                with open(self.opts.pickle_file,'rb') as f:
                    self.artists = pickle.load(f)
                print( " Initial: %s" % self )
                self.artists = [] # otherwise we append to the loaded list!
            self.build_song_data()
            with open(self.opts.pickle_file,'wb') as f:
                pickle.dump(self.artists,f)
            print( "   Final: %s" % self )
            self.stats_table(True)
        elif os.path.exists(self.opts.pickle_file):
            with open(self.opts.pickle_file,'rb') as f:
                self.artists = pickle.load(f)
            print( "    Read: %s" % self )
        else:
            print("Error: no stored data")
    def build_song_data(self):
        letters = self.myglob( self.opts.root + '/*' )
        #letters = [ self.opts.root + '/D' ] # testing: dylan only
        #letters = [ self.opts.root + '/Y' ] # testing: young only
        #letters = [ self.opts.root + '/H' ] # testing: hot tuna only
        if self.sort:
            letters.sort()
        print("Updating: ", end='')
        for letter in letters:
            if self.ignore_path(letter):
                continue
            print( letter.split('/')[-1], end=' ' )
            artists = self.myglob( letter + '/*' )
            if self.sort:
                artists.sort()
            for artist in artists:
                for base, dirs, files in os.walk(artist):
                    for d in dirs:
                        path = base + '/' + d
                        self.process_album(path)
            #break # for testing; do one letter only
        print(".")
        artist_index = 0
        for a in self.artists:
            artist_index += 1
            a.index = artist_index

        # rank
        artists = self.artists[:]
        artists.sort(key=lambda a: len(a.albums))
        artists.reverse()
        artists.sort(key=lambda a: sum([len(x.songs) for x in a.albums]))
        artists.reverse()
        for i, artist in enumerate(artists):
            artist.rank = '%d/%d' % ( i+1, len(artists) )

        return
    def play_album(self,pattern):
        albums = []
        for x in self.artists:
            for y in x.albums:
                if y.bootleg and not self.opts.boots:
                    continue
                if pattern.lower() in y.name.lower():
                    albums.append(y)
        print( "Matches:" )
        for i,a in enumerate(albums):
            print("  %2d %s" % (i+1,a.playlist))
        for a in albums:
            a.play()
    def stats_table(self,verbose=False):
        self.artists.sort(key=lambda a: len(a.albums))
        self.artists.reverse()
        self.artists.sort(key=lambda a: sum([len(x.songs) for x in a.albums]))
        self.artists.reverse()

        lines = [ '<table>' ]
        lines.append( '<tr>' )
        lines.append( '<td></td>' )
        lines.append( '<td></td>' )
        lines.append( '<td>Official<br>Albums</td>' )
        lines.append( '<td>Official<br>Songs</td>' )
        lines.append( '<td>Bootleg<br>Albums</td>' )
        lines.append( '<td>Bootleg<br>Songs</td>' )
        lines.append( '<td>Total<br>Albums</td>' )
        lines.append( '<td>Total<br>Songs</td>' )
        lines.append( '</tr>' )

        if verbose:
            print( "" )
            print( "                             (official)       (bootlegs)        (total)   " )
            print( "                           albums  songs   albums   songs   albums   songs" )

        for (i,a) in enumerate(self.artists[0:100]):
            boots = [ x for x in a.albums if x.bootleg ]
            boot_albums = len(boots)
            boot_songs = sum( [ len(x.songs) for x in boots ] )

            tot_songs  = sum([ len(x.songs) for x in a.albums ])
            tot_albums = len(a.albums)
            boot_albums  = len(boots)

            off_albums = tot_albums - boot_albums
            off_songs  = tot_songs - boot_songs

            a_link = '<a href="%s">%s</a>' % ( a.discog_fname(), a.alt_name )

            lines.append( '<tr>' )
            lines.append( '<td>%d</td>' % (i+1)  )
            lines.append( '<td>%s</td>' % a_link )
            lines.append( '<td>%d</td>' % off_albums )
            lines.append( '<td>%d</td>' % off_songs )
            lines.append( '<td>%d</td>' % boot_albums )
            lines.append( '<td>%d</td>' % boot_songs )
            lines.append( '<td>%d</td>' % tot_albums )
            lines.append( '<td>%d</td>' % tot_songs )
            lines.append( '</tr>' )

            
            if verbose:
                print( "  %3d %-20s  %6d  %5d   %6d   %5d     %4d  %6d" % 
                  ( i+1, a.alt_name,
                    off_albums,  off_songs, 
                    boot_albums, boot_songs,
                    tot_albums,  tot_songs ))

        lines.append( '</table>' )
        return lines
    def search(self,query):
        # receives a dictionary of 'artist', 'album', 'song', 'date'
        matches = []
        for x in self.artists:
            if not query['artist'] or query['artist'].lower() in x.name.lower():
                for y in x.albums:
                    if y.bootleg and not self.opts.boots:
                        continue
                    if not query['album'] or query['album'].lower() in x.name.lower():
                        for z in y.songs:
                            if not query['song'] or query['song'].lower() in z.lower():
                                matches.append( y.path + '/' + z )
        return matches
    def my_dates(self):
        dates = []
        gd = gigproc.GIG_data(self.opts.mygigs_path)
        for gig in gd.gigs:
            dates.append( { 'ordinal': gig.date.toordinal(), 'venue': gig.venue } )
        return dates
    def get_albums_by_year(self):
        if not self.albums_by_year:
            years  = []
            albums = []
            for artist in self.artists:
                for album in artist.albums:
                    if album.year:
                        try:
                            pos = years.index(album.year)
                            albums[pos].append(album)
                        except ValueError:
                            years.append(album.year)
                            albums.append([album])

            # add empty list for missing years
            all_years = set(years)
            missing_years = list( set(range(min(years),max(years)+1)) - all_years )
            for m in missing_years:
                years.append(m)
                albums.append( [] )

            zipped = list( zip(years,albums) )
            zipped.sort( key=lambda x: x[0] )
            self.albums_by_year = zipped
        return self.albums_by_year
    def get_my_gigs(self):
        if not self.my_gigs:
            for artist in self.artists:
                for album in artist.albums:
                    if album.bootleg and album.mine:
                        self.my_gigs.append(album)
        return self.my_gigs
    def plot_albums_by_year(self,dest=None):
        years = [ z[0] for z in self.get_albums_by_year() ]
        totals = [ len(z[1]) for z in self.get_albums_by_year() ]

        fig, ax = plt.subplots()
        bar1 = ax.bar( years, totals,  align='center', color='#153E7E' )

        tick_pos = [ y for y in years if y % 5 == 0 ]
        tick_lab = [ str(y)[2:] for y in tick_pos ]

        plt.xticks(tick_pos, tick_lab)
        ax.tick_params(direction='out')
        plt.grid(b=True, which='both') #, color='0.65',linestyle='-')
        ax.set_axisbelow(True)

        if dest:
            fig.savefig( dest, bbox_inches='tight', dpi=300)
            plt.close()
        else:
            plt.show()
    def alphabet(self):
        letters = []
        artists = []

        self.artists.sort(key=lambda a: a.name)

        for a in self.artists:
            if a.name[0] in letters:
                index = letters.index(a.name[0])
                artists[index].append(a)
            else:
                letters.append(a.name[0])
                artists.append([a])
        return letters, artists
    def make_html(self):
        letters, artists = self.alphabet()

        header_lines = [ '<html>', '<body>', '<head>' ]
        header_lines.append( '<title>Songproc</title>' )
        header_lines.append( '<link rel="stylesheet" type="text/css" href="style.css">' )
        #header_lines.append( '<link rel="shortcut icon" href="img/note.ico" type="image/x-icon">' )
        header_lines.append( '</head>' )
        footer_lines = [ '</body>', '</html>' ]

        alpha_div = [ '<div id=alphabet>' ]
        #alpha_div.append( ' <a href="%d.html">#</a>' % datetime.datetime.now().year )
        alpha_div.append( ' <a href="stats.html">%</a>' )
        alpha_div.append( ' <a href="years.html">#</a>' )
        for l in letters:
            alpha_div.append( ' <a href="%s.html">%s</a>' % ( l, l ) )
            # if l == 'M':
            #     alpha_div.append( '<br>' )
        alpha_div.append( '</div>' )
        
        for letter, artists in zip(letters,artists):
            fname = letter + '.html'
            lines = header_lines[:] + alpha_div[:]
            letter_div = [ '<div id=letter>' ]
            for a in artists:
                line = ''
                if a.div_albums():
                    line += '<br> <a href="%s">%s</a>' % ( a.discog_fname(), a.name )
                    # only add a boot div if there was an album div:
                    div_boots = a.div_boots()
                    if div_boots[0]:
                        discog_fname_b = letter + str(a.index).zfill(3) + 'b.html'
                        line += ' <a class=boot href="%s">+</a>' % ( discog_fname_b )
                if line:
                    letter_div.append(line)
            letter_div.append( '</div>' )

            # make empty letter page:
            lines += letter_div
            if lines:
                lines += footer_lines[:]
                with open(self.opts.html_root + fname, 'w') as f:
                    for l in lines:
                        f.write('\n' + l)

            # maker artist/dicog pages:
            for a in artists:
                div_boots, decades  = a.div_boots( a.discog_fname() )
                div_albums = a.div_albums( a.discog_fname_b() if div_boots else None )
                if div_albums:
                    lines = header_lines[:] + alpha_div[:] + letter_div[:]
                    lines += div_albums
                    lines += footer_lines[:] 
                    with open( self.opts.html_root + a.discog_fname(), 'w') as f:
                        for l in lines:
                            f.write('\n' + l)

                    # only add a boot div if there was an album div:
                    if div_boots:
                        lines = header_lines[:] + alpha_div[:] + letter_div[:]
                        lines += div_boots + footer_lines[:] 
                        with open( self.opts.html_root + a.discog_fname_b(), 'w') as f:
                            for l in lines:
                                f.write('\n' + l)
                        if decades:
                            for d in decades:
                                dlines = header_lines[:] + alpha_div[:] + letter_div[:]
                                dlines += d['lines'] + footer_lines[:]
                                with open( self.opts.html_root + a.discog_fname_b(d['name']), 'w') as f:
                                    for l in dlines:
                                        f.write('\n' + l)


        lines = header_lines[:] + alpha_div[:] + footer_lines[:]
        with open( self.opts.html_root + 'index.html', 'w') as f:
            for l in lines:
                f.write('\n' + l)

        # compute years div
        years_div = [ '<div id=letter>', '<br>' ]
        first = self.get_albums_by_year()[0][0]
        last = self.get_albums_by_year()[-1][0]

        if first % 5 > 0:
            pre = str(first)[0:3]
            for i in range(0,first % 5):
                years_div.append( pre + str(i) )
        for year, albums in self.get_albums_by_year():
            if year % 5 == 0:
                years_div.append( '<br>' )
            if str(year)[-1] == '0':
                years_div.append( '<br>' )
            years_div.append( ' <a href="%d.html">%d</a>' % ( year, year ) )

        if last % 5 > 0:
            last += 1
            while last % 5 > 0:
                years_div.append( str(last) )
                last += 1

        years_div.append( '</div>' )

        # make empty years page:
        self.plot_albums_by_year( self.opts.html_root + 'years_plot.png')
        lines = header_lines[:] + alpha_div[:] + years_div[:]
        lines.append( '<div id=discography>' )
        lines.append( '<br>' )
        lines.append( '<img src="years_plot.png" width=750>' )
        lines.append( '</div>' )
        lines += footer_lines[:]
        with open(self.opts.html_root + 'years.html', 'w') as f:
            for l in lines:
                f.write('\n' + l)

        for i, (year, albums) in enumerate(self.get_albums_by_year()):
            lines = header_lines[:] + alpha_div[:] + years_div[:] 
            lines.append( '<div id=discography>' )
            prev_string = '< '
            if i > 0:
                prev_year = self.get_albums_by_year()[i-1][0]
                prev_string = '<a href="%d.html">&lt;</a> ' % prev_year
            next_string = ' >'
            if i < len(self.get_albums_by_year())-1:
                next_year = self.get_albums_by_year()[i+1][0]
                next_string = ' <a href="%d.html">&gt;</a>' % next_year
            lines.append( '<h1>' + prev_string + str(year) + next_string + '</h1>' )
            n_albums = 0
            square = int(math.sqrt(len(albums))) + 3
            for a in albums:
                if n_albums % square == 0:
                    lines.append( '<br>' )
                lines.append( a.html_img_link() )
                n_albums += 1
            lines.append( '</div>' )
            lines += footer_lines[:]
            with open( self.opts.html_root + str(year) + '.html', 'w') as f:
                for l in lines:
                    f.write('\n' + l)

        # make stats page
        stats_lines = header_lines[:] + alpha_div[:]
        stats_lines += [ '<div id=discography>', '<br>' ]
        stats_lines += self.stats_table()
        stats_lines += [ '<br>', '</div>' ]
        stats_lines += footer_lines[:]
        with open(self.opts.html_root + 'stats.html', 'w') as f:
            for l in stats_lines:
                f.write('\n' + l)


        # compute my gigs div
        my_gigs_div = [ '<div id=letter>', '<br>' ]
        my_years = [ x.date.year for x in self.get_my_gigs() ]
        my_years = list(set(my_years)) # unique
        my_years.sort()

class LAUD_gui(QMainWindow, Ui_MainWindow):
    def __init__(self, data):
        super(self.__class__, self).__init__()
        self.data = data
        self.setupUi(self)
        self.is_fullscreen = False

        self.letterListModel = QStandardItemModel()
        self.letterList.setModel(self.letterListModel)
        self.fillLetterList()

        self.artistListModel = QStandardItemModel()
        self.artistList.setModel(self.artistListModel)

        self.albumListModel  = QStandardItemModel()
        self.albumList.setModel(self.albumListModel)

        self.bootListModel  = QStandardItemModel()
        self.bootList.setModel(self.bootListModel)

        self.videoListModel  = QStandardItemModel()
        self.videoList.setModel(self.videoListModel)

        self.songListModel  = QStandardItemModel()
        self.songList.setModel(self.songListModel)

        self.artistList.selectionModel().currentChanged.connect(self.onRowChanged)
        QShortcut(QKeySequence("f"), self.videoPlayer, self.fFullscreen)

    def onRowChanged(self, current, previous):
        # this is for cursor up/down movements
        indices = self.artistList.selectedIndexes()
        if len(indices) > 0:
            index = indices[0]
            item = self.artistListModel.itemFromIndex(index)
            artist = item.data()
            self.rebuildAlbumLists(artist)

    def fillLetterList(self):
        letters, artists = self.data.alphabet()

        for l,a in zip(letters,artists):
            item = QStandardItem()
            item.setText(l)
            item.setData(a)
            self.letterListModel.appendRow(item)

        # we need albums_by_year() to return a list of 
        # artist objects, whose name is the year.
        aby = []

        for year,albums in self.data.get_albums_by_year():
            artist = LAUD_artist( str(year), '' )
            artist.albums = albums
            aby.append(artist)

        by_year_item = QStandardItem()
        by_year_item.setText('#')
        by_year_item.setData(aby)
        self.letterListModel.appendRow(by_year_item)

    def onLetterClick(self,index):
        item = self.letterListModel.itemFromIndex(index)
        artists = item.data()

        self.artistListModel.clear()

        for a in artists:
            a_item = QStandardItem()
            a_item.setText(a.name)
            a_item.setData(a)
            self.artistListModel.appendRow(a_item)

    def onArtistClick(self,index):
        item = self.artistListModel.itemFromIndex(index)
        artist = item.data()
        self.rebuildAlbumLists(artist)

    def rebuildAlbumLists(self,artist):
        self.albumListModel.clear()
        n_albums = 0
        for a in artist.getAlbums():
            n_albums += 1
            a_item = QStandardItem()
            a_item.setText(a.name)
            a_item.setData(a)
            a_item.setEditable(False)
            self.albumListModel.appendRow(a_item)
        self.tabWidget.setTabEnabled( 0, n_albums > 0 )

        self.bootListModel.clear()
        n_boots = 0
        for a in artist.getBoots():
            n_boots += 1
            a_item = QStandardItem()
            a_item.setText(a.name)
            a_item.setData(a)
            if a.mine:
                a_item.setBackground(QColor('cyan'))
            a_item.setEditable(False)
            self.bootListModel.appendRow(a_item)
        self.tabWidget.setTabEnabled( 1, n_boots > 0 )

        self.videoListModel.clear()
        n_videos = 0
        for a in artist.getVideos():
            n_videos += 1
            a_item = QStandardItem()
            a_item.setText(a.name)
            a_item.setData(a)
            if a.mine:
                a_item.setBackground(QColor('cyan'))
            a_item.setEditable(False)
            self.videoListModel.appendRow(a_item)
        self.tabWidget.setTabEnabled( 2, n_videos > 0 )

    def onAlbumClick(self,index):
        tabIndex = self.tabWidget.currentIndex()
        item = None
        video = False

        if tabIndex == 0:
            item = self.albumListModel.itemFromIndex(index)
        elif tabIndex == 1:
            item = self.bootListModel.itemFromIndex(index)
        elif tabIndex == 2:
            item = self.videoListModel.itemFromIndex(index)
            video = True

        album = item.data()

        self.songListModel.clear()

        if video:
            for v in album.videos:
                v_item = QStandardItem()
                splits = v.split(os.sep)
                v_item.setText(splits[-1])
                v_item.setData(v)
                self.songListModel.appendRow(v_item)
        else:
            for s in album.psongs:
                s_item = QStandardItem()
                s_item.setText(s.title)
                s_item.setData(s)
                self.songListModel.appendRow(s_item)

    def onSongClick(self,index):
        item = self.songListModel.itemFromIndex(index)
        song = item.data()
        self.pauseButton.setCheckState(Qt.Unchecked) # not paused

        if self.tabWidget.currentIndex() == 2:
            # video: the data is the path
            print(song)
            self.phononPlay(song)
        else:
            # song class
            self.phononPlay(song.path)

    def phononPlay(self,path):
        self.is_fullscreen = False
        vp = self.videoPlayer
        vp.show()
        media = Phonon.MediaSource(path)
        vp.load(media)
        vp.play()

    def onFullscreen(self,state):
        if state == Qt.Unchecked:
            self.videoPlayer.videoWidget().exitFullScreen()
        elif state == Qt.Checked:
            self.videoPlayer.videoWidget().enterFullScreen()

    def fFullscreen(self):
        if self.videoPlayer.isPlaying():
            if self.is_fullscreen:
                self.songList.setFocus()
                self.videoPlayer.videoWidget().exitFullScreen()
                self.is_fullscreen = False
            else:
                self.videoPlayer.videoWidget().enterFullScreen()
                self.is_fullscreen = True

    def onPause(self,state):
        if state == Qt.Unchecked:
            self.videoPlayer.play()
        elif state == Qt.Checked:
            self.videoPlayer.pause()

class LAUD_interface():
    @staticmethod
    def gui(data):
        app = QApplication(sys.argv)
        form = LAUD_gui(data)
        form.show()
        app.exec_()


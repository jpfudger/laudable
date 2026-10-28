import sqlite3
import os

from laudable.config import LAUD_database_path, LAUD_music_root

VIDEO_EXTENSIONS = ('.mp4','.mpg','.flv','.avi','.wmv','.m4v','.mov','.webm')

class AlbumInfo:
    artist_name = None
    artist_path = False
    songs = []
    album_name = None
    playlist_path = None
    artwork_path = None
    order = 0
    section = 1
    year = 0
    date = 0
    bootleg = False
    mine = False
    videos = []

def get_mine():
    # No longer used.
    # It was used to generate the "mine" files in each bootleg directory.
    # Now we just look for the "mine" file explicitly.

    path = r"/mnt/nas/Data/python/gigproc/gigs/playlists"
    regex = rf"^{LAUD_music_root}{os.sep}\w{os.sep}([^{os.sep}]+){os.sep}" \
                    + rf".*(\d\d\d\d)\.(\d\d)\.(\d\d)"
    import re
    import datetime

    my_artists = {}

    with open(path) as f:
        for line in f:
            m = re.match(regex, line)
            if m:
                artist = m.group(1)
                year = int(m.group(2))
                month = int(m.group(3))
                day = int(m.group(4))
                date = datetime.date(year, month, day)
                # print(artist, date.strftime("%Y-%b-%d"))

                if artist not in my_artists:
                    my_artists[artist] = []
                my_artists[artist].append(date)

    return my_artists

def get_album_info(root, files, my_gig_artists=None):
    import datetime
    import re
    import os

    songs = []
    videos = []
    album_base = os.path.basename(root)
    album_name = album_base # may be tweaked later
    playlist_path = None
    artwork_path = None
    album_order = 0
    album_section = 1
    year = 0
    date = 0
    artist_name = None
    bootleg = "/Bootlegs/" in root
    mine = False
    info = None

    start_number_regex = r"^\d\d+\s*-*\.*\s+"

    if "Dylan, Bob" in root and not bootleg:
        album_name = re.sub(start_number_regex, "", album_name)

    all_songs_start_with_number = True

    for f in files:
        all_start_with_number = True
        if f.endswith(".mp3"):
            if re.search(r"^\d+ ", f):
                pass
            else:
                all_start_with_number = False

    for f in files:
        if f.endswith(".mp3"):
            song = {}

            sname = f[:-4]
            if all_songs_start_with_number:
                sname = re.sub(start_number_regex, "", sname)

            song["name"] = sname
            song["path"] = os.path.join(root,f)
            song["order"] = 0
            songs.append(song)
        elif os.path.splitext(f)[1] in VIDEO_EXTENSIONS:
            video = {}
            video["name"] = os.path.splitext(f)[0]
            video["path"] = os.path.join(root,f)
            videos.append(video)
        elif f == "mine":
            mine = True
        elif f.endswith(".m3u"):
            playlist_path = os.path.join(root,f)
        elif f.endswith(".jpg"):
            artwork_path = os.path.join(root,f)

    if songs:
        m = re.search("(" + str(LAUD_music_root) + r"/./[^\/]+)/", root)
        if m:
            artist_path = m.group(1)
            artist_name = os.path.basename(artist_path)

            if not bootleg:
                # look for album year from info
                info_path = os.path.join(artist_path, "info")

                if os.path.isfile(info_path):
                    with open(info_path) as f:
                        #print(info_path)
                        section = 1
                        for i, line in enumerate(f, start=1):
                            line = line.strip()
                            splits = line.split("#")
                            if splits[0].strip().lower() == album_base.lower():
                                if len(splits) > 1 and splits[1]:
                                    year = int(splits[1])
                                    date = f"{year}-01-01"
                                album_order = i
                                album_section = section
                            if not line:
                                section += 1

            else:
                # look for date in album name
                m_date1 = re.search(r"^(\d\d\d\d)\.(\d\d)\.(\d\d)\b", album_base)
                d = None
                if m_date1:
                    year = int(m_date1.group(1))
                    month = int(m_date1.group(2))
                    day = int(m_date1.group(3))

                    if day == 0: day = 1
                    if month == 0: month = 1

                    #print(year,month,day)
                    d = datetime.date(year=year, month=month, day=day)
                    date = d.strftime("%Y-%m-%d")

                if d and artist_name and my_gig_artists:
                    # No longer used (since my_gig_artists never supplied).
                    # This is how I wrote a "mine" file in each directory
                    # listed in path = r"/mnt/nas/Data/python/gigproc/gigs/playlists"
                    if artist_name in my_gig_artists:
                        artist_dates = my_gig_artists[artist_name]
                        if d in artist_dates:
                            #print(f"{artist_name} - {date} - is mine!")
                            mine = True
    
                            # f_mine = os.path.join(root,"mine")
                            # print(f_mine)
                            # with open(f_mine, "a"):
                            #     os.utime(f_mine)

                if not year:
                    m_date2 = re.search(r"^(\d\d\d\d)\.(\d\d)\b", album_base)
                    if m_date1:
                        year = int(m_date2.group(1))
                        month = int(m_date2.group(2))
                    
                        if month == 0: month = 1

                        #print(year,month,None)
                        d = datetime.date(year=year, month=month, day=1)
                        date = d.strftime("%Y-%m-%d")

                if not year:
                    m_date3 = re.search(r"^(\d\d\d\d)\b", album_base)
                    if m_date3:
                        year = int(m_date3.group(1))
                        #print(year,None,None)
                        d = datetime.date(year=year, month=1, day=1)
                        date = d.strftime("%Y-%m-%d")

        if playlist_path and os.path.isfile(playlist_path):
            # fill in song order
            with open(playlist_path) as f:
                playlist_lines = []
                for line in f:
                    playlist_lines.append(line.strip())

                #print(playlist_lines)

                for song in songs:
                    fname = os.path.basename(song["path"])
                    try:
                        order = playlist_lines.index(fname) + 1
                        song["order"] = order
                    except ValueError:
                        pass
        else:
            pass
            #print(f"\nNO PLAYLIST PATH FOR DIR {root}")
        
        if not artist_name:
            raise Exception("Failed to get artist from " + root)
        
        info = AlbumInfo()
        info.artist_name = artist_name
        info.artist_path = artist_path
        info.songs = songs
        info.album_name = album_name
        info.playlist_path = playlist_path
        info.artwork_path = artwork_path
        info.order = album_order
        info.section = album_section
        info.year = year
        info.date = date
        info.bootleg = bootleg
        info.mine = mine
        info.videos = videos

    #print(info)

    return info

def LAUD_update_database():
    if os.path.exists(LAUD_database_path):
        backup = LAUD_database_path.with_suffix(".backup")
        os.rename(LAUD_database_path, backup)

    db = sqlite3.connect(LAUD_database_path)
    c = db.cursor()

    create_tables = True

    if create_tables:
        c.execute("""CREATE TABLE ARTISTS(
            id          integer primary key,
            name        text unique,
            path        text,
            favourite   integer
            )""")

        c.execute("""CREATE TABLE ALBUMS(
            id          integer primary key,
            artist_id   integer,
            name        text,
            playlist    text,
            artwork     text,
            album_order integer,
            section     integer,
            date        text,
            year        integer,
            bootleg     integer,
            mine        integer
            )""")

        c.execute("""CREATE TABLE SONGS(
            id      integer primary key,
            name    text,
            path    text
            )""")

        c.execute("""CREATE TABLE ALBUM_SONGS(
            song_id     integer,
            album_id    integer,
            track_order integer
            )""")

        c.execute("""CREATE TABLE VIDEOS(
            id      integer primary key,
            name    text,
            path    text
            )""")
            
        c.execute("""CREATE TABLE ALBUM_VIDEOS(
            video_id    integer,
            album_id    integer
            )""")
        
    ARTIST_IDS = {}
    width = os.get_terminal_size()[0]
    #my_gig_artists = get_mine()

    for root,dirs,files in os.walk(LAUD_music_root, True):
        if r"/_Cl/" in root: continue # some non ascii chars in filenames
        #if r"/A/" not in root: continue
        #if r"/Bootlegs/" in root: continue
        #if r"/TTRH/" in root: continue
        if r"/Dylan, Bob/Stuff" in root: continue
        #if r"/Interviews/" in root: continue

        relative_root = os.path.relpath(root, LAUD_music_root)

        dirs.sort()
        files.sort()

        string = f"=== scanning: {relative_root}"
        print(string.ljust(width), end="\r")

        album_info = get_album_info(root, files)

        if album_info:
            if album_info.artist_name in ARTIST_IDS:
                artist_id = ARTIST_IDS[album_info.artist_name]
            else:
                fav = False
                if album_info.artist_path:
                    fav_path = os.path.join(album_info.artist_path, "fav")
                    fav = os.path.isfile(fav_path)
                c.execute(f"""INSERT OR IGNORE INTO ARTISTS(name, path, favourite)
                              VALUES ( \"{album_info.artist_name}\", 
                                       \"{root}\",
                                       {fav}
                                     )
                              RETURNING id""")
                artist_id = c.fetchone()[0]
                #print(f"artist_id: {artist_id}")
                ARTIST_IDS[album_info.artist_name] = int(artist_id)

            c.execute(f"""INSERT INTO ALBUMS( artist_id, name, playlist,
                                              artwork, album_order, section,
                                              date, year, bootleg, mine )
                          VALUES (   {artist_id},
                                   \"{album_info.album_name}\", 
                                   \"{album_info.playlist_path}\", 
                                   \"{album_info.artwork_path}\", 
                                     {album_info.order}, 
                                     {album_info.section},
                                   \"{album_info.date}\",
                                     {album_info.year},
                                     {album_info.bootleg},
                                     {album_info.mine}
                                 )
                          RETURNING id""")
            album_id = c.fetchone()[0]
            #print(f"album_id: {album_id}")

            for song in album_info.songs:
                c.execute(f"""INSERT OR IGNORE INTO SONGS(name, path)
                              VALUES (\"{song['name']}\", 
                                      \"{song['path']}\")
                              RETURNING id""")
                song_id = c.fetchone()[0]

                #print(album_id, song_id, song['order'])
                c.execute(f"""INSERT INTO ALBUM_SONGS(song_id,album_id,track_order)
                              VALUES ( {song_id}, {album_id}, 
                                       {song['order']} )
                              """)

            for video in album_info.videos:
                c.execute(f"""INSERT OR IGNORE INTO VIDEOS(name, path)
                              VALUES (\"{video['name']}\", 
                                      \"{video['path']}\")
                              RETURNING id""")
                song_id = c.fetchone()[0]

                #print(album_id, song_id, song['order'])
                c.execute(f"""INSERT INTO ALBUM_VIDEOS(video_id,album_id)
                              VALUES ( {song_id}, {album_id} )
                              """)

    print() # to terminate the previous print

    db.commit()

    size = os.path.getsize(LAUD_database_path) / (1024*1024)

    print(f"Written {LAUD_database_path} ({size:.2} MB)")


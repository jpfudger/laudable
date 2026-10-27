import sqlite3

from laudable.config import LAUD_database_path
from laudable.errors import LAUD_query_error

class LAUD_query:
    # used in main.py to construct the query passed to LAUD_search
    
    def __init__(self, init={}):
        self.pattern  = init.get("pattern", None)
        self.song     = init.get("song", None)
        self.album    = init.get("album", None)
        self.artist   = init.get("artist", None)
        self.official = init.get("official", True)
        self.bootlegs = init.get("bootlegs", False)
        self.year     = init.get("year", 0)
        self.mine     = init.get("mine", False)
        self.videos   = init.get("videos", False)

        self.sort_by_song   = init.get("sort_by_song", False)
        self.sort_by_artist = init.get("sort_by_artist", False)
        self.sort_by_year   = init.get("sort_by_year", False)
        self.n              = init.get("n", 0)
        self.shuffle        = init.get("shuffle", 0)

        self.escape_char = "|"

    def __str__(self):
        string = ""
        return f"""
            pattern  : {self.pattern}
            song     : {self.song}
            album    : {self.album}
            artist   : {self.artist}
            official : {self.official}
            bootlegs : {self.bootlegs}
            year     : {self.year}
            mine     : {self.mine}
            videos   : {self.videos}
            """

    def escape_all(self):
        d = {}
        d[ord("%")] = f"{self.escape_char}%"
        d[ord("_")] = f"{self.escape_char}_"

        if self.pattern:
            if isinstance(self.pattern, str):
                self.pattern = self.pattern.translate(d)
            elif isinstance(self.pattern, list):
                self.pattern = [ p.translate(d) for p in self.pattern ]
        if self.song:
            self.song = self.song.translate(d)
        if self.album:
            self.album = self.album.translate(d)
        if self.artist:
            self.artist = self.artist.translate(d)

    def empty_query(self):
        if self.pattern:
            return False
        if self.song:
            return False
        if self.album:
            return False
        if self.artist:
            return False
        if self.year:
            return False

        return True

    def check(self):
        if (not self.official) and (not self.bootlegs):
            raise LAUD_query_error("Impossible query (!offical && !bootleg)")
        elif self.empty_query():
            raise LAUD_query_error("Empty query")

def LAUD_search(q, debug=False):
    connect = sqlite3.connect(LAUD_database_path)
    cursor = connect.cursor()

    q.check()
    q.escape_all()

    query = "SELECT S.path, S.name, AR.name, AL.name, AL.year, AL.bootleg, AL.mine "

    if q.videos:
        query += "FROM VIDEOS S " \
               + "JOIN ALBUM_VIDEOS SS ON SS.video_id = S.id "
    else:
        query += "FROM SONGS S " \
               + "JOIN ALBUM_SONGS SS ON SS.song_id = S.id "

    query += "JOIN ALBUMS AL ON AL.id = SS.album_id " \
           + "JOIN ARTISTS AR ON AR.id = AL.artist_id "

    where = []
    params = []

    if q.pattern:
        patterns = q.pattern
        if isinstance(patterns, str):
            patterns = [ patterns ]

        for pattern in patterns:
            where.append(f"S.path LIKE ? ESCAPE '{q.escape_char}' ")
            params.append(f"%{pattern}%")

    if q.song:
        where.append(f"S.name LIKE ? ESCAPE '{q.escape_char}' ")
        params.append(f"%{q.song}%")

    if q.album:
        where.append(f"AL.name LIKE ? ESCAPE '{q.escape_char}' ")
        params.append(f"%{q.album}%")

    if q.artist:
        where.append(f"AR.name LIKE ? ESCAPE '{q.escape_char}' ")
        params.append(f"%{q.artist}%")

    if q.year:
        where.append(f"AL.year = ? ")
        params.append(q.year)

    if q.mine:
        where.append(f"AL.mine = 1 ")

    if not q.official:
        where.append("AL.bootleg = 1 ")

    if not q.bootlegs:
        where.append("AL.bootleg = 0 ")

    if where:
        query += "WHERE " + "AND ".join(where)

    if q.sort_by_song:
        query += " ORDER BY S.name ASC"

    if q.sort_by_artist:
        query += " ORDER BY AR.name ASC"

    if q.sort_by_year:
        query += " ORDER BY CASE WHEN AL.year is 0 then 9999 end, AL.year ASC, S.name"

    if debug: print(query)
    if debug: print(params)

    try:
        cursor.execute(query, params)
    except sqlite3.OperationalError:
        print("Failed to execute query:")
        print(query)
        print(params)
        exit(1)

    data = cursor.fetchall()

    if q.n and len(data) > q.n:
        data = data[:q.n]

    if q.shuffle:
        import random
        random.shuffle(data)

    if debug: print(data)

    return data

def LAUD_print_stats():
    connect = sqlite3.connect(LAUD_database_path)
    cursor = connect.cursor()

    query = "SELECT COUNT(S.name) FROM SONGS S"
    cursor.execute(query)
    n_songs = cursor.fetchone()[0]

    query = """SELECT COUNT(S.name) 
               FROM SONGS S 
               JOIN ALBUM_SONGS SS ON SS.song_id = S.id
               JOIN ALBUMS AL ON AL.id = SS.album_id
               WHERE AL.mine = 1
               """
    cursor.execute(query)
    n_songs_mine = cursor.fetchone()[0]

    query = "SELECT COUNT(AL.name) FROM ALBUMS AL"
    cursor.execute(query)
    n_albums = cursor.fetchone()[0]

    query = "SELECT COUNT(AL.name) FROM ALBUMS AL WHERE AL.mine = 1"
    cursor.execute(query)
    n_albums_mine = cursor.fetchone()[0]

    query = "SELECT COUNT(V.path) FROM VIDEOS V"
    cursor.execute(query)
    n_videos = cursor.fetchone()[0]

    query = "SELECT COUNT(A.name) FROM ARTISTS A"
    cursor.execute(query)
    n_artists = cursor.fetchone()[0]

    print(f"{n_songs} songs ({n_songs_mine} mine)")
    print(f"{n_albums} albums ({n_albums_mine} mine)")
    print(f"{n_videos} videos")
    print(f"{n_artists} artists")

def LAUD_dump(dump_path=None):
    if not dump_path:
        from datetime import datetime
        timestamp = int(datetime.now().timestamp())
        fname = f"laudable-dump-{timestamp}"

        from pathlib import Path
        p = Path(LAUD_database_path) / ".." / fname
        dump_path = p.resolve()

    connect = sqlite3.connect(LAUD_database_path)
    cursor = connect.cursor()

    query = """SELECT S.name, AR.name, AL.name
               FROM SONGS S
               JOIN ALBUM_SONGS SS ON SS.song_id = S.id
               JOIN ALBUMS AL ON AL.id = SS.album_id
               JOIN ARTISTS AR ON AR.id = AL.artist_id
               """

    cursor.execute(query)
    data = cursor.fetchall()

    dump_lines = []

    for song, artist, album in data:
        dump_lines.append(f"{song}|{artist}|{album}")

    with open(dump_path, "w") as f:
        for line in dump_lines:
            f.write(line + "\n")

    print(f"Dumped {len(dump_lines)} to {dump_path}")

class LAUD_queries:
    def __init__(self):
        connect = sqlite3.connect(LAUD_database_path)
        self.cursor = connect.cursor()

    def query(self, q, p=[]):
        try:
            self.cursor.execute(q,p)
        except sqlite3.OperationalError as e:
            self._print("Failed to excute query:")
            self._print(q)
            #print(f"With error: {e}")
            raise e
        data = self.cursor.fetchall()
        return data

    def get_all_artists(self):
        q = "SELECT name FROM ARTISTS"
        artists = [ x[0] for x in self.query(q) ]
        return artists

    def get_albums_of_artist(self, artist):
        # with lots of album info

        # The WITH statement allows the return of the number of songs for
        # each album. This slows down the html generation from 18 seconds -> 28 seconds.
        # Maybe it's quicker to looking each song individually? Or maybe not?

        q = """
            WITH 
                ARTIST_ALBUM_SONGS AS (
                    SELECT AL.id album_id, COUNT(S.id) n_songs
                    FROM SONGS S
                    JOIN ALBUM_SONGS SS ON SS.song_id = S.id
                    JOIN ALBUMS AL ON AL.id = SS.album_id
                    JOIN ARTISTS AR ON AR.id = AL.artist_id
                    WHERE AR.name = ?
                    GROUP BY album_id
                    )
            SELECT AL.name, 
                   AL.year, 
                   AL.section, 
                   AL.album_order O, 
                   AL.playlist, 
                   AL.artwork,
                   AL.bootleg,
                   AL.mine,
                   AL.date,
                   AAS.n_songs
            FROM ALBUMS AL
            JOIN ARTISTS AR ON AR.id = AL.artist_id
            JOIN ARTIST_ALBUM_SONGS AAS ON AAS.album_id = AL.id
            WHERE AR.name = ?
            ORDER BY CASE WHEN O is 0 then 9999 END, O, AL.year, AL.name
            """
        p = [ artist, artist ]

        results = self.query(q, p)

        albums = []
        bootlegs = []

        for name, year, section, order, playlist, artwork, bootleg, mine, date, n_songs in results:
            if artwork == "None": artwork = None
            if playlist == "None": playlist = None

            d = { "name" :      name,
                  "artist" :    artist,
                  "year" :      year,
                  "section" :   section,
                  "order" :     order,
                  "playlist" :  playlist,
                  "artwork" :   artwork,
                  "bootleg" :   bootleg,
                  "mine" :      mine,
                  "date" :      date,
                  "n_songs" :   n_songs,
                }

            if not playlist:
                print(f"No playlist for: {artist} - {name}")
            elif bootleg:
                bootlegs.append(d)
            else:
                albums.append(d)

        return albums, bootlegs

    def get_stats(self, n_artists=100):
        # For top n artists, return the following:
        # n albums, n songs, n bootlegs, n bootleg songs, total albums, total songs

        q = """
            WITH 
                OFFICIAL_ALBUMS AS (
                    SELECT AL.artist_id artist_id, COUNT(AL.id) n
                    FROM ALBUMS AL
                    WHERE AL.bootleg = 0
                    GROUP BY artist_id
                    ),
                BOOTLEG_ALBUMS AS (
                    SELECT AL.artist_id artist_id, COUNT(AL.id) n
                    FROM ALBUMS AL
                    WHERE AL.bootleg = 1
                    GROUP BY artist_id
                    ),
                OFFICIAL_SONGS AS (
                    SELECT AL.artist_id artist_id, COUNT(S.id) n
                    FROM SONGS S
                    JOIN ALBUM_SONGS SS ON SS.song_id = S.id
                    JOIN ALBUMS AL ON AL.id = SS.album_id
                    WHERE AL.bootleg = 0
                    GROUP BY artist_id
                    ),
                BOOTLEG_SONGS AS (
                    SELECT AL.artist_id artist_id, COUNT(S.id) n
                    FROM SONGS S
                    JOIN ALBUM_SONGS SS ON SS.song_id = S.id
                    JOIN ALBUMS AL ON AL.id = SS.album_id
                    WHERE AL.bootleg = 1
                    GROUP BY artist_id
                    )
            SELECT AR.name, OA.n, BA.n, OS.n, BS.n
            FROM ARTISTS AR
            JOIN OFFICIAL_ALBUMS OA ON OA.artist_id = AR.id
            JOIN BOOTLEG_ALBUMS BA ON BA.artist_id = AR.id
            JOIN OFFICIAL_SONGS OS ON OS.artist_id = AR.id
            JOIN BOOTLEG_SONGS BS ON BS.artist_id = AR.id
            ORDER BY OS.n + BS.n DESC
            LIMIT ?
            """

            # SELECT AR.name, COUNT(S.id) N_S, COUNT(AL.id) N_A
            # FROM SONGS S
            # JOIN ALBUM_SONGS SS ON SS.song_id = S.id
            # JOIN ALBUMS AL ON AL.id = SS.album_id
            # JOIN ARTISTS AR ON AR.id = AL.artist_id
            # ORDER BY N_S

        p = [ n_artists ]

        self.cursor.execute(q, p)
        data = self.cursor.fetchall()

        stats = []

        for artist, oa, ba, os, bs in data:
            #print(artist.ljust(20), oa, ba, os, bs)
            d = { "artist": artist,
                  "albums": oa,
                  "bootleg_albums": ba,
                  "songs": os,
                  "bootleg_songs": bs,
                 }
            stats.append(d)

        return stats


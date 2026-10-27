#!/usr/bin/env python3
from laudable.queries import LAUD_query, LAUD_search, LAUD_print_stats, LAUD_dump
from laudable.update import LAUD_update_database
from laudable.errors import LAUD_query_error
from laudable.htmlgen import LAUD_html
import argparse
from datetime import datetime

def play(playlist, args):
    import subprocess
    
    playlist_path = r'/tmp/laudable_tmp_playlist.m3u'
    if args.debug:
        print(f"playlist_path: {playlist_path}")

    if len(playlist) > args.max:
        print(f"Restricting playlist to first {args.max} songs")
        playlist = playlist[:args.max]

    with open(playlist_path, "w") as f:
        for song in playlist:
            f.write(song + "\n")

    if args.videos:
        command = f"mplayer -really-quiet -playlist {playlist_path}"
        command = f"mplayer -quiet -playlist {playlist_path}"
    else:
        command = f"audacious {playlist_path}"
        command = f"GDK_BACKEND=x11 audacious {playlist_path}"

    subprocess.Popen(command, shell=True,
                     stdout=subprocess.DEVNULL, 
                     stderr=subprocess.DEVNULL )

def make_playlist(data, args):
    playlist = []

    # l_name = 0
    # l_artist = 0
    # l_album = 0

    # for path, name, artist, album in data:
    #     if len(name) > l_name: l_name = len(name)
    #     if len(artist) > l_artist: l_artist = len(artist)
    #     if len(album) > l_album: l_album = len(album)

    artists = {}

    got_boot = False
    got_mine = False

    for path, name, artist, album, year, bootleg, mine in data:
        if artist in artists:
            artists[artist] += 1
        else:
            artists[artist] = 1

        if year > 0 and not album.startswith(str(year)):
            album += f" [{year}]"

        flag = "   "
        if mine:
            got_mine = True
            flag = "** "
        elif bootleg:
            got_boot = True
            flag = " * "

        print(f"{name:40} {artist:20} {flag}{album}")
        if args.debug:
            print(f"    {path}")
        
        playlist.append(path)

    print("==========")
    notes = []
    if got_boot: 
        notes.append("* = bootleg")
    if got_mine:
        notes.append("** = mine")
    note_string = ""
    if notes:
        note_string = "(" + (", ".join(notes)) + ")"

    songs_str = "song" if len(playlist) == 1 else "songs"
    artists_str = "artist" if len(artists) == 1 else "artists"
    print(f"{len(playlist)} {songs_str} by {len(artists)} {artists_str} {note_string}")

    return playlist

def get_args():
    parser = argparse.ArgumentParser("laudable")
    parser.add_argument("pattern", nargs="*", type=str, default=None, metavar="<>",
                        help="filter using entire song path")
    parser.add_argument("--song", "-s", type=str, default=None, metavar="<>",
                        help="filter using song name")
    parser.add_argument("--album", "-a", type=str, default=None, metavar="<>",
                        help="filter using album name")
    parser.add_argument("--artist", "-A", type=str, default=None, metavar="<>",
                        help="filter using artist name")
    parser.add_argument("--bootlegs", "-b", action="store_true",
                        help="include bootlegs")
    parser.add_argument("--year", "-y", type=int, default=None, metavar="<>",
                        help="restrict to year")
    parser.add_argument("-o", action="store_true",
                        help="output only; don't play")
    parser.add_argument("--stats", action="store_true",
                        help="print statistics and exit")
    parser.add_argument("--shuffle", action="store_true",
                        help="shuffle playlist file")
    parser.add_argument("--max", type=int, default=500, metavar="<>",
                        help="max length of playlist [500]")
    parser.add_argument("--update", action="store_true",
                        help="update song database")
    parser.add_argument("--debug", action="store_true",
                        help="print song paths")
    parser.add_argument("--dump", action="store_true",
                        help="dump songs to file")
    parser.add_argument("--sort", choices=["song", "artist", "year"], default="song",
                        help="how to sort results (and playlist)")
    parser.add_argument("-n", type=int, default=0, metavar="<>",
                        help="how many results to return")
    parser.add_argument("--html", action="store_true",
                        help="generate html")
    parser.add_argument("--mine", "-m", action="store_true",
                        help="my gigs (including bootlegs)")
    parser.add_argument("--videos", "-v", action="store_true",
                        help="videos (includig bootlegs)")
    args = parser.parse_args()

    if args.sort == "song":   args.sort_by_song = True
    if args.sort == "artist": args.sort_by_artist = True
    if args.sort == "year":   args.sort_by_year = True

    if args.mine:             args.bootlegs = True
    if args.videos:           args.bootlegs = True

    return args

def main():
    args = get_args()

    if args.update or args.html:
        if args.update:
            print("Updating database...")
            start_time = datetime.now()
            LAUD_update_database()
            delta = datetime.now() - start_time
            print(f"Update time taken: {delta}")

            LAUD_print_stats()
            LAUD_dump()

        if args.html:
            print("Updating HTML...")
            start_time = datetime.now()
            LAUD_html()
            delta = datetime.now() - start_time
            print(f"HTML update time taken: {delta}")
    elif args.stats:
        LAUD_print_stats()
    elif args.dump:
        LAUD_dump()
    else:
        query = LAUD_query(vars(args))

        try:
            data = LAUD_search(query)
        except LAUD_query_error as e:
            print(f"Laudable error: {e}")
            exit(1)

        playlist = make_playlist(data, args)
        if playlist and not args.o: 
            play(playlist, args)

if __name__ == "__main__":
    main()


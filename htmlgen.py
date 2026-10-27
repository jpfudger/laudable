from laudable.config import LAUD_html_root, LAUD_music_root
from laudable.queries import LAUD_queries
from datetime import datetime
import re
import matplotlib.pyplot as plt

SPLIT_ARIST_ALBUMS_BY_DECADE = False

class LAUD_html():
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.queries = LAUD_queries()

        self.alphabet_lines = []

        self.make_css()
        self.make_javascript()
        self.make_html()
    
    def _print(self, msg=""):
        if self.verbose:
            print(msg)

    def _favourites(self):
        favs = []
        favs.append("Adams, Ryan")        # A
        favs.append("Beach Boys")         # B
        favs.append("Cohen, Leonard")     # C
        favs.append("Dylan, Bob")         # D
        favs.append("Earle, Steve")       # E
        favs.append("Felice Brothers")    # F
        favs.append("Grateful Dead")      # G
        favs.append("Hitchcock, Robyn")   # H
        favs.append("Isbell, Jason")      # I
        favs.append("Jansch, Bert")       # J
        favs.append("Kinks")              # K
        favs.append("Led Zeppelin")       # L
        favs.append("Marling, Laura")     # M
        favs.append("Newman, Randy")      # N
        favs.append("Oasis")              # O
        favs.append("Petty, Tom")         # P
        favs.append("Queen")              # Q
        favs.append("Rolling Stones")     # R
        favs.append("Springsteen, Bruce") # S
        favs.append("Thompson, Richard")  # T
        favs.append("U2")                 # U
        favs.append("Velvet Underground") # V
        favs.append("Waits, Tom")         # W
        favs.append("XTC")                # X
        favs.append("Young, Neil")        # Y
        favs.append("Zevon, Warren")      # Z
        return favs

    def make_css(self):
        path = LAUD_html_root / "style.css"

        string = """
            body {
                font-family: sans-serif;
                color: gray;
                background: black;
                }

            .col1 {
                column-count: 1;
                }
            
            .col2 {
                column-count: 2;
                width: 40%;
                }
            
            .col3 {
                column-count: 3;
                width: 50%;
                }
            
            #alphabet {
                position: absolute;
                float: left;
                width: 90%;
                top: 10;
                left: 10;
                font-size: x-large;
                font-weight: bold;
                }
            
            #index {
                position: absolute;
                float: left;
                height: 90%;
                width: 18%;
                top: 50;
                left: 10;
                /* overflow-y: auto; */
                }
          
            #content {
                position: absolute;
                float: left;
                width: 85%;
                left: 15%;
                top: 50;
                height: 90%;
                }

             a:link, a:visited {
                 text-decoration: none;
                 color: #C9BE62; /* yellow */
                 text-decoration: bold;
                 }
             
             a.boot:link, a.boot:visited, a.boot:active {
                 text-decoration: none;
                 color: #27ae60; /* green */
                 text-decoration: bold;
                 }
            a.boot-name {
                font-size: small;
                color: #27ae60; /* green */
                }
            a.mine {
                color: #C9BE62; /* yellow */
                }
            img.album {
                width: 100px;
                height: 100px;
                border: 1px solid #C9BE62; /* yellow */
                }
            img.years {
                width: 750px;
                }
            span.boot-date {
                display: inline-block;
                font-family: mono;
                color: gray;
                font-size: small;
                padding-right: 10px;
                width: 120px;
                height: 10px;
                }
            a.studio {
                color: #3498db; /* cyan */
                }
            .stats {
                border-collapse: collapse;
                border: 1px solid gray;
                padding: 5px;
                }
            .count {
                display: inline-block;
                font-family: monospace;
                font-size: small;
                }

        """

        with open(path, "w") as f:
            f.write(string)
        
    def make_javascript(self):
        path = LAUD_html_root / "script.js"

        string = """
            function nextPage() {
                // look for > in <a> tags and jump to the link
                var tags = document.getElementsByTagName("a");
                for ( var i=0; i<tags.length; i++ )
                    {
                    if ( tags[i].innerHTML == "&gt;" )
                        { 
                        window.open(tags[i].href, target="_self");
                        }
                    }
                }

            function previousPage() {
                // look for < in <a> tags and jump to the link
                var tags = document.getElementsByTagName("a");
                for ( var i=0; i<tags.length; i++ )
                    {
                    if ( tags[i].innerHTML == "&lt;" )
                        { 
                        window.open(tags[i].href, target="_self");
                        }
                    }
            }

            function checkKey(e) {
                e = e || window.event;

                if      ( e.keyCode == '65' ) { window.open("a.html", target="_self"); }
                else if ( e.keyCode == '66' ) { window.open("b.html", target="_self"); }
                else if ( e.keyCode == '67' ) { window.open("c.html", target="_self"); }
                else if ( e.keyCode == '68' ) { window.open("d.html", target="_self"); }
                else if ( e.keyCode == '69' ) { window.open("e.html", target="_self"); }
                else if ( e.keyCode == '70' ) { window.open("f.html", target="_self"); }
                else if ( e.keyCode == '71' ) { window.open("g.html", target="_self"); }
                else if ( e.keyCode == '72' ) { window.open("h.html", target="_self"); }
                else if ( e.keyCode == '73' ) { window.open("i.html", target="_self"); }
                else if ( e.keyCode == '74' ) { window.open("j.html", target="_self"); }
                else if ( e.keyCode == '75' ) { window.open("k.html", target="_self"); }
                else if ( e.keyCode == '76' ) { window.open("l.html", target="_self"); }
                else if ( e.keyCode == '77' ) { window.open("m.html", target="_self"); }
                else if ( e.keyCode == '78' ) { window.open("n.html", target="_self"); }
                else if ( e.keyCode == '79' ) { window.open("o.html", target="_self"); }
                else if ( e.keyCode == '80' ) { window.open("p.html", target="_self"); }
                else if ( e.keyCode == '81' ) { window.open("q.html", target="_self"); }
                else if ( e.keyCode == '82' ) { window.open("r.html", target="_self"); }
                else if ( e.keyCode == '83' ) { window.open("s.html", target="_self"); }
                else if ( e.keyCode == '84' ) { window.open("t.html", target="_self"); }
                else if ( e.keyCode == '85' ) { window.open("u.html", target="_self"); }
                else if ( e.keyCode == '86' ) { window.open("v.html", target="_self"); }
                else if ( e.keyCode == '87' ) { window.open("w.html", target="_self"); }
                else if ( e.keyCode == '88' ) { window.open("x.html", target="_self"); }
                else if ( e.keyCode == '89' ) { window.open("y.html", target="_self"); }
                else if ( e.keyCode == '90' ) { window.open("z.html", target="_self"); }

                else if ( e.keyCode == '188' ) { previousPage(); }
                else if ( e.keyCode == '190' ) { nextPage(); }
                }

            document.onkeydown = checkKey;
        """

        with open(path, "w") as f:
            f.write(string)

    def get_alphabet_lines(self):
        if not self.alphabet_lines:
            self.alphabet_lines = []
    
            self.alphabet_lines.append("<a href=stats.html>%</a>")
            self.alphabet_lines.append("<a href=years.html>#</a>")
            self.alphabet_lines.append("|")

            alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            for letter in alpha:
                lurl = LAUD_html_root / f"{letter.lower()}.html"
                link = f"<a href=\"{lurl}\">{letter}</a>"
                self.alphabet_lines.append(link)

        return self.alphabet_lines

    def _make_artist_fname(self, artist_name):
        fname = artist_name.lower()
        fname = re.sub(r"[,'\- ]+", "_", fname)
        return fname

    def make_html(self):
        letters = {}
        all_artists = self.queries.get_all_artists()
        albums_by_year = {}

        for artist in all_artists:
            self._print()
            self._print(f"=== {artist}")

            fname = self._make_artist_fname(artist)
            fname_boots = fname + "_boots"
            albums, bootlegs = self.queries.get_albums_of_artist(artist)
            a_data = { "fname": fname, "fname_boots": fname_boots, "albums": albums, "bootlegs": bootlegs }

            initial = artist[0]
            if initial not in letters:
                letters[initial] = {}
            letters[initial][artist] = a_data

            for album in albums:
                year = album["year"]
                if year:
                    if year not in albums_by_year:
                        albums_by_year[year] = []
                    albums_by_year[year].append(album)

        for letter, artists in letters.items():
            letter_path = LAUD_html_root / f"{letter.lower()}.html"
            letter_artist_lines = []
            for a in sorted(artists):
                a_data = artists[a]
                aurl = LAUD_html_root / f"{a_data['fname']}.html"
                b_link = f" <a class=boot href=\"{a_data['fname_boots']}.html\">+</a>" if a_data["bootlegs"] else ""
                alink = f"<a href=\"{aurl}\">{a}</a>{b_link}<br>"
                letter_artist_lines.append(alink)

            self.write_html(letter_artist_lines, [], letter_path)

            for a in artists:
                a_data = artists[a]
                self.make_artist_pages(a, a_data["fname"], letter_artist_lines, a_data["albums"], a_data["bootlegs"])

        self.make_index_page()
        self.make_stats_page()
        self.make_years_pages(albums_by_year)

    def make_artist_pages(self, artist, fname, letter_artist_lines, albums, bootlegs):
        fname_boots = fname + "_boots"
        
        lines = []
        b_link = f" <a class=boot href=\"{fname_boots}.html\">+</a>" if bootlegs else ""
        lines.append(f"<h2>{artist}{b_link}</h2>")

        #sections = {}
        #for a in albums:
        #    section = a["section"]
        #    if section not in sections:
        #        sections[section] = []
        #    sections[section].append(section
        
        last_section = None
        section_lines = []
        sections = [ section_lines ]
        last_decade = None

        for a in albums:
            name     = a["name"]
            year     = a["year"]
            section  = a["section"]
            order    = a["order"]
            playlist = a["playlist"]
            artwork  = a["artwork"]
            bootleg  = a["bootleg"]

            if not playlist:
                continue

            if not artwork:
                artwork = "../blank.jpg"

            if last_section is None:
                last_section = section
            elif last_section != section:
                last_section = section
                section_lines = []
                sections.append(section_lines)

            decade = int(str(year)[:3])

            if SPLIT_ARIST_ALBUMS_BY_DECADE:
                if len(sections) == 1: # first section only (don't split misc sections)
                    if last_decade is not None and last_decade != decade:
                        section_lines.append("<br>")

            last_decade = decade
            
            self._print(f"    {name} ({year}) [{section}]")
            
            hover = f"{name}, {year}" if year else name
            img = f"<img class=album title=\"{hover}\" src=\"{artwork}\">"
            section_lines.append(f"<a href=\"{playlist}\">{img}</a>")

        for section_lines in sections:
            for i, sl in enumerate(section_lines):
                lines.append(sl)

                # Maybe add a line break to make things looks nice.
                # This reproduces the logic from laudable1, but
                # it leaves a lot to be desired...

                if (not SPLIT_ARIST_ALBUMS_BY_DECADE) and len(sl) >= 12:
                    if len(sl) == 12:
                        if (i+1) % 6 == 0:
                            lines.append('<br>')
                    elif len(sl) == 14:
                        if (i+1) % 7 == 0:
                            lines.append('<br>')
                    elif len(sl) == 16:
                        if (i+1) % 8 == 0:
                            lines.append('<br>')
                    elif len(sl) == 18:
                        if (i+1) % 9 == 0:
                            lines.append('<br>')
                    elif len(sl) == 20:
                        if (i+1) % 10 == 0:
                            lines.append('<br>')
                    elif (i+1) % 12 == 0:
                        lines.append('<br>')

            lines.append("<br> <br>")
        
        path = LAUD_html_root / (fname + ".html")
        self.write_html(letter_artist_lines, lines, path)
        
        if artist in self._favourites():
            # favourite: duplicate artist page as letter page
            letter_path = LAUD_html_root / f"{artist[0].lower()}.html"
            self.write_html(letter_artist_lines, lines, letter_path)
        
        if bootlegs:
            self.make_artists_bootlegs_pages(artist, bootlegs, fname_boots, letter_artist_lines)
    
    def make_artists_bootlegs_pages(self, artist, bootlegs, fname, letter_artist_lines):
        lines = []
        o_fname = fname.replace("_boots", "")
        lines.append(f"<h2>{artist} <a class=boot href=\"{o_fname}.html\">+</a></h2>")

        if len(bootlegs) > 50:
            # partition into years
            years = {}

            for a in bootlegs:
                year = a["year"]
                if year not in years:
                    years[year] = []
                years[year].append(a)

            expanded_years = self._expand_years(list(years.keys()), start_at=[0])

            year_list = list(years.keys())
            year_list.sort()

            for year in expanded_years:
                if year in years:
                    yr_lines = []
                    yr_lines.append(f"<h2>{artist} <a class=boot href=\"{o_fname}.html\">+</a></h2>")

                    index = year_list.index(year)

                    prev_link = "&lt;"
                    if index > 0 and year_list[index-1] != 0:
                        prev_link = f"<a href=\"{fname}_{year_list[index-1]}.html\">&lt;</a>"

                    next_link = "&gt;"
                    if index < len(year_list)-1:
                        next_link = f"<a href=\"{fname}_{year_list[index+1]}.html\">&gt;</a>"

                    yr_lines.append(f"<h2>{prev_link} {year} {next_link}</h2>")

                    colclass = self._colclass(years[year])
                    yr_lines.append(f"<div class={colclass}>")
                    
                    for b in years[year]:
                        yr_link = self._format_bootleg(b)
                        yr_lines.append(yr_link + "<br>")

                    yr_lines.append("</div>")

                    yr_path = LAUD_html_root / (fname + f"_{year}.html")
                    self.write_html(letter_artist_lines, yr_lines, yr_path)

                    link = f"<a href=\"{yr_path}\">{year}</a>"
                    lines.append(link)
                else:
                    lines.append(str(year))

                if str(year).endswith("9"):
                    lines.append("<br>")

            if 0 in years:
                lines.append("<br> <br>")
                # add misc (which will have been stripped out by _expand_years()
                for b in years[0]:
                    yr_link = self._format_bootleg(b)
                    lines.append(yr_link + "<br>")

        else:
            colclass = self._colclass(bootlegs)
            lines.append(f"<div class={colclass}>")
            noyears = []
            last_decade = None
            for b in bootlegs:
                line = self._format_bootleg(b)

                if b["year"] == 0:
                    noyears.append(line + "<br>")
                else:
                    decade = str(b["year"])[2]
                    if not last_decade is None and last_decade != decade:
                        lines.append("<br>")
                    last_decade = decade

                    lines.append(line + "<br>")

            if noyears:
                lines.append("<br>")
                for line in noyears:
                    lines.append(line)

            lines.append("</div>")
        
        path = LAUD_html_root / (fname + ".html")
        self.write_html(letter_artist_lines, lines, path)

    def make_index_page(self):
        path = LAUD_html_root / "index.html"
        self.write_html([], [], path)

    def make_stats_page(self):
        path = LAUD_html_root / "stats.html"

        index = []
        content = []

        content.append("<table class=stats>")
        content.append("<thead>")
        content.append("<tr>")
        content.append("<th class=stats></th>")
        content.append("<th class=stats>Artist</th>")
        content.append("<th class=stats>Official<br>Albums</th>")
        content.append("<th class=stats>Official<br>Songs</th>")
        content.append("<th class=stats>Bootleg<br>Albums</th>")
        content.append("<th class=stats>Bootleg<br>Songs</th>")
        content.append("<th class=stats>Total<br>Albums</th>")
        content.append("<th class=stats>Total<br>Songs</th>")
        content.append("</tr>")
        content.append("</thead>")
        content.append("<tbody>")

        n = 1
        for stat in self.queries.get_stats():
            artist = stat["artist"]
            fname = LAUD_html_root / (self._make_artist_fname(artist) + ".html")
            link = f"<a href=\"{fname}\">{artist}</a>"
            row = "<tr>"
            row += f"<td class=stats>{n}</td>"
            row += f"<td class=stats>{link}</td>"
            row += f"<td class=stats>{stat['albums']}</td>"
            row += f"<td class=stats>{stat['songs']}</td>"
            row += f"<td class=stats>{stat['bootleg_albums']}</td>"
            row += f"<td class=stats>{stat['bootleg_songs']}</td>"
            row += f"<td class=stats>{stat['albums']+stat['bootleg_albums']}</td>"
            row += f"<td class=stats>{stat['songs']+stat['bootleg_songs']}</td>"
            row += "</tr>"
            content.append(row)
            n += 1

        content.append("</tbody>")
        content.append("</table>")

        self.write_html(index, content, path)

    def _colclass(self, giglist):
        colclass = "col1"
        if len(giglist) > 25: colclass = "col2"
        if len(giglist) > 50: colclass = "col3"
        return colclass

    def _expand_years(self, years, start_at=[0,5]):
        years = [y for y in years if y > 0 ]
        years.sort()

        start_year = years[0]
        while True:
            if int(str(start_year)[-1]) in start_at:
                break
            start_year -= 1

        ret_years = list(range(start_year, years[-1]+1))

        return ret_years

    def _format_bootleg(self, bootleg):
        playlist = bootleg["playlist"]
        mine = bootleg["mine"]

        date = ""
        name = bootleg["name"]
        studio = False

        if bootleg["year"] and " " in name:
            #print(bootleg["name"], "-", bootleg["date"])
            dir_date, name = bootleg["name"].split(" ", maxsplit=1)

            dt = datetime.strptime(bootleg["date"], "%Y-%m-%d")
            date = dt.strftime("%Y-%b-%d")

            if dir_date != dt.strftime("%Y.%m.%d"):
                # date is incomplete!
                date = ""
                y = str(bootleg["year"])
                m = dt.strftime("%m")


                if dir_date in [ str(y), f"{y}.00.00", f"{y}.00" ]:
                    date = y
                elif dir_date in [ f"{y}.{m}", f"{y}.{m}.00"]:
                    date = dt.strftime("%Y-%b")
                else:
                    #print(f"   >{dir_date}<", "   ", f"{y}.{m}")
                    date = dir_date

                    m_dir_month = re.match(r"\d\d\d\d\.(\d\d)$", dir_date)
                    if m_dir_month:
                        dummy_date = datetime.strptime(dir_date + ".01", "%Y.%m.%d")
                        if dummy_date:
                            date = dummy_date.strftime("%Y-%b")

        if name.startswith("[") and name.endswith("]"):
            name = name[1:-1]

        studio_keywords = [ 'studio', 'rehears', 'demo', 'outtake', 'session', 'acetate', 'radio', 'bbc' ]
        for kw in studio_keywords:
            if kw in name.lower():
                studio = True
                break

        classes = [ "boot-name" ]
        if mine: classes.append("mine")
        if studio: classes.append("studio")

        class_string = " class=\"" + ( " ".join(classes) ) + "\""

        date_tag = f"<span class=boot-date>{date}</span>"
        link_tag = f"<a href=\"{playlist}\"{class_string}>{name}</a>"

        link = date_tag + " " + link_tag

        n_songs = bootleg["n_songs"]
        if n_songs:
            link += f" <div class=count>{n_songs}</div>"

        return link

    def plot_albums_by_year(self, albums_by_year, dest_path):
        years = list(albums_by_year.keys())
        years.sort()
        years = list(range(years[0], years[-1]+1))
        totals = []
        for year in years:
            if year in albums_by_year:
                totals.append(len(albums_by_year[year]))
            else:
                totals.append(0)

        fig, ax = plt.subplots()
        bar1 = ax.bar( years, totals,  align='center', color='#153E7E' )

        tick_pos = [ y for y in years if y % 5 == 0 ]
        tick_lab = [ str(y)[2:] for y in tick_pos ]

        plt.xticks(tick_pos, tick_lab)
        ax.tick_params(direction='out')
        plt.grid(visible=True, which='both') #, color='0.65',linestyle='-')
        ax.set_axisbelow(True)

        fig.savefig(dest_path, bbox_inches='tight', dpi=300)
        plt.close()

    def make_years_pages(self, albums_by_year):
        path = LAUD_html_root / "years.html"

        years = albums_by_year.keys()
        years = list(years)
        years.sort()
        expanded_years = self._expand_years(years)

        plot_path = LAUD_html_root / "years.png"
        self.plot_albums_by_year(albums_by_year, plot_path)

        year_index_lines = [ "<br>" ]
        for year in expanded_years:
            ylink = str(year)
            if year in years:
                ylink = f"<a href=\"{year}.html\">{year}</a>"
            year_index_lines.append(ylink + "&nbsp;")

            if str(year).endswith("9"):
                year_index_lines.append("<br><br>")
            elif str(year).endswith("4"):
                year_index_lines.append("<br>")

        for year in years:
            ypath = LAUD_html_root / f"{year}.html"
            index = years.index(year)

            prev_link = "&lt;"
            if index > 0:
                prev_link = f"<a href=\"{years[index-1]}.html\">&lt;</a>"

            next_link = "&gt;"
            if index < len(years)-1:
                next_link = f"<a href=\"{years[index+1]}.html\">&gt;</a>"

            year_album_lines = [ f"<h2>{prev_link} {year} {next_link}</h2>" ]
            for a in albums_by_year[year]:
                hover = f"{a['name']}, {a['artist']}"
                artwork = a['artwork']
                if not artwork:
                    artwork = "../blank.jpg"
                img = f"<img class=album title=\"{hover}\" src=\"{artwork}\">"
                year_album_lines.append(f"<a href=\"{a['playlist']}\">{img}</a>")

            self.write_html(year_index_lines, year_album_lines, ypath)

        self.write_html(year_index_lines, [ f"<img class=years src=\"{plot_path}\">" ], path)

    def write_html(self, index, content, path):
        title = "Laudable"

        lines = []
        lines.append("<html>")
        lines.append("<head>")
        lines.append(f"    <title>{title}</title>")
        lines.append("    <link rel=\"stylesheet\" type=\"text/css\" href=\"style.css\">")
        lines.append("    <link rel=\"shortcut icon\" href=\"../vinyl.ico\" type=\"image/x-icon\">")
        lines.append("    <script src=\"script.js\"></script>")
        lines.append("</head>")
        lines.append("<body>")
        lines += [ "<div id=alphabet>" ]
        lines += self.get_alphabet_lines()
        lines += [ "</div>" ]

        lines += [ "<div id=index>" ]
        if index:
            lines += index
        lines += [ "</div>" ]

        lines += [ "<div id=content>" ]
        if content:
            lines += content
        lines += [ "</div>" ]

        lines.append("</body>")
        lines.append("</html>")

        with open(path, "w") as f:
            for line in lines:
                f.write(line + "\n")


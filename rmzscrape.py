'''
   Module     : rmzscrape.py
   Description: extract "MP3" format movies from rapidmoviez website and
                create an HTML file listing those movies and their link
   Author     : ricS
   Date       : 24 June 2021
'''

import datetime
import os
from requests_html import HTML, HTMLSession

# constants
BASE_URL = "https://rmz.cr/l/m"
LINK_BASE_URL = "https://rmz.cr"
MAX_PAGES = 30

# create out directory if not existing in current directory
if not os.path.exists("out"):
    os.mkdir("out")

# generate a filename based on datetime
dt = datetime.datetime.now()
filename = "out\\RMZ_" + dt.strftime("%m%d%Y_%H%M") + ".html"

# get bookmarked link if the file exists
last_link = "NONE"
bookmark_file = "out\\bookmark.txt"
if os.path.isfile(bookmark_file):
    with open(bookmark_file, "r") as fp:
        last_link = fp.readline().rstrip()
        last_link = last_link.replace('\n','')

session = HTMLSession()

# scrape the pages for MP3 movies
movies = []
page = 1
is_first = True
firstEntryLink = ""
while page <= MAX_PAGES:
    print("Scanning page", page, "...")
    url = BASE_URL + '/' + str(page)
    r = session.get(url)
    
    blogpost = r.html.find('.blog-post')

    for post in blogpost:
        entry = post.find('h3', first=True)

        # get title - just the first line)
        title = entry.text.split('\n')[0]

        # get link
        anchor = entry.find('a', first=True)
        link = anchor.attrs['href'].split('?')[0]

        # if link is bookmarked before, set this as the last page 
        if link.upper == last_link:
            page = MAX_PAGES

        # filter out - only take those with "MP3" in the title
        if title.upper().find("MP3") >= 0:
            movies.append([title, link])

        # save the first entry found (so next time, we'll stop here)
        if is_first:
            firstEntryLink = link.upper()
            is_first = False

    page = page+1
    
# write to html file
print("Writing to html file...")
count = 0
with open(filename, 'w') as fp:
    fp.write('<html>\n')
    fp.write('<head>\n')
    fp.write('</head>\n')
    fp.write('<body>\n')
    fp.write('<h1>' + filename + '</h1>\n')

    for movie in movies:
        fp.write('<h3><a href="' + LINK_BASE_URL + movie[1] + '" target="_new">'+ movie[0] + '</a>\n')
        count += 1 

    fp.write('</body>\n')
    fp.write('</html\n')    

print("File", filename, "created.")

# write bookmark
if len(firstEntryLink) > 0:
    with open(bookmark_file, "w") as fp:
        fp.write(firstEntryLink)

print('Total movies extracted from site:', count)
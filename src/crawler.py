#!/usr/bin/python3


# pip install --user requests beautifulsoup4
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import sys


# , depth, maxdepth, visited
def crawl(url, depth, maxdepth, visited):
    if depth > maxdepth:
        return
    visited.append(url)

    """5
    Given an absolute URL, print each hyperlink found within the document.

    Your task is to make this into a recursive function that keeps following
    links until one of two base cases are reached:

    0) No new, unvisited links are found
    1) The maximum depth of recursion is reached

    You will need to change this function's signature to fulfill this
    assignment.
    """

    try:
        response = requests.get(url)
        # response is not None or

        if not response.ok:
            print(f"crawl({url}): {response.status_code} {response.reason}")
            return
        print('    ' * depth, end='')
        print(url)

        html = BeautifulSoup(response.text, 'html.parser')
        links = html.find_all('a')

        for a in links:
            link = a.get('href')
            link = link if link == None else link.split('#')[0]

            if link:
                # Create an absolute address from a (possibly) relative URL
                absoluteURL = urljoin(url, link)

                # Only deal with resources accessible over HTTP or HTTPS
                if absoluteURL.startswith('http'):

                    if absoluteURL not in visited:
                        crawl(absoluteURL, depth + 1, maxdepth, visited)


    except Exception as e:
        print(f"crawl(): {e}")
    return


## An absolute URL is required to begin
if len(sys.argv) < 2:
    print("Error: no Absolute URL supplied")
    sys.exit(1)
else:
    url = sys.argv[1]

parsed = urlparse(url)
if parsed.scheme == '' or parsed.netloc == '':
    print("Error: Invalid URL supplied.\nPlease supply an absolute URL to this program")
    sys.exit(2)

## The user may override the default recursion depth of 3
maxDepth = 3
if len(sys.argv) > 2:
    maxDepth = int(sys.argv[2])

plural = 's'
if maxDepth == 1:
    plural = ''

print(f"Crawling from {url} to a maximum depth of {maxDepth} link{plural}")
crawl(url, 0, maxDepth, [])

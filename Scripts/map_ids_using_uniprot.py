import urllib,urllib2

import sys

if __name__ == '__main__':
    filename = sys.argv[1]
    ids = None
    with open(filename, "r") as f:
        ids = " ".join(map(lambda x: x.rstrip(), f))





    url = 'http://www.uniprot.org/mapping/'

    params = {
    'from':'P_REFSEQ_AC',
    'to':'ACC',
    'format':'tab',
    'query':ids
    }

    data = urllib.urlencode(params)
    request = urllib2.Request(url, data)
    contact = "" # Please set your email address here to help us debug in case of problems.
    request.add_header('User-Agent', 'Python %s' % contact)
    response = urllib2.urlopen(request)
    page = response.read(200000)
    print page
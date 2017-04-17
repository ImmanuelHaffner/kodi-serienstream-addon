#
#   This file implements an API to SerienStream.to
#

import json
import re
import sys
import urllib
import urllib2


class SerienStream:
    base_url = 'https://serienstream.to'

    @staticmethod
    def search(search_string):
        url = SerienStream.base_url + '/ajax/search'
        post_data = {'keyword': search_string}
        print('URL: ' + url)
        print('POST: ' + urllib.urlencode(post_data))
        try:
            req = urllib2.Request(url, urllib.urlencode(post_data).encode())
            json_data = urllib2.urlopen(req).read()
            data = json.loads(json_data)
            return data
        except urllib2.HTTPError:
            return list()

if __name__ == '__main__':
    search_string = sys.argv[1]
    print('Searching SerienStream.to for "' + search_string + '"')
    data = SerienStream.search(search_string)

    print
    for d in data:
        title = re.sub('<[/a-zA-Z]*>', '', d['title'])
        print(title)
        print(d['link'])
        print

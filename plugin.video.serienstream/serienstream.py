#
#   This file implements an API to SerienStream.to
#

from pyquery import PyQuery
from selenium import webdriver
import json
import re
import sys
import urllib
import urllib2


class SerienStream:
    base_url = 'https://serienstream.to'
    embed_url = 'https://openload.co/embed'

    @staticmethod
    def search(search_string):
        url = SerienStream.base_url + '/ajax/search'
        post_data = {'keyword': search_string}
        try:
            req = urllib2.Request(url, urllib.urlencode(post_data).encode())
            json_data = urllib2.urlopen(req).read()
            data = json.loads(json_data)
            return data
        except urllib2.HTTPError:
            return list()

    @staticmethod
    def get_seasons(url):
        dom = PyQuery(url=url)
        dom.make_links_absolute(base_url=SerienStream.base_url)
        seasons = dom('div#stream ul:first-child a')
        season_list = list()
        for s in seasons:
            season = PyQuery(s)
            season_list.append((season.text(), season.attr.href))
        return season_list

    @staticmethod
    def get_episodes(url):
        dom = PyQuery(url=url)
        dom.make_links_absolute(base_url=SerienStream.base_url)
        episodes = dom('table.seasonEpisodesList td.seasonEpisodeTitle > a')
        episode_list = list()
        for e in episodes:
            episode = PyQuery(e)
            episode_list.append((episode.text(), episode.attr.href))
        return episode_list

    @staticmethod
    def get_hosters_for_episode(url):
        dom = PyQuery(url=url)
        dom.make_links_absolute(base_url=SerienStream.base_url)
        hosters = dom('div.hosterSiteVideo > ul > li > div > a')
        hoster_list = list()
        for h in hosters:
            hoster = PyQuery(h)
            hoster_list.append((hoster.find('h4').text(), hoster.attr.href))
        return hoster_list

if __name__ == '__main__':
    search_string = sys.argv[1]
    print(u'Searching SerienStream.to for "' + search_string + '"')
    data = SerienStream.search(search_string)


    #
    #   Get seasons
    #
    series = data[0]
    title = re.sub('<[/a-zA-Z]*>', '', series['title'])
    link = series['link']
    print(u'getting seasons for series "{}" from "{}"'.format(title, link))
    seasons = SerienStream.get_seasons(link)
    for title, url in seasons:
        print(u'{} - {}'.format(title, url))
    print

    #
    #   Get episodes
    #
    url = seasons[0][1]
    episodes = SerienStream.get_episodes(url)
    for title, url in episodes:
        print(u'{} - {}'.format(title, url))
    print

    #
    # Get hoster
    #
    url = episodes[0][1]
    hosters = SerienStream.get_hosters_for_episode(url)
    for title, url in hosters:
        print(u'{} - {}'.format(title, url))
    print

    #
    # Get video
    #
    url = hosters[0][1]
    print(u'getting video from URL "{}"'.format(url))
    headers = { 'User-Agent' : 'Mozilla/5.0' }
    req = urllib2.Request(url, None, headers)
    html = urllib2.urlopen(req).read()
    dom = PyQuery(html)

    browser = webdriver.PhantomJS()
    browser.get(url)
    streamurl = browser.find_element_by_css_selector('span#streamurl')
    print(streamurl.text)
    print(unicode(streamurl.get_attribute('outerHTML'), 'utf-8'))
    browser.close()

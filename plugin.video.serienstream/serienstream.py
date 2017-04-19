#
#   This file implements an API to SerienStream.to
#

from pyquery import PyQuery
from selenium import webdriver
from xvfbwrapper import Xvfb
import json
import re
import sys
import urllib
import urllib2


class SerienStream:
    base_url = 'https://serienstream.to'
    embed_url = 'https://openload.co/embed'
    stream_url = 'https://openload.co/stream'
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'

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

    @staticmethod
    def redirect_to_hoster(url):
        print('redirecting')
        headers = { 'User-Agent' : SerienStream.user_agent }
        req = urllib2.Request(url, None, headers)
        redirect_url = urllib2.urlopen(req).geturl()
        print(redirect_url)

if __name__ == '__main__':
    search_string = sys.argv[1]
    print(u'>>> Searching SerienStream.to for "' + search_string + '"')
    series = SerienStream.search(search_string)
    for s in series:
        print(u'{} - {}'.format(s['title'], s['link']))
    print


    #
    #   Get seasons
    #
    my_series = series[0]
    series_title = re.sub('<[/a-zA-Z]*>', '', my_series['title'])
    series_link = my_series['link']
    print(u'>>> Getting seasons for series "{}" ({})'.format(series_title, series_link))
    seasons = SerienStream.get_seasons(series_link)
    for title, url in seasons:
        print(u'{} - {}'.format(title, url))
    print

    #
    #   Get episodes
    #
    my_season = seasons[0]
    season_title, season_link = my_season
    print(u'>>> Getting episodes for season "{}" of series "{}" ({})'.format(season_title, series_title, season_link))
    episodes = SerienStream.get_episodes(season_link)
    for title, url in episodes:
        print(u'{} - {}'.format(title, url))
    print

    #
    # Get hoster
    #
    episode_title, episode_link = episodes[0]
    print(u'>>> Getting hosters for episode "{}" of season "{}" of series "{}" ({})'.format(episode_title, season_title, series_title, episode_link))
    hosters = SerienStream.get_hosters_for_episode(episode_link)
    for title, url in hosters:
        print(u'{} - {}'.format(title, url))
    print

    #
    #   Redirect to hoster
    #
    hoster_title, hoster_link = hosters[0]
    print(u'>>> Redirecting URL "{}" to hoster "{}"'.format(hoster_link, hoster_title))
    headers = { 'User-Agent' : SerienStream.user_agent }
    req = urllib2.Request(hoster_link, None, headers)
    con = urllib2.urlopen(req)
    redirected_link = con.geturl()
    print(redirected_link)
    print

    #
    # Get embedded URL
    #
    assert 'openload' in redirected_link
    print(u'>>> Get embedded URL from "{}" ({})'.format(hoster_title, redirected_link))
    video_code = redirected_link[22:]
    embedded_link = SerienStream.embed_url + '/' + video_code
    print(embedded_link)
    print

    #
    #   Get video URL
    #
    print(u'>>> Getting video URL from "{}" ({})'.format(hoster_title, embedded_link))
    display = Xvfb()
    display.start()
    browser = webdriver.Chrome()
    browser.get(embedded_link)
    # browser.execute_script('dispatchEvent(new Event("load"));');
    stream_code = browser.find_element_by_css_selector('span#streamurl').get_attribute('innerHTML')
    browser.close()
    browser.quit()
    display.stop()

    stream = SerienStream.stream_url + '/' + stream_code
    print(stream)

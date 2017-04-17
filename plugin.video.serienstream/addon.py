#
#   Serienstream.to plugin for KODI.
#

import re
import sys
import urllib
import urlparse
import xbmcgui
import xbmcplugin

from serienstream import SerienStream


def strip_html(string):
    return re.sub('<[/a-zA-Z]*>', '', string)

class Menu:
    def __init__(self, argv):
        self.base_url = argv[0]
        self.handle = int(argv[1])
        self.query_string = argv[2][1:]
        self.query = dict(urlparse.parse_qsl(self.query_string))

    def log(self, msg, level=xbmc.LOGNOTICE):
        xbmc.log(level=level, msg='{}, {}, {}: {}'.format(self.base_url, self.handle, self.query_string, msg))

    def build_url(self, query=None):
        if query:
            return self.base_url + '?' + urllib.urlencode(query)
        else:
            return self.base_url

    def addListItem(self, text, query, icon='Defaultfolder.png'):
        li = xbmcgui.ListItem(text, iconImage=icon)
        xbmcplugin.addDirectoryItem(handle=self.handle, url=self.build_url(query), listitem=li, isFolder=True)


    #
    #   A function for every menu level
    #
    def showMainMenu(self):
        self.addListItem('Search', {'action': 'search'}, 'DefaultAddonsSearch.png')
        xbmcplugin.endOfDirectory(self.handle)

    def showSearchMenu(self, search_string):
        data = SerienStream.search(search_string)

        if data:
            for entry in data:
                self.addListItem(strip_html(entry['title']), None)
            xbmcplugin.endOfDirectory(self.handle)

        else:
            dialog = xbmcgui.Dialog()
            dialog.ok('Search failed', 'Nothing found for', '"' + search_string + '"')
            self.showMainMenu()

    # Displays the menu items
    def show(self):
        action = self.query.get('action', None)

        if action is None:
            self.showMainMenu()

        elif action == 'search':
            self.log('Requesting user input for search')
            kb = xbmc.Keyboard(heading='Search for series')
            kb.doModal()

            if kb.isConfirmed():
                self.showSearchMenu(kb.getText())
            else:
                self.log('User input aborted')
                self.showMainMenu()

        else:
            self.log('Invalid action')
            raise "Invalid action"

if __name__ == '__main__':
    menu = Menu(sys.argv)
    xbmcplugin.setContent(menu.handle, 'movies')
    menu.show()

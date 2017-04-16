#
#   Serienstream.to plugin for KODI.
#

import sys
import urllib
import urlparse
import xbmcgui
import xbmcplugin

base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])


def build_url(query):
    return base_url + '?' + urllib.urlencode(query)

xbmcplugin.setContent(addon_handle, 'movies')
mode = args.get('mode', None)


if mode is None:
    url = build_url({'mode': 'search'})
    li = xbmcplugin.ListItem('Search', IconImage='DefaultVideo.png')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0] == 'search':
    kb = xbmc.Keyboard(heading='Search for series')
    kb.doModal()

    li_up = xbmcplugin.ListItem('..')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=build_url(), listitem=li_up)

    if kb.isConfirmed():
        li_ok = xbmcplugin.ListItem('OK')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=build_url(), listitem=li_ok)

    xbmcplugin.endOfDirectory(addon_handle)

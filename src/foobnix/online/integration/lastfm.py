'''
Created on 24 Apr 2010

@author: Matik
'''

from foobnix.model.entity import CommonBean
from foobnix.thirdparty import pylast
from foobnix.thirdparty.pylast import WSError
from foobnix.util import LOG
from foobnix.util.configuration import FConfiguration


__all__ = [
    'connected',
    'search_top_tracks',
    'search_top_albums',
    'search_tags_genre',
    'search_top_similar',
    'unimplemented_search',
    ]


network = None
try:
    LOG.error('trying to connect to last.fm')
    API_KEY = FConfiguration().API_KEY
    API_SECRET = FConfiguration().API_SECRET
    
    username = FConfiguration().lfm_login
    password_hash = pylast.md5(FConfiguration().lfm_password)
    network = pylast.get_lastfm_network(api_key=API_KEY, api_secret=API_SECRET, username=username, password_hash=password_hash)
except:
    LOG.error("last.fm connection error")


def connected():
    return network is not None

def search_top_albums(query):
    #unicode(query, "utf-8")
    artist = network.get_artist(query)
    if not artist:
        return None
    try:
        albums = artist.get_top_albums()
    except WSError:
        print "No artist with that name"
        return None
    
    beans = []    
    print "Albums: ", albums  
    
    for i, album in enumerate(albums):
        if i > 6:
            break;
        try:            
            album_txt = album.item
        except AttributeError:
            album_txt = album['item']
        
        tracks = album_txt.get_tracks()
        bean = CommonBean(name=album_txt.get_title(), path="", color="GREEN", type=CommonBean.TYPE_FOLDER, parent=query);
        beans.append(bean)
        
        for track in tracks:
            bean = CommonBean(name=track, path="", type=CommonBean.TYPE_MUSIC_URL, parent=album_txt.get_title());
            beans.append(bean)
            
    return beans


def search_tags_genre(query):
    beans = [] 
    
    tag = network.get_tag(query)
    bean = CommonBean(name=tag.get_name(), path="", color="GREEN", type=CommonBean.TYPE_GOOGLE_HELP, parent=None)
    beans.append(bean)
    try:
        tracks = tag.get_top_tracks()
    except:
        return None
    
    for j, track in enumerate(tracks):
        if j > 20:
            break
        try:            
            track_item = track.item
        except AttributeError:
            track_item = track['item']
        bean = CommonBean(name=track_item.get_artist().get_name() + " - " + track_item.get_title(), path="", type=CommonBean.TYPE_MUSIC_URL, parent=tag.get_name())
        beans.append(bean)
    
       
    tags = network.search_for_tag(query)
    print "tags"
    print tags
    
    
    flag = True
    
    for i, tag in enumerate(tags.get_next_page()):        
        if i == 0:
            print "we find it top", tag, query
            continue
        
            
        
        if i < 4:
            bean = CommonBean(name=tag.get_name(), path="", color="GREEN", type=CommonBean.TYPE_GOOGLE_HELP, parent=None)
            beans.append(bean)
            
            tracks = tag.get_top_tracks()
            for j, track in enumerate(tracks):
                if j > 10:
                    break
                try:            
                    track_item = track.item
                except AttributeError:
                    track_item = track['item']
                bean = CommonBean(name=track_item.get_artist().get_name() + " - " + track_item.get_title(), path="", type=CommonBean.TYPE_MUSIC_URL, parent=tag.get_name())
                beans.append(bean)
        else:
            if flag:
                bean = CommonBean(name="OTHER TAGS", path="", color="#FF99FF", type=CommonBean.TYPE_FOLDER, parent=None)
                beans.append(bean)
                flag = False
            bean = CommonBean(name=tag.get_name(), path="", color="GREEN", type=CommonBean.TYPE_GOOGLE_HELP, parent=None)
            beans.append(bean)
            
    return beans



def search_top_tracks(query):
    #unicode(query, "utf-8")
    artist = network.get_artist(query)
    if not artist:
        return None
    try:
        tracks = artist.get_top_tracks()
    except WSError:
        print "No artist with that name"
        return None
    
    beans = []    
    print "Tracks: ", tracks 
        
    for track in tracks:
        
        try:            
            track_item = track.item
        except AttributeError:
            track_item = track['item']
        
        #print track.get_duration()
        
        bean = CommonBean(name=str(track_item), path="", type=CommonBean.TYPE_MUSIC_URL, parent=query);
        beans.append(bean)
        
    return beans

def search_top_similar(query):
    #unicode(query, "utf-8")
    
    artist = network.get_artist(query)
    if not artist:
        return None
    
    artists = artist.get_similar(10)
    beans = []   
    for artist in artists:
        try:            
            artist_txt = artist.item
        except AttributeError:
            artist_txt = artist['item']
            
        print artist, artist_txt
        title = str(artist_txt)
        bean = CommonBean(name=title, path="", type=CommonBean.TYPE_FOLDER, color="GREEN", parent=query);
        beans.append(bean)
        tops = search_top_tracks(title)
        for top in tops:
            beans.append(top)
        
        
            
    return beans


def unimplemented_search(query):
    return None
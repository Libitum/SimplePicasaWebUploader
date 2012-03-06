#!/usr/bin/env python
# ^-^ coding: utf-8 ^-^
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

'''
This is a command line interface for easy use of Simple PicasaWeb Uploader without GUI.
'''
__author__ = "Libitum@about.me"
__version__ = "$Revision: 0.1$"[11:-1]

import os
import getpass
try:
    import spwu
except ImportError, e:
    print "ERROR: Miss some Module, please install it first..."
    print e
    exit(1)

def login():
    email = raw_input("Google Account:")
    passwd = getpass.getpass("Password:")
    return (email, passwd)

def get_path():
    photo_list = []
    print 'Please input your photo path or dir path...'
    path = raw_input("Path:")
    if os.path.isfile(path):
        photo_list.append(path)
        return photo_list
    elif os.path.isdir(path):
        paths = os.listdir(path)
        for p in paths:
            if os.path.isfile(os.path.join(path, p)):
                photo_list.append(os.path.join(path, p))

        return photo_list
    else:
        print 'Your input is not a photo path or dir path. Please reinput it...'
        return get_path()

def get_album_id(albums):
    print 'Please select a albums for the Photos.'
    print 'Id\tAlbum Name'
    for i in range(len(albums)):
        print "%d\t%s" % (i+1, albums[i].title.text)

    id = int(raw_input('Please input the id you want to choose. 0 for new album:'))
    if id <= len(albums):
        if id <= 0:
            return raw_input("Please input the new ablum's name:")
        else:
            return albums[id-1]
    else:
        print "Your input is Error. Please reinput it"
        return get_album_id(albums)

def run():
    print "Welcome use PicasaWeb Uploader. version:%s" % __version__
    client = spwu.SPWU()
    try:
        email, passwd = login()
        client.login(email, passwd)
        file_list = get_path()
        albums = client.get_albums_list()
        album = get_album_id(albums)
        if isinstance(album, (str, unicode)):
            print 'Insert a new album named %s' % album
            album = client.add_album(album)

        for i in range(len(file_list)):
            print 'Uploading pic %s. No. %d of %d' % (file_list[i], i, len(file_list))
            client.upload_photo(file_list[i], album)

        print 'Upload Complete.'
    except Exception, e:
        print e
    finally:
        client.clean()

if __name__ == "__main__":
    run()

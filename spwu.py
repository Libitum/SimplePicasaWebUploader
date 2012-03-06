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
This is a essential class for Simple PicasaWeb Uploader
Depends on:
    gdata-python-client: http://code.google.com/p/gdata-python-client/downloads/list
    Python Image Library: http://www.pythonware.com/products/pil/
    pyexiv2: http://tilloy.net/dev/pyexiv2
'''

__author__ = "Libitum@about.me"
__version__ = "$Revision: 0.1$"[11:-1]

import os, tempfile
import gdata.photos.service
import gdata.media
import gdata.geo
import Image
import pyexiv2

MAX_SIZE = 2048

class SPWU:
    def __init__(self):
        '''Constructor Function. Make temp dir for resize photos'''
        self.client = gdata.photos.service.PhotosService()
        self.client.source = 'PicasaWeb Uploader'
        self.tmpdir = tempfile.mkdtemp() + os.sep

    def login(self, email, passwd):
        '''Login google account. Should be used before other opts'''
        self.client.email = email
        self.client.password = passwd
        self.client.ProgrammaticLogin()

    def get_albums_list(self):
        '''Get the albums list
        Return: The albums list.
        '''
        albums = self.client.GetUserFeed()
        return albums.entry

    def add_album(self, title, summary=''):
        '''Insert a new album
        Args:
            title: str. The title of the album.
            summary: str. The description of the album.
        Return: The new album object.
        '''
        return self.client.InsertAlbum(title, summary)

    def upload_photo(self, file_path, album=None, resize=True):
        '''Upload a photo to the album
        Args:
            file_path: str. The file's path to be uploaded
            album: album.entry (optional). The album which the photo should be uploaded in
            resize: Boolean (optional). True for resizing thr photo to 2048px.
        '''
        if resize == True:
            file_path = self.__resize(file_path)

        album_id = 'default' if album is None else album.gphoto_id.text
        album_url = '/data/feed/api/user/default/albumid/%s' % album_id
        photo_name = os.path.splitext(os.path.basename(file_path))[0]
        photo = self.client.InsertPhotoSimple(album_url, photo_name, '', file_path)

    def clean(self):
        '''clean the temp dir used for resizing photos'''
        files = os.listdir(self.tmpdir)
        for f in files:
            path = os.path.join(self.tmpdir, f)
            os.remove(path)
        os.rmdir(self.tmpdir)

    def __resize(self, file_path):
        '''Resize the photo to be uploaded.
        Return: The resized temp photo path.
        '''
        file_name = os.path.basename(file_path)
        tmp_file = self.tmpdir + file_name
        img = Image.open(file_path)
        w, h = img.size
        m = w if w > h else h
        r_w = w * MAX_SIZE / m
        r_h = h * MAX_SIZE / m
        img.resize((r_w, r_h), Image.ANTIALIAS).save(tmp_file)

        #copy the exif info
        source_exif = pyexiv2.ImageMetadata(file_path)
        source_exif.read()
        dest_exif = pyexiv2.ImageMetadata(tmp_file)
        dest_exif.read()
        source_exif.copy(dest_exif)
        dest_exif['Exif.Photo.PixelXDimension'] = r_w
        dest_exif['Exif.Photo.PixelYDimension'] = r_h
        dest_exif.write()

        return tmp_file


def test():
    print "Please use spwu_cl.py for command line or spwu_gui.py for GUI"

if __name__ == "__main__":
    test()

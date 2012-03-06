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

__author__ = "Libitum@about.me"
__version__ = "$Revision: 0.1$"[11:-1]

from Tkinter import Tk, Frame, Label, Entry

__version__ = '0.1'

class GUI:
    def __init__(self, root):
        frame1 = Frame(root)
        frame1.pack(ipadx=20, pady=20)
        self.labUser = Label(frame1, text="Google Account:")
        self.labUser.pack(side="left", padx=10)
        self.enyUser = Entry(frame1)
        self.enyUser.pack(side="left")
        self.labPwd = Label(frame1, text="Password:")
        self.labPwd.pack(side="left", padx=10)
        self.enyPwd = Entry(frame1)
        self.enyPwd['show'] = '*'
        self.enyPwd.pack(side="left")

def main():
    root = Tk()
    root.title("PicasaWeb Uploader v%s" % __version__)
    root.resizable(False, False)
    root.geometry('400x500+300+100')

    app = GUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

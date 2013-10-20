#!/usr/bin/env python2
# -*- coding: utf8 -*-
import gtk, gtk.glade
import urllib2
import urllib
from IPython import embed

class PastieClient:
    PASTES = { 'Ruby (on Rails)':'ruby_on_rails', 'Ruby':'ruby', 'Python':'python',
        'Plain Text':'plain_text', 'ActionScript':'actionscript', 'C/C++':'c++',
        'CSS':'css', 'Diff':'diff', 'HTML (Rails)':'html_rails', 'HTML / XML':'html',
        'Java':'java', 'JavaScript':'javascript', 'Objective C/C++':'objective-c++',
        'PHP':'php', 'SQL':'sql', 'Shell Script':'shell-unix-generic'
    }

    LANGS = ('Ruby (on Rails)', 'Ruby', 'Python', 'Plain Text', 'ActionScript', 'C/C++', 'CSS', 'Diff', 'HTML (Rails)', 'HTML / XML', 'Java', 'JavaScript', 'Objective C/C++', 'PHP', 'SQL', 'Shell Script')
         
    URL = 'http://pastie.org/pastes'

    def __init__(self, text='', syntax='Plain Text', private=False):
        self.text = text
        self.syntax = syntax
        self.private = private

    def __send_request(self, params):
        data = urllib.urlencode(params)
        request = urllib2.Request(URL, data)
        request.add_header('User-Agent', 'PastiePythonClass/1.0 +http://hiler.pl/')

        try:
            firstdatastream = opener.open(request)
        except:
            return 'Coś poszło nie tak, przepraszamy.'
        else:
            return firstdatastream.url

    def paste(self):
        if not PASTES.has_key(self.syntax):
            return 'Zły język.'
        
        opener = urllib2.build_opener()
        params = {
                  'paste[body]':self.text,
                  'paste[parser]': self.__class__.PASTES[self.syntax],
                  'paste[authorization]':'burger' #pastie protecion against general spam bots
                  }

        if self.private:
            params['paste[restricted]'] = '1'
        else:
            params['paste[restricted]'] = '0'

        return self.__send_request(params)
            
            

class PastieTray():
    def __init__(self, image=None):
        self.tray = gtk.StatusIcon()
        self.tray.set_from_file('pastie.gif')
        
    def show(self):
        self.tray.set_visible(True)
        
    def hide(self):
        self.tray.set_visible(False)
    
    def connect(self, event):
        self.tray.connect("activate", event)


class PastieWindow:
    ATTRS = [ "pastie_window", "hide_widget_item", "close_widget_item", "about_item",
            "textview", "language_select_box", "private_check" "spinner", "paste_button" ]

    def __init__(self):
        self.hidden = True
        self.builder = gtk.Builder()
        self.builder.add_from_file("pastie.glade")
        self.__build_attributes()
        self.__hook_events()

    def __build_attributes(self):
        for attr in self.__class__.ATTRS:
            obj = self.builder.get_object(attr)
            setattr(self, attr, obj)

    def __hook_events(self):
        self.pastie_window.connect("delete_event", self.hide)
        self.hide_widget_item.connect("activate", self.hide)
        self.close_widget_item.connect("activate", gtk.main_quit)

    def hide(self, widget=None, event=None):
        self.hidden = True
        self.pastie_window.hide()
        self.textview.get_buffer().set_text('')
        self.private_check.set_active(False)
        return True #for delete_event, it will save window from destroying

    def show(self, widget=None, event=None):
        self.hidden = False
        self.pastie_window.set_size_request(315, 150)
        self.pastie_window.show()
        self.textview.grab_focus()

    def toggle(self, widget=None, event=None):
        if self.hidden:
            self.show()
        else:
            self.hide()

    @property
    def text(self):
        buff = self.textview.get_buffer()
        start, end = buff.get_bounds()
        return buff.get_text(start, end)

    @property
    def is_priavate(self):
        return self.private_check.get_active()

    @property
    def language(self):
        active = self.language_select_box.get_active()
        return self.language_select_box.get_model()[active][0]


class Pastie:
    def __init__(self):
        self.window = PastieWindow()
        self.tray = PastieTray()
        self.tray.show()
        self.__hook_events()

    def paste(self, ev):
        text = self.window.text
        language = self.window.language
        priavate = self.window.is_priavate

        clipboard = gtk.clipboard_get('CLIPBOARD')
        
        p = pastie.Pastie(text, language, priv)
        url = p.paste()

        clipboard.set_text(url)
        clipboard.store()

        self.window.hide()
    
    def _setup_langs(self):
        for lang in pastie.LANGS:
            self.syntaxlist.append_text(lang)

        self.syntaxlist.set_active(3) #sets active posision in syntax list

    def __hook_events(self):
        self.tray.connect(self.window.toggle)
        self.window.paste_button.connect("clicked", self.paste)
    

pastie = Pastie()

gtk.main()

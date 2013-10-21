#!/usr/bin/env python2
# -*- coding: utf8 -*-

import gtk, gtk.glade, gobject
import inspect, os
import threading
import urllib2
import urllib

def resource_path(resource_name):
    relative_path =  inspect.getfile(inspect.currentframe())
    real_path = os.path.realpath(relative_path)
    real_dir = os.path.dirname(real_path)
    return os.path.join(real_dir, resource_name)

class PastieClient:
    PASTES = { 'Ruby (on Rails)':'ruby_on_rails', 'Ruby':'ruby', 'Python':'python',
        'Plain Text':'plain_text', 'ActionScript':'actionscript', 'C/C++':'c++',
        'CSS':'css', 'Diff':'diff', 'HTML (Rails)':'html_rails', 'HTML / XML':'html',
        'Java':'java', 'JavaScript':'javascript', 'Objective C/C++':'objective-c++',
        'PHP':'php', 'SQL':'sql', 'Shell Script':'shell-unix-generic'
    }

    LANGS = ('Plain Text', 'Ruby (on Rails)', 'Ruby', 'Python', 'ActionScript',
        'C/C++', 'CSS', 'Diff', 'HTML (Rails)', 'HTML / XML', 'Java',
        'JavaScript', 'Objective C/C++', 'PHP', 'SQL', 'Shell Script')
         
    URL = 'http://pastie.org/pastes'

    def __init__(self, text='', syntax='Plain Text', private=False):
        self.text = text
        self.syntax = syntax
        self.private = private

    def __send_request(self, opener, params):
        data = urllib.urlencode(params)
        request = urllib2.Request(self.__class__.URL, data)
        request.add_header('User-Agent', 'PastiePythonClass/1.0 +http://hiler.pl/')

        try:
            firstdatastream = opener.open(request)
        except:
            return 'Something went wrong, sorry.'
        else:
            return firstdatastream.url

    def paste(self):
        if not self.__class__.PASTES.has_key(self.syntax):
            return 'Worng language.'
        
        opener = urllib2.build_opener()
        params = {
                  'paste[body]':self.text,
                  'paste[parser]': self.__class__.PASTES[self.syntax],
                  'paste[authorization]':'burger'
                  }

        if self.private:
            params['paste[restricted]'] = '1'
        else:
            params['paste[restricted]'] = '0'

        return self.__send_request(opener, params)
            
            

class PastieTray():
    def __init__(self, image=None):

        self.tray = gtk.StatusIcon()
        self.tray.set_from_file(resource_path('pastie.gif'))
        
    def show(self):
        self.tray.set_visible(True)
        
    def hide(self):
        self.tray.set_visible(False)
    
    def connect(self, event):
        self.tray.connect("activate", event)


class PastieWindow:
    ATTRS = [ "pastie_window",  "textview", "language_select_box",
            "private_check", "spinner", "paste_button" ]

    def __init__(self):
        self.hidden = True
        self.builder = gtk.Builder()
        self.builder.add_from_file(resource_path("pastie.glade"))
        self.__build_attributes()
        self.__hook_events()

    def __build_attributes(self):
        for attr in self.__class__.ATTRS:
            obj = self.builder.get_object(attr)
            setattr(self, attr, obj)

        combobox = self.language_select_box
        liststore = gtk.ListStore(gobject.TYPE_STRING)
        combobox.set_model(liststore)
        cell = gtk.CellRendererText()
        combobox.pack_start(cell, True)
        combobox.add_attribute(cell, 'text', 0)

    def __hook_events(self):
        self.pastie_window.connect("delete_event", self.hide)

    def hide(self, widget=None, event=None):
        self.hidden = True
        self.pastie_window.hide()
        self.textview.get_buffer().set_text('')
        self.private_check.set_active(False)

        self.spinner.stop()
        self.spinner.set_visible(False)

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

    def add_language(self, lang):
        self.language_select_box.append_text(lang)

    def spin(self):
        self.spinner.set_visible(True)
        self.spinner.start()

    def disable(self):
        self.textview.set_sensitive(False)
        self.paste_button.set_sensitive(False)
        self.private_check.set_sensitive(False)
        self.language_select_box.set_sensitive(False)
        self.menu_bar.set_sensitive(False)

    def enable(self):
        self.textview.set_sensitive(True)
        self.paste_button.set_sensitive(True)
        self.private_check.set_sensitive(True)
        self.language_select_box.set_sensitive(True)
        self.menu_bar.set_sensitive(False)

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
        self.__setup_langs()
    
    def __async_paste(self, language, text, private):
        p = PastieClient(text, language, private)
        url = p.paste()

        clipboard = gtk.clipboard_get('CLIPBOARD')
        clipboard.set_text(url)
        clipboard.store()

        gobject.idle_add(self.__async_finish)

    def __async_finish(self):
        self.window.hide()
        self.enable()
        return False


    def __setup_langs(self):
        for lang in PastieClient.LANGS:
            self.window.add_language(lang)

        self.window.language_select_box.set_active(0)

    def __hook_events(self):
        self.tray.connect(self.window.toggle)
        self.window.paste_button.connect("clicked", self.paste)

    def paste(self, ev):
        self.window.spin()
        self.window.disable()
        language = self.window.language
        text = self.window.text
        private = self.window.is_priavate

        threading.Thread(target=self.__async_paste, args=(language, text, private)).start()


if __name__ == "__main__":
    pastie = Pastie()
    gtk.gdk.threads_init()
    gtk.main()

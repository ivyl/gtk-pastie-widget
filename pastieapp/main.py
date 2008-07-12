import gtk, gtk.glade
import pastietray
import pastie


def send_clicked(ev):
    start, end = buff.get_bounds()
    text = buff.get_text(start, end)
    priv = privcheck.get_active()
    
    active = syntaxlist.get_active()
    syntax = syntaxlist.get_model()[active][0]
    
    clipboard = gtk.clipboard_get('CLIPBOARD')
    
    p = pastie.Pastie(text, syntax, priv)
    clipboard.set_text(p.paste())
    
    clipboard.store()
    hide()

    
def hide(widget=None, event=None):
    global hidden 
    hidden = True
    window.hide()
    buff.set_text('')
    privcheck.set_active(False)
    return True #for delete_event, it will save window from destroying
    
    
def show(widget=None, event=None):
    global hidden 
    hidden = False
    window.set_size_request(315, 150)
    window.show()
    textview.grab_focus()
    
def on_pastie_icon(widget=None, event=None):
    if hidden:
        show()
    else:
        hide()
    

tray = pastietray.PastieTray()
tray.create_tray()
tray.show_tray()

hidden = True

glade = gtk.glade.XML("window.glade")
window = glade.get_widget("window")
textview = glade.get_widget("text")
buff = glade.get_widget("text").get_buffer()
privcheck = glade.get_widget("private")
syntaxlist = glade.get_widget("syntax")

window.set_decorated(False)
window.set_icon_from_file('pastie.gif')
window.connect("delete_event", hide)

for lang in pastie.LANGS:
    syntaxlist.append_text(lang)
        
syntaxlist.set_active(3) #sets active posision in syntax list
    
glade.get_widget("send_button").connect("clicked", send_clicked)
glade.get_widget("close_button").connect("clicked", hide)
glade.get_widget("exit_button").connect("clicked", gtk.main_quit)

tray.connect(on_pastie_icon)
gtk.main()

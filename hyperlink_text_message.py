import re
import webbrowser
from tkinter import *

class HyperlinkMessageBox(Toplevel):
    hyperlinkPattern = re.compile(r'<a href="(?P<address>.*?)">(?P<title>.*?)'
                                  '</a>')
    def __init__(self, master, title=None, message=None, **options):
        Toplevel.__init__(self, master)
        self.geometry("200x200")
        self.title(title or master.title())
        self.text = Text(self, wrap=WORD, bg=master.cget('bg'),
                         height=self.cget('height'))
        self._formatHyperLink(message)
        self.text.config(state=DISABLED)
        self.text.pack(side=TOP, fill=X)
        self.makeButtons()

    def makeButtons(self):
        Button(self, text="Ok",
               command=lambda *a, **k: self.destroy()).pack()

    def _formatHyperLink(self, message):
        text = self.text
        start = 0
        for index, match in enumerate(self.hyperlinkPattern.finditer(message)):
            groups = match.groupdict()
            text.insert("end", message[start: match.start()])
            #insert hyperlink tag here
            text.insert("end", groups['title'])
            text.tag_add(str(index),
                         "end-%dc" % (len(groups['title']) + 1),
                         "end",)
            text.tag_config(str(index),
                            foreground="blue",
                            underline=1)
            text.tag_bind(str(index),
                          "<Enter>",
                          lambda *a, **k: text.config(cursor="hand"))
            text.tag_bind(str(index),
                          "<Leave>",
                          lambda *a, **k: text.config(cursor="arrow"))
            text.tag_bind(str(index),
                          "<Button-1>",
                          self._callbackFactory(groups['address']))
            start = match.end()
        else:
            text.insert("end", message[start:])

    def _callbackFactory(self, url):
        return lambda *args, **kwargs: webbrowser.open(url)


if __name__ == "__main__":
    import re
    def dirsel(obj, search):
        for item in dir(obj):
            if re.search(search, item):
                print(item)

    root = Tk()
    h = HyperlinkMessageBox(root, "My App", 'Some message <a href="http://www.google.com">Google</a>.')
    root.mainloop()

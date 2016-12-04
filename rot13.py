import os

import webapp2
import jinja2
import string

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)

def rot13(alphabet, letter):
    num = alphabet.find(letter)
    num = num+13
    if num >= 26:
        num = num-26
    newltr = alphabet[num]
    return newltr

specialchars = ["<",">"]

def converttext(text):
    newtext = ""
    for i in text:
        if i.isspace() or i.isdigit():
            newltr = i
        elif i in list(string.punctuation):
            newltr = i
        elif i.isupper():
            newltr = rot13(string.ascii_uppercase, i)
        else:
            newltr = rot13(string.ascii_lowercase, i)
        newtext += newltr
    return newtext


class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))


class MainPage(Handler):
    def get(self):
        self.render("encrypt.html", text="")

    def post(self):
        user_text = self.request.get("text")

        text_converted = converttext(user_text)

        self.render("encrypt.html", text=text_converted)

app = webapp2.WSGIApplication([
    ('/', MainPage)
], debug=True)

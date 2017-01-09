#!/usr/local/bin/python2.7

import os
import jinja2
import webapp2
import cgi
import re

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader= jinja2.FileSystemLoader(template_dir), autoescape = True)

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASSWD_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")


errname = "Invalid username"
errpass = "Invalid password"
errverify = "Password does not match"
erremail = "Invalid email"

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)
    
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class SignupHandler(Handler):

    def render_front(self, username="", errname="", errpass = "", errverify="", email="", erremail=""):
        self.render("signup.html", username = username, errname = errname, errpass = errpass, errverify=errverify, email = email, erremail = erremail)
        
    def get(self):
        #visits = self.request.cookies.get('username')
        self.render_front()
    
    def post(self):
        user_username = self.request.get('username')
        user_password = self.request.get('password')
        cookie_username = self.request.cookies.get('username')
        cookie_password = self.request.cookies.get('password')
        
        errname = ""
        errpass = ""
        errverify = ""
        erremail = ""
        
        if not valid_username(user_username):
            errname = "Invalid username"
        if not valid_password(user_password):
            errpass = "Invalid password"
        if not valid_verify(user_password, user_verify):
            errverify = "Password does not match"
        if valid_username(user_username) and valid_password(user_password):
            #self.response.out.write(user_username)
            self.response.headers.add_header('Set-Cookie', 'username=%s; Path=/' % str(user_username))
            self.redirect("/hw4_1/welcome")
        else:
            self.render_front(user_username, errname, errpass, errverify, user_email, erremail)

class WelcomeHandler(Handler):
    def render_front(self, username=""):
        self.render("welcome.html", username=username)
    def get(self):
        #self.response.headers['Content-Type'] = 'text/plain'
        #self.response.out.write(self.request)
        username = self.request.cookies.get('username')
        #username = self.request.get("username")
        #username = "test"
        self.render_front(username)
    

def valid_password(s):
    return PASSWD_RE.match(s)
def valid_username(s):
    return USER_RE.match(s)
def valid_verify(s1, s2):
    if s1 == s2:
        return True
    else:
        return False
def valid_email(s):
    if s:
        return EMAIL_RE.match(s)
    else:
        return True

def sanitize(s):
    return cgi.escape(s, quote = True)
 
#  USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
#  def valid_username(username):
#    return USER_RE.match(username)
        
#class RotHandler(webapp2.RequestHandler):
    #def rot13(self, s)
        #self.response.headers['Content-Type'] = 'text/plain'
        #self.response.out.write(self.request)

app = webapp2.WSGIApplication([('/hw4_1/login', SignupHandler), (r'/hw4_1/welcome', WelcomeHandler)],
                              debug=True)

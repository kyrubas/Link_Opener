import webbrowser, requests
from tkinter import *
import urllib.request
class Log_in:
    def __init__(self, loginURL, username, password):
        self.loginURL = loginURL
        self.username = username
        self.password = password
    def log_in_to_site(self):
        auth_handler = urllib.request.HTTPBasicAuthHandler()
        auth_handler.add_password(realm = None,
                                  uri=self.loginURL,
                                  user=self.username,
                                  passwd=self.password)
        opener = urllib.request.build_opener(auth_handler)
        urllib.request.install_opener(opener)
       
class Scrape_data:
    def __init__(self, web_page):
        self.page = web_page
        self.page_response = None
        self.page_text = None
        self.page_links = []
        self.begin_link = 0
        self.end_link = 0
    def get_response(self):
        self.page_response = urllib.request.urlopen(self.page)
    def get_text(self):
        self.page_text = self.page_response.read().decode('utf-8')
    def get_page_links(self):
        while self.page_text.find('<a href="') != -1:
            self.begin_link = self.page_text.find('<a href="')+len('<a href="')
            self.end_link = self.page_text.find('"',self.begin_link)
            self.page_links.append(self.page_text[self.begin_link:self.end_link])
            self.page_text = self.page_text[self.begin_link+1:]
        return self.page_links
 
class Open_pages:
    def __init__(self, web_page_list, identifier = ""):
        self.page_list = web_page_list
        self.identifer = identifier
        self.tab_open_count = 0
    def open_browser(self):
        webbrowser.open("about:blank:",new=0, autoraise=True)
    def new_tab_pages(self):
        if self.identifer == "":
            for each in self.page_list:
                webbrowser.open(each,new=2,autoraise=True)
                self.page_list = self.page_list
                self.tab_open_count += 1
                if self.tab_open_count == 50:
                    self.page_list = self.page_list[self.page_list.index(each)+1:]
                    self.tab_open_count = 0
                    break
        else:
            for each in self.page_list:
                #print(each.find(self.identifer),each)
                if each.find(self.identifer) != -1:
                    webbrowser.open(each,new=2,autoraise=True) 
                    self.page_list = self.page_list
                    self.tab_open_count += 1
                if self.tab_open_count == 50:
                    self.page_list = self.page_list[self.page_list.index(each)+1:]
                    self.tab_open_count = 0
                    break
                
def run_program():
    if login_page.get() !="" and username_field.get() != "" and password_field.get() != "":
        Log_in(login_page.get(),username_field.get(),password_field.get())
    thepage = Scrape_data(webpage_entry.get())
    thepage.get_response()
    thepage.get_text()
    thepage.get_page_links()
    global page_opener
    page_opener = Open_pages(thepage.page_links, ident_entry.get())
    page_opener.open_browser()
    page_opener.new_tab_pages()
    #print(thepage.page_response)
    #print(thepage.page_links)


def open_next50():
    print(page_opener)
    page_opener.new_tab_pages()
    return page_opener
    
tk = Tk()
 
webpage_box_label = Label(tk, text = "Web Site: ")
webpage_box_label.pack()
 
webpage_entry = Entry(tk)
webpage_entry.pack()
 
ident_box_label = Label(tk, text = "Identifier (Optional): ")
ident_box_label.pack()
 
ident_entry = Entry(tk)
ident_entry.pack()
 
run_button = Button(tk, text = "Run", command = run_program)
run_button.pack()
 
login_page_label = Label(tk, text = "Log-in Page URL")
login_page_label.pack()
 
login_page = Entry(tk)
login_page.pack()
 
username_label = Label(tk, text = "Username")
username_label.pack()
 
username_field = Entry(tk)
username_field.pack()
 
password_label = Label(tk, text = "Password")
password_label.pack()
 
password_field = Entry(tk,show="*")
password_field.pack()

open_next_50_btn = Button(tk, text = "Open Next 50",command = open_next50)
open_next_50_btn.pack()
 
tk.mainloop()


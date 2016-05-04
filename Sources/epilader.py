# ******************************************************************************
#                                                                              *
#                                 EPILADER PY                                  *
#                                                                              *
#                Retrieve all GPA from the input list and sort them            *
#                                                                              *
#  Created by Thomas Chafiol  -  thomaschaf@gmail.com  -  03  /  07  /  2013   *
# ******************************************************************************
import pycurl
import io
import json
import sys

from option import Option
from notes import Notes
from log import *

class Epilader:
    INTRA_URL = "https://intra.epitech.eu/"
    JSON_CONF = "./Config/conf.json"

    def __init__(self, arg):
        self.curl = pycurl.Curl()
        self.option = Option()
        self.option.parse(arg)
        self.log = Log(self.option.isVerboseMode())
        self.datas = []
        config = json.loads(open(Epilader.JSON_CONF).read())
        self.login    = config["login"]
        self.password = config["password"]
        self.notes = Notes(config["projets"], config["modules"])

    def __del__(self):
        self.curl.close()

    def set_cookies(self):
        self.curl.setopt(self.curl.POST, 1)
        self.curl.setopt(self.curl.URL, Epilader.INTRA_URL)
        self.curl.setopt(self.curl.POSTFIELDS, 'login=' + self.login + '&password=' + self.password)
        self.curl.setopt(pycurl.FOLLOWLOCATION, 1)
        self.curl.setopt(self.curl.COOKIEFILE, '')

    def find_gpa(self, request_result):
        request_result = json.loads(request_result)
        try:
            gpa = float([x for x in request_result["gpa"] if (x["cycle"] == "bachelor")][0]['gpa'])
        except:
            self.log.error(Log.NO_GPA)
            return -1
        return gpa

    def find_moyenne(self, request_result):
        self.notes.init()
        request_result = json.loads(request_result)
        for note in request_result["notes"]:
            self.notes.add_note(note)
        return self.notes.moyenne()

    def request(self, href):
        self.curl.setopt(self.curl.URL, href)
        reponse = io.BytesIO()
        self.curl.setopt(self.curl.WRITEFUNCTION, reponse.write)
        try:
            self.curl.perform()
        except KeyboardInterrupt:
            raise KeyboardInterrupt
        except:
            self.log.error(Log.REQUEST_FAIL)
            print ; return ""
        return reponse.getvalue().decode("utf-8")

    def launch(self):
        try:
            while True:
                user = input()
                if user == "" or user == "EOF":
                    return
                href_gpa = Epilader.INTRA_URL + "user/" + user + "/?format=json"
                href_note = Epilader.INTRA_URL + "user/" + user + "/notes/?format=json"
                if user[0] != '#':
                    gpa = self.find_gpa(self.request(href_gpa))
                    moyenne = self.find_moyenne(self.request(href_note))
                    self.log.write(user + "\t: " + str(gpa) + "\t: " + str(moyenne))
                    if gpa > 0:
                      self.datas.append([user, gpa, moyenne])
        except (KeyboardInterrupt, EOFError):
            print("KeyboardInterrupt") ; return

    def sort(self):
        self.datas.sort(key=lambda x: x[1], reverse=True)

    def display(self):
        rank = 1
        for d in self.datas:
            self.option.write(str(rank) + " " + d[0] + "\t" + str(d[1]) + "\t" + str(d[2]) + "\n")
            rank += 1

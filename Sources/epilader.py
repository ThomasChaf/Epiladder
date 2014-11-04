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
        self.projets  = config["projets"]

    def __del__(self):
      self.curl.close()

    def set_cookies(self):
        self.curl.setopt(self.curl.POST, 1)
        self.curl.setopt(self.curl.URL, Epilader.INTRA_URL)
        self.curl.setopt(self.curl.POSTFIELDS, 'login=' + self.login + '&password=' + self.password)
        self.curl.setopt(pycurl.FOLLOWLOCATION, 1)
        self.curl.setopt(self.curl.COOKIEFILE, '')

    def find_gpa(self, request_result):
        i = request_result.find("G.P.A.")
        needle = "\"value\">"
        i = request_result.find(needle, i) + len(needle)
        try:
            gpa = float(request_result[i:i+4].replace(",", "."))
        except:
            self.log.error(Log.NO_GPA)
            return -1
        return gpa

    def json_objet(self, string, start_with, end_with):
        i = string.find(start_with) + len(start_with)
        j = string.find(end_with, i) + 1
        assert(i != j)
        return json.loads(string[i:j])

    def find_moyenne(self, request_result):
        try:
            modules = self.json_objet(request_result, "modules:", "],")
            notes   = self.json_objet(request_result, "notes:", "\n});")
        except:
            self.log.error(Log.NO_MOYENNE)
            return -1
        moyenne = 0.0
        coef = 0
        for m in modules:
            if m['title'] in self.projets:
                for projet in self.projets[m['title']]:
                    obj_note = list(filter(lambda x : x['title'] == projet, notes))
                    if len(obj_note) < 1:
                        note = 0
                    else:
                        note = obj_note[0]['final_note']
                    moyenne += (note * m['credits'])
                    coef += m['credits']
        return round(moyenne / coef, 2)

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
                href_gpa = Epilader.INTRA_URL + "user/" + user + "/"
                href_note = Epilader.INTRA_URL + "user/" + user + "/#!/notes/all"
                if user[0] != '#':
                    gpa = self.find_gpa(self.request(href_gpa))
                    moyenne = self.find_moyenne(self.request(href_note))
                    self.log.write(user + "\t: " + str(gpa) + "\t: " + str(moyenne))
                    if gpa > 0:
                      self.datas.append([user, gpa, moyenne])
        except KeyboardInterrupt:
            print("KeyboardInterrupt") ; return

    def sort(self):
        self.datas.sort(key=lambda x: x[1], reverse=True)

    def display(self):
        rank = 1
        for d in self.datas:
            self.option.write(str(rank) + " " + d[0] + "\t" + str(d[1]) + "\t" + str(d[2]) + "\n")
            rank += 1

#!/usr/bin/env python2
# -*-: coding utf-8 -*-

CONFIGURATION_ENCODING_FORMAT = "utf-8"

import ConfigParser
import io

class SnipsConfigParser(ConfigParser.SafeConfigParser):
    def to_dict(self):
        return {section : {option_name : option for option_name, option in self.items(section)} for section in self.sections()}


def read_configuration_file(configuration_file):
    try:
        with io.open(configuration_file, encoding=CONFIGURATION_ENCODING_FORMAT) as f:
            conf_parser = SnipsConfigParser()
            conf_parser.readfp(f)
            return conf_parser.to_dict()
    except (IOError, ConfigParser.Error) as e:
        print e
        return dict()


def render_configuration_file_template(username="", password="", client_id="", client_secret=""):
    return "[http]\nenabled = true\nhostname = 0.0.0.0\nport = 6680\n[local]\nenabled = false\n\n[spotify]\nusername = {}\npassword = {}\nclient_id = {}\nclient_secret = {}\n".format(username, password, client_id, client_secret)


if __name__ == "__main__":
    configuration_file = read_configuration_file("config.ini")

    print render_configuration_file_template(username=configuration_file['secret']['spotify_username'],
                                             password=configuration_file['secret']['spotify_password'],
                                             client_id=configuration_file['secret']['spotify_client_id'],
                                             client_secret=configuration_file['secret']['spotify_client_secret'])

    

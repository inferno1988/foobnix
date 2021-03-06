#-*- coding: utf-8 -*-
'''
Created on 1 сент. 2010

@author: ivan
'''
import urllib2
import logging
from foobnix.fc.fc import FC
class ProxyPasswordMgr:
    def __init__(self):
        self.user = self.passwd = None
    def add_password(self, realm, uri, user, passwd):
        self.user = user
        self.passwd = passwd
    def find_user_password(self, realm, authuri):
        return self.user, self.passwd

def set_proxy_settings():
    if FC().proxy_enable and FC().proxy_url:
        #http://spys.ru/proxylist/
        proxy = FC().proxy_url
        user = FC().proxy_user
        password = FC().proxy_password
        
        logging.info("Proxy enable:"+ proxy+ user+ password)
        
        proxy = urllib2.ProxyHandler({"http" : proxy})
        proxy_auth_handler = urllib2.ProxyBasicAuthHandler(ProxyPasswordMgr())
        proxy_auth_handler.add_password(None, None, user, password)
        opener = urllib2.build_opener(proxy, proxy_auth_handler)
        urllib2.install_opener(opener)
    else:
        logging.info("Proxy not enable")

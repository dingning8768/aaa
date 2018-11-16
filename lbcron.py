#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import sys
import urllib2
import json


class lbApi:
    def __init__(self):
        self.__url = 'http://10.254.1.9/nitro/v1/config'
        self.__username = 'nsapi'
        self.__password = 'Api@201710'
        self.__content = 'Content-Type:application/json'

    def post_request(self, prefix, obj=None):
        url = self.__url + prefix
        headers = {'X-NITRO-USER': self.__username, 'X-NITRO-PASS': self.__password, 'Content-Type': self.__content}
        req = urllib2.Request(url, obj, headers)
        try:
            response = urllib2.urlopen(req)
        except urllib2.HTTPError as e:
            # HTTPError and URLError all have reason attribute
            print ("The server conldn't fulfill the request")
            print ("Error code: ", e.code)
            print ('Error Reason: ', e.reason)
        except urllib2.URLError as e:
            # Only HTTPError has code attribute
            print ("We failed to reach a server")
            print ("Reason: ", e.reason)
        else:
            respon = response.read()
            try:
                if respon + "200" == "200":
                    print ("ok")
                else:
                    content = json.loads(respon)
                    return content
            except Exception as e:
                print (e)


def get_lb(service_group_name):
    prefix = '/servicegroup_servicegroupmember_binding/' + service_group_name
    lbapi = lbApi()
    content = lbapi.post_request(prefix)
    if content["errorcode"] == 0:
        content_list = content["servicegroup_servicegroupmember_binding"]
        for n in content_list:
            print ("""GroupName: %s ServerName: %s Port: %s State: %s""" % (
                n["servicegroupname"], n["servername"], n["port"], n["svrstate"]))
    else:
        print ("openrate failed")
        # print content


def set_enable_disable(is_able, *nums):
    prefix = '/servicegroup?action=' + is_able
    if is_able == "enable":
        if len(nums) == 1:
            obj_dict = {
                "servicegroup": {"servicegroupname": nums[0][0], "servername": nums[0][1], "port": nums[0][2]}}
        else:
            obj_list = [{"servicegroupname": n[0], "servername": n[1], "port": n[2]} for n in nums]
            obj_dict = {"servicegroup": obj_list}
    else:
        print (len(nums))
        print (nums)
        if len(nums) == 1:
            obj_dict = {
                "servicegroup": {"servicegroupname": nums[0][0], "servername": nums[0][1], "port": nums[0][2],
                                 "graceful": "YES"}}
        else:
            obj_list = [{"servicegroupname": n[0], "servername": n[1], "port": n[2], "graceful": "YES"} for n in nums]
            obj_dict = {"servicegroup": obj_list}
    data = json.dumps(obj_dict)
    print (data)
    lbapi = lbApi()
    # data = urllib.urlencode(obj_dict)
    content = lbapi.post_request(prefix, obj=data)
    if content["errorcode"] == 0:
        print ("operate ok")
    else:
        print ("operate failed")


def config_list(service_group_name, env_list):
    pass


def main(env_list, *num):
    pass


if __name__ == '__main__':
    try:
        # sys.argv[0] = service_group_name , sys.argv[1] = a_or_b , sys.argv[2] = env_list , sys.argv[3] = is_able
        print (len(sys.argv))
        if len(sys.argv) != 5:
            sys.exit()
        else:
            service_group_name = sys.argv[1]
            a_or_b = sys.argv[2]
            env_list_port = sys.argv[3]
            is_able = sys.argv[4]
            # for n in env_list_port.split():
            if a_or_b == "DEFAULT":
                #print ("nihao")
                get_lb(service_group_name)
            else:
                args = [(service_group_name, n.split(":")[1], n.split(":")[2]) for n in env_list_port.split("_") if a_or_b.split("_")[0] == n.split(":")[0]]
                #print (args)
                set_enable_disable(is_able.lower(), *args)
            # args = [("test2", "10.70.1.128", "8081"), ("test2", "10.70.1.128", "8082")]
    except SystemExit:
        print ("Exception::Usage: lbcron.py <directory path of lbcron.py>")


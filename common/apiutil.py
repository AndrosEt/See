#-*- coding: UTF-8 -*-
import hashlib
import urllib
from urllib import parse
import urllib.request
import base64
import json
import time
import datetime
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.iai.v20200303 import iai_client, models

url_preffix='https://iai.tencentcloudapi.com'
t = time.time()

def setParams(array, key, value):
    array[key] = value


def genSignString(parser):
    uri_str = ''
    for key in sorted(parser.keys()):
        if key == 'app_key':
            continue
        uri_str += "%s=%s&" % (key, parse.quote(str(parser[key]), safe=''))
    sign_str = uri_str + 'app_key=' + parser['app_key']

    hash_md5 = hashlib.md5(sign_str.encode('utf-8'))
    return hash_md5.hexdigest().upper()


class AiPlat(object):
    def __init__(self, secret_id, secret_key):
        self.secret_id = secret_id
        self.secret_key = secret_key
        self.data = {}
        self.url_data = ''
        self.header = {}

    def invoke(self, params):
        self.url_data = urllib.parse.urlencode(params).encode("utf-8")
        req = urllib.request.Request(self.url, self.url_data)
        try:
            rsp = urllib.request.urlopen(req)
            str_rsp = rsp.read().decode('utf-8')
            dict_rsp = json.loads(str_rsp)
            return dict_rsp
        except Exception as e:
            print(e)
            return {'ret': -1}

    def person_create(self, image):
        userName = int(round(time.time() * 1000))

        setParams(self.data, 'Action', "CreatePerson")
        setParams(self.data, 'Version', "2020-03-03")
        setParams(self.data, 'GroupId', "douyin-shenzheng")
        setParams(self.data, 'PersonName', str(userName))
        setParams(self.data, 'PersonId', str(userName))
        image_data = base64.b64encode(image)
        setParams(self.data, 'Image', image_data.decode("utf-8"))
        try:
            cred = credential.Credential(self.secret_id, self.secret_key)
            httpProfile = HttpProfile()
            httpProfile.endpoint = "iai.tencentcloudapi.com"

            clientProfile = ClientProfile()
            clientProfile.httpProfile = httpProfile
            client = iai_client.IaiClient(cred, "ap-beijing", clientProfile)

            req = models.CreatePersonRequest()
            params = self.data

            req.from_json_string(json.dumps(params))

            resp = client.CreatePerson(req)
            print("-------------------------------------- created face: ", resp.FaceId)

            return resp.to_json_string()

        except TencentCloudSDKException as err:
            print(err)



    def face_detectface(self, image):
        userName = int(round(t * 1000))

        setParams(self.data, 'Action', "DetectFace")
        setParams(self.data, 'Version', "2020-03-03")
        setParams(self.data, 'NeedFaceAttributes', 1)
        setParams(self.data, 'NeedQualityDetection', 1)
        image_data = base64.b64encode(image)
        setParams(self.data, 'Image', image_data.decode("utf-8"))
        try:
            cred = credential.Credential(self.secret_id, self.secret_key)
            httpProfile = HttpProfile()
            httpProfile.endpoint = "iai.tencentcloudapi.com"

            clientProfile = ClientProfile()
            clientProfile.httpProfile = httpProfile
            client = iai_client.IaiClient(cred, "ap-beijing", clientProfile)

            req = models.DetectFaceRequest()

            req.from_json_string(json.dumps(self.data))

            resp = client.DetectFace(req)
            if len(resp.FaceInfos) > 0 :
                if resp.FaceInfos[0].FaceQualityInfo.Score > 75:
                    self.person_create(image)
                else:
                    print("Bad face: ", resp.FaceInfos[0].FaceQualityInfo.Score)
            else:
                print("No face")

        except TencentCloudSDKException as err:
            print(err)
# -*- coding: utf-8 -*-
from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
# 导入对应产品模块的 client models。
from tencentcloud.cvm.v20170312 import cvm_client, models

# 导入可选配置项
from tencentcloud.common.profile import client_profile
from tencentcloud.common.profile.http_profile import HttpProfile
try:
    # 实例化一个认证对象，入参需要传入腾讯云账户 secretId，secretKey
    cred = credential.Credential("secretId", "secretKey")

    # 实例化要请求产品 (以 cvm 为例) 的 client 对象
    client = cvm_client.CvmClient(cred, "ap-shanghai")

    # 实例化一个请求对象
    req = models.DescribeZonesRequest()

    # 通过 client 对象调用想要访问的接口，需要传入请求对象
    resp = client.DescribeZones(req)
    # 输出 json 格式的字符串回包
    print(resp.to_json_string())

except TencentCloudSDKException as err:
    print(err)
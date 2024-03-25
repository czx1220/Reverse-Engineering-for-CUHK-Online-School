import requests
import json
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA
import base64

## 基础设置
username = ""
password = ""


# 1. 进入登录页面
url = "https://user.wangxiao.cn/login"
sess = requests.session()
resp = sess.get(url)

# 2. 验证码
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0",
    "Content-Type":"application/json;charset=UTF-8",
    "Host":"user.wangxiao.cn",
    "Cookie":"safedog-flow-item=; mantis_lp6894=http://tg.wangxiao.cn/?agent=zhongda&u_user=bdzdyc01ka&u_plan=PinPaiCi_PC_TongYong_QuanGuo&u_unit=SouSuoCi&u_kwid=2020082210000020&bd_vid=9706530204686560903; mantis_lp_id6894=lp:c0c2751b79fa4425a3ca36026157e177@6894; mantisrf6894=%257B%2522ad%2522%253A%2522bing%2522%252C%2522type%2522%253A%2522sem%2522%252C%2522source%2522%253A%2522referer%2522%257D; mantis6894=e98b9abef4124c5c9274452fc582a35f@6894; trefurl=yTkO9hBeR9kh8WcIz58dWE7G8YCPSdFkvF1xYWejAYk/iy4+WG/wv7A6LuWcLbTIxd9jIhwPn8nQRgi27RO8iHTXt6jNwG992SDdoK1rEwvUyBPODo9SBqcWL5GcZcMzUZW0aH6avp7nPWnvE41PhWOg9TV8Nb2sbwJF3fR/X3pjgFsvD+yFyLdan9xAHmTVZ6TWh1e3b6Z0DTljZZiNnw==; sessionId=1699269543530; agentmembers=wx; Hm_lvt_86efc728d941baa56ce968a5ad7bae5f=1699269548; _bl_uid=nql3moO3mq2tys7gsqdIqts80ek3; pc_346995134_exam=fangchan; Hm_lpvt_86efc728d941baa56ce968a5ad7bae5f=1699274488",
}
verify_code_url = "https://user.wangxiao.cn/apis//common/getImageCaptcha"
verify_resp = sess.post(verify_code_url,headers = headers)
verify_dic = verify_resp.json()
verify_b64_img = verify_dic["data"].split(",")[-1]

def base64_api(img):
    data = {"username":username,"password":password,"typeid":typeid,"image":img}
    result = json.loads(
        requests.post("http://api.ttshitu.com/predict",json=data).text
    )
    if result['success']:
        return result["data"]["result"]
    else:
        return result["message"]

verify_code = base64_api(verify_b64_img)

# 3. 对密码进行加密

# 无js混淆的RSA加密
gettime_url = "https://user.wangxiao.cn/apis//common/getTime"
gettime_resp = sess.post(gettime_url,headers = headers)
gettime_data = gettime_resp.json()["data"]

public_key = "-----BEGIN RSA PUBLIC KEY-----\nZ0Cg7opDNYJM/lFDbRIILRx3pp0HMEkY5Cc/39s8CxDsNVeMw3A+TYi+4bsHyJajR9st/6ib4KGa9+rCS98JM/z8oOLIMAMQVCJ2ehV2fr17SjLdUH3pDlN1A3idTK7crUdd/UUUhJee9pDTI6LI0OX7wH0hBpMb85TUs1aDteE=\n-----END PUBLIC KEY-----"
key = RSA.import_key(public_key)
rsa = PKCS1_v1_5.new(key)

#  encryptFn(pwd + '' + ress.data)
password = password +str(gettime_data)
miwen = rsa.encrypt(password.encode("utf-8"))
miwen = base64.b64encode(miwen).decode("utf-8")

# 4. 进行登录
login_url = "https://user.wangxiao.cn/passwordLogin"
login_data = {
    "imageCaptchaCode": verify_code,
    "password":miwen,
    "userName":username
}

login_resp = sess.post(login_url, data = json.dumps(login_data), headers = headers)
print(login_resp.text)
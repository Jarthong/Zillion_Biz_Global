import requests
import sys
import json
import hmac, base64, struct, hashlib, time
def get_google_code(secret):
    """
    :return: googlecode

    """
    intervals_no = int(time.time()) // 30
    key = base64.b32decode(secret, True)
    msg = struct.pack(">Q", intervals_no)
    h = hmac.new(key, msg, hashlib.sha1).digest()
    # 很多网上的代码不可用，就在于这儿，没有chr字符串
    o = ord(chr(h[19])) & 15
    h = (struct.unpack(">I", h[o:o + 4])[0] & 0x7fffffff) % 1000000

    # 这儿需要注意，程序返回的是去0的字符串，比如验证码是005123，程序计算的结果是5123，所以，需要在前面补0，补到六位数
    return '%06d' % h

if __name__ == '__main__':
    googel_code = get_google_code('X4IAREJPQHJXG4C4')
    print(googel_code)
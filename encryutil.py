from Crypto.Cipher import DES
import base64
import sys
import traceback;

key = 'P2MYLIKE'
class Encrypt():
    def __init__(self, key) :
        self.key = key
    def encrypt_des(self,cipher):
        if cipher is None:
            return ""
        try:
            # ECB方式
            generator = DES.new(self.key, DES.MODE_ECB)
            # 非8整数倍明文补位
            pad = 8 - len(cipher) % 8
            pad_str = ""
            for i in range(pad):
                pad_str = pad_str + chr(pad)
            # 加密
            encrypted = generator.encrypt(cipher + pad_str)
            # 编码得密文
            result = base64.b64encode(encrypted)
            return str(result, encoding="utf-8")
        except:
            info = sys.exc_info()
            print(info[0])
            print(info[1])
            traceback.print_tb(info[2], limit=1, file=sys.stdout)
            return ""

    def decrypt_des(self,encrypted):
        if encrypted is None:
            return ""
        try:

            # ECB方式
            generator = DES.new(self.key, DES.MODE_ECB)
            # 解码
            crypted_str = base64.b64decode(encrypted)
            # 解密
            result = generator.decrypt(crypted_str)
            return str(result, encoding="utf-8")
        except:
            info = sys.exc_info()
            print(info[0])
            print(info[1])
            traceback.print_tb(info[2], limit=1, file=sys.stdout)
            return ""
# t=Encrypt(key);
# print(t.encrypt_des("http://10.100.81.187:8080/MylikeOMS"))
# print(t.encrypt_des("10.100.81.187"))

# #
# #
# print(decrypt_des("Uh5XJ0Ri8bErYgEPLcf10TxYUrSZ2nXiB+z5EWHYbI8="))
# print(decrypt_des("1+2ipxwHGpmQzpd0CExaFw=="))

# -*- coding: UTF-8 -*-
#author:winter
#time 201808
#基类
import hashlib
# import ed25519
class base:
    #字母表
    alphabet='123456789AbCDEFGHJKLMNPQRSTuVWXYZaBcdefghijkmnopqrstUvwxyz'
    def __init__(self):
        return 'base init'

    def base58decode(self,data):
        """
        base58 解码
        :param data:
        :return:
        """
        result = 0

        for d in data:
            charIndex = self.alphabet.find(d)
            result = result * len(self.alphabet)
            result = result + charIndex

        decoded = hex(result)

        # if data[0] == Base58Alphabet[0]:
        #     decoded = str(0x0) + decoded

        return decoded

    def ascToHexString(self,data):
        #ascii 转16进制，会补全为2位

        length = len(data)
        retString = '';
        for i in range(0,length):
            hexString = str(hex(ord(data[i:i+1])))[2:]
            if len(hexString)<2: #补全操作
                hexString = "0" + hexString
            retString = retString + hexString

        return retString

    def base58encode(self,data):
        result = []
        # 首先将字符串转换成十六进制数
        x = int(data, 16)
        base = 58
        zero = 0

        while x != zero:
            x, mod = divmod(x, base)
            result.append(self.alphabet[mod])

        # if data[0] == str(0x0):
        #     result.append(Base58Alphabet[0])

        # 利用自己实现的reverse算法，当然实际工作中直接调用python标准库中的函数
        return "".join(self.reverse(result))


    def reverse(self,res):
        """
        反转列表
        :param res:
        :return:
        """

        if len(res) <= 1:
            return res

        length_half = int(len(res) / 2)
        length = len(res) - 1

        for i in range(length_half):
            tmp = res[i]
            res[i] = res[length-i]
            res[length-i] = tmp

        return res

    def hash256(self,data):
        #hash256 编码，入参为字符串，出参还是字符串
        hashString_ob = hashlib.new("sha256");
        hashString_ob.update(data)
        hashString_f = hashString_ob.digest()
        return hashString_f


    def to_ascii(self,h):
        list_s = []
        for i in range(0,len(h),2):
            list_s.append(chr(int(h[i:i+2].upper(),16)))
        return ''.join(list_s)

    def to_hex(self,s):
        list_h = []
        for c in s:
            list_h.append(str(hex(ord(c)))[-2:]) #取hex转换16进制的后两位

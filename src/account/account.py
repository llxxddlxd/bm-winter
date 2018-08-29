# -*- coding: UTF-8 -*-
#author:winter
#time 201808
#账号类
import sys
import os
import hashlib
import random
import ed25519
class account():
    alphabet='123456789AbCDEFGHJKLMNPQRSTuVWXYZaBcdefghijkmnopqrstUvwxyz'#字母表
    privateKey = '' #私钥
    publicKey = ''  #公钥
    address = ''    #地址
    rawPrivateKey = ''#原始私钥
    rawPublicKey = '' #原始公钥

    def __init__(self):
        print 'account init'
    def __del__(self):
        print 'account del'
    def activate(self):
        print 'active'
    def setMetadata(self):
        print 'set Metadata'
    def setPrivilege(self):
        print 'setPrivilege'
    def getInfo(self):
        print 'getInfo'

    def randomString(self,n):
        return (''.join(map(lambda xx:(hex(ord(xx))[2:]),os.urandom(n))))[0:32]

    def randomCharRand(self,n):
        #生成指定个数的字节  字符串
        byteString = '';
        # tempArr = (17,236,24,183,207,250,207,180,108,87,224,39,189,99,246,85,138,120,236,78,228,233,41,192,124,109,156,104,235,66,194,24);
        for i in range(0,n):
            tempRand = random.randint(0,255)
            byteString = byteString + chr(tempRand)
            # byteString = byteString + chr(tempArr[i])
        return byteString

    def randomByRandom(self):
        # os.urandom(32)
        signing_key, verifying_key = ed25519.create_keypair(entropy=os.urandom)
        # print signing_key.to_ascii(encoding="hex")
        # print len(signing_key.to_seed())
        vk = signing_key.get_verifying_key()
        self.rawPrivateKey = signing_key.to_seed();
        rawPublicKey = vk.to_ascii(encoding="hex")
        self.rawPublicKey = self.to_ascii(rawPublicKey)

    def genPrivateKey(self):
        #1产生32字节  随机字符串
        self.randomByRandom();
        firstString= self.rawPrivateKey
        # print len(self.rawPublicKey)
        # self.rawPrivateKey = firstString = self.randomCharRand(32);
        # self.setRawPublicKey();
        #2拼上version
        secondString = chr(1) + firstString;
        #3拼上prefix
        thirdString = chr(218) + chr(55) + chr(159) + secondString;
        #4拼上后尾的0
        fourthString = thirdString + chr(0)
        #5 2次hash256
        hashString_f = self.hash256(fourthString)
        hashString_s = self.hash256(hashString_f)
        hashString = hashString_s[0:4]
        # hexString = self.ascToHexString(hashString_s);
        fifthString = fourthString + hashString
        #6 调用base 中的base58加密
        hexString = self.ascToHexString(fifthString);
        # print hexString;
        privateKey = self.base58encode("0x"+hexString)
        return privateKey;

    def genPublicKey(self):
        # 1 原生rawPublicKey
        # tt = (21,118,76,208,23,224,218,117,50,113,250,38,205,82,148,81,162,27,130,83,208,1,240,212,54,18,225,158,198,50,87,10);
        # tempstr = ''
        # for i in range(0,32):
        #     tempstr = tempstr + chr(tt[i])
        # firstString= tempstr
        firstString= self.rawPublicKey
        # self.setRawPublicKey();
        # 2拼上version
        secondString = chr(1) + firstString;
        # 3拼上prefix
        thirdString = chr(176) + secondString;
        # 5 2次hash256
        hashString_f = self.hash256(thirdString)
        hashString_s = self.hash256(hashString_f)
        hashString = hashString_s[0:4]
        # hexString = self.ascToHexString(hashString_s);
        fourthString = thirdString + hashString
        # 6 调用base 中的16进制加密
        hexString = self.ascToHexString(fourthString);
        # print len(hexString)
        return hexString;


    def genAddress(self):
        #1原生公钥  1次hash256
        # tt = (21,118,76,208,23,224,218,117,50,113,250,38,205,82,148,81,162,27,130,83,208,1,240,212,54,18,225,158,198,50,87,10);
        # tempstr = ''
        # for i in range(0,32):
        #     tempstr = tempstr + chr(tt[i])
        # print len(tempstr)
        firstString= self.rawPublicKey
        firstString = self.hash256(firstString)
        firstString = firstString[12:32]
        # print len(firstString)
        #2拼上version
        secondString = chr(1) + firstString;
        #3拼上prefix
        thirdString = chr(1) + chr(86) + secondString;
        #5 2次hash256
        hashString_f = self.hash256(thirdString)
        hashString_s = self.hash256(hashString_f)
        hashString = hashString_s[0:4]
        # hexString = self.ascToHexString(hashString_s);
        fourthString = thirdString + hashString
        #6 调用base 中的base58加密
        hexString = self.ascToHexString(fourthString);
        # print hexString;
        address = self.base58encode("0x"+hexString)
        return address;

    def setRawPublicKey(self):
        # print len(self.rawPrivateKey)
        print (os.urandom)
        # vkey_hex = vk.to_ascii(encoding="hex")
        # print "the public key is", vkey_hex


    def create(self):
        #1生成私钥
        self.privateKey = self.genPrivateKey()
        #2公私
        self.publicKey = self.genPublicKey()
        #3地址
        self.address = self.genAddress()

        retInfo = {"privateKey":self.privateKey,"publicKey":self.publicKey,"address":self.address}
        return retInfo

    def base58decode(self, data):
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

    def ascToHexString(self, data):
        # ascii 转16进制，会补全为2位

        length = len(data)
        retString = '';
        for i in range(0, length):
            hexString = str(hex(ord(data[i:i + 1])))[2:]
            if len(hexString) < 2:  # 补全操作
                hexString = "0" + hexString
            retString = retString + hexString

        return retString

    def base58encode(self, data):
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

    def reverse(self, res):
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
            res[i] = res[length - i]
            res[length - i] = tmp

        return res

    def hash256(self, data):
        # hash256 编码，入参为字符串，出参还是字符串
        hashString_ob = hashlib.new("sha256");
        hashString_ob.update(data)
        hashString_f = hashString_ob.digest()
        return hashString_f

    def to_ascii(self, h):
        list_s = []
        for i in range(0, len(h), 2):
            list_s.append(chr(int(h[i:i + 2].upper(), 16)))
        return ''.join(list_s)

    def to_hex(self, s):
        list_h = []
        for c in s:
            list_h.append(str(hex(ord(c)))[-2:])  # 取hex转换16进制的后两位

#test start
# account = account();
# account.randomByRandom();
# ret = account.create();
# print ret
# exit;



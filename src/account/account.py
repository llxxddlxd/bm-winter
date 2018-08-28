# -*- coding: UTF-8 -*-
#author:winter
#time 201808
import sys
import os
import random
import ed25519
# sys.path.append(os.path.abspath(".."))
from base import base
class account(base):
    '账号类'
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

#test start
account = account();
# account.randomByRandom();
ret = account.create();
print ret
exit;



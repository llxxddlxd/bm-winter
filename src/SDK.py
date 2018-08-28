# -*- coding: UTF-8 -*-
#author:winter
#time 201808
class SDK(object):
    def __new__(cls):
        # 关键在于这，每一次实例化的时候，我们都只会返回这同一个instance对象
        if not hasattr(cls, 'instance'):
            cls.instance = super(SDK, cls).__new__(cls)
        return cls.instance



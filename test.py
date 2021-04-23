# -*- coding: utf-8 -*-
"""
Created on Fri Apr  9 14:00:34 2021

@author: Hen676
"""
from enum import Enum

class Raid_Emoji(Enum):
    ONE = '1️⃣'
    TWO = '2️⃣'
    THREE = '3️⃣'
    FOUR = '4️⃣'
    SEVEN = '7️⃣'
    
    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_ 
    
    
print(Raid_Emoji.has_value('1️⃣'))
    
if any(xs in ['Leader','Admin'] for xs in ['v','y','x']):
    print('role true')
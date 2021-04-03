# -*- coding: utf-8 -*-
"""
Created on Sat Apr  3 14:11:00 2021

@author: Hen676
"""

import logging
import bot

if '__main__' == __name__:
    # run client 
    logging.basicConfig(filename='debug.log',
                        level=logging.INFO,
                        format='%(asctime)s %(message)s',
                        datefmt='%d/%m/%Y %I:%M:%S %p')
    
    faded_bot = bot.Faded_Bot()
    faded_bot.start()
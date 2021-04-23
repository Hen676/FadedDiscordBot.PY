# -*- coding: utf-8 -*-
"""
Created on Sat Apr  3 14:11:00 2021

main.py: Faded Vanguard Discord Bot main 

Todo:
    * clean code
    * add custom rich presences (aka playing "wash your hands")
"""
__author__ = "Henry John Timms"
__copyright__ = "Copyright 2021, Henry John Timms"
__license__ = "MIT"
__program__ = "Faded Vanguard Discord Bot"
__version__ = "1.0.0"

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
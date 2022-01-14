#!/usr/bin/python
# -*- coding: UTF-8 -*-

#import chardet
import os
import sys 
import time
import numpy as np
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt
import spidev as SPI
sys.path.append("..")
from lib import LCD_1inch28
from PIL import Image,ImageDraw,ImageFont
from GridEye import GridEye


def ge_visualize_LCD():
    # Raspberry Pi pin configuration:
    RST = 27
    DC = 25
    BL = 18
    bus = 0
    device = 0
    try:
        # display with hardware SPI:
        ''' Warning!!!Don't  creation of multiple displayer objects!!! '''
        #disp = LCD_1inch28.LCD_1inch28(spi=SPI.SpiDev(bus, device),spi_freq=10000000,rst=RST,dc=DC,bl=BL)
        disp = LCD_1inch28.LCD_1inch28()
        # Initialize library.
        disp.Init()

        # Clear display.
        disp.clear()

        # print("currentdpi={}, currentfigsize={}".format(mpl.rcParams['figure.dpi'], mpl.rcParams['figure.figsize']))
        plt.figure(figsize=(2, 2))

        while(1):
            # Get grideye data
            myeye = GridEye(0x19)
            pixel = np.array(myeye.pixelOut())
            pixel.resize(8, 8)

            # Convert GrideyeData to heatmap image
            sns.heatmap(pixel, annot=True, cbar=False, square=True, xticklabels=False, yticklabels=False)
            plt.savefig("../pic/ge_heatmap.jpg", dpi=120)
            plt.clf()
            
            image = Image.open('../pic/ge_heatmap.jpg')
            im_r=image.rotate(180)
            disp.ShowImage(im_r)
            
    except IOError as e:
        print(e)
    except KeyboardInterrupt:
        disp.module_exit()
        exit()


if __name__ == '__main__':
    ge_visualize_LCD()
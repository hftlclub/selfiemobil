##Fotoautomat mit Raspberry Pi
#Make 1/15
#

import RPi.GPIO as IO
import time
import os
import picamera
from os.path import basename, splitext
import sys
import getopt
import ftplib
import PIL.Image
import PIL.ImageEnhance
from PIL import Image
import pygame



countdownList = ['3_', '2_', '1_']


def shot():
    ## define filename for output image
    timestamp = time.ctime(time.time())
    timestamp = timestamp.replace(" ", "_")
    timestamp = timestamp.replace(":", "")
    destFile = "./selfies/selfie-" + timestamp + ".jpg"
   
    ## show countdown overlays
    for i in countdownList:
        nmbr = Image.open('./img/' + i + '.png')
        rgbNmbr = Image.new('RGB', (((nmbr.size[0] + 31) // 32) * 32, ((nmbr.size[1] + 15) // 16) * 16, ) )
        rgbNmbr.paste(nmbr, (0, 0))
        c = piCam.add_overlay(rgbNmbr.tostring(), size=nmbr.size)
        c.alpha = 100
        c.layer = 3
        time.sleep(1)
        piCam.remove_overlay(c)


    ## take picture
    smile = PIL.Image.open('./img/0_.png')
    rgbSmile = Image.new('RGB', (((smile.size[0] + 31) // 32) * 32, ((smile.size[1] + 15) // 16) * 16, ) )
    rgbSmile.paste(smile, (0, 0))
    olSmile = piCam.add_overlay(rgbSmile.tostring(), size=smile.size)
    olSmile.layer = 3
    
    piCam.resolution = (2048, 1536)
    piCam.capture(destFile)


    
    wait = PIL.Image.open('./img/wait.png')
    rgbWait = Image.new('RGB', (       ((wait.size[0] + 31) // 32) * 32, ((wait.size[1] + 15) // 16) * 16, ) )
    rgbWait.paste(wait, (0, 0))
    olWait = piCam.add_overlay(rgbWait.tostring(), size=wait.size)
    olWait.layer = 3
    
    piCam.remove_overlay(olSmile)
    
    


    resultImg = PIL.Image.open(destFile)
    resultImg = resultImg.transpose(Image.FLIP_LEFT_RIGHT) 
    
    
    rgbResultImg = Image.new('RGB', (       ((resultImg.size[0] + 31) // 32) * 32, ((resultImg.size[1] + 15) // 16) * 16, ) )
    rgbResultImg.paste(resultImg, (0, 0))
    olResult = piCam.add_overlay(rgbResultImg.tostring(), size=resultImg.size)
    olResult.layer = 3
    
    
    piCam.remove_overlay(olWait)
    

    ## add logo to image
    logo = PIL.Image.open('./img/logo.png')
    logo.show();
    logo = logo.resize((248, 120), Image.ANTIALIAS) #190, 92
    brightness = 0.8
    logo = PIL.ImageEnhance.Brightness(logo).enhance(brightness)
    pos = (30,1385)
# comment out next line to disable logo
#    resultImg.paste(logo, pos, mask=logo) 

    #mask=logo for logo transparency
    #bild.alpha_composite(logo,bild)
    resultImg.save(destFile)
    #t = splitext(basename(destFile))[0]   
    
    piCam.resolution = (1024,768)
    
    time.sleep(3)
    piCam.remove_overlay(olResult)	



## camera initialization
pygame.init()
piCam = picamera.PiCamera()
piCam.preview_fullscreen = True
piCam.resolution = (1024,768)
piCam.hflip = False
piCam.vflip = True
piCam.annotate_text_size=160
#piCam.annotate_background=picamera.Color('red')
piCam.start_preview(fullscreen=True)
piCam.iso = 0
piCam.video_stabilization = True
piCam.exposure_compensation = 5


## configure IO pin
IO.setwarnings(False)
IO.setmode(IO.BCM)
Taster = 24
IO.setup(Taster, IO.IN, pull_up_down=IO.PUD_DOWN)
finished = False




## application loop
while not finished:
    while not IO.input(Taster):
        pygame.event.get()
        pass
    time.sleep(0.05)
    if IO.input(Taster):
        shot()

#!/usr/bin/python

import urllib,urlparse,string,time,os,sys,re,cmath
from datetime import datetime, timedelta
from sys import argv

def Makegpcolor(gempakCMD,COLOR,DEVICE):

   gempakCMD += ['gpcolor << EOF ']
   gempakCMD += ['COLOR    = {} '.format(COLOR)]
   gempakCMD += ['DEVICE = {}'.format(DEVICE)]
   gempakCMD += [''] 
   gempakCMD += ['run']
   gempakCMD += ['']
   gempakCMD += ['exit']
   gempakCMD += ['']
   gempakCMD += ['EOF']
   return gempakCMD 

def Makegpmap(gempakCMD,GAREA,deviceFile,vgOutFileName,LATLON,tblfile,TEXT,Format,MAP, XYpoints,PANEL,Title):
    
    gempakCMD += ['gpmap << EOF '] 
    gempakCMD += ['\\\$mapfil=hipowo.gsf\n\\\$RESPOND=no']
    gempakCMD += ['MAP      = {} '.format(MAP)]
    gempakCMD += ['GAREA    = {}'.format(GAREA)]
    gempakCMD += ['PROJ     = mer']
    gempakCMD += ['SATFIL   = ']
    gempakCMD += ['RADFIL   =  ']
    gempakCMD += ['LATLON   = {} '.format(LATLON)]
    gempakCMD += ['PANEL    = {} '.format(PANEL)]
    gempakCMD += ['TITLE    = {}'.format(Title)]
    gempakCMD += ['TEXT     = {}  '.format(TEXT)]
    gempakCMD += ['CLEAR    = no ']
    gempakCMD += ['DEVICE   = {}  {} {}'.format(Format,deviceFile,XYpoints)]
    gempakCMD += ['LUTFIL   = ']
    gempakCMD += ['STNPLT   =  ']
    gempakCMD += ['VGFILE   = {} {} '.format(vgOutFileName,tblfile)]
    gempakCMD += ['']
    gempakCMD += ['run']
    gempakCMD += ['']
    gempakCMD += ['exit']
    gempakCMD += ['']
    gempakCMD += ['EOF']

    return gempakCMD

def Makegptext(gempakCMD,textLegendFile,deviceFile,TXTLOC,TEXT,Format,XYpoints,PANEL):

   gempakCMD += ['gptext << EOF']
   gempakCMD += ['\\\$mapfil=hipowo.gsf\n\\\$RESPOND=no']
   gempakCMD += ['PROJ     = MER']
   gempakCMD += ['PANEL    = {}'.format(PANEL)]
   gempakCMD += ['COLORS   = 1']
   gempakCMD += ['TEXT     = {}'.format(TEXT)]
   gempakCMD += ['CLEAR    = no']
   gempakCMD += ['DEVICE   = {}  {} {}'.format(Format,deviceFile,XYpoints)]
   gempakCMD += ['TXTFIL   = {}'.format(textLegendFile)]
   gempakCMD += ['TXTLOC   = {}'.format(TXTLOC)]
   gempakCMD += ['COLUMN   = 1']
   gempakCMD += ['']
   gempakCMD += ['run']
   gempakCMD += ['']
   gempakCMD += ['exit']
   gempakCMD += ['']
   gempakCMD += ['EOF']

   return gempakCMD


def writefile(outFileName,dataarray ):
    with open(outFileName, 'w') as f:
     for item in dataarray:
       f.write("{}\n".format(item))
    return True


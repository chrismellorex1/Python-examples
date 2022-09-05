#!/usr/bin/python
#
#
import urllib, urlparse, string, time, os, sys, re, cmath

def definition_elements(definitions):

#                     r    g    b 
   fdeckdict={'AIRC' : [ 255 , 0 , 0] , 
           'AMSR' : [ 174 , 170 , 170] , 
           'AMSU' : [ 174 , 170 , 170] ,
           'ANAL' : [ 255 , 255 , 255] ,
           'ASCT' : [ 0 , 170 , 0] ,
           'DRPS' : [ 114 , 97 , 97] ,
           'DVTO' : [ 117 , 54 , 22] ,
           'DVTS' : [ 117 , 54 , 22] ,
           'GPMI' : [ 174 , 170 , 170] ,
           'OSCT' : [ 242 , 153 , 224] ,
           'RDRC' : [ 153 , 224 , 242] ,
           'RDRD' : [ 153 , 245 , 242] , 
           'SATC' : [ 242 , 190 , 153] ,
           'SSMI' : [ 174 , 170 , 170] ,
           'SSMS' : [ 174 , 170 , 170] ,
           'WSAT' : [ 174 , 170 , 170] , 
           'sources' : ["AIRC","AMSR","AMSU","ANAL","ASCT","DRPS","DVTO","DVTS","GPMI","OSCT","RDRC","RDRD","SATC","SSMI","SSMS","WSAT"]
            }

   adeckdict = {}
   adeckdict={ 'models' :  ["AC00","AEMI","AEMN","AHNI","AP","AVNI","AVNO","AVNX","BEST","CARQ","CEM2","CEMI","CEMN","CHC2","CHCI","CLP5","COT2" \
           ,"COTC","COTI","CTC2","CTCI","CTCX","DRCL","DSHP","DSPE","DSWR","EC00","ECME","ECMO","ECO2","ECOI","EE","EGR2" \
           ,"EGRI","EGRR","EHH2","EHHI","EMH","EMH2","EMHI","EMN2","EMN3","EMN4","EMNI","EMX","EMX2","EMXI","EN","EP","FSSE" \
           ,"GFEX","GFL2","GFLI","GFSL","GFSO","HCCA","HHFI","HHNI","HMNI","HMON","HWFI","HWRF","ICON","IVCN","IVDR","IVRI" \
           ,"LGEM","LGME","NEMN","NGX","NGX2","NGXI","NNIC","NVG2","NVGI","NVGM","OCD5","OFCI","OFCL","OFCO","OFCP","OFP2","OFPI" \
           ,"RI25","RI30","RVCN","RVCX","SHF5","SHIP","SHPE","TABD","TABM","TABS","TBDE","TBME","TBSE","TCLP","TVCA","TVCE" \
           ,"TVCN","TVCX","TVDG","UE","UEM2","UEMI","UEMN","UKX","UKX2","UKXI","XTRP"]
            }

 
       
   definitions={'FDECK' : fdeckdict}
   definitions.update( {'ADECK' : adeckdict } )
   return definitions


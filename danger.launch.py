#!/usr/bin/python

import urllib, urlparse, string, time, os, sys, re, cmath
from datetime import datetime, timedelta
from makeGempak import *

send=True
###
now = datetime. now()
hour=hh=now.strftime("%H")
###
#######################################################
###
###
houroffset=0

dat=datetime.strftime(datetime.now() + timedelta(hours = int(houroffset)), '%Y%m%d')
wk=day=datetime.strftime(datetime.now() + timedelta(hours = int(houroffset)), '%d')
actday=datetime.strftime(datetime.now() + timedelta(hours = int(houroffset)), '%a')
fmonth=datetime.strftime(datetime.now() + timedelta(hours = int(houroffset)), '%B')
yy=year=datetime.strftime(datetime.now() + timedelta(hours = int(houroffset)), '%Y')
mon=datetime.strftime(datetime.now() + timedelta(hours = int(houroffset)), '%m')
time=datetime.strftime(datetime.now() + timedelta(hours = int(houroffset)), '%a %B %d %Y')

houroffset=24
yesterdy=datetime.strftime(datetime.now() - timedelta(hours = int(houroffset)), '%Y%m%d')
nextday=datetime.strftime(datetime.now() + timedelta(hours = int(houroffset)), '%Y%m%d')

basin="atlantic"
active="y"

if str(basin) == "atlantic" : 
  if  int(hour) > 1 and  int(hour) <= 6:  
       hh="03"
       wmoid="PWEK89"
       dat='{}{}'.format(dat,hh)
  elif int(hour) >= 7 and int(hour) <= 13: 
       hh="09"
       wmoid="PWEK90"
       dat='{}{}'.format(dat,hh)
  elif int(hour) >= 14 and int(hour) <= 18: 
       hh="15"
       wmoid="PWEK91"
       dat='{}{}'.format(dat,hh)
  elif  int(hour) >= 19 and int(hour) <= 23: 
       hh=21
       wmoid="PWEK88"
       dat='{}{}'.format(dat,hh)
  else:
     print "This is not the proper time to run the script"
     print "Try again later. "
###     rm -f dat2
###     rm -f dat3
     exit()
   
  psdevice='ps | danger_atl_{}.ps | 11;8.5 | M'.format(dat)
  pname='danger_atl_{}.ps'.format(dat)
  tdevice='tiff | {}'.format(wmoid)
  fname='{}.FAX'.format(wmoid)
  gfdevice='gf | danger_atl_{}.gif | 896;716'.format(dat)
  gfname='danger_atl_{}.gif'.format(dat)
  gname='danger_atl_{}'.format(dat)
  bwdevice='gf | danger_atl_{}bw.gif | 896;716'.format(dat)
  bwname='danger_atl_{}bw.gif'.format(dat)
  bname='danger_atl_{}bw'.format(dat)
  bas="atl"
  latlon="1/10/3/1;1/10;10/-5.;-8./2"
  labelloc="#5.0;-32.0"
  sendfile="danger_atlc.vgf"
  label='VALID: {}00 UTC {} {} {}, {}'.format(hh,actday,fmonth,day,year)
  area="-7;-104;61;-2"
if  str(active) == "n" and str(basin) == "atlantic" : 
       area="-7;-104;61;-2"
       print "Ok...going to launch default graphic."
       sendfile="danger_atlc_default.vgf"
       label='VALID: {}00 UTC {} {} {}, {}'.format(hh,actday,fmonth,day,year)

if str(basin) == "pacific" :
  if  int(hour) > 1 and  int(hour) <= 6:
       hh="03"
       wmoid="PWFK88"
       dat='{}{}'.format(dat,hh)
  elif int(hour) >= 7 and int(hour) <= 13:
       hh="09"
       wmoid="PWFK89"
       dat='{}{}'.format(dat,hh)
  elif int(hour) >= 14 and int(hour) <= 18:
       hh="15"
       wmoid="PWFK90"
       dat='{}{}'.format(dat,hh)
  elif  int(hour) >= 19 and int(hour) <= 23:
       hh=21
       wmoid="PWFK91"
       dat='{}{}'.format(dat,hh)
  else:
     print "This is not the proper time to run the script"
     print "Try again later. "
###     rm -f dat2
###     rm -f dat3
     exit()


  area="-7;-180;41;-80"
  psdevice='ps | danger_epac_{}.ps | 11;8.5 | M'.format(dat)
  pname='danger_epac_{}.ps'.format(dat)
  tdevice='tiff | {}'.format(wmoid)
  fname='{}.FAX'.format(wmoid)
  gfdevice='gf | danger_pac_{}.gif | 896;716'.format(dat)
  gfname='danger_pac_{}.gif'.format(dat)
  gname='danger_pac_{}'.format(dat)
  bwdevice='gf | danger_pac_{}bw.gif | 896;716'.format(dat)
  bwname='danger_pac_{}bw.gif'.format(dat)
  bname='danger_pac_{}bw'.format(dat)
  bas="pac"
  latlon="1/10/3/1;1/10;10//2"
  labelloc="#5.0;-140.0"
  sendfile="danger_epac.vgf"
  label='VALID: {}00 UTC {} {} {}, {}'.format(hh,actday,fmonth,day,year)


if str(basin) == "pacific" and str(active) == "no":
      print "Ok...going to launch default graphic."
      sendfile="danger_epac_default.vgf"
      label='VALID: {}00 UTC {} {} {}, {}'.format(hh,actday,fmonth,day,year)

labelout=[]
labelout += ["TROPICAL CYCLONE MARINE GRAPHIC\n" ]
labelout += [ "NATIONAL HURRICANE CENTER\n"]
labelout += [ "TROPICAL ANALYSIS AND FORECAST BRANCH\n"]
labelout += [ "MIAMI FLORIDA  33165\n"]
labelout += [ 'VALID: {}00 {}\n'.format(hh,time)]
sent=writefile("label.file",labelout )

labelout=[]
labelout += ["SEE PRODUCT NOTICE BULLETIN FOR FURTHER DETAILS"]
sent=writefile("notice.file",labelout )

######################
#### FIRST & SECOND  #
######################################################
#### CREATE TIFF VERSION OF ATLANTIC SEA STATE CHART.#
#### THIS VERSION GOES DIRECTLY TO THE MARTA & GOES  #
#### TO OSO VIA DBNET.                               #
######################################################
###
###echo Creating TIFF version of $basin Danger Zone graphic now...

Gempakscript=[]
Gempakscript=Makegpmap(Gempakscript,area,tdevice,sendfile,latlon,' ','1.5/22//221///sw',' ','1//2', ' ','0','1/-2/{}'.format(label) )
Gempakscript=Makegptext(Gempakscript,'notice.file',tdevice,'.40;.90','1.5/22/1/221/1/c/sw',' ',' ','0')
Gempakscript=Makegptext(Gempakscript,'logo | 1.5',tdevice,'.80;.90','1.2/22/1/111/1/c/sw',' ',' ','0')

if  str(active) == "n": 
  Gempakscript=Makegptext(Gempakscript,'label.file',tdevice,labelloc,'1.0/11/1/221/1/c/sw',' ',' ','0')
 
Gempakscript += ['gpend']

###display ${wmoid}.tiff
##########################################
#### CREATE A POSTSCRIPT FILE TO PRINT ! #
##########################################
###
Gempakscript=Makegpmap(Gempakscript,area,psdevice,sendfile,latlon,' ','1.2/22//221///sw',' ','1//2', ' ','0','1/-2/{}'.format(label) )
Gempakscript=Makegpmap(Gempakscript,area,psdevice,sendfile,latlon,' ','1.5/22//221///sw',' ','1//2', ' ','0','1/-2/{}'.format(label) )
Gempakscript=Makegptext(Gempakscript,'notice.file',psdevice,'.40;.90','1.5/22/1/111/1/c/sw',' ',' ','0')
Gempakscript=Makegptext(Gempakscript,'logo | 1.5',psdevice,'.80;.90','1.6/22/1/111/1/c/sw',' ',' ','0')

if  str(active) == "n":
  Gempakscript=Makegptext(Gempakscript,'label.file',psdevice,labelloc,'1.2/11/1/221/1/c/sw',' ',' ','0')

Gempakscript += ['gpend']

###
#############################################
#### CREATE ONE GIF FILE FOR TPC'S WEBSITE. #
#############################################

Gempakscript=Makegpmap(Gempakscript,area,gfdevice,sendfile,latlon,' ','1.5/21//121///sw',' ','1//2', ' ','0','1/-2/{}'.format(label) )
Gempakscript=Makegptext(Gempakscript,'notice.file',gfdevice,'.40;.90','1.5/22/1/111/1/c/sw',' ',' ','0')
Gempakscript=Makegptext(Gempakscript,'logo | 1.5',gfdevice,'.80;.90','1.4/21/1/111/1/c/sw',' ',' ','0')

if  str(active) == "n":
  Gempakscript=Makegptext(Gempakscript,'label.file',gfdevice,labelloc,'1.1/11/1/221/1/c/sw',' ',' ','0')

Gempakscript += ['gpend']

###
###cp $gfname danger_${bas}.gif
###
###
#######################################
#### CREATING A BLACK/WHITE GIF FILE. #
#### CREATE ONE B/W GIF FILE FOR TPC'S WEBSITE. #
########################################
#### Set colors to black & white only. #
########################################

Gempakscript=Makegpcolor(Gempakscript,'101=bla;1=van;2=red;3=gre;4=blu;5=yel;6=cya;7=mag;8=bro;9=cor ',bwdevice)
Gempakscript=Makegpcolor(Gempakscript,'10=apr;11=pin;12=dkp;13=mdv;14=mar;15=fir;16=orr;17=ora;18=dko;19=gol',bwdevice)
Gempakscript=Makegpcolor(Gempakscript,'20=dky;21=lwn;22=mdg;23=dkg;24=grp;25=ltb;26=sky;27=mdc;28=vio;29=pur ',bwdevice)
Gempakscript=Makegpcolor(Gempakscript,'30=plu;31=whi;32=bla ','bwdevice')

Gempakscript=Makegpmap(Gempakscript,area,bwdevice,sendfile,latlon,' ','1.5/21//121///sw',' ','1//2', ' ','0','1/-2/{}'.format(label) )
Gempakscript=Makegptext(Gempakscript,'notice.file',bwdevice,'.40;.90','1.1/11/1/111/1/c/sw',' ',' ','0')
Gempakscript=Makegptext(Gempakscript,'logo | 1.5',bwdevice,'.80;.90','1.4/21/1/111/1/c/sw',' ',' ','0')


if  str(active) == "n":
  Gempakscript=Makegptext(Gempakscript,'label.file',bwdevice,labelloc,'1.1/11/1/221/1/c/sw',' ',' ','0')

Gempakscript += ['gpend']

for line in Gempakscript:
 print line

###gpend
###
###cp ${bwname} danger_${bas}_${hh}bw.gif
###cp ${bwname} danger_${bas}bw.gif 
###
###
###############################
#### PUT COLORS BACK TO COLOR #
#### INSTEAD OF BLACK & WHITE #
###############################

Gempakscript=Makegpcolor(Gempakscript,'101=bla;1=van;2=red;3=gre;4=blu;5=yel;6=cya;7=mag;8=bro;9=cor ','gf|dummy.gif')
Gempakscript=Makegpcolor(Gempakscript,'10=apr;11=pin;12=dkp;13=mdv;14=mar;15=fir;16=orr;17=ora;18=dko;19=gol','gf|dummy.gif')
Gempakscript=Makegpcolor(Gempakscript,'20=dky;21=lwn;22=mdg;23=dkg;24=grp;25=ltb;26=sky;27=mdc;28=vio;29=pur ','gf|dummy.gif')
Gempakscript=Makegpcolor(Gempakscript,'30=plu;31=whi;32=bla ','gf|dummy.gif')
Gempakscript += ['gpend']
###
###rm -f dummy.gif*
###rm notice.file
###
##############################################################
#### CALL THE SEND SCRIPT TO ACTUALLY SEND OUT THE PRODUCTS. #
##############################################################
###
###/bin/ksh danger_send $dat $basin $wmoid
###
###exit

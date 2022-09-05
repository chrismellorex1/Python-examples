#!/usr/bin/python

#### highwind.launch.py mello 12/2019                                  #
#######################################################
####
###    Will import into GFE 
####################################
import urllib, urlparse, string, time, os, sys, re, cmath
from datetime import datetime, timedelta
from makeGempak import * 

send=True

now = datetime. now()
hh=now.strftime("%H")

print hh
###
if int(hh) < 1:
  houroffset=24

else:
  houroffset=48

dat=datetime.strftime(datetime.now() + timedelta(hours = int(houroffset)), '%Y%m%d')
wk=day=datetime.strftime(datetime.now() + timedelta(hours = int(houroffset)), '%d')
actday=datetime.strftime(datetime.now() + timedelta(hours = int(houroffset)), '%a')
fmonth=datetime.strftime(datetime.now() + timedelta(hours = int(houroffset)), '%B')
yy=year=datetime.strftime(datetime.now() + timedelta(hours = int(houroffset)), '%Y')
mon=datetime.strftime(datetime.now() + timedelta(hours = int(houroffset)), '%m')

basin="atlantic"
active="y"
###
if  str(basin) == "atlantic" : 
###  print "Are there any high wind or seas EAST OF 100W?"
###  print "Are there any high wind or seas WEST OF 80W?"
###  print " y  <or>  n"
    active="y"

valid=day
if int(hh) >= 4 and int(hh) < 8 : 
   cycle=00
   awmoid="PWEK89"
   pwmoid="PWFK89"
elif  int(hh) >= 8 and int(hh) < 14: 
   print "Emily is cool"
   cycle=06
   awmoid="PWEK90"
   pwmoid="PWFK90"
elif int(hh) >= 14 and int(hh) < 20: 
   cycle=12
   awmoid="PWEK91"
   pwmoid="PWFK91"
elif int(hh) >= 20 or int(hh) < 2 :
   cycle=18
   awmoid="PWEK88"
   pwmoid="PWFK88"
else:
   print " "
   print "This time is either too late for the"
   print "18Z graphic or too early for the 00z"
   print "Exiting..."
   print " "
   exit()

print cycle
print awmoid
print pwmoid
#################################
#### Create label for vgf file. #
#################################
###
synop='VALID: {}00 UTC {}/{}/{}'.format(cycle,mon,wk,yy)
print synop

label=[]
###
label +=  "48HR HIGH WIND AND SEAS GRAPHIC\n" #> labelfile
label +=  '{} \n '.format(synop) # >> labelfile


with open("labelfile", 'w') as file_handler:
    for item in label:
        file_handler.write("{}".format(item))

if basin == "atlantic":
   area='-3;-105;31;-31'
   psdevice='ps | hiwind_atl_{}{}.ps | 11;8.5 | M'.format(dat,cycle)
   pname='hiwind_atl_{}{}.ps'.format(dat,cycle)
   tdevice='tiff | {}'.format(awmoid)
   tname=awmoid
   fname='{}.FAX'.format(awmoid)
   gfdevice='gf | hiwind_atl_{}{}.gif | 896;716'.format(dat,cycle)
   gfname='hiwind_atl_{}{}.gif'.format(dat,cycle)
   gname='hiwind_atl_{}{}'.format(dat,cycle)
   bwdevice='gf | hiwind_atl_{}{}bw.gif | 896;716'.format(dat,cycle)
   bwfname='hiwind_atl_{}{}bw.gif'.format(dat,cycle)
   bwname='hiwind_atl_{}{}bw'.format(dat,cycle)

   loc="#34.0;-90.00"
   loc2="#27.0;-100.00" 

if  active == "n" and basin == "atlantic" : 
       print "Ok...going to launch default graphic."
       sendfile="atlwind_default.vgf"
       label='VALID: {}00 UTC {} {} {}, {}'.format(cycle,actday,fmonth,day,year)
if active == "y" and  basin == "atlantic"  :
       sendfile="highwind_launch.file"            #`cat highwind_launch.file` 
#       os.system('cp -f {} HOLD.vgf.'.format(sendfile))
#       os.system('rm -f highwind_*.vgf')
#       os.system('mv -f HOLD.vgf {}'.format(sendfile))
       label='VALID: {}00 UTC {} {} {}, {}'.format(cycle,actday,fmonth,day,year)



if  str(basin) == "pacific" and str(active) == "yes": 
      area="-3;-144;32;-78"
      psdevice='ps | hiwind_pac_{}{}.ps | 11;8.5 | M'.format(dat,cycle)
      pname='hiwind_pac_{}{}.ps'.format(dat,cycle)
      tdevice='tiff | {}'.format(pwmoid)
      tname='{}'.format(pwmoid)
      fname='{}.FAX'.format(pwmoid)
      gfdevice='gf | hiwind_pac_{}{}.gif | 896;716'.format(dat,cycle)
      gfname='hiwind_pac_{}{}.gif'.format(dat,cycle)
      gname='hiwind_pac_{}{}'.format(dat,cycle)
      bwdevice='gf | hiwind_pac_{}{}bw.gif | 896;716'.format(dat,cycle)
      bwfname='hiwind_pac_{}{}bw.gif'.format(dat,cycle)
      bwname='hiwind_pac_{}{}bw'.format(dat,cycle)
      loc='#33.0;-95.00'
      loc2='#25.0;-102.0'


if  str(basin) == "pacific" and str(active) == "no":
      print "Ok...going to launch default graphic."
      sendfile="pacwind_default.vgf"
      label='VALID: {}00 UTC {} {} {}, {}'.format(cycle,actday,fmonth,day,year)


if  str(basin) == "pacific" and str(active) == "yes":
#      sendfile=`cat highwind_launch.file`
#      cp -f $sendfile HOLDPAC.vgf
#      rm -f highwind_*.vgf
#      mv -f HOLDPAC.vgf $sendfile
       label='VALID: {}00 UTC {} {} {}, {}'.format(cycle,actday,fmonth,day,year)

if  str(basin) != "pacific" and str(basin) != "atlantic":
       print "You entered an incorrect basin name!"
       print "Please re-run the script."
       exit()

labelout=[]
labelout += ["48HR HIGH WIND AND SEAS GRAPHIC\n" ]
labelout += [ "HIGH WIND(KT) AND SEAS (FT)\n"]  
labelout += [ "NATIONAL HURRICANE CENTER\n"]
labelout += [ "TROPICAL ANALYSIS AND FORECAST BRANCH\n"] 
labelout += [ "MIAMI FLORIDA  33165\n"] 

with open("labelfile", 'w') as file_handler:
    for item in labelout:
        file_handler.write("{}".format(item))


#####################
#### FIRST & SECOND #
#####################
######################################################
#### CREATE TIFF VERSION OF HIGH WIND/WAVE CHART.    #
#### THIS VERSION GOES DIRECTLY TO THE MARTA & GOES  #
#### TO OSO VIA DBNET.                               #
######################################################
Gempakscript=[]
Gempakscript=Makegpmap(Gempakscript,area,tdevice,sendfile,'1/10/3/1;1/10;10//2',' ','1.3/22//221///sw',' ','1//3', ' ','0','1/-2/{}'.format(label) )
Gempakscript=Makegptext(Gempakscript,'labelfile',tdevice,loc,'1.0/22/1/221/1/c/sw',' ',' ','0') 
Gempakscript=Makegptext(Gempakscript,'logo | 1.5',tdevice,loc2,'1.2/22/1/221/1/c/sw',' ',' ','0')
Gempakscript += ['gpend']

###display ${tname}.tiff

##########################################
#### CREATE A POSTSCRIPT FILE TO PRINT ! #
##########################################
###echo Making a local copy of $basin High Wind/Wave graphic to print now...

Gempakscript=Makegpmap(Gempakscript,area,psdevice,sendfile,'1/10/3/1;1/10;10//2',' ','1.5/22//221///hw',' ','1//3',' ','0','1/-2/{}'.format(label))
Gempakscript=Makegptext(Gempakscript,'labelfile',psdevice,loc,'1.0/22/1/221/1/c/sw',' ',' ','0')
Gempakscript=Makegptext(Gempakscript,'logo | 1.5',psdevice,loc2,'1.2/22/1/221/1/c/sw',' ',' ','0')
Gempakscript += ['gpend']

###
#############################################
#### CREATE ONE GIF FILE FOR TPC'S WEBSITE. #
#############################################
###
###echo Creating GIF version of $basin High Wind Graphic now...

Gempakscript=Makegpmap(Gempakscript,area,gfdevice,sendfile,'1/10/3/1;1/10;10//2',' ','1.3/22//221///sw',' ','1//3',' ','0','1/-2/{}'.format(label))
Gempakscript=Makegptext(Gempakscript,'logo | 1.5',gfdevice,loc2,'1.2/22/1/221/1/c/sw',' ',' ','0')
Gempakscript=Makegptext(Gempakscript,'labelfile',gfdevice,loc,'1.0/22/1/221/1/c/sw',' ',' ','0')
Gempakscript += ['gpend']


#################################################
#### CREATE ONE B/W GIF FILE FOR TPC'S WEBSITE. #
#################################################
###
###echo Creating B/W GIF version of ${basin} now...
###
########################################
#### Set colors to black & white only. #
########################################
###
Gempakscript=Makegpcolor(Gempakscript,'101=white;1=bla;2=bla;3=bla;4=bla;5=bla;6=bla;7=bla;8=bla;9=bla',bwdevice)
Gempakscript=Makegpcolor(Gempakscript,'10=bla;11=bla;12=bla;13=bla;14=bla;15=bla;16=bla;17=bla;18=bla;19=bla',bwdevice)
Gempakscript=Makegpcolor(Gempakscript,'20=bla;21=bla;22=bla;23=bla;24=bla;25=bla;26=bla;27=bla;28=bla;29=bla',bwdevice)
Gempakscript=Makegpcolor(Gempakscript,'30=bla;31=bla;32=bla',bwdevice)
Gempakscript=Makegpmap(Gempakscript,area,bwdevice,sendfile,'1/10/3/1;1/10;10//2',' ','1.3/22//221///sw',' ','1//3',' ','0','1/-2/{}'.format(label))
Gempakscript=Makegptext(Gempakscript,'logo | 1.5',bwdevice,loc2,'1.2/22/1/221/1/c/sw',' ',' ','0')
Gempakscript=Makegptext(Gempakscript,'labelfile',bwdevice,loc,'1.0/22/1/221/1/c/sw',' ',' ','0')
Gempakscript += ['gpend']

###gpend
###
####mv ${bwname}.gif ${bwfname}
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

for line in Gempakscript:
 print line

###rm -f dummy.gif*
###
###
##############################################################
#### CALL THE SEND SCRIPT TO ACTUALLY SEND OUT THE PRODUCTS. #
##############################################################

if send: 
    print "send out the products"
###
###   /bin/ksh highwind_send ${dat}${cycle} $basin $awmoid
###   /bin/ksh highwind_send ${dat}${cycle} $basin $pwmoid

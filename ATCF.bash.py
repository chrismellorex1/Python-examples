#!/usr/bin/python
# This scripts readis listofATC.conf that reads a list of know models from the ATCF adecks
#
#
####################################
import urllib, urlparse, string, time, os, sys, re, cmath
from definitions import *
from datetime import datetime
now = datetime. now()
hour=now.strftime("%H")
year=now.strftime("%Y")
day=now.strftime("%d")
month=now.strftime("%m")
cycle="00"

timeargument=str(year)+str(month)+str(day)+str(cycle) 
print timeargument

atcffile="aal132019.dat"
atcffile="fal052019.dat"
os.system("cd /Users/chrismello/scripts")
os.system("touch touch.xml")
os.system("rm *.xml")
os.system("cp Adeck.conf listofATCF.conf")

firststring=atcffile[0:1]
print firststring
if firststring == "a": 
  os.system("cp Adeck.conf listofATCF.conf")
if firststring == "b":
  os.system("cp Bdeck.conf listofATCF.conf")
  timeargument=str(year) 
if firststring == "f":
  fdeckaltered=[] 
  os.system("cp Fdeck.conf listofATCF.conf")
  timeargument=str(year)
  print timeargument 
  command="cp " + str(atcffile) + "  atcffile.old"
  os.system(command)
  with open(atcffile, 'r') as f: #open the file
     contents = open(atcffile, 'r').readlines() #put the lines to a variable (list).
  for currentline in contents:
     replacesource=[] 
     replacesource=["AIRC","AMSR","AMSU","ANAL","ASCT","DRPS","DVTO","DVTS","GPMI","OSCT","RDRC","RDRD","SATC","SSMI","SSMS","WSAT"] 
     for source in replacesource:
       if source in currentline:
          replace="FDECK-"+str(source)  
          currentline=currentline.replace(source, replace)
          print currentline 
     fdeckaltered += [currentline]    
  with open(atcffile, 'w') as f:
    for item in fdeckaltered:
        f.write("%s\n" % item)    

#cat listofATCF.conf | while read model
#do
#echo $model
#./convert-adeck-two-xml.py $atcffile $model ${year}${month}${day}${cycle}
#done
#ls -ltr *.xml | grep -v " 520 " | grep -v " 516 "   |  grep -v " 518 "   | awk '{print $9}' > sendlist

#cat sendlist | while read currentmodel 
#do
#echo $currentmodel 
   
#   decktest=`wc $currentmodel  | awk '{print $1}' `
#   if [ `echo "$decktest > 11" | bc` -eq 1 ];then
#     scp  $currentmodel  ldad@nhcn-ldad:/data/ldad/ATCF
#     echo "SENDING $currentmodel $decktest PASSED "
#      else
#     echo "FAILED $currentmodel $decktest FAILED to small"
#      fi

#done
#cp  ${atcffile}.old $atcffile 
#mv *.xml ../data 

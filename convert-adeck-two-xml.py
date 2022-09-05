#!/usr/bin/python
#
#
#  Script to convert A-deck to xml file for AWIPS2 ingest 
#  created by Chris Mello 
#             File name     wildcard of model    date cycle 
# arguments   aal052019.dat     UE               2019090712
#
#
#
#
#

import urllib, urlparse, string, time, os, sys, re, cmath
from definitions import *  


class createXML:
      
    def __init__(self, body, contents, deckfilename,model, modeldata,modelname,outfile,requestedtime): 
        self.body = body
        self.contents = contents
        self.deckfilename = deckfilename
        self.model = model
        self.modelname = modelname
        self.modeldata = modeldata
        self.outfile = outfile
        self.requestedtime = requestedtime 
         



    def writefile(self):

        outfile=self.outfile
        body=self.body
        deckfilename=self.deckfilename

        file=re.sub('[2][0][1-2][0-9]+', '', deckfilename)
        file=re.sub('\.', '', file)
        file=file.replace("dat", "")
        outfile= file + "-" +  outfile
        print outfile 
        print "TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT"
        with open(outfile, 'w') as f:

#    Get the storm name from the name of the file replaces the string ATCF in the xml file with the stormmane
  
          stormname=re.sub('[2][0][1-2][0-9]+', '', deckfilename)
          stormname=re.sub('\.', '', stormname) 
          stormname=stormname.replace("dat", "")

#     Get the forecast hour from the name of the ourput xml file ...fill replace the F000_00Z string in the file with a forecast hour number 6-240    
 
          timestamp=re.sub('[2][0][1][0-9]+', '', outfile) 
          sitelist=[]
          sitelist=["CHC2" ,"CEM2", "CLP5", "CHC2", "CEM2", "AC00", "COT2", "CTC2", "EC00", "ECMO", "ECO2", "EGR2", "EHH2", "EMH2", "EMN2", "EMN3", "EMN4", "EMX2", "GFL2", "NGX2", \
                   "NVG2", "OCD5", "OFP2", "RI25", "RI30", "SHF5", "UEM2", "UKX2" ]   
          for model in sitelist: 
             timestamp=timestamp.replace(model, "XXX")      
          timestamp=re.sub('\.xml', '', timestamp)
          timestamp=timestamp.replace("dat", "")
          timestamp=timestamp.replace("tracks", "")
          timestamp=timestamp.replace("Lows", "")
          timestamp=re.sub('[A-Z]+', '', timestamp)
 
          for item in body:
            item=item.replace("ATCF", stormname  ) 
            item=item.replace("F000_00Z", timestamp )
            f.write("{}\n".format(item))
        return True

    
    def extractdata(self):

        contents=self.contents
        model=self.model
        requestedtime=self.requestedtime 

        size=len(contents)
        sum = 0
        simplelist=[]

#     Read the A-deck file...use the basic split command to parse out the data.
#    puts data into a list and returns the data to a variable for further analysis
#
        for currentline in contents:
            currentline=currentline.replace(" ", "");
            splitline= currentline.split(",")
            FDECKtest=str(model)
            if FDECKtest != "FDECK":
               time=splitline[2]
               currentmodel=splitline[4]
               hour=int(splitline[5])
               lat_str=splitline[6]
               lon_str=splitline[7]
               pressure_str=splitline[9]
            if FDECKtest == "FDECK":
               time=splitline[2]
               currentmodel=splitline[4]
               hour=int(0)
               lat_str=splitline[7]
               if lat_str == "":
                  lat_str="700N"
               print lat_str  
               lon_str=splitline[8]
               if lon_str == "":
                  lon_str="900W"
               pressure_str="0"



#   gets rid of the E W N S in the lattitude longitude section...creates approriate sign for AWIPS2 to plot  
        
            if 'N' in lat_str:
                lat_str=lat_str.replace("N", "")
                lat=(float(lat_str)/10)
            else:
                lat_str=lat_str.replace("S", "")
                lat=(float(lat_str)/-10)

            if 'W' in lon_str:
                lon_str=lon_str.replace("W", "")
                lon=(float(lon_str)/-10)
            else:
                lon_str=lon_str.replace("E", "")
                lon=(float(lon_str)/10)
            
            if FDECKtest == "FDECK": 
               if lat > 100:
                lat=float(lat/10.0)
               if lon < 1000:
                lon=float(lon/10.0)
               if lat > 70:
                lat=float(lat/10.0)


            pressure=float(pressure_str)

            if re.search(model,currentmodel):
                print currentmodel

            modeltest=str(model) 
            if modeltest=="BEST" or modeltest== "FDECK":     
                requestedtime=time
            if requestedtime == time:    
                if re.search(model,currentmodel):
                    printline = {'lat':lat, 'lon':lon, 'pressure':pressure, 'time':time, 'model':currentmodel, 'hour':hour}
                    simplelist.append(printline) 
                    print "Match Found"
                    print currentmodel
                else:
                    print "no match"
        return simplelist 


    def makelows(self):

        modeldata=self.modeldata
        modelname=self.modelname
        deckfilename= self.deckfilename

        size=len(modeldata)
        print size
        sum = 0
#    Create the standard xml header needed for PGEN in AWIPS2 

        header=[]    
        header += ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>']
        header += ['<Products xmlns:ns2="http://www.example.org/productType">']
        header += ['<Product outputFile="linetest.xml" useFile="false" saveLayers="false" onOff="true" status="UNKNOWN" center="NH2" forecaster="cmello" type="ATCF_Atlantic(F000_00Z)" name="ATCF_{model}(F000_00Z)">'.format(model=modelname)]
        header += [' <Layer filled="false" monoColor="false" onOff="true" name="ATCF_{model}(F000_00Z)">'.format(model=modelname)]
        header += ['    <Color alpha="255" blue="0" green="255" red="255"/>']
        header += ['    <DrawableElement>']

        all_tracks = {"{model}tracks{tau:02}".format(model=modelname, tau=tau):  {'xml':[], 'tau':tau} for tau in range(0, 241, 6)}

        modeltest=str(modelname)
        if modeltest=="FDECK":
         all_tracks = {"{model}tracks{tau:02}".format(model=modelname, tau=tau):  {'xml':[], 'tau':tau} for tau in range(0,5, 6)} 
        else:
         all_tracks = {"{model}tracks{tau:02}".format(model=modelname, tau=tau):  {'xml':[], 'tau':tau} for tau in range(0, 241, 6)}


#
#   The deck data is a reformatted list  
#    This part is complicated....Ok...we are going to create xml for each model forecast hour..see above ..so we make    
#     need to make a loop to create a header for each model at each time stamp....copies the head info above into each file.

        for key, data in all_tracks.items():
            data['xml'].extend(header)

        body=[]
        for currentline in modeldata:
            lon = currentline['lon']
            lat = currentline['lat']

#    This moves the mslp label slightly offset of the L 
                
            lonoff=( lon -  (-.95554346123567)) 
            latoff= ( lat  - .0393467566458869)

            lonoff=lon
#        latoff=lat

            pressure = currentline['pressure']
            hour = currentline['hour']
        
            if pressure == 0:
                print "pressure missing"
                print pressure

# 1008 is the threshold for Atlantic 
            modeltest=str(modelname)
            if modeltest=="FDECK":
               pressure=float(1004) 

       # 1008 is the threshold for Atlantic
        
            if pressure < 1009 and pressure != 0:   


                if pressure < 100: 
                 pressure=modeltest
                body=[] 
                blue="255"
                red="255"
                green="255"
                body += ['<Symbol clear="true" sizeScale="1.0" lineWidth="1.0" pgenType="FILLED_LOW_PRESSURE_L" pgenCategory="Symbol" >' ]
                body += ['  <Color alpha="255" blue="0" green="0" red="255"/>' ]
                body += ['  <Color alpha="255" blue="0" green="255" red="0"/>' ]
                body += ['  <Point Lon=\"{lon}" Lat="{lat}"/>'.format(lon=lon, lat=lat)]
                body += ['</Symbol>' ]

                if modeltest=="FDECK":
                  pressure=currentline['model']
                  pressure=pressure.replace("FDECK-", "")
                  lonoff=( lon -  (-.0035554346123567))
                  latoff= ( lat  - .00393467566458869)

                  definitions={}  
                  library=definition_elements(definitions)
                  FDECKdefinitions=library['FDECK']
                  red, green , blue = FDECKdefinitions[pressure]
 

                body += ['<Text auto="false" hide="false" xOffset="0" yOffset="0" displayType="NORMAL" mask="false" rotationRelativity="SCREEN_RELATIVE" rotation="0.0" ithw="0" iwidth="0" justification="CENTER" style="BOLD" fontName="Courier" fontSize="10.0" pgenType="General Text" pgenCategory="Text"  > ']
                body += ['  <Color alpha="255" blue="{blue}" green="{green}" red="{red}" />'.format(blue=blue, green=green, red=red)]
                body += ['  <Point Lon=\"{lon}" Lat="{lat}"/>'.format(lon=lonoff, lat=latoff)]
                body += ['  <textLine>{pressure}</textLine>'.format(pressure=pressure)]
                body += ['</Text>']
                all_tracks['{model}tracks{hour:02}'.format(hour=hour,model=modelname )]['xml'].extend(body)


 

        tail=[]
        tail += ['</DrawableElement>']
        tail += ['   </Layer>' ]
        tail += ['</Product>' ]
        tail += ['</Products>' ]

        for key, data in all_tracks.items():
            data['xml'].extend(tail)

        for key, data in all_tracks.items():
            writefile("{model}Lows{}.xml".format(data['tau'], model=modelname ), data['xml'], deckfilename)


    def maketracks(self):

        modeldata=self.modeldata
        modelname=self.modelname
        deckfilename= self.deckfilename


        print "-------------------------Mello----------------------------------------------------------------"
        print modelname 

        modeltest=str(modelname)
        if modeltest=="BEST" or modeltest=="FDECK":
          all_tracks = {'tracks{}'.format(tau):{'xml':[], 'tau':tau} for tau in range(0, 5, 6)} 
        else:
          all_tracks = {'tracks{}'.format(tau):{'xml':[], 'tau':tau} for tau in range(0, 241, 6)}
        size=len(modeldata)
        print size
        sum = 0
        header=[]    
        header+= ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>']
        header+= ['<Products xmlns:ns2="http://www.example.org/productType">']
        header+= ['<Product outputFile="linetest.xml" useFile="false" saveLayers="false" onOff="true" status="UNKNOWN" center="NH2" forecaster="cmello" type="ATCF_{model}(F000_00Z)" name="ATCF_{model}(F000_00Z)">'.format(model=modelname)]
        header+= [' <Layer filled="false" monoColor="false" onOff="true" name="ATCF_{model}(F000_00Z)">'.format(model=modelname)]
        header+= ['    <Color alpha="255" blue="0" green="255" red="255"/>']
        header+= ['    <DrawableElement>']
      
        for key, data in all_tracks.items():
            data['xml'].extend(header)

        simplelist=[]
        body=[]
        oldlat=60
        oldlon=90    
        oldhour=400
        lat=42
        lon=72


        for currentline in modeldata:
            lon = currentline['lon']
            lat = currentline['lat']
            pressure = currentline['pressure']
            hour = currentline['hour']
            time = currentline['time']
            lineWidth="1.0"
 
            if pressure == 0:
                print "pressure missing"
                print pressure
        
            if pressure < 1009 and pressure != 0:   
                body=[] 
                blue="251"
                red="51"
                green="255"

                if pressure <= 1004 and pressure > 990:
                   blue="255"
                   red="0"
                   green="0"
                   print "Tropical Storm" 

                if pressure <= 990 and pressure > 965:
                   blue="0"
                   red="255"
                   green="0"
                   print "Hurricane"

                if pressure <= 965:
                   blue="255"
                   red="255"
                   green="0"
                   print "Major Hurricane" 

                modeltest=str(modelname)
                if modeltest=="BEST":
                   blue="255"  
                   red="255"
                   green="255" 
                   lineWidth="2.5"

                body += ['<Line flipSide="false" fillPattern="SOLID" filled="false" closed="false" smoothFactor="2" sizeScale="1.0" lineWidth="{lineWidth}" pgenCategory="Lines" pgenType="LINE_SOLID">'.format(lineWidth=lineWidth)]
                body += ['<Color alpha="255" blue="{blue}" green="{green}" red="{red}" />'.format(blue=blue, green=green, red=red)]
                body += ['<Point Lon=\"{lon}" Lat="{lat}"/>'.format(lon=lon, lat=lat)]
                body += ['<Point Lon=\"{lon}" Lat="{lat}"/>'.format(lon=oldlon, lat=oldlat)]
                body += ['</Line>']


                QCchecklat=(oldlat - lat) ** 2
                QCchecklon=(oldlon - lon) ** 2
            
                if QCchecklat  > 30 or QCchecklon > 30:
                    body=[]

                modeltest=str(modelname)
                if modeltest=="BEST":
                   oldhour=-10 

                if hour <= oldhour :
                   body=[]

                oldlat=lat          
                oldlon=lon
                oldhour=hour    
            
                for key, data in all_tracks.items():
                    if hour <= data['tau']:
                        data['xml'].extend(body)

        tail=[]
        tail += ['</DrawableElement>']
        tail += ['   </Layer>' ]
        tail += ['</Product>' ]
        tail += ['</Products>' ]

  
        for key, data in all_tracks.items():
            data['xml'].extend(tail)

        for key, data in all_tracks.items():
            writefile("{model}{}.xml".format(key,model=modelname), data['xml'], deckfilename)





print " _________________   START MAIN PROGRAM ________________________________"

deckfilename= sys.argv[1]
modelname= sys.argv[2]
requestedtime= sys.argv[3]

print deckfilename
print "-------------------------------------------------------"
with open(deckfilename, 'r') as f: #open the file
     contents = open(deckfilename, 'r').readlines() #put the lines to a variable (list).

# reformat raw deck data into a list with lat lon pressure times and models 
#modeldata=extractdata(contents, modelname, requestedtime)
# Make low xml files
#makelows=makelows(modeldata,modelname,deckfilename)
# Make the xml track files
#maketracks=maketracks(modeldata,modelname,deckfilename)

body=[]
model=''
modeldata=[]
outfile=[]

classinstance=createXML(body, contents, deckfilename,model, modeldata,modelname,outfile,requestedtime)
modeldata=classinstance.extractdata()
classinstance.modeldata=modeldata
makelows=classinstance.makelows()
maketracks=classinstance.maketracks()





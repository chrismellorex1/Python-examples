# ---------------------------------------------------------------------
# This software is in the public domain, furnished "as is", without
# technical  support, and with no warranty, express or implied, as to
# its usefulness for any purpose.
#
# CWF_WT_Overrides.TextUtility
#
#  This file is used for WFO specific overrides of the CWF_
#  formatter.
#
#
# Methods:
#   Overrides:
#
#   Additions:
#
# ---------------------------------------------------------------------

import string, time, re, os, types, copy, AFPS, math
import TextRules
import ModuleAccessor
import SampleAnalysis

# for UTC Overrides
import TimeDescriptor

#########################################################################
# CONFIGURATION SECTION

# Thresholds for combining final steep and swell waves
# Logic is based on values being LESS THAN these thresholds

steepThreshold = 3.0
swellThreshold = 4.0
pdDiffThreshold = 6
dirDiffThreshold = 90 # degrees

steepDescriptor = "steep "
swellDescriptor = "swell"

steepnessDivisor = 300

# PCT change in sub periods to trigger trend wording in FIRST PERIOD ONLY
steepPctForTrends = 50
swellPctForTrends = 50

# PCT diff required between swell and steep trends (if they are in opposite directions)
# for trend wording to be cancelled : Applies only to COMBINED SEAS
cancellingPctForTrends = 50

# END CONFIGURATION SECTION
#########################################################################

#**********************************************************************
# MAKE NO CHANGES HERE
# The minimum contents of this file are the following class definition
# and the __init__ method with only "pass" line in it.

class CWF_ST_Overrides:
    def __init__(self):
        pass

    def first_period_seas_phrase(self):
        return {
            "setUpMethod": self.seas_setUp,
            "wordMethod": self.combined_seas_first_period_words,
            #"phraseMethods": self.standard_phraseMethods(),
            "phraseMethods": self.standard_vector_phraseMethods(),
         }


    def seas_phrase(self):
        return {
            "setUpMethod": self.seas_setUp,
            "wordMethod": self.combined_seas_words,
            #"phraseMethods": self.standard_phraseMethods(),
            "phraseMethods": self.standard_vector_phraseMethods(),
         }

    def seasWaveHeight_element(self, tree, node):
        # Weather element to use for reporting seas
        # "COMBINED SEAS 10 TO 15 FEET."
        # IF above wind or swell thresholds
        return "WaveHeight"
    #return "Wave1"

    def seas_setUp(self, tree, node, periodFlag=0):
        FILE = open("/data/local/seas_setUpLog", "a")

        areaLabel = node.getAreaLabel()
        timeRange = node.getTimeRange()
    # Old method returns WaveHeight
        elementName = self.seasWaveHeight_element(tree, node)

    #elementName = "Wave1"
        FILE.write("ELEMENT: " + elementName + "\n")

        descriptor = self.phrase_descriptor(tree, node, "seas", elementName)

        FILE.write("DESCRIPTOR: " + descriptor + "\n")

        node.set("descriptor", descriptor)

        seas = self.ElementInfo(elementName, "List")

        elementInfoList = [seas]
        self.subPhraseSetUp(tree, node, elementInfoList, self.scalarConnector)
        return self.DONE()


    def combined_seas_first_period_words(self, tree, node):
        FILE = open("/data/local/combinedSeasFirstPeriodLog","a")
        FILE.write("------------------------------\n")

        desc = ""
        phrase = node.getParent()
        phrase.set("descriptor",desc)
        waveStr = "waves..." + self.one_wave_first_period_words(tree,node)
        FILE.write("WAVE WORDS: \n"+waveStr+"\n")
        FILE.write("WAVE STR: "+waveStr+"\n")
        return self.setWords(node, waveStr)


    def combined_seas_words(self, tree, node):
        FILE = open("/data/local/combinedSeasLog","a")
        FILE.write("------------------------------\n")

        desc = ""
        phrase = node.getParent()
        phrase.set("descriptor",desc)
        waveStr = "waves..." + self.one_wave_words(tree,node)
        FILE.write("WAVE WORDS: \n"+waveStr+"\n")
        FILE.write("WAVE STR: "+waveStr+"\n")
        return self.setWords(node, waveStr)


    def one_wave_first_period_words(self, tree, node):
        FILE = open("/data/local/oneWaveFirstPeriodWordsLog","a")
        FILE.write("-------------------------------\n")
        elementInfo = node.getAncestor("firstElement")
        elementName = elementInfo.name
        FILE.write("ELEMENT NAME: " + elementName + "\n")
        areaLabel = node.getAreaLabel()
        timeRange = node.getTimeRange()
        argDict = tree.get("argDict")

        statDict = node.getStatDict()
        stats = self.getStats(statDict, elementName)
        units = self.units_descriptor(tree, node, "units", "ft")
        waveUnit = self.units_descriptor(tree, node, "unit", "ft")
        if statDict is None:
            return

        waveWords = self.waves_words(tree, node,includeTrends=1)

        FILE.write("PRE WAVE WORDS: "+waveWords+"\n")

        return waveWords



    def one_wave_words(self, tree, node):
        FILE = open("/data/local/oneWaveWordsLog","a")
        FILE.write("-------------------------------\n")
        elementInfo = node.getAncestor("firstElement")
        elementName = elementInfo.name
        FILE.write("ELEMENT NAME: " + elementName + "\n")
        areaLabel = node.getAreaLabel()
        timeRange = node.getTimeRange()
        argDict = tree.get("argDict")

        statDict = node.getStatDict()
        stats = self.getStats(statDict, elementName)
        units = self.units_descriptor(tree, node, "units", "ft")
        waveUnit = self.units_descriptor(tree, node, "unit", "ft")
        if statDict is None:
            return

        waveWords = self.waves_words(tree, node)

        FILE.write("PRE WAVE WORDS: "+waveWords+"\n")

    return waveWords

    def waves_words(self, tree, node,includeTrends=0):

        FILE = open("/data/local/waveWordsLog","a")
        FILE.write("--------------------------------\n")

    #wavesPhrase = self.waves_words

        #wave1 = self.ElementInfo("Wave1", "List", self.VECTOR())
    #wave2 = self.ElementInfo("Wave2", "List", self.VECTOR())
    #wave3 = self.ElementInfo("Wave3", "List", self.VECTOR())
    #wave4 = self.ElementInfo("Wave4", "List", self.VECTOR())

        wave1 = self.ElementInfo("Wave1", "MinMax", self.VECTOR()) #, phraseDef=wavesPhrase, primary=0)
        wave2 = self.ElementInfo("Wave2", "MinMax", self.VECTOR()) #, phraseDef=wavesPhrase, primary=0)
        wave3 = self.ElementInfo("Wave3", "MinMax", self.VECTOR()) #, phraseDef=wavesPhrase, primary=0)
        wave4 = self.ElementInfo("Wave4", "MinMax", self.VECTOR()) #, phraseDef=wavesPhrase, primary=0)

        wave5 = self.ElementInfo("Wave5", "MinMax", self.VECTOR()) #, phraseDef=wavesPhrase, primary=0)

        elementInfoList = []

        node.set("periodFlag", 1)
        #period1 = self.ElementInfo("Period1", "MinMax", primary=0)
        #period2 = self.ElementInfo("Period2", "MinMax", primary=0)
        #period3 = self.ElementInfo("Period3", "MinMax", primary=0)
        #period4 = self.ElementInfo("Period4", "MinMax", primary=0)

        period1 = self.ElementInfo("Period1", "List", primary=0)
        period2 = self.ElementInfo("Period2", "List", primary=0)
        period3 = self.ElementInfo("Period3", "List", primary=0)
        period4 = self.ElementInfo("Period4", "List", primary=0)

        period5 = self.ElementInfo("Period5", "MinMax", primary=0)

        elementInfoList.append(wave1)
        elementInfoList.append(wave2)
        elementInfoList.append(wave3)
        elementInfoList.append(wave4)

        elementInfoList.append(period1)
        elementInfoList.append(period2)
        elementInfoList.append(period3)
        elementInfoList.append(period4)

##        words = self.subPhraseSetUp(tree, node, elementInfoList, self.vectorConnector)
#########################################################################
        ### ABOVE IS FROM WAVES_SETUP
        #periodFlag = node.getAncestor("periodFlag")

        statDict = node.getStatDict()

        ### initialize the subPhrase list
        subPhrases = []

        elementInfoList = node.getAncestor("elementInfoList")

        ### loop through all the wave grids

    # Set up main arrays (lists) for each wave (should be the same number of list elements as wave groups (4)
    # These will end up with the final individual values for each wave group

        wavesWords = []
        magVals = []
        dirVals = []
        perVals = []

    # Create list of start and end Mags (heights) in case we need to indicate trends.
        startMags = []
        endMags = []

        for waves, period in [("Wave1", "Period1"),("Wave2", "Period2"),("Wave3", "Period3"),("Wave4", "Period4")]: #,("Wave5", "Period5")]:

            FILE.write("-----------------------------------------\n")
            FILE.write("WAVE: "+ waves + "\n" )

            ### grab the info for wave grids
            for elementInfo in elementInfoList:
                if elementInfo.name == waves:
                    wavesInfo = elementInfo
                    break

        # OLD METHOD - 021213
            #wavesWords = ""#self.simple_vector_phrase(tree, node, wavesInfo, checkRepeating=1)

        # LIST OF STATS OF WAVES (hgt and dir)
        # ORIGINAL
            wavestats = tree.stats.get(waves, node.getTimeRange(), node.getAreaLabel(), mergeMethod="List")
        # VERSION 2
        # wavestats = tree.stats.get(waves, node.getTimeRange(), node.getAreaLabel(), mergeMethod="moderatedMinMax")
        # VERSION 3
        # wavestats = tree.stats.get(waves, node.getTimeRange(), node.getAreaLabel(), mergeMethod="moderatedMax")

        # Gives values (min,max and direction) for each SUB PERIOD
        # EG (((7.0, 9.0), 343.84718623318213), (Feb 12 13 22:00:00 GMT, Feb 13 13 02:00:00 GMT))
        TR = node.getTimeRange()
        FILE.write("TIME RANGE: " + str(TR) + "\n")

            statsByRange = self.makeRangeStats(tree, self.VECTOR(), wavestats, node.getTimeRange())

        # LIST OF STATS OF PERIOS (pd)
        perstats = tree.stats.get(period, node.getTimeRange(), node.getAreaLabel(), mergeMethod="List")

        perStatsByRange = self.makeRangeStats(tree, self.VECTOR(), perstats, node.getTimeRange())
        #for i in range(len(perStatsByRange)):
        #    FILE.write("PERSTATS BY RANGE: " + str(i) + ": " + str(perStatsByRange[i]) + "\n"  )

        #######################################################################
        # Loop through stats by range to get MAX VALUE IN SUB PERIOD for each wave
        # Also get associated DIR and PER for max value

        dirList = []
        perList = []
        dirIndex = 0
        maxMag = 0

        # Create variables to test for trends
        startMag=0
        endMag=0

        for i in range(len(statsByRange)):
            #FILE.write("STATS BY RANGE " + str(i) + ": " + str(statsByRange[i]) + "\n"  )
        #FILE.write("PER STATS BY RANGE " + str(i) + ": " + str(perStatsByRange[i]) + "\n"  )

        # Set the start mag for trends
        if includeTrends:
            if i==0:
                startMag = int(statsByRange[i][0][0][1])
            elif i == len(statsByRange) - 1:
                endMag = int(statsByRange[i][0][0][1])
            else:
                pass
        else:
            startMag = 999
            endMag = 999

        FILE.write("MAG = " + str(int(statsByRange[i][0][0][1])) + "\n"  )
        FILE.write("DIR = " + str(int(statsByRange[i][0][1])) + "\n"  )

        try:
            myList=[]
            FILE.write("PER MIN = " + str(int(perStatsByRange[i][0][0])) + "\n")
            FILE.write("PER MAX = " + str(int(perStatsByRange[i][0][1])) + "\n")
            myList.append(int(perStatsByRange[i][0][0]))
            myList.append(int(perStatsByRange[i][0][1]))

            maxPd = self._getListMax(myList)
            avgPd = self._getListAverage(myList)
            FILE.write("PER AVG = " + str(avgPd) + "\n")

        except:
            FILE.write("PER(backup) = " + str(int(perStatsByRange[i][0])) + "\n"  )
            # Just use the max
            maxPd = int(perStatsByRange[i][0])
            avgPd = int(perStatsByRange[i][0])

        if int(statsByRange[i][0][0][1]) > maxMag:
            maxMag = int(statsByRange[i][0][0][1])
            dirIndex = i # set index to use to get associated DIR

         dirList.append(int(statsByRange[i][0][1]))
        perList.append(maxPd)
        #perList.append(avgPd)

        FILE.write("START MAG: " + str(startMag) + "\n")
        FILE.write("END MAG: " + str(endMag) + "\n")

         selectedDir = dirList[dirIndex]
        selectedPer = perList[dirIndex]

        FILE.write("SELECTED MAG: " + str(maxMag) + "\n")
        FILE.write("SELECTED DIR: " + str(selectedDir) + "\n")
        FILE.write("SELECTED PER: " + str(selectedPer) + "\n")
        FILE.write("**\n")

        # ADD MAG/DIR TO LIST OF MAG/DIR VALS TO USE IN THE END:
        # IF PD is 0 or 1 then grid does not cover enough area
        if int(selectedPer < 2):
        pass
        else:
                magVals.append(maxMag)
            dirVals.append(selectedDir)
            perVals.append(selectedPer)
        startMags.append(startMag)
        endMags.append(endMag)

        ###############################################################################################
    # Set wave words in local sub routine. This is where the waves get either ignored or combined

    # TEST HOW BIG startMags is
        FILE.write("SIZEOF startMags: " + str(len(startMags)) + "\n")
        FILE.write("SIZEOF endMags: " + str(len(endMags)) + "\n")
         FILE.write("SIZEOF magVals: " + str(len(magVals)) + "\n")

    wavesWords = self._buildSeasSubPhrases(tree, node, magVals, dirVals, perVals, startMags, endMags, elementInfoList)

    # This does not alwasy work and can cause the formatter to crash
    #FILE.write("END WAVE WORDS: " + str(wavesWords[0]) + "\n")

    ###############################################################################################
    # Go through the phrases that have passed the height threshold and build "waveWords"

    for i in range(len(wavesWords)):
        FILE.write("WAVES WORDS " + str(i) + ": " + wavesWords[i] + "\n")
        subPhrases.append(wavesWords[i])

    ###############################################################################################
        ## assemble the subPhrases using appropriate connectors

        i = 0
        words = ""  ### initialize the words variable
        for i in range (len(subPhrases)):
            if (len(subPhrases) - i) == 1:  ### one entry or last entry
                words = words + subPhrases[i]
            elif (len(subPhrases) - i) > 2:  ### 2 or more sub phrases
        continue
                words = words + subPhrases[i] + "..."
            else: ### next to last
                words = words + subPhrases[i] + "...and "

    ###############################################################################################

    FILE.write("RETURN WORDS: "+words+"\n")
        return words

    def _getListAverage(self,myList):
     sum=0
    index=0
    for i in range(len(myList)):
        # SKIP IF VALUE IS 1 or 0
        if myList[i] < 2:
        pass
        else:
            try:
            sum+=int(myList[i])
            index+=1
            except:
            return 0
    if index == 0:
        return 0
    else:
        avg=int(sum/index)
        return avg

    def _getListMax(self,myList):
    # Used only for Period at the moment
    max=0
    for i in range(len(myList)):
        try:
        if myList[i] > max:
            max = myList[i]
        except:
        return 0
    return max

    #def _buildSeasSubPhrases(self,tree,node, magVals, dirVals, perVals, elementInfoList):
    def _buildSeasSubPhrases(self,tree,node, magVals, dirVals, perVals, startMags, endMags, elementInfoList):
    # Loop through arrays (lists)  of mag,dir,and per to compare and then build two main arrays
    # of STEEP and SWELL waves.
    # Then build the strings
    # and then add the strings to wavesWords and then append to subphrases

    FILE = open("/data/local/buildSeasPhraseLog","a")

    wavesWords=[]

    # Initialize the two main buckets (STEEP and SWELL)
    steepWaveList=[]
    swellWaveList=[]

    steepHgt=[]
    steepDir=[]
    steepPer=[]
    steepStartMags=[]
    steepEndMags=[]

    swellHgt=[]
    swellDir=[]
    swellPer=[]
    swellStartMags=[]
    swellEndMags=[]

    steepWave=[]
    swellWave=[]

    steepStartVal=0
        steepEndVal=0
    swellStartVal=0
        swellEndVal=0
    combinedStartVal=0
    combinedEndVal=0

    # Set up check to differentiate start mag and end mag when we loop through each
    startCheck=0

    for i in range(len(magVals)):   # assume these arrays are all the same size
        # divide into steep and swell
        if self._determineSteepnessValue(magVals[i],perVals[i]):
            steepWaveList.append(i)
        steepHgt.append(magVals[i])
        steepPer.append(perVals[i])
        steepDir.append(dirVals[i])
        steepStartMags.append(startMags[i])
        steepEndMags.append(endMags[i])
        else:
        swellWaveList.append(i)
        swellHgt.append(magVals[i])
        swellPer.append(perVals[i])
        swellDir.append(dirVals[i])
        swellStartMags.append(startMags[i])
        swellEndMags.append(endMags[i])

        FILE.write("----------------------------------------\n")
        FILE.write("INDEX: " + str(i) + "\n")
        FILE.write("MAG: " + str(magVals[i]) + "\n")
        FILE.write("PER: " + str(perVals[i]) + "\n")
        FILE.write("DIR: " + str(dirVals[i]) + "\n")
        FILE.write("START MAG: " + str(startMags[i]) + "\n")
        FILE.write("END MAG: " + str(endMags[i]) + "\n")

    # Loop through both the steep waves and the swell

    if len(steepHgt) > 0:
        # get array of hgt,per,dir from the combined values of all STEEP WAVES
        steepWave = self._combineWaves(steepHgt,steepPer,steepDir)

        if len(startMags) != 0:
            steepStartWave = self._combineWaves(steepStartMags,steepPer,steepDir)
            steepEndWave = self._combineWaves(steepEndMags,steepPer,steepDir)

        steepStartVal = steepStartWave[0]
        steepEndVal = steepEndWave[0]

        FILE.write("STEEP START NUMBERS: ")
        for i in range(len(steepStartWave)):
            FILE.write(str(steepStartWave[i]) + ", ")
        FILE.write("\n")

        FILE.write("STEEP END NUMBERS: ")
        for i in range(len(steepEndWave)):
                    FILE.write(str(steepEndWave[i]) + ", ")
        FILE.write("\n")

    if len(swellHgt) > 0:
        # get array of hgt,per,dir from the combined values of all SWELL
        swellWave = self._combineWaves(swellHgt,swellPer,swellDir)

        if len(startMags) != 0:
                swellStartWave = self._combineWaves(swellStartMags,swellPer,swellDir)
                swellEndWave = self._combineWaves(swellEndMags,swellPer,swellDir)

        swellStartVal = swellStartWave[0]
        swellEndVal = swellEndWave[0]

                FILE.write("SWELL START NUMBERS: ")
                for i in range(len(swellStartWave)):
                    FILE.write(str(swellStartWave[i]) + ", ")
                FILE.write("\n")

        FILE.write("SWELL END NUMBERS: ")
                for i in range(len(swellEndWave)):
                    FILE.write(str(swellEndWave[i]) + ", ")
                FILE.write("\n")

    # Need to get combined start and end vals for if we have trends (mainly downward) with combined values
    combinedStartVal = math.sqrt(steepStartVal*steepStartVal + swellStartVal*swellStartVal)
    combinedEndVal = math.sqrt(steepEndVal*steepEndVal + swellEndVal*swellEndVal)

    ###########################################################3333
    # TEST IF WE NEED TO USE A TREND

    # Initialize the toggles as NO TRENDS
    steepBuildTrend=0
    steepDimTrend=0
    swellBuildTrend=0
    swellDimTrend=0

    steepBuildingPct = 0
    swellBuildingPct = 0

    if steepStartVal or steepEndVal: # One of these could be zero ...
        #if steepStartVal != 0:
        # For diminishing
        if steepStartVal > 4 and steepEndVal > 1:  # Assume we have a wave that is worth mentioning
        steepBuildDiff = int(steepEndVal - steepStartVal)
             steepBuildingPct = int(100 * steepBuildDiff / steepStartVal)
        # For building
        elif steepStartVal != 0:
        steepBuildDiff = int(steepEndVal - steepStartVal)
                steepBuildingPct = int(100 * steepBuildDiff / steepStartVal)
        # Otherwise:
        else:
        steepBuildingPct = 0

    if swellStartVal or swellEndVal:
        #if swellStartVal != 0:
        if swellStartVal > 4 and swellEndVal > 1:
        swellBuildDiff = int(swellEndVal - swellStartVal)
                swellBuildingPct = int(100 * swellBuildDiff / swellStartVal)
        elif swellStartVal != 0:
        swellBuildDiff = int(swellEndVal - swellStartVal)
                swellBuildingPct = int(100 * swellBuildDiff / swellStartVal)
            else:
                swellBuildingPct = 0

    if steepBuildingPct > steepPctForTrends:
        FILE.write("STEEP BUILD PCT:" + str(steepBuildingPct) + "\n")
        steepBuildTrend = 1
    elif steepBuildingPct < (-1 * steepPctForTrends):
        FILE.write("STEEP DIM PCT:" + str(steepBuildingPct) + "\n")
        steepDimTrend = 1
    else:
        FILE.write("NO STEEP TRENDS: \n" )

    if swellBuildingPct > swellPctForTrends:
            FILE.write("SWELL BUILD PCT:" + str(swellBuildingPct) + "\n")
            swellBuildTrend = 1
        elif swellBuildingPct < (-1 * swellPctForTrends):
            FILE.write("SWELL DIM PCT:" + str(swellBuildingPct) + "\n")
            swellDimTrend = 1
        else:
            FILE.write("NO SWELL TRENDS: \n" )

    # CHECK FOR OPPOSING TRENDS IN STEEP AND SWELL
    combinedBuildTrend=0
    combinedDimTrend=0
    if steepBuildTrend and swellBuildTrend:
        combinedBuildTrend = 1
    elif steepDimTrend and swellDimTrend:
        combinedDimTrend = 1
    elif steepBuildTrend and swellDimTrend:
        if int(math.fabs(steepBuildingPct + swellBuildingPct)) < cancellingPctForTrends:  # Steep is rising swell is falling
        pass  # leave combined trends zero
        elif int(math.fabs(steepBuildingPct)) > int(math.fabs(swellBuildingPct)):
        combinedBuildTrend = 1
        else:
        combinedDimTrend = 1
    elif steepDimTrend and swellBuildTrend:
        if int(math.fabs(swellBuildingPct + steepBuildingPct)) < cancellingPctForTrends:  # Steep is rising swell is falling
        pass # leave combined trends zero
        elif int(math.fabs(swellBuildingPct)) > int(math.fabs(steepBuildingPct)):
                combinedBuildTrend = 1
            else:
                combinedDimTrend = 1
    elif swellDimTrend or steepDimTrend:
        combinedDimTrend = 1
    elif swellBuildTrend or steepBuildTrend:
        combinedBuildTrend = 1

        ######################################################
    # TEST TO EITHER COMBINE SWELL AND STEEP OR KEEP THEM SEPARATE
    domHgt=domPd=domDir=0
    if len(steepWave) and len(swellWave):
        FILE.write("GOT BOTH SWELL AND STEEP!!\n")
        # Get either the dominant hgt,pd,dir from the two wave groups
        # or 0,0,0...which means keep them separate
        domHgt,domPd,domDir = self._getDominantWave(steepWave,swellWave)
        FILE.write("DOMINANT HGT,PD,DIR: " + str(domHgt) + " : " +  str(domPd) + " : " + str(domDir) + "\n")

    elementInfo = elementInfoList[0]


    myHour = time.strftime("%H", time.localtime())
    FILE.write("CURRENT HOUR = " + myHour + "\n")

    # IF THIS IS SENT BEFORE NOON THE REST OF THE PERIOD SHOULD BE "TODAY"
    # OTHERWISE IT IS "TONIGHT" (up until midnight that is...)
    if int(myHour) < 12:
        periodDesc = "through the day"
    else:
        periodDesc = "overnight"

    if domHgt: # Assume domPd and domDir will also be non-zero...
        magString = self.vector_mag(tree, node, domHgt, domHgt, elementInfo.outUnits, "Wave1")
        perString = self.embedded_period_phrase(tree, node, domPd)
        dirString = self.vector_dir(domDir)

        dimString = self.vector_mag(tree, node, combinedEndVal, combinedEndVal, elementInfo.outUnits, "Wave1")

        buildTrendWords = ""
        dimTrendWords = ""
        if combinedDimTrend:
        dimTrendWords = "...subsiding to " + dimString + " " + periodDesc
        if combinedBuildTrend:
        buildTrendWords = "buiding to "

        wavesWords.append(dirString + " " + buildTrendWords + magString + perString + dimTrendWords)
        #wavesWords.append(dirString + " " + buildTrendWords + magString + perString)

        return wavesWords

    # This continues if previous fails (and thus does not return words)
        if len(steepWave) > 0:
        steepMag=steepWave[0]
        steepPer=steepWave[1]
        steepDir=steepWave[2]
            localMagString = self.vector_mag(tree, node, steepMag, steepMag, elementInfo.outUnits, "Wave1")
            localPerString = self.embedded_period_phrase(tree, node, steepPer)
            localDirString = self.vector_dir(steepDir)

        dimString = self.vector_mag(tree, node,steepEndVal,steepEndVal, elementInfo.outUnits, "Wave1")

        buildTrendWords = ""
        dimTrendWords = ""
        if steepDimTrend:
        dimTrendWords = "...subsiding to " + dimString
        if steepBuildTrend:
        buildTrendWords = "building to "

        wavesWords.append(localDirString + " " + buildTrendWords + localMagString + localPerString + dimTrendWords )
        #wavesWords.append(localDirString + " " + buildTrendWords + localMagString + localPerString)

    if len(swellWave) > 0:
        swellMag=swellWave[0]
            swellPer=swellWave[1]
            swellDir=swellWave[2]
            localMagString = self.vector_mag(tree, node, swellMag, swellMag, elementInfo.outUnits, "Wave1")
            localPerString = self.embedded_period_phrase(tree, node, swellPer)
            localDirString = self.vector_dir(swellDir)

        dimString = self.vector_mag(tree, node, swellEndVal, swellEndVal, elementInfo.outUnits, "Wave1")

        buildTrendWords = ""
        dimTrendWords = ""
            if swellDimTrend:
                dimTrendWords = "...subsiding to " + dimString
            if swellBuildTrend:
                buildTrendWords = "building to "

        wavesWords.append(localDirString + " " + buildTrendWords + localMagString + localPerString + dimTrendWords)
        #wavesWords.append(localDirString + " " + buildTrendWords + localMagString + localPerString)


    return wavesWords


    def _determineSteepnessValue(self,waveHgt,wavePd):
    # Subroutine to simply flag if wave is considered "STEEP"
    # waveHgt AND wavePd could both be 0.
    FILE = open("/data/local/steepnessLog","a")

    FILE.write("WAVE HGT: " + str(waveHgt) + "\n")
        FILE.write("WAVE PD: " + str(wavePd) + "\n")

    try:
        logEntry = 1.0 / wavePd
        FILE.write("LOG ENTRY: " + str(logEntry) + "\n")
    except:
        FILE.write("NO LOG ENTRY\n")

    try:
        value = math.exp(-3.3 * math.log(logEntry))
        steepness = value / steepnessDivisor
        FILE.write("STEEPNESS VALUE: " +str(steepness) + "\n")
    except:
        FILE.write("STEEPNESS VALUE:  NOT AVAILABLE\n")
        return 0

    if waveHgt > steepness:
        FILE.write("STEEP WAVE: " + str(waveHgt) + " - " + str(wavePd) + "\n")
            return 1
    else:
        return 0

    def _combineWaves(self,waveHgt,wavePd,waveDir):
    # ASSUME WE ARE GETTING 3 LISTS OF THE SAME LENGTH!
    # RETURNS LIST with  Hgt,Per,Dir

    FILE = open("/data/local/combineWavesLog","a")

    steepnessList=[]
    pdHgtSum=0.0
    avgPd=0
    hgtSum=0.0
    sqrHgtSum=0.0

    maxHgt=0
     maxHgtIndex=0

    for i in range(len(waveHgt)):
        if wavePd[i] > 0:

        # Collect to get resulting period weighted by height of each component wave
        pdHgtSum += float(waveHgt[i]) * float(wavePd[i])
            hgtSum += float(waveHgt[i])

        # Collect to get resulting height (sum of squares)
        sqrHgtSum += float(waveHgt[i])*float(waveHgt[i])

        if waveHgt[i] > maxHgt:
            maxHgt = waveHgt[i]
            maxHgtIndex = i

    # Calculate predominant period (weighted by height)
    try:
        avgPd = pdHgtSum / hgtSum
        FILE.write("WEIGHTED AVG PERIOD: "+str(avgPd)+"\n")
    except:
        FILE.write("COULD NOT CALCULATE PERIOD\n")
        return 0,0,0

    returnHgt = math.sqrt(sqrHgtSum)
    returnPer = avgPd
    returnDir = waveDir[maxHgtIndex]

    return returnHgt,returnPer,returnDir

    def _getDominantWave(self,steepWave,swellWave):
    # Process two wave groups to determine if we should combine the values and, if so,
    # what the period should be
    # takes TWO WAVES (arrays) with Hgt,Pd,Dir
    # returns either Hgt,Pd,Dir or 0,0,0

    FILE=open("/data/local/getDominantWaveLog", "a")

    returnHgt=0
    returnPd=0
    returnDir=0

    FILE.write("STEEP: " + str(steepWave[0]) + "\n")
    FILE.write("SWELL: " + str(swellWave[0]) + "\n")


    ##############################################################################
    # OPTION 1 : Both are below threshold => COMBINE Hgt AND USE LARGEST FOR Pd/Dir
    if steepWave[0] < steepThreshold and swellWave[0] < swellThreshold:
        sqrdHgt=(steepWave[0]*steepWave[0]) + (swellWave[0]*swellWave[0])
        returnHgt=int(math.sqrt(sqrdHgt))
        if (steepWave[0]>swellWave[0]):
        returnPd=int(steepWave[1])
        returnDir=int(steepWave[2])
        else:
        returnPd=int(swellWave[1])
        returnDir=int(swellWave[2])
        FILE.write("OPTION 1: \n")

    ##############################################################################
    # OPTION 2 : Swell is above threshold...steep is not => COMBINE Hgt AND USE SWELL Pd/Dir
    elif (steepWave[0] < steepThreshold) and (swellWave[0] >= swellThreshold):
        sqrdHgt=(steepWave[0]*steepWave[0]) + (swellWave[0]*swellWave[0])
        returnHgt=int(math.sqrt(sqrdHgt))
        returnPd=int(swellWave[1])
        returnDir=int(swellWave[2])
        FILE.write("OPTION 2\n")

    ##############################################################################
    # OPTION 3 : Steep is above threshold...swell is not => COMBINE Hgt AND USE STEEP pd/Dir
    elif (steepWave[0] >= steepThreshold) and (swellWave[0] < swellThreshold):
        sqrdHgt=(steepWave[0]*steepWave[0]) + (swellWave[0]*swellWave[0])
        returnHgt=int(math.sqrt(sqrdHgt))
        returnPd=int(steepWave[1])
        returnDir=int(steepWave[2])
        FILE.write("OPTION 3\n")

    ##############################################################################
    # OPTION 4 : BOTH are above thresholds.
    # Pd AND Dir close? => Yes: COMBINE AND USE LARGER FOR Pd/Dir No: Don't combine...return 0,0,0
    else:

        # ***********************
        # COMBINED HGT - IF WE RETURN COMBINED SEAS WE USE ALL THE ENERGY
        sqrdHgt=(steepWave[0]*steepWave[0]) + (swellWave[0]*swellWave[0])
        combinedHgt=int(math.sqrt(sqrdHgt))

        # ***********************
        #  PERIOD DIFF - FOR TESTING
        perDiff = int(swellWave[1] - steepWave[1])
        if perDiff < 0:     # assume swellPd is longer but check just in case :-)
        perDiff = -1 * perDiff

        # ***********************
        # DIRECTION DIFF - FOR TESTING
        if swellWave[2] < 90:
        swellTestDir = swellWave[2] + 360
        else:
        swellTestDir = swellWave[2]
        if steepWave[2] < 90:
        steepTestDir = steepWave[2] + 360
        else:
        steepTestDir = steepWave[2]
        dirDiff = int(swellTestDir - steepTestDir)
        if dirDiff < 0:
        dirDiff = -1 * dirDiff

        # ***********************
        #  GET FINAL PD and DIR - BOTH HAVE TO BE LESS THAN THRESHOLD TO COMBINE
        #                 IE If one is different enough we keep them separate
        if (perDiff < pdDiffThreshold) and (dirDiff < dirDiffThreshold):
        # COMBINE!
        if steepWave[0] > swellWave[0]:
            returnPd=steepWave[1]
            returnDir=steepWave[2]
        else:
            returnPd=swellWave[1]
            returnDir=swellWave[2]
        returnHgt=combinedHgt
        else:
         # KEEP SEPARATE (ie return all zeros)
        returnHgt=0
        returnPd=0
        returnDir=0

        FILE.write("OPTION 4\n")

    return returnHgt,returnPd,returnDir

    def Xweather_setUp(self, tree, node):

    FILE=open("/data/local/weatherSetupLog","a")

        resolution = node.get("resolution")
        if resolution is not None:
            mergeMethod = "Average"
        else:
            #mergeMethod = "List"
        mergeMethod = "Max"

        elementInfoList = [self.ElementInfo("Wx", mergeMethod, self.WEATHER())]

        self.subPhraseSetUp(tree, node, elementInfoList, self.wxConnector,
                            resolution)
        node.set("allTimeDescriptors", 1)

        if self.areal_sky_flag(tree, node):
            self.disableSkyRelatedWx(tree, node)

        return self.DONE()


    def Xweather_words(self, tree, node):
    FILE=open("/data/local/weather_wordsLog","a")
        # Create a phrase to describe a list of weather sub keys for one sub-period
        # Get rankList
        statDict = node.getStatDict()
        rankList = self.getStats(statDict, "Wx")
        if self._debug:
print("\n SubKeys in weather_words", rankList)
print("   TimeRange", node.getTimeRange(), node.getAreaLabel())
print("   Phrase name", node.getAncestor("name"))
        if rankList is None or len(rankList) == 0:
            return self.setWords(node, "")

        # Check against PoP
        rankList = self.checkPoP(tree, node, rankList)

        # Check visibility
        subkeys = self.getSubkeys(rankList)
        if self.checkVisibility(tree, node, subkeys):
            return self.setWords(node, "null")

        # Get the weather words
        words = self.getWeatherWords(tree, node, rankList)
        node.set('reportedRankList', rankList)

    FILE.write("WORDS INITIAL: " + words + "\n")

        # Add embedded visibility
        words = self.addEmbeddedVisibility(tree, node, subkeys, words)
        if not words:
            words = "null"
        if self._debug:
print("   Setting words", words)

        # To replace multiple "and's" with ellipses
        words = self.useEllipses(tree, node, words)

    FILE.write("WORDS FINAL: " + words + "\n")

        return self.setWords(node, words)

    def wxCombinations(self):
        # This is the list of which wxTypes should be combined into one.
        # For example, if ("RW", "R") appears, then wxTypes of "RW" and "R" will
        # be combined into one key and the key with the dominant coverage will
        # be used as the combined key.
        # You may also specify a method which will be
        #  -- given arguments subkey1 and subkey2 and
        #  -- should return
        #     -- a flag = 1 if they are to be combined, 0 otherwise
        #     -- the combined key to be used
        #  Note: The method will be called twice, once with (subkey1, subkey2)
        #  and once with (subkey2, subkey1) so you can assume one ordering.
        #  See the example below, "combine_T_RW"
        #

    # NOTE: The order matters here and should match the order of wx
    # elements in the subperiods.

        return [
        #("RW","L"),
        #("R","L"),
        #("L","RW"),
        #("L","R"),
        #("R", "RW"),
                #("RW", "R"),
                #("SW", "S"),
                self.combine_T_RW,
            ]

    ##########################################################################3
    # Local Over-ride to eliminate subphrases in Waves that occasionally happen

    def assembleSubPhrases(self, tree, phrase):
        # Assembles sub-phrases adding the time descriptor
        # Check for data

    FILE=open("/data/local/assembleSubPhrasesLog","a")

        # See if ready to process
        if not self.phrase_trigger(tree, phrase):
            return
        if not self.consolidateSubPhrases_trigger(tree, phrase):
            return

#print("NODE", phrase.get("name"), phrase.getTimeRange())
        if self.useUntilPhrasing(tree, phrase):
            return self.assembleUntilSubPhrases(tree, phrase)

        fcst = ""
        index = 0

    FILE.write("--------------------------------------------\n")

        #FILE.write("Assemble Subphrases " + str(phrase.get('name')) + str(phrase) + "\n")

    wtWords = ""
    phraseName = str(phrase.get('name'))
    FILE.write("PHRASE NAME: " + phraseName + "\n")

        for subPhrase in phrase.get("childList"):
            # Check to make sure we have words
            words = subPhrase.get("words")
            if words is None:
                return

        # Set wtWords first run through only...
        if not index:
        wtWords = subPhrase.get("words")
        FILE.write("WT Words: " + words + "\n")

#print("  words", words)
#print("     ", subPhrase.getTimeRange(), subPhrase)
#print("     ", subPhrase.getAncestor("conjunctiveQualifier"))
#print("     ", subPhrase.getAreaLabel())
            if not words:
                continue

            if index == 0:
                #if not subPhrase.get("null"):
                if not self.isNull(subPhrase):
                    # Get descriptor
                    descriptor = phrase.get("descriptor")
                    if descriptor is not None and descriptor:
                        fcst = fcst + descriptor + " "
            else:
                # Get connector
                connectorMethod = phrase.get("connectorMethod")
                connector = connectorMethod(tree, subPhrase)

                if index == 2:

            # ADDED TO BYPASS THIS !!
            continue

                    # Add conjunctive "THEN" to make 3+ subPhrase phrases
                    # flow better. e.g.
                    # "N WIND 10 TO 20 KT RISING TO 30 KT EARLY IN THE
                    # AFTERNOON...THEN RISING TO GALES TO 40 KT LATE
                    # IN THE AFTERNOON."
                    elementName = phrase.getAncestor("elementName")
                    useThenConnector = self.useThenConnector(
                        tree, phrase, elementName, elementName)
                    if useThenConnector:
                        thenConnector = self.thenConnector(
                            tree, phrase, elementName, elementName)
                        if thenConnector:
                            # Add another time descriptor
                            subPhrase.set("timeDescFlag", 1)
                        connector = thenConnector + connector

                fcst = fcst + connector

            # Time Descriptor
            timeDescriptor = self.format(
                self.subPhrase_timeDescriptor(tree, phrase, subPhrase))

            # Get words again in case they were changed by connector method
            fcst = fcst + subPhrase.get("words") # + timeDescriptor

            index = index + 1
#print("  words", fcst)

    FILE.write("SUBPHRASES COMBINED: " + fcst + "\n")
    seasphraseREO = re.compile("seas")

    if seasphraseREO.search(phraseName): ## Meaning we found an element and it is not one of our wave grids
        phrase.set("words", wtWords)
    else:
        phrase.set("words", fcst)
#    phrase.set("words", fcst)

        return self.DONE()

    def combine_T_RW(self, subkey1, subkey2):
    FILE = open("/data/local/combineTRWLog","a")
        # Combine T and RW only if the coverage of T
        # is dominant over the coverage of RW
        wxType1 = subkey1.wxType()
        wxType2 = subkey2.wxType()

    FILE.write("-----------------------------\n")
    FILE.write("SUBKEY1: " + str(wxType1) + "\n")
    FILE.write("SUBKEY2: " + str(wxType2) + "\n")

        if wxType1 == "T" and wxType2 == "RW":
            order = self.dominantCoverageOrder(subkey1, subkey2)
            if order == -1 or order == 0:
                return 1, subkey1
    else:
        order = self.dominantCoverageOrder(subkey1, subkey2)
        FILE.write("ORDER: " + str(order) + "\n")
        return 1, subkey1

        return 0, None


# ---------------------------------------------------------------------
# $Revision$  $Date$
#
# This software is in the public domain, furnished "as is", without
# technical  support, and with no warranty, express or implied, as to
# its usefulness for any purpose.
#
# mergeProds.TextUtility
#
# Version: 1.04 - 01/21/2009
#
#  This module provides methods to merge the content of a previous
#  issuance of a product into the new text created by a GFE formatter.
#  For narrative products like the ZFP and CWF, short term updates
#  from the text can be merged with the text for the longer range
#  periods from the previously issued product. The number of periods
#  to replace are selectable at run time.
#
#  For other products like NOW, SPS, HWO, etc, that the formatter
#  just basically creates place holder text, the entire text from
#  the previous product is returned.
#
#  To do the merging, products are split into "groups" and then each group
#  is parsed for a UGC line and periods.  A group is defined as a
#  UGC line followed by lines of text terminated by a line with "$$"
#  on it. Period text is defined simply as starting with a single "."
#  in the first column and terminated by the start of another period
#  or a blank line. The primary method for decoding a product is:
#    def _splitSegProd(self,product)
#
#  There are two primary methods for merging products:
#
#    def _mergeNarrative(self,new,old,index,synopsis=0)
#    def _mergeGeneric(self,new,old,hdlns=1)
#
#  The following products have specific method names but generally
#  only call either _mergeNarrative and _mergeGeneric:
#
#    def _mergeZFP(self,new,old,index): Calls _mergeNarrative
#    def _mergeCWF(self,new,old,index): Calls _mergeNarrative
#    def _mergeNSH(self,new,old,index): Calls _mergeNarrative
#    def _mergeESF(self,new,old,hdln=0): Calls _mergeGeneric
#    def _mergeNOW(self,new,old,hdln=1): Calls _mergeGeneric
#    def _mergePNS(self,new,old,hdln=0): Calls _mergeGeneric
#    def _mergeSPS(self,new,old,hdln=0): Calls _mergeGeneric
#    def _mergeRWS(self,new,old,hdln=1): Calls _mergeGeneric
#    def _mergeHWO(self,new,old): HWO specific merge method
#
# Change History:
#   1.04 - 01/21/2009 - Made re matches case insensitive
#   1.03 - 06/19/2007 - Bug fix for multiple headlines not separated
#           by a blank line. Also added an extra blank line before the $$ when
#           there is a headline but no forecast text; this is needed due to
#           the text locking of the GFE editor.
#   1.02 - 10/31/2006 - Bug fix for when UGC line ending "ddhhmm-"
#           token is split onto a new line
#   1.01 - 01/17/2006 - First release based on and replaces mergeZFPs
# ---------------------------------------------------------------------
import re
import string

# This is for testing outside of GFE, leave commented out
##def readprod(name):
##    fp=open(name,"r")
##    p=fp.read()
##    fp.close
##    return p

class mergeProds:
    def __init__(self):
        pass
    def _parseUGCLine(self, ugcString):
        """Parses a ugc encoded string into a list of UGC codes.

        Input string must be of form "VAZ001-004>006" without the -ddhhmm-
        terminator. Returns a list of strings of UGC codes:
        ["VAZ001","VAZ004","VAZ005","VAZ006"]."""

        # Parses UGC encoding
        ugc=ugcString.split("-")
        ugcList=[]
        stc=ugcString[0:3]
        for c in ugc:
            if c.find(">") > 1:
                startUGC, endUGC=c.split(">")
                if len(startUGC) > 3:
                    stc=startUGC[0:3]
                    startUGC=startUGC[3:]
                for i in range(int(startUGC), int(endUGC) + 1):
                    ugcList.append("%s%3.3d" % (stc, i))
            elif len(c) > 3:
                stc=c[0:3]
                ugcList.append(c)
            else:
                ugcList.append(stc + c)
        return ugcList
    def _splitPeriods(self, text, offset):
        """Extracts the individual period forecasts from ZFP text.

        Input arguments:
        text: the zfp text, normally only the text from one area (zone combo)
        offset: character index offset of text passed in relative to the
        begining of the whole ZFP product.
        Returns: a list of tuples, one for each period. The tuple contains
        the start and end positions of the period in the ZFP, the period
        label such as "Monday Night", and the actual period text:
        (startCharIndex, endCharIndex, period label, period text). If index
        is > 0, then startCharIndex and are offset by this amount to
        give positions relative to the start of the ZFP, not just the
        start of the text argument (which is usually a single Zone group)."""

        # This is the re expression to get the period label which must be "."
        # in column 1 and terminated with "...". Extended to look over multiple
        # Lines.
        periodExp = re.compile(r"\.(.*?)\.\.\.(?=.*\n)", re.DOTALL)

        # Need to make sure there are no lines with spaces only
        t=re.sub("\n *\n", "\n\n", text) + "\n\n"
        periods_exp=re.compile(r"\n([.][A-Za-z].*?)(?=\n[.\n])", re.DOTALL)
        pList=periods_exp.findall(t)
        periods=[]
        for p in pList:
            p += "\n"
            i=text.find(p) + offset
            j=i + len(p)
            # Extract Period Label (i.e., "Monday Night")
            m=periodExp.match(p)
            if m is not None:
                perLabel=m.group(1)
            else:
                perLabel=""
            periods.append((i, j, perLabel, p))
            #D print "P",i,j,perLabel
        #D print ":"+pList[-1]+":"
        return periods
    def _textdbRead(self, productID, host=None):
        """Gets a product from the AWIPS Text database.

        'host' is set only when ssh is desired, normally not needed.
        For use in operational GFE, use the Baseline method
        getPreviousProduct instead of this method.
        """
        import os

        # use the command directly - assumes FXA environment setup
        if host is None:
            # set path to textdb command
            if 'FXA_HOME' in os.environ:
                cmd = os.environ['FXA_HOME'] + "/bin/textdb -r " + productID
            else:
                cmd = "/awips/fxa/bin/textdb -r " + productID

            # issue the command
            db = os.popen(cmd, 'r')
            previousProduct = db.read()
            db.close()

        # use ssh to access the given host, requires passwordless ssh setup
        else:
            cmd = "ssh " + host + " 'textdb -r " + productID + "'"
            db = os.popen(cmd, 'r')
            previousProduct = db.read()
            db.close()
        return previousProduct

    def _splitSegProd(self, product):
        """Decodes a segemented product into individual goups.
        Version 1.0

        This is a basic parser for a segmented product. A group is defined
        by a line that starts with what looks like UGC encoding, text then
        terminated by a blank line followed by "$$".
        The "text" of the group must be delimited by a blank line from the
        group header and/or any headlines.
        Parsing is done by regular expressions.

        Returns a tupple of a UCG dictionary and a list. The UGC dictionary
        has keys of UGC codes and values of group index the UGC belongs to.
        The returned list is actually a list of dictionaries for each
        group. Each group dictionary has the following keys:
        groupText: tupple of start,end character indices of the text for the
           entire group (rstrip'ed). The terminating "$$" is not included.
        ugcText: tupple of start,end character indices of the UGC line
           (rstrip'ed).
        timeText: tupple of start,end character indices of the Issuance Time
           line (rstrip'ed) (i.e., "1042 AM EST FRI JAN 6 2006").
           (-1,-1) returned if not able to find a time.
        hdlnText: tupple of start,end character indices of all headline lines
           at the top of the group text (rstrip'ed). If no headlines, both
           start and end will be set to the start of fcstText.
        fcstText: tupple of start,end character indices of remaining text after
          any headlines. There must be a blank line separating this section from
          the group header and/or the last headline.
        ugcList: List of UGC codes valid for this group.
        periodsList: List of period information. See _splitPeriods.

        All indices are absolute character positions in the product text.
        In general, terminating newlines are not included in the index ranges.
        There are some product specific exceptions for the above rules
        (NOW where headlines are after the .NOW... line and non segmented
        products like PNS.
        """

        groups_exp=re.compile(
            r"\n([A-Z][A-Z][CZ]\d\d\d[->].*?)(?=\$\$)", re.DOTALL)
        # RE to extract ugcs, used with newlines removed before searching
        ugc_exp=re.compile(
            r"([A-Z][A-Z][CZ]\d\d\d[->]?.*)-[0-3][0-9][0-2][0-9][0-5][0-9]-")
        # RE to get ugc line(s) exactly as in product
        ugclines_exp=re.compile(
            r"([A-Z][A-Z][CZ]\d\d\d[->]?.*)-[ \n]*[0-3][0-9][0-2][0-9][0-5][0-9]-", re.DOTALL)
        blankline_exp=re.compile(r"\n *\n.")
        # Build re to find NWS issue time string of form:
        # "HHMM AM EST MON JAN 10 2005"
        s="[012]?[0-9][0-5][0-9] +.+" + \
           " (JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC) " + \
           ".+(19|20)[0-9][0-9]"
        time_exp=re.compile(s, re.IGNORECASE)
        hdln_exp=re.compile(r"\n(\.\.\..+?\.\.\.)(?= *\n)", re.DOTALL)

        groups=groups_exp.findall(product)
        groupList=[]
        groupNo=0
        ugcToGroupDict={}
        print("_splitSegProd: Processing", len(groups), "groups")
        for grp in groups:
            g=grp.rstrip()
            groupDict={}
            groupDict['ugcText']=(-1, -1)
            #D print groupNo, g
            gstart=product.find(g)
            glen=len(g)
            gend=gstart + glen
            groupDict['groupText']=(gstart, gend)
            #D print groupNo, gstart,gend
            # Now do ugc parsing. First strip out all newlines
            # to get UGC string that may be on continuation lines
            t=re.sub(" *\n", "", g)
            m=ugc_exp.search(t)
            #D print "UGC string=",m.group(1)
            ugcList=[]
            if m is not None:
                ugcList=self._parseUGCLine(m.group(1))
                #D print ugcList
                for c in ugcList:
                    #D print "c=",c
                    ugcToGroupDict[c] = groupNo
                # Get position of ugc string in product
                m=ugclines_exp.search(g)
                if m is not None:
                    start=g.find(m.group(0)) + gstart
                    end=start + len(m.group(0))
                    groupDict['ugcText']=(start, end)

            # Find issuance time string
            m=time_exp.search(g)
            if m is not None:
                timestart=g.find(m.group(0))
                timeend=timestart + len(m.group(0))
                groupDict['timeText']=(timestart+gstart, timeend + gstart)
            else:
                timestart=0
                groupDict['timeText']=(-1, -1)

            # Find where the text for the group starts. This is defined
            # Simply as the first text line after a blank line. Therefore,
            # there must be a blank line after the header (UGC list,
            # UGC name list, city list, issuance time string) and before
            # the segment text. Start looking after the issuance time line
            # to handle a product like PNS
            m=blankline_exp.search(grp[timestart:])
            if m is not None:
                textstart=grp[timestart:].find(m.group(0)) + \
                           len(m.group(0)) - 1 + timestart
            else:
                textstart=glen

            # Special case for NOW with headlines after .NOW... line
            hdln_start=textstart
            hdln_end=textstart
            if grp[textstart:].find(".NOW...") == 0:
                textstart=grp[textstart:].find("\n") + textstart + 1
                #D print "NOW: .now... ends at",textstart + gstart
                while textstart < glen - 1 and grp[textstart] == "\n":
                    textstart += 1
            #D print "Initial textstart=",textstart + gstart

            hdln_start=textstart
            hdln_end=textstart
            # Find all headlines at the top of the forecast section.
            # This logic is to ensure anything that looks like a
            # headline that is not at the top will not be captured.
            # Thus all headlines must be grouped together at the top
            # and a blank line must separate the end of headlines and
            # the begining of the rest of the text.
            for hdln in hdln_exp.findall(grp):
                i=grp.find(hdln)
                if i > textstart:
                    hdln_end=textstart
                    break
                else:
                    hdln_end=i + len(hdln)
                # Start search for blank line with newline ending headline
                m=blankline_exp.search(grp[hdln_end - 1:])
                if m is not None:
                    textstart=grp[hdln_end:].find(m.group(0)) + len(m.group(0)) - 1 + hdln_end
                else:
                    textstart=glen
                    print("No lines after headlines, textstart=", textstart + gstart)

            groupDict['ugcList']=ugcList
            groupDict['hdlnText']=(hdln_start + gstart, hdln_end + gstart)
            groupDict['fcstText']=(textstart+ gstart, gend)

            # Decode any periods in the text
            groupDict['periodsList']=self._splitPeriods(grp, gstart)
            groupList.append(groupDict)
            groupNo += 1
            print("groupText=", groupDict['groupText'])
            print("hdlnText=", groupDict['hdlnText'])
            print("fcstText=", groupDict['fcstText'])
        return ugcToGroupDict, groupList
    def _mergeNarrative(self,new,old,index,synopsis=0):
        """Merges previous forecast into update forecast.
        Use this for narrative type products like ZFP and CWF.

        Input arguments:
        new: ZFP update text
        old: old zfp text
        index: index of last period to keep in the new ZFP.
               1 means keep first period, however, period
               lists used here are indexed starting at 0
               so 1 also means the second period index in
               the period lists.  Will do some limited
               checking to match up periods in the old and
               the new products. This is done by comparing
               the period labels (i.e., "Monday Night").
        synopsis: flag for CWF type products which have a
               synopsis group which should be skipped. The
               value is actually a slice value of which
               group index to start processing. Should be
               0 for ZFP, 1 for CWF.
        Returns: merged text or the new text if any problems
        encountered."""

        # Sanity check of index value.
        if not isinstance(index, type(1)) or index < 0:
            return new

        newDict, newList=self._splitSegProd(new)
        oldDict, oldList=self._splitSegProd(old)
        #D print "oldDict=",oldDict
        #D print "newDict=",newDict
        fcst = ""
        last=0
        for gnewDict in newList[synopsis:]:
            gbnew, genew = gnewDict['groupText']
            ugcList = gnewDict['ugcList']
            pnewList = gnewDict['periodsList']

            # Make sure enough periods
            if index >= len(pnewList):
                return new

            # copy everthing in the new product starting at the
            # end of the last period from the previous group
            fcst += new[last:gbnew]
            oldGrpIndex=-1
            for z in ugcList:
                if z in oldDict:
                    oldGrpIndex=oldDict[z]
                    break
            if oldGrpIndex < 0:
                # Couldn't match zones to previous zone groups, abort
                print("_merge_narrative: Couldn't match zones to previous zone groups, abort")
                return new
            goldDict=oldList[oldGrpIndex]

            # Each period is a tuple of start and end character
            # Positions, period label (i.e., "Monday Night",
            # and then the actual period text
            pbnew, penew, newPerLabel, newPerText=pnewList[index]

            # append text from the start of the group to
            # the end of the last requested period from the
            # new product
            fcst += new[gbnew:pbnew]

            gbold, geold = goldDict['groupText']
            ugcList = goldDict['ugcList']
            poldList = goldDict['periodsList']

            # Attempt to match periods in the old and new products
            # based on the period label. This should account for
            # going from nightime issuance to daytime issuance.
            # If can't match, just use the index as passed in.
            pIndex = index
            if newPerLabel:
                i = index
                while i < len(poldList):
                    pbold, peold, oldPerLabel, oldPerText=poldList[i]
                    if oldPerLabel == newPerLabel:
                        pIndex = i
                        break
                    i += 1
            if pIndex >= len(poldList):
                print("Could not match periods", pIndex, index)
                return new

            # Now copy periods from old product
            #D print "Copying old",index,pIndex
            for pbold, peold, oldPerLabel, oldPerText in poldList[pIndex:]:
                #D print "Updating from old:", oldPerText
                fcst += oldPerText

            # Set up to append from the last period in the new text to the
            # end of the group in the next iteration
            pbnew, penew, newPerLabel, newPerText=pnewList[-1]
            last=penew
        fcst += new[last:]
        # Clean it up
        fcst=fcst.rstrip() + "\n"
        fcst=re.sub(r"\n+\$\$", "\n\n$$", fcst)
        # Check for headline and no forecast. Add an extra blank line to
        # prevent headline locking to the end of the segment
        fcst=re.sub(r"\.\.\.\n\n+\$\$", "...\n\n\n$$", fcst)

        return fcst
    def _mergeGeneric(self,new,old,hdlns=1):
        """Merges previous forecast into current.
        Use this with a any GenericReport product that does not
        have any special sections and the formatter returns
        something like:
          |* text *|
        for the segment text.

        Input arguments:
        new: Product text from the formatter
        old: old product text
        hdlns: Flag 0 or 1 to try to preserve any headlines
        in the new product/filter out headlines in old. If 0,
        all the text from the new is replaced with the old.

        Returns: merged text or the new text if any problems
        encountered.

        Assumptions: Product is a segmented product with one
        or more UGC groupings. Each segment has a line that
        starts with ".text...", each "." is literal "." character.
        This pattern is used as the start of the text to copy.
        The first line containing the ".text..." pattern is
        preserved from the new product. The old product is
        copied starting after the newline ending the .text...
        pattern until the end of the segment. Segments must be
        terminated with "\n\n$$" (i.e. blank line before $$ is
        required).
        Also, if the new contains framing codes, only the first
        encountered set of framing codes in the new is changed;
        it is replaced with the old text (within framing codes).
        """

        # Framing code reg exp
        fc_exp=re.compile(r"\|\* .+? \*\|", re.DOTALL)
        newDict, newList=self._splitSegProd(new)
        oldDict, oldList=self._splitSegProd(old)
##        print("oldDict=",oldDict)
##        print("newDict=",newDict)
        fcst = ""
        last=0
        for gnewDict in newList:

            gbnew, genew = gnewDict['groupText']
            ugcList = gnewDict['ugcList']

            # copy everthing in the new product starting at the
            # end of the last period from the previous group
            fcst += new[last:gbnew]
            oldGrpIndex=-1
            for z in ugcList:
                if z in oldDict:
                    oldGrpIndex=oldDict[z]
                    break
            if oldGrpIndex < 0:
                # Couldn't match zones to previous zone groups
                print("_mergeGeneric: Couldn't match zones to previous zone groups, abort")
                fcst += new[gbnew:genew]
            else:
                goldDict=oldList[oldGrpIndex]
                gbold, geold = goldDict['groupText']
                #D print gnewDict['hdlnText'],gnewDict['fcstText']
                #D print goldDict['hdlnText'],goldDict['fcstText']
                if hdlns == 0:
                    # Completely replace new text with old
                    tnewStart = gnewDict['hdlnText'][0]
                    toldStart = goldDict['hdlnText'][0]
                    fcst += new[gbnew:tnewStart]
                else:
                    # Don't include any previous headlines
                    # but keep any new ones.
                    tnewStart = gnewDict['fcstText'][0]
                    toldStart = goldDict['fcstText'][0]
                    # There are headlines make sure to insert blank line after
                    if gnewDict['hdlnText'][0] < gnewDict['hdlnText'][1]:
                        fcst += new[gbnew:gnewDict['hdlnText'][1]] + "\n\n"
                    else:
                        fcst += new[gbnew:tnewStart]
                #D print "new,old start",tnewStart,toldStart

                newFcst=new[tnewStart:genew]
                oldText=old[toldStart:geold].rstrip()
                #D print "New ",newFcst
                #D print "Old ",oldText
                if fc_exp.search(newFcst) is not None:
                    # Substitute old text for text in framing codes in new
                    fcst += fc_exp.sub("|*\n" + oldText + "\n*|", newFcst, 1)
                else:
                    fcst += old[toldStart:geold]

                # Set up to append from the last period in the new text to the
                # end of the group in the next iteration
            last=genew
        fcst += new[last:]
        # Clean it up
        fcst=fcst.rstrip() + "\n"
        fcst=re.sub(r"\n+\$\$", "\n\n$$", fcst)
        # Check for headline and no forecast. Add an extra blank line to
        # prevent headline locking to the end of the segment
        fcst=re.sub(r"\.\.\.\n\n+\$\$", "...\n\n\n$$", fcst)

        return fcst
    def _mergeOFF1(self, new, old, index):
        return self._mergeNarrative(new, old, index, 1)
    def _mergeOFF2(self, new, old, index):
        return self._mergeNarrative(new, old, index, 17)
    def _mergeZFP(self, new, old, index):
        return self._mergeNarrative(new, old, index, 0)
    def _mergeCWF(self, new, old, index):
        return self._mergeNarrative(new, old, index, 1)
    def _mergeNSH(self, new, old, index):
        return self._mergeNarrative(new, old, index, 0)
    def _mergeESF(self,new,old,hdln=0):
        fcst=self._mergeGeneric(new, old, hdln)
        if fcst != new:
            # Get rid of extra stuff in framing codes from the baseline version of ESF
            fcst=re.sub(r"(?i)\|\* INSERT FORECAST AND NARRATIVE HYDROLOGIC INFORMATION HERE \*\|",
                        "", fcst)
            fcst=re.sub(r"\n+\$\$", "\n\n$$", fcst)
        return fcst
    def _mergeNOW(self,new,old,hdln=1):
        return self._mergeGeneric(new, old, hdln)
    def _mergePNS(self,new,old,hdln=0):
        return self._mergeGeneric(new, old, hdln)
    def _mergeSPS(self,new,old,hdln=0):
        return self._mergeGeneric(new, old, hdln)
    def _mergeRWS(self,new,old,hdln=1):
        return self._mergeGeneric(new, old, hdln)
    def _mergeHWO(self, new, old):
        """Merges previous forecast into current.

        Input arguments:
        new: Product text from the formatter
        old: old product text
        Returns: merged text or the new text if any problems
        encountered.
        Assumptions: Product is a segmented product with one
        or more UGC groupings. Each segment has a line that
        starts with ".text...", each "." is literal "." character.
        This pattern is used as the start of the text to copy.
        The first line containing the ".text..." pattern is
        preserved from the new product. The old product is
        copied starting after the newline ending the .text...
        pattern until the end of the segment. Segments must be
        terminated with "\n\n$$" (i.e. blank line before $$ is
        required)."""

        newDict, newList=self._splitSegProd(new)
        oldDict, oldList=self._splitSegProd(old)
##        print("oldDict=",oldDict)
##        print("newDict=",newDict)
        fcst = ""
        last=0
        index = 0
        for gnewDict in newList:
            gbnew, genew = gnewDict['groupText']
            ugcList = gnewDict['ugcList']
            pnewList = gnewDict['periodsList']

            # Make sure enough periods
            if index >= len(pnewList):
                return new

            # copy everthing in the new product starting at the
            # end of the last period from the previous group
            fcst += new[last:gbnew]
            oldGrpIndex=-1
            for z in ugcList:
                if z in oldDict:
                    oldGrpIndex=oldDict[z]
                    break
            if oldGrpIndex < 0:
                # Couldn't match zones to previous zone groups
                print("_mergeHWO: Couldn't match zones to previous zone groups, abort")
                fcst += new[gbnew:genew]
            else:
                # The first period from a HWO should be the .DAY ONE... line
                # So take the text from the formatter up to the end of
                # .DAY ONE... line
                pbnew, penew, newPerLabel, newPerText=pnewList[0]

                fcst += new[gbnew:penew]

                goldDict=oldList[oldGrpIndex]
                gbold, geold = goldDict['groupText']
                poldList = goldDict['periodsList']

                # Now copy periods from old product
                #D print "Copying old",index,pIndex
                pbold, peold, oldPerLabel, oldPerText = poldList[0]
                oldText = old[peold:geold].strip()

                # Force blank line after first period line
                # with the first '+ "\n"'
                fcst += "\n" + oldText + "\n\n"

                # Set up to append from the last period in the new text to the
                # end of the group in the next iteration
            last=genew
        fcst += new[last:]

        # This section inserts the period labels from the new into the old
        # To attempt to make sure the day names are correct i.e.,
        #    .DAYS TWO THROUGH SEVEN...SATURDAY THROUGH THURSDAY
        # The period labels must be terminated by a blank line (i.e., "\n\n")!
        p1_exp=re.compile(r"(\.DAY ONE\.\.\.[A-Za-z].*?)(?=\n\n)", re.DOTALL|re.IGNORECASE)
        p2_exp=re.compile(r"(\.DAYS TWO THROUGH SEVEN\.\.\.[A-Za-z].*?)(?=\n\n)",
                          re.DOTALL|re.IGNORECASE)
        # Find the Day 1, Days 2 labels in the new product
        m=p1_exp.search(new)
        if m is None:
            return fcst
        p1new=m.group(1)
        m=p2_exp.search(new)
        if m is None:
            return fcst
        p2new=m.group(1)
        # Find the Day 1, Days 2 labels in the old product
        m=p1_exp.search(old)
        if m is None:
            return fcst
        p1old=m.group(1)
        m=p2_exp.search(old)
        if m is None:
            return fcst
        p2old=m.group(1)
        # Now replace the labels from the old with the new
        fcst=re.sub(p1old, p1new, fcst)
        fcst=re.sub(p2old, p2new, fcst)
        # Clean it up
        fcst=fcst.rstrip() + "\n"
        fcst=re.sub(r"\n+\$\$", "\n\n$$", fcst)
        return fcst

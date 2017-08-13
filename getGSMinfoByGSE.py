#-*- coding: utf-8 -*-
#python version 3.4.4
import urllib.request
import time
import re
import os
urlbase='https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc='
# GSE69925 GSE20347 GSE23964 GSE70409 GSE77531 GSE67508 GSE63941 GSE45670
# GSE61587 GSE26886 GSE45168 GSE47404 GSE10127 GSE17351 GSE76860 GSE32424
# GSE29968
GSE='GSE29968' 
GSEfile=GSE+".txt"
outfile=GSE+'_sampleInfo.txt'

done={}
if os.path.exists(outfile):
    print("Reading finished GSMs...")

    outfileH=open(outfile,"r")
    l=outfileH.readline()
    while l:
        tmp=l.split("\t")
        #print(tmp[0])
        done[tmp[2]]=1
        l=outfileH.readline()
    #print(GSM)
    outfileH.close()
    #print(done.keys())
    print("Continue downloading "+GSE+"...")
    outfileH=open(outfile,"a")
else:
    print("Downloading "+GSE+"...")
    outfileH=open(outfile,"a")
    header="title\tGSE\tGSM\tsite\thistology\tsubtype\tcharacteristics\n"
    outfileH.write(header)
n=0
url=urlbase+GSE
GSEpageRaw=urllib.request.urlopen(url).read().decode('utf-8')
GSM_s=GSEpageRaw.find('>GSM',0)+1
GSM_e=GSEpageRaw.find('<',GSM_s)
GSM=GSEpageRaw[GSM_s:GSM_e]
while 1:
    if GSM in done.keys():
        print(GSM+" has been retrieved!")
    else:
        GSMurl=urlbase+GSM
        print("retrieving "+GSMurl)
        GSMPageRaw=urllib.request.urlopen(GSMurl).read().decode('utf-8')
        print(GSM+" retrieved!")
        titl_s=GSMPageRaw.find("<td nowrap>Title</td>\n<td style=\"text-align: justify\">",0)+54
        titl_e=GSMPageRaw.find("</td>",titl_s)
        titl=GSMPageRaw[titl_s:titl_e]
        site_s=GSMPageRaw.find('primary site:',titl_e)+14
        site_e=GSMPageRaw.find('<br>',site_s)
        site=''
        if site_s > titl_e & site_e > site_s: 
            site=GSMPageRaw[site_s:site_e]
        hist_s=GSMPageRaw.find('histology:',titl_e)+11
        hist_e=GSMPageRaw.find('<br>',hist_s)
        hist=''
        if hist_s>titl_e & hist_e>hist_s:
            hist=GSMPageRaw[hist_s:hist_e]
        subT_s=GSMPageRaw.find('histology subtype1:',titl_e)+20
        subT_e=GSMPageRaw.find('<br>',subT_s)
        subT=''
        if subT_s>titl_e & subT_e>subT_s:
            subT=GSMPageRaw[subT_s:subT_e]
        char=GSMPageRaw.find('Characteristics',titl_e)+20
        char_s=GSMPageRaw.find('>',char)+1
        char_e=GSMPageRaw.find('</td>',char_s)
        chara=''
        if char_e>char_s: #char_s>titl_e & 
            chara=GSMPageRaw[char_s:char_e]
            chara=chara.replace('<br>',';')
        outline=titl+"\t"+GSE+"\t"+GSM+"\t"+site+"\t"+hist+"\t"+subT+"\t"+chara+"\n"
        outfileH.write(outline)
        outfileH.flush()
        n+=1
        time.sleep(0.5) # 2 
        if n % 3: time.sleep(1) # 3
    GSM_s=GSEpageRaw.find('>GSM',GSM_e)+1
    if GSM_s < GSM_e: break
    GSM_e=GSEpageRaw.find('<',GSM_s)
    GSM=GSEpageRaw[GSM_s:GSM_e]

##GSEfileH=open(GSEfile,"r")
##l=GSEfileH.readline()
##l.strip("\n")
##l.strip("\r")
##pattern=re.compile(r"GSM\d+")
##while l:
##    GSMp=pattern.search(l)
##    if GSMp != None:
##        GSM=l[GSMp.start():GSMp.end()]
##    else:
##        next
##    if GSM in done.keys():
##        print(GSM+" has been retrieved!")
##    else:
##        GSMurl=urlbase+GSM
##        print("retrieving "+GSMurl)
##        GSMPageRaw=urllib.request.urlopen(GSMurl).read().decode('utf-8')
##        print(GSM+" retrieved!")
##        titl_s=GSMPageRaw.find("<td nowrap>Title</td>\n<td style=\"text-align: justify\">",0)+54
##        titl_e=GSMPageRaw.find("</td>",titl_s)
##        titl=GSMPageRaw[titl_s:titl_e]
##        site_s=GSMPageRaw.find('primary site:',titl_e)+14
##        site_e=GSMPageRaw.find('<br>',site_s)
##        site=GSMPageRaw[site_s:site_e]
##        hist_s=GSMPageRaw.find('histology:',site_e)+11
##        hist_e=GSMPageRaw.find('<br>',hist_s)
##        hist=GSMPageRaw[hist_s:hist_e]
##        #subT_s=GSMPageRaw.find('histology subtype1:',hist_e)+20
##        #subT_e=GSMPageRaw.find('<br>',subT_s)
##        #subT=GSMPageRaw[subT_s:subT_e]
##        subT=''
##        outline=titl+"\t"+GSM+"\t"+site+"\t"+hist+"\t"+subT+"\n"
##        outfileH.write(outline)
##        outfileH.flush()
##        n+=1
##        time.sleep(2)
##        if n % 3: time.sleep(3)
##    l=GSEfileH.readline()
##    l.strip("\n")
##    l.strip("\r")
##outfileH.close() 

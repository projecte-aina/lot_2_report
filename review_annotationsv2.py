#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 12 10:13:01 2023

@author: crodrig1
"""

import json, sys
from collections import Counter
#import jsonl
from termcolor import colored, cprint
import random
from optparse import OptionParser

# file = "../entregas/Lote2-Pilot_annotations_output.json"

# all_anns = json.load(open(file))


def convert(filej):
    annos = filej['annos']
    text = filej['text']
    superannos = []
    for ann in annos:
        start,end = ann['offsets']
        ann['start'] = start
        ann['end'] = end
        cadena = text[start:end]
        ann['mention'] = cadena
        ann['label'] = ann['type']
        superannos.append(ann)
    filej['spans'] = superannos
    z = filej.pop('annos')
    return filej


def counting(tag, nous, mention=None):
    tag_container = []
    for filej in nous:
        if mention:
            etqs = [(x[tag],x['mention']) for x in filej['spans']]
            tag_container = tag_container + etqs
        else:
            etqs = [x[tag] for x in filej['spans']]
            tag_container = tag_container + etqs
    counTag = Counter(tag_container)
    print("Total "+tag+" annotations: ",len(tag_container))
    print(" in ",len(nous)," documents")
    return counTag, len(tag_container)


def countLabel(label, nous):
    tag_container = []
    for filej in nous:
         etqs = [x['mention'] for x in filej['spans'] if (x['label'] == label)]
         tag_container = tag_container + etqs
    counTag = Counter(tag_container)
    print("Total "+label+" annotations: ",len(tag_container))
    print(" in ",len(nous)," documents")
    return counTag

#pol = countLabel('event-political',nous)

def searchEnt(nous,tall=None):
    keyword = input("Which Entity? ")
    while keyword != "":
        ocurr = []
        for filej in nous:
            for x in filej['spans']:
                if x['mention'] == keyword:
                    ocurr.append((x['mention'],x['offsets'],x['label'],filej['text']))
        
        keyw = colored(keyword, "red", "on_yellow", attrs=["bold", "dark"])
        tipus_found = []
        for o in ocurr:
            st = o[1][0]
            en = o[1][-1]
            tipus = colored(o[2], "blue", "on_white", attrs=["bold", "dark"])
            tipus_found.append(o[2])
            if tall:
                if st-tall < 0:
                    s = o[-1][:st]+keyw+o[-1][en:en+tall]
                else:
                    s = o[-1][st-tall:st]+keyw+o[-1][en:en+tall]
                
                print(s)
                print(tipus)
            else:
                s = o[-1][:st]+keyw+o[-1][en:]
                print(s)
                print(tipus)
        print("Ocurrences: ",len(ocurr))
        totipus = Counter(tipus_found)
        print(totipus.most_common(10))
        print("Do you want to search another entity?")
        keyword = input("Which Entity ")
    else:
        print("finished")
                   
def searchQ(nous,tall=None):
    """
    Checking annotation for Qs
    Parameters
    ----------
    nous : list
        DESCRIPTION.
    qcode : string
        DESCRIPTION.

    Returns
    -------
    None.

    """
    qcode = input("Which Q code? ")
    while qcode != "":
        print("For Code ",qcode)
        ocurr = []
        for filej in nous:
            for x in filej['spans']:
                if x['elink'] != None:
                    if x['elink'] == qcode:
                        ocurr.append((x['mention'],x['offsets'],x['label'],filej['text']))
            
        url = colored("https://www.wikidata.org/wiki/"+qcode, "red", "on_yellow", attrs=["bold", "dark"])
        
        tipus_found = []
        for o in ocurr:
            st = o[1][0]
            en = o[1][-1]
            tipus = colored(o[2], "blue", "on_white", attrs=["bold", "dark"])
            keyw = colored(o[0], "black", "on_yellow", attrs=["bold", "dark"])
            tipus_found.append(o[2])
            if tall:
                if st-tall < 0:
                    s = o[-1][:st]+keyw+o[-1][en:en+tall]
                else:
                    s = o[-1][st-tall:st]+keyw+o[-1][en:en+tall]
                
                print(s)
                print(tipus)
            else:
                s = o[-1][:st]+keyw+o[-1][en:]
                print(s)
                print(tipus)
        print(url)
        print("Ocurrences: ",len(ocurr))
        totipus = Counter(tipus_found)
        print(totipus.most_common(10))
        print("Do you want to search another qcode?")
        qcode = input("Which Q code now? ")
    else:
        print("finished")

def searchType(nous,labels,tall=None):
    print("Possible labels:")
    print(labels)
    tipus = input("Which type? ")
    while tipus != "":
        ocurr = []
        for filej in nous:
            for x in filej['spans']:
                if x['label'] == tipus:
                    ocurr.append((x['mention'],x['offsets'],x['label'],filej['text']))   
        tip = colored(tipus, "red", "on_yellow", attrs=["bold", "dark"])
        tipus_found = []
        for o in ocurr:
            st = o[1][0]
            en = o[1][-1]
            #tipus = colored(o[2], "blue", "on_white", attrs=["bold", "dark"])
            mention = colored(o[0], "black", "on_yellow", attrs=["bold", "dark"])
            tipus_found.append(o[2])
            if tall:
                if st-tall < 0:
                    s = o[-1][:st]+mention+o[-1][en:en+tall]
                else:
                    s = o[-1][st-tall:st]+mention+o[-1][en:en+tall]
                
                print(s)
                print(tip)
            else:
                s = o[-1][:st]+mention+o[-1][en:]
                print(s)
                print(tip)
        print("Ocurrences: ",len(ocurr))
        totipus = Counter(tipus_found)
        print(totipus.most_common(10))
        print("Do you want to search anothe type?")
        print("Possible labels:")
        print(labels)
        tipus = input("Which type? ")
    else:
        print("finished")
    
def consistencia(nous):
    ocurrd = {}
    for filej in nous:
        for x in filej['spans']:
            if x['elink'] != None:
                if x['elink'] in ocurrd.keys():
                    conQ = ocurrd[x['elink']]
                    conQ.append(x)
                    ocurrd[x['elink']] = conQ
                else:
                    ocurrd[x['elink']] = [x]
    return ocurrd
    


#searchQ(nous,"Q1333388",50)


def main(argv=None):
    parser = OptionParser()
    parser.add_option("-f", "--filetoprocess", dest="inputfile",  help="input file with annotations",default="../entregas/Lote2-Pilot_annotations_output.json")
    parser.add_option("-r", "--report", dest="report",  help="name for basic stats report and prodigy files",default="report_")
    parser.add_option("-s", "--search", dest="search",  help="Search types, mentions or elinks",default=None)
    options, args = parser.parse_args(argv)
    #print(options)
    all_anns = json.load(open(options.inputfile))
    nous = []
    labels = []
    labels.sort()
    for filej in all_anns:
        etqs = [x['type'] for x in filej['annos']]
        labels = list(set(etqs).union(set(labels)))
        newann = convert(filej)
        nous.append(newann)
        totaldocs = len(nous)
    if options.search:
        print("What do you want to search?\n\n")
        opt = input("(T) Type\n(M) mention\n(Q) Qcode\n(any other) Exit\n")
        if opt.upper() == "M":
            searchEnt(nous,100)
        elif opt.upper() == "Q":
            searchQ(nous,100)
        elif opt.upper() == "T":
            print(labels)
            searchType(nous,labels,100)
        else:
            exit()
    else:
        if options.report:
            empty = []
            for z in nous:
                if z["spans"]  == []:
                    empty.append(z)
            with open(options.report+"_empty_.json","w") as empt:
                json.dump(empty,empt,indent=1,ensure_ascii=False)
            with open("sample_4Prodigy.json","w") as bt:
                json.dump(random.sample(nous,int(int(len(nous))/10)),bt,indent=1,ensure_ascii=False)
            with open("labels.txt","w") as bt:
                for l in labels:
                    bt.write(l+"\n")
            wout = open(options.report+"_report.txt","w")
            wout.write("Report for file: "+options.inputfile+"\n\n")
            import datetime
            dt = datetime.datetime.now()
            wout.write(str(dt)+"\n")
            wout.write("="*16)
            tag = 'label'        
            counTag, totalTags = counting(tag, nous)
            wout.write("\nTotal "+tag+" annotations: "+str(totalTags)+"\n")
            wout.write(" in "+str(len(nous))+" documents\n\n")
            wout.write("\n=============\n")
            wout.write(str(len(empty))+" documents (NOT Annotated)\n\n")
            wout.write("\n50 Most common Anotations\n\n")
            for x in counTag.most_common(50):
                wout.write(x[0]+"\t"+str(x[-1])+"\n")
            wout.write("\n****************\n\n")  
            wout.write("\nLabels and mentions:\n\n")
            counTags, tottags = counting(tag, nous,1)
            for x in counTags.most_common(50):
                wout.write(str(x[0])+"\t"+str(x[-1])+"\n")
            wout.write("\n\nLabelling inconsistencies:\n")
            ocurrd = consistencia(nous)
            #print("Total of different Q codes: ",len(ocurrd.keys())+"\n")
            wout.write("\nTotal of different Q codes: "+str(len(ocurrd.keys()))+"\n")
            for q in ocurrd.copy().keys():
                if len(ocurrd[q]) == 1:
                    ocurrd.pop(q)
            #print("Q codes with more than one annotation: ",len(ocurrd.keys())+"\n")
            wout.write("\nQ codes with more than one annotation: "+str(len(ocurrd.keys()))+"\n\n")
            n = 0
            for q in ocurrd:
                qgroup = ocurrd[q]
                alltypes = [x['label'] for x in qgroup]
                if len(set(alltypes)) == 1:
                    pass
                else:
                    n += 1
                    wout.write(str(q)+" \t"+str(set(alltypes))+"\n")
            wout.write("\n\nInconsistent Qs vs. types: "+str(n)+"\n")
            wout.close()


                    
if __name__ == "__main__":
  sys.exit(main())

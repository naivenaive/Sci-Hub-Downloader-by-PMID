# -*- coding: utf-8 -*-
"""
Created on Wed Mar  4 19:06:00 2020

@author: Naive
"""
from __future__ import print_function
import requests
import xml.etree.ElementTree as ET
import sys
import calendar
import argparse
import os
from bs4 import BeautifulSoup as bs

def pmid_to_bibtex(pmids,_try=3):
    #modify from "https://gist.github.com/tommycarstensen/ec3c57761f3846c339de925b66f4ac1b"
    #add doi and fix some bugs
    output=""
    dic={}
    ## Fetch XML data from Entrez.
    efetch = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi'
    for i in range(_try):
        try:
            if i==0: print("Try {} time".format(i+1))
            r = requests.get(
        '{}?db=pubmed&id={}&rettype=abstract'.format(efetch, ','.join(pmids)),timeout=(3.1,7))
        except:
            if i==_try-1: 
                print("Fail in getting DOI from PUBMED.\n")
                return dic, output
            print("Try {} times".format(i+2))
            continue
        else: 
            break
    ##print(r.text)
    
    ## Loop over the PubMed IDs and parse the XML.
    root = ET.fromstring(r.text)
    for PubmedArticle in root.iter('PubmedArticle'):
        PMID = PubmedArticle.find('./MedlineCitation/PMID')
        #ISSN = PubmedArticle.find('./MedlineCitation/Article/Journal/ISSN')
        Volume = PubmedArticle.find('./MedlineCitation/Article/Journal/JournalIssue/Volume')
        Issue = PubmedArticle.find('./MedlineCitation/Article/Journal/JournalIssue/Issue')
        Year = PubmedArticle.find('./MedlineCitation/Article/Journal/JournalIssue/PubDate/Year')
        Month = PubmedArticle.find('./MedlineCitation/Article/Journal/JournalIssue/PubDate/Month')
    ##    Year = PubmedArticle.find('./MedlineCitation/Article/ArticleDate/Year')
    ##    Month = PubmedArticle.find('./MedlineCitation/Article/ArticleDate/Month')
        Title = PubmedArticle.find('./MedlineCitation/Article/Journal/ISOAbbreviation')
        ArticleTitle = PubmedArticle.find('./MedlineCitation/Article/ArticleTitle')
        MedlinePgn = PubmedArticle.find('./MedlineCitation/Article/Pagination/MedlinePgn')
        Abstract = PubmedArticle.find('./MedlineCitation/Article/Abstract/AbstractText')
        doi = PubmedArticle.find("./MedlineCitation/Article/ELocationID[@EIdType='doi']")
        authors = []
        for Author in PubmedArticle.iter('Author'):
            try:
                LastName = Author.find('LastName').text
                ForeName = Author.find('ForeName').text
            except AttributeError:  # e.g. CollectiveName
                continue
            authors.append('{}, {}'.format(LastName, ForeName))
        ## Use InvestigatorList instead of AuthorList
        if len(authors) == 0:
            ## './MedlineCitation/Article/Journal/InvestigatorList'
            for Investigator in PubmedArticle.iter('Investigator'):
                try:
                    LastName = Investigator.find('LastName').text
                    ForeName = Investigator.find('ForeName').text
                except AttributeError:  # e.g. CollectiveName
                    continue
                authors.append('{}, {}'.format(LastName, ForeName))
        if len(authors) == 0:
            authors =["no_authors_listed"]
        if Year is None:
            _ = PubmedArticle.find('./MedlineCitation/Article/Journal/JournalIssue/PubDate/MedlineDate')
            Year = _.text[:4]
            Month = '{:02d}'.format(list(calendar.month_abbr).index(_.text[5:8]))
        else:
            Year = Year.text
            if Month is not None:
                Month = Month.text
        try:
            for _ in (PMID.text, Volume.text, Title.text, ArticleTitle.text, MedlinePgn.text, Abstract.text, ''.join(authors)):
        ##        assert '"' not in _, _
                if _ is None:
                    continue
                assert '{' not in _, _
                assert '}' not in _, _
        except AttributeError:
            pass
        ## Save the bibtex formatted output.
        try:
            output+=('\n@Article{{pmid{}_{}_{},\n'.format(
                PMID.text, authors[0].split(',')[0], Year))
        except IndexError:
            print('IndexError', pmids, file=sys.stderr, flush=True)
        except AttributeError:
            print('AttributeError', pmids, file=sys.stderr, flush=True)
        output+=(' Author="{}",\n'.format(' AND '.join(authors)))
        output+=(' Title={{{}}},\n'.format(ArticleTitle.text))
        output+=(' Journal={{{}}},\n'.format(Title.text))
        output+=(' Year={{{}}},\n'.format(Year))
        if Volume is not None:
            output+=(' Volume={{{}}},\n'.format(Volume.text))
        if Issue is not None:
            output+=(' Number={{{}}},\n'.format(Issue.text))
        if MedlinePgn is not None:
            output+=(' Pages={{{}}},\n'.format(MedlinePgn.text))
        if Month is not None:
            output+=(' Month={{{}}},\n'.format(Month))
        if doi is not None:
            output+=(' doi={{{}}},\n'.format(doi.text))
        output+=('}\n')
        
        
        _dic={}
        _dic["PMID"]=PMID.text if PMID is not None else ""
        _dic["authors"]=authors
        _dic["ArticleTitle"]=ArticleTitle.text if ArticleTitle is not None else ""
        _dic["JournalTitle"]=Title.text if Title is not None else ""
        _dic["Year"]=Year
        _dic["Volume"]=Volume.text if Volume is not None else ""
        _dic["Issue"]=Issue.text if Issue is not None else ""
        _dic["MedlinePgn"]=MedlinePgn.text if MedlinePgn is not None else ""
        _dic["Month"]=Month
        _dic["doi"]= doi.text if doi is not None else ""
        _dic["bibtex"]= "pmid"+_dic["PMID"]+"_"+_dic["authors"][0].split(',')[0]+\
                        "_"+ Year
        dic[PMID.text]=_dic
    print(output)
    return dic, output


# Extract Mirror
def get_links(target,_try=3):
    # Get response of target page
    # from Sci-Hub and create soup object
    print("Extracting download links...")
    for i in range(_try):
        try:
            if i==0: print("Try {} time".format(i+1))
            response = requests.get(target,timeout=(3.1,7))
        except:
            if i==_try-1: 
                print("Fail in getting DOI from PUBMED.\n")
                return ""
            print("Try {} times".format(i+2))
            continue
        else: 
            break
    
    soup = bs(response.content, "lxml")
    # Extract DOI
    try:
        mirror = soup.find("iframe", attrs={"id": "pdf"})['src'].split("#")[0]
        if mirror.startswith('//'):
            mirror = mirror[2:]
            mirror = 'https://' + mirror
        print("Sci-Hub URL: {}".format(mirror))
    except Exception:
        print("Mirror not found")
        mirror = ""
    # Extract download link
    return mirror


# Download paper
def download_paper(mirror, _dir, _try=3):
    # Response from mirror link, if return 0, failed
    print("Sending request")
    for i in range(_try):
        try:
            if i==0: print("Try {} time".format(i+1))
            response = requests.get(mirror,timeout=(3.1,7))
        except:
            if i==_try-1: 
                print("Fail in getting PDF.\n")
                return 0
            print("Try {} times".format(i+2))
            continue
        else: 
            break
    print("Response received")
    # If header states PDF then write to _dir
    if response.headers['content-type'] == "application/pdf":
        size = round(int(response.headers['Content-Length'])/1000000, 2)
        print("Downloaded {} MB".format(size))
        with open(_dir, "wb") as f:
            f.write(response.content)
        f.close()
        print("Save in {}\n".format(_dir))
    else:
        print("Fail in getting PDF.")
        return(0)
    # Check if firefox exists and open download link
    # in firefox
#    elif re.match("text/html", response.headers['content-type']):
#        print("Looks like captcha encountered.")
#        print("Download link is \n" + mirror + "\n")
#        time.sleep(2)
#        wbb.open_new(mirror) 




if __name__ == "__main__":
    #define command line arguments
    parser = argparse.ArgumentParser(description="Sci-Hub downloader: \
                                     Download PDFs from Sci-Hub using PMIDs")
    parser.add_argument('-p','--pmids', nargs='+',help="Provide multiple PMIDs like -p/--pmids 31014115 30293440...")
    parser.add_argument('-f','--file', help="Provide .txt file with PMIDs, one PMID in each line")
    parser.add_argument('-d','--download_dir',default="", help="Path for saving downloaded BIBTEX file and PDFs, \
                        defaultly save in DESKTOP/Sci_Hub_Download")
    parser.add_argument('-s','--sci_hub',default="https://sci-hub.tw/",help="Site for Sci-hub to get PDF source,\
                        dafault is https://sci-hub.tw/")
    parser.add_argument('-t','--try_times', type=int, default=3, help="Times for trying to connect with Sci-hub server,\
                        default is 3")
    parser.add_argument('-n','--number', default=False, action='store_true',help="T/F, if set True, the PDF file name will\
                        be named like '008_pmid30293440_Tian_2019', by default the PDF name is 'pmid30293440_Tian_2019'")
    args = parser.parse_args()
    
    #args.pmids=["31014115","30293440"]
    #set combine file pmids with pmids
    if args.file:
        file_pmids = [line.rstrip('\n') for line in open(args.file)]
    else:
        file_pmids=[]
    args.pmids = file_pmids+ args.pmids
    #analyze pmids and obtain bibtex
    print("Analyzing DOI...")
    bibs, output =pmid_to_bibtex(args.pmids,args.try_times)
    print("DOI analyse finished")
    #set ouput directory
    if args.download_dir == "":
        default_dir= os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
        download_dir = os.path.join(default_dir, "Sci_Hub_Download")
    else:
        download_dir = args.download_dir
    if not os.path.exists(download_dir): os.mkdir(download_dir)
    #save bibtex file
    with open(os.path.join(download_dir,"bibtex.txt"), "w", encoding='utf-8') as text_file:
        text_file.write(output)
    text_file.close()
    print("Save Bibtex in {}\n".format(os.path.join(download_dir,"bibtex.txt")))
    #set diffrence for bibtex file and pmids input
    pmid_get=[]
    [pmid_get.append(bib["PMID"]) for bib in bibs.values()]
    _diff = list(set(args.pmids) - set(pmid_get))
    #suppress error for bibs[pmid]["doi"]
    for name in _diff:
        bibs[name] = {"doi":""} 
    #get sci-hub website
    sci_hub = args.sci_hub
    #initiate
    i=1; fail=[]
    file_names = next(os.walk(download_dir))[2]
    for pmid in args.pmids:
        #bibtex can't find or doi not exist in bibtex,save pmid to fail
        if bibs[pmid]["doi"]!="":
            url = sci_hub + bibs[pmid]["doi"]
        else:
            print("Can't find doi for PMID: {}\n".format(pmid))
            fail.append(pmid)
            i+=1
            continue
        #set pdf name
        if args.number:
            pdf_name = "%03d_"%i+bibs[pmid]["bibtex"]+".pdf"
        else:
            pdf_name = bibs[pmid]["bibtex"]+".pdf"
        #set pdf saving directory
        _dir=os.path.join(download_dir,pdf_name)
        #if file already exists, do not download
        if pdf_name in file_names:
            print("{} already exists for PMID: {}\n".format(pdf_name,pmid))
            i+=1
            continue
        #get pdf url mirror
        mirror = get_links(url,args.try_times)
        #if mirror not found, if fail in saving pdf add pmid to fail
        if not mirror:
            print("Sci-Hub URL not available for PMID: {}\n".format(pmid))
            fail.append(pmid)
        else:
            print("Downloading paper with PMID: {}".format(pmid))
            tag = download_paper(mirror, _dir, _try=args.try_times)
            if tag==0: fail.append(pmid)
        i+=1
    #set log and save
    log = "Request PMID:\n  {}\n".format(" ".join(args.pmids))
    log+= "Succeed in obtaining Bibtex of PMID:\n  {}\n".format(" ".join(pmid_get))
    if len(_diff)!=0: 
        log+="Fail in obtaining Bibtex of PMID:\n  {}\n".format(" ".join(_diff[::-1]))
    log+= "Succeed in obtaining PDF of PMID:\n  {}\n".format(" ".join(list(set(args.pmids) - set(fail))[::-1]))
    if len(fail)!=0: 
        log+="Fail in downloading PDF of PMID:\n  {}\n".format(" ".join(fail))
    with open(os.path.join(download_dir,"log.txt"), "w", encoding='utf-8') as text_file:
        text_file.write(log)
    text_file.close()
    print(log)
    print("Save log in {}\n".format(os.path.join(download_dir,"log.txt")))
    print("Finished.")
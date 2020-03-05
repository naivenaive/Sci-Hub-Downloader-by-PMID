# Sci-Hub Downloader by PMID

## Disclaimer

This application is for educational purpose only. I do not take responsibility of what you choose to do with this application.


## About

*Sci-Hub downloader by PMID* is a command line wrapper of Sci-Hub written in Python. *Sci-Hub downloader by PMID*  first convert PMID into Bibtex and obtain the corresponding doi. Then, the doi is combined with Sci-Hub address to fetch the article in PDF format. You can use the script to download research articles from your terminal itself by providing PMID.  

Hope you find it useful.

## Installation


This application is designed to run on Windows machines. Please refer requirements.txt file and manually install the mentioned dependencies. 

```md
pip3 install requests beautifulsoup4 xml
```
If you are using a Linux system, you may need to modify the script.

## Usage

After ensuring everything is set, fire up sci_hub_downloader.py

```md
$ python sci_hub_downloader.py -h

usage: sci_hub_downloader.py [-h] [-p PMIDS [PMIDS ...]] [-f FILE]
                             [-d DOWNLOAD_DIR] [-s SCI_HUB] [-t TRY_TIMES]
                             [-n]

Sci-Hub downloader: Download PDFs from Sci-Hub using PMIDs

optional arguments:
  -h, --help            show this help message and exit
  -p PMIDS [PMIDS ...], --pmids PMIDS [PMIDS ...]
                        Provide multiple PMIDs like -p/--pmids 31014115
                        30293440...
  -f FILE, --file FILE  Provide .txt file with PMIDs, one PMID in each line
  -d DOWNLOAD_DIR, --download_dir DOWNLOAD_DIR
                        Path for saving downloaded BIBTEX file and PDFs,
                        defaultly save in DESKTOP/Sci_Hub_Download
  -s SCI_HUB, --sci_hub SCI_HUB
                        Site for Sci-hub to get PDF source, default is
                        https://sci-hub.tw/
  -t TRY_TIMES, --try_times TRY_TIMES
                        Total retrying times to connect with web server,
                        default is 3
  -n, --number          T/F, if set True, the PDF file name will be named like
                        '008_pmid30293440_Tian_2019', by default the PDF name
                        is 'pmid30293440_Tian_2019'
```
### -h
This flag displays help message.

### -p/--pmids
This is the PMID（NOT PMCID） of the paper to be downloaded. Multiple PMIDs are supported as shown below.

Example usage
```md
$ python sci_hub——downloader.py -p 31014115
$ python sci_hub——downloader.py --pmids 31014115 
$ python sci_hub——downloader.py -p 31014115 30293440
$ python sci_hub——downloader.py --pmids 31014115 30293440
```
### -f/--file
This optional flag specifies the script to read a .txt file with each PMID in each line. A sampled file named "sample_pmids.txt" is  provided in the repository. The content is shown below.

### -d/--download_dir
This flag specifies the directory for saving corresponding BIBTEX  and PDFs. By default, the PDF files downloaded are saved in 'DESKTOP/Sci_Hub_Download'

### -s/--sci_hub
This flag specifies the site for Sci-hub to get PDF source, default is https://sci-hub.tw/. You can specify the Sci-Hub source as
```md
$ python sci_hub——downloader.py -p 31014115 -s htttps://sci-hub.io/
```
### -t/--try_times
For each request , the script will retry for a total of ```try_times ``` times.  The default is 3.

### -n/--number
 This flag is a boolean. By default the PDF name is  'pmid30293440_Tian_2019'.  If set True, the PDF file name will be named like '008_pmid30293440_Tian_2019'.  It can be set True as following:
 ```md
$ python sci_hub——downloader.py -p 31014115 -n 
 ```

### Download/storage
The script first convert the PMIDs to BIBTEX format. The Bibtex format references will be printed in the console and saved in the download directory name "bibtex.txt". 

Then, the script will download the articles, the details are presented in the console.  After downloading articles, a brief log is printed in the console and a file named "log.txt" is saved in the download directory.

Here is a sample command:
```md
$ python sci_hub_downloader.py -p 31014115 abcd 30293440 123
$ python sci_hub_downloader.py -f  sample_pmids.txt
```
The output is presented as following:
```
Analyzing DOI...
Try 1 time

@Article{pmid31014115_Huang_2019,
 Author="Huang, Yu-Yuan AND Qian, Shu-Xia AND Guan, Qiao-Bing AND Chen, Ke-Liang AND Zhao, Qian-Hua AND Lu, Jia-Hong AND Guo, Qi-Hao",
 Title={Comparative study of two Chinese versions of Montreal Cognitive Assessment for Screening of Mild Cognitive Impairment.},
 Journal={Appl Neuropsychol Adult},
 Year={2019},
 Pages={1-6},
 Month={Apr},
 doi={10.1080/23279095.2019.1602530},
}

@Article{pmid30293440_Tian_2019,
 Author="Tian, Zhen AND Huang, Yike AND Yue, Tao AND Zhou, Jiaqing AND Tao, Lu AND Han, Ling AND Yan, Kexiang AND Huang, Qiong AND Zhang, Zhenghua AND Shao, Chunhong",
 Title={A Chinese cross-sectional study on depression and anxiety symptoms in patients with psoriasis vulgaris.},
 Journal={Psychol Health Med},
 Year={2019},
 Volume={24},
 Number={3},
 Pages={269-280},
 Month={03},
 doi={10.1080/13548506.2018.1529323},
}

@Article{pmid123_Keighley_1975,
 Author="Keighley, M R AND Asquith, P AND Edwards, J A AND Alexander-Williams, J",
 Title={The importance of an innervated and intact antrum and pylorus in preventing postoperative duodenogastric reflux and gastritis.},
 Journal={Br J Surg},
 Year={1975},
 Volume={62},
 Number={10},
 Pages={845-9},
 Month={Oct},
}

DOI analyse finished
Save Bibtex in .\Desktop\Sci_Hub_Download\bibtex.txt

Extracting download links...
Try 1 time
Sci-Hub URL: https://dacemirror.sci-hub.tw/journal-article/2bccd4844862193168c2c00ef8011a30/huang2019.pdf
Downloading paper with PMID: 31014115
Sending request
Try 1 time
Response received
Downloaded 0.72 MB
Save in
.\Desktop\Sci_Hub_Download\pmid31014115_Huang_2019.pdf

Can't find doi for PMID: abcd

Extracting download links...
Try 1 time
Sci-Hub URL: https://cyber.sci-hub.tw/MTAuMTA4MC8xMzU0ODUwNi4yMDE4LjE1MjkzMjM=/tian2018.pdf
Downloading paper with PMID: 30293440
Sending request
Try 1 time
Response received
Downloaded 1.27 MB
Save in .\Desktop\Sci_Hub_Download\pmid30293440_Tian_2019.pdf

Can't find doi for PMID: 123

Request PMID:
  31014115 abcd 30293440 123
Succeed in obtaining Bibtex of PMID:
  31014115 30293440 123
Fail in obtaining Bibtex of PMID:
  abcd
Succeed in obtaining PDF of PMID:
  30293440 31014115
Fail in downloading PDF of PMID:
  abcd 123

Save log in .\Desktop\Sci_Hub_Download\log.txt

Finished.
```
## Known issues
During developing and testing the script,  the console gives an error message: Can't connect to HTTPS URL because the SSL module is not available.  Here is a solution: [https://github.com/conda/conda/issues/8273](https://github.com/conda/conda/issues/8273)

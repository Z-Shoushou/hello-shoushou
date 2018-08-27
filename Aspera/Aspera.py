"""
Usage:
    Aspera.py [-vrh] (-nProject_number>|-f<Project_file>) -t<File_type>

Arguments:
    Project_number      Required input project number
    Project_file        Required project numbers file
    File_type           Required input file type

Options:
    -h --help           show this
    -v                  verbose mode
    -q, --quite Sel     quite mode
    -r                  make report
    -n <Project_number>,--number <Project_number>        project number
    -f <Project_file>,--file <Project_file>              project number file
    -t <File_type>,--type <File_type>                     project file type

Example
    Aspera.py -v -n PXD003452 -t REQUEST
    Aspera.py -f test.txt -t REASULT,OTHER
"""

from docopt import docopt
import requests
import json as js
import os

parameter = r"ascp -QT -l 500m -P33001 -i C:/Users/Shoushou/ssh.ssh/asperaweb_id_dsa.openssh "
Store_address = "C:/Users/Shoushou/biostar/aspera/"
DownloadLink = []
cmd = []

def project_judge(arguments):
    project_number = arguments['--number']
    project_file = arguments['--file']
    if type(project_number) == type("abc"):
        number_download(project_number)
    else :
        file_download(project_file)

def number_handling (project_number) :
    # Handling the url when only got one project number.
    url = 'https://www.ebi.ac.uk/pride/ws/archive/file/list/project/' + str(project_number)
    return url

def number_download(project_number):
    url = number_handling(project_number)
    DownloadLink = get_link(url)
    cmd = tansform(DownloadLink)
    command_download(cmd)

def file_handling (project_file):
    # Handling the url when got a project number file
    project_list = []
    with open(project_file) as f:
        for line in f:
            list = line.split(',')
            for i in range(len(list)):
                url = 'https://www.ebi.ac.uk/pride/ws/archive/file/list/project/' + str(list[i])
                project_list.append(url)
    return project_list

def file_download(project_file) :
    urls = file_handling(project_file)
    for i in range(len(urls)):
        print("Beginning download the project " + urls[i][-9:] + " file.")
        DownloadLink = get_link(urls[i])
        cmd = tansform(DownloadLink)
        command_download(cmd)
        print ("Project " + urls[i][-9:] + " download has been finished.")

def get_link (url):
    # From the project number the user input get the download link.
    print('Handing web data and get the download link...')
    wbdata = js.loads(requests.get(url).text)
    data_1 = wbdata["list"]
    for i in range(len(data_1)) :
        type = data_1[i]['fileType']
        if type in file_type :
            DownloadLink.append(data_1[i]['asperaDownloadLink'])
    print("Web data ande download link have been handed.")
    return DownloadLink

def tansform (DownloadLink):
    # Transform the link into windows cmd commend.
    print ("Getting the download command prompt...")
    for i in range(len(DownloadLink)):
        combine = parameter + DownloadLink[i] + " " + Store_address
        cmd.append(combine)
    print ("The download command prompt has been finished.")
    return cmd

def command_download (cmd) :
    for i in range(len(cmd)) :
        print (cmd[i])
        os.system(cmd[i])

if __name__ == '__main__':
    arguments = docopt(__doc__)
    file_type = arguments['--type']
    project_judge(arguments)
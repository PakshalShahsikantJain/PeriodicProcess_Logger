##################################################################################################################
##
##  Author : Pakshal Shahikant Jain 
##  Date : 09/05/2021
##  Program : Automated Scipt To Display Current Running Process Of Machine At Time Interval of 1 Min and Sending Log
##            file to mentioned email adderess
##
##################################################################################################################
import os
import time
import psutil
from sys import *
import schedule
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

i = 0

def ProcessDisplay(FolderName = "Marvellous") :
    Data = [] 
    global i 

    if not os.path.exists(FolderName) :
        os.mkdir(FolderName)
    
    File_Path = os.path.join(FolderName,"Marvellous%s.txt"%i)
    i = i + 1
    fd = open(File_Path,"w")

    for proc in psutil.process_iter() :
        value = proc.as_dict(attrs = ['pid','name','username'])
        Data.append(value)

    for element in Data :
        fd.write("%s\n"% element)

    EMAIL_ADDRESS = "thechainsmokers78@gmail.com"
    EMAIL_PASSWORD = "xmhyfrbiublwkvqy"
    sentTo =  "pakshal1256@gmail.com"
    subject = "Log File of Current Processes Running in System";
    message = "This Mail Contains Report of Current Running Processes in System";

    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = sentTo
    msg['Subject'] = subject
    msg['Message'] = message

    filename = os.path.basename(File_Path)
    fd = open((File_Path),'rb')
    part = MIMEBase('application','octet-stream')
    part.set_payload((fd).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition',"attachment; filename= %s"%filename)

    msg.attach(part);
    msg.attach(MIMEText(message))

    server = smtplib.SMTP_SSL('smtp.gmail.com',465)
    server.login(EMAIL_ADDRESS,EMAIL_PASSWORD)
    text = msg.as_string()
    server.sendmail(EMAIL_ADDRESS,sentTo,text)
    server.quit()

def main() :
    print("--------------Marvellous Infosystems----------------------")
    print("Script Title :" + argv[0])

    if argv[1] == '-u' or argv[1] == '-U' :
        print("Usage : Application_Name Schedule_Time Directory_Name");
        exit();

    if argv[1] == '-h' or argv[1] == '-H' :
        print("Help : It is used to create log file of Running Processes");
        exit();

    schedule.every(int(argv[1])).minutes.do(ProcessDisplay);

    while True :
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__" :
    main()

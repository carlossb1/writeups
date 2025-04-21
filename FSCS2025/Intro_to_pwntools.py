# Introductory CTF challenge demonstrating basic pwntools functionality
# While solvable manually via netcat, the challenge encourages the participants
# to solve it using code as a way to practice Python exploitation skills

from pwn import *
from termcolor import cprint

connect = remote('chall.fcsc.fr', 2053)

# Receive and print initial messages
print(connect.recvline())
print(connect.recvline())

# Send the string asked from the server after connection
connect.sendlineafter(b'>>>', 'Go!'.encode())

# Receive more lines, as well as the one containing the number that we need to perform an operation
resp = connect.recvlines(4)

# Extract first number from server response
number1 = resp[2].split(b':')[1].split()[1].decode()

# Search for the challenge delimiter line - Here you can use the recvuntil() function from pwntools to achieve the same results
line_found = ''
while not line_found:
    response = connect.recvline()
    if b'===' in response:  # Look for the challenge separator marker
        line_found += response.decode()
        print(f'[MARK FOUND] {line_found}')
        break
    else:
        print(f'[DEBUG] - RECEIVED LINE: {response}')
        continue

# Extract second number from the challenge
number2 = connect.recvline().split()[-1].decode()

# Calculate solution by summing both numbers
result = int(number1) + int(number2)

# Submit the calculated result when prompt appears
connect.sendlineafter(b'>>>', str(result).encode())

cprint('[+] SENDING PAYLOAD', 'blue')

# Retrieve and display the flag from server response
cprint(f'[!] FLAG RETRIEVED: {connect.recvlines(2)[1]}', 'green')

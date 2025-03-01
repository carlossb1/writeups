# Room - CapstoneChallenge - TryHackMe 
Autor: carlossb1\
Level: Medium\
Tópico: Linux Privilege Escalation


## Introdução

Essa room está disponível no fim do módulo sobre escalação de privilégios no Linux.\
Recebemos um usuário e senha para realizar login via SSH na máquina.

User: leonard\
Password: Penny123 (lol)

## Enumeração

Conexão via SSH com as credenciais fornecidas

![Img1](https://github.com/user-attachments/assets/6390b8d6-bd0e-4a32-89eb-7104832f4554)

o `ls -la` nos fornece alguns arquivos interessantes - vamos olhar o .bash_history:

![Img2](https://github.com/user-attachments/assets/4290b99e-632d-4ea2-9e64-abea3dd6c448)

Podemos ver que no histórico constam alguns comandos que nos trazem as seguintes informações: existem outros dois usuários (nissy e root), e a flag2 está no diretório 'root_flag'. Vamos guardar essas informações e seguir buscando algum vetor de ataque.

Procurando arquivos executáveis:
`find / -perms a=x 2>/dev/null`

Procurando arquivos com SUID habilitado:
`find / -perms -u=s 2>/dev/null`

![Img3](https://github.com/user-attachments/assets/133fe08d-ee67-43cc-a750-b7622e98ca75)

Vemos alguns binários com SUID habilitado, que pode ser um vetor de ataque interessante. Consultando o [GTFIOBINS](https://gtfobins.github.io/gtfobins/base64/) vemos que o binário Base64, quando possui o SUID habilitado, permite que o usuário consiga burlar as restrições de permissão e ler arquivos mesmo sem ter o nível de privilégio necessário.


## Exploração

### Truque
Sabendo que a flag2 está no diretório root_flag, podemos usar o payload `LFILE=/home/root_flag/flag2.txt ; base64 "$LFILE" | base64 --decode` e ler o conteúdo do arquivo:

![WhatsApp Image 2025-03-01 at 15 04 37](https://github.com/user-attachments/assets/81b836f4-6265-4a27-b6c6-13ab40722e26)

Encontramos a flag2.

### Escalação de privilégio

Como esse é o objetivo da room, vamos seguir realizando a escalação de privilégios. Uma das formas de atingir esse objetivo, agora que sabemos que podemos ler arquivos retritos, é obtendo as hashes das senhas dos usuários.

### Obtenção das hashes

Passwd:
`LFILE=/etc/passwd ; base64 "$LFILE" | base64 --decode`

Shadow:
`LFILE=/etc/shadow ; base64 "$LFILE" | base64 --decode`

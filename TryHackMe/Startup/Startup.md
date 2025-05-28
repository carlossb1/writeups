# Room - CapstoneChallenge - TryHackMe 
Autor: carlossb1\
Level: Easy\
Tópico: Web / Linux


## Introdução

Essa room é bem simples, envolvendo transferência de arquivos via FTP para um diretório que está hospedando um servidor com backend em PHP, obtendo execução de código remoto e assim conseguindo acesso ao webserver.

A parte de escalação de privilégio também é um cenário simples, vemos alguns arquivos suspeitos, e através da análise conseguimos obter a senha de um usuário, e depois de autenticados como esse usuário, abusar de um cronjob com permissões de root que faz chamadas à um script externo.

## Enumeração

nmap -sC -sV para rodar os scripts padrão e retornar as informações de versão dos serviços em execução

Algumas informações interessantes: o servidor FTP permite login com o usuário Anonymous, e o nmap já foi capaz de retornar os arquivos disponíveis no diretório.

![image](https://github.com/user-attachments/assets/e0877fcb-f129-4dbc-889b-115af3c0247c)


Portas abertas: 21,22 e 80.

### Porta 80:
Uma página web sem nada de interessante no primeiro momento.

![image](https://github.com/user-attachments/assets/360e0625-8a39-4121-ab20-0ed0d18f180b)

Realizando uma varredura por diretórios, encontramos 
![image](https://github.com/user-attachments/assets/8d248236-f4f5-4a4f-ab3d-f92c2eba6f03)


![image](https://github.com/user-attachments/assets/397e98d9-a956-4a96-b50c-df2ca2a71a4d)




### Porta 21
Vamos ver o que temos no ftp

![image](https://github.com/user-attachments/assets/1cfb29bf-c860-4890-b7d4-b8d4a8093265)



## Exploração
Sabendo que os conteúdos acessíveis via FTP estão sendo refletidos no webserver, podemos criar um PoC e enviá-lo via FTP para o servidor e fazer o teste de execução de código remoto.

![image](https://github.com/user-attachments/assets/880c8149-2609-4d14-842f-a8da1814e0d8)

Nosso arquivo aparece

![image](https://github.com/user-attachments/assets/5cbfa196-72b4-474d-88cf-148e0ccf4a48)


Ao acessá-lo, vemos que nosso código foi executado, retornando a mensagem "Hello, world" conforme esperado. Agora podemos repetir esse passo, mas dessa vez utilizando o código de um shell reverso.


![image](https://github.com/user-attachments/assets/9ac82ef2-c709-4fa0-b2a9-22e2a3de2793)


Utilizei o código do PentestMonkey [https://github.com/pentestmonkey/php-reverse-shell] 

![image](https://github.com/user-attachments/assets/7f56b233-cf51-4cb6-9692-55226fb5be58)

Agora basta iniciar nosso listener no netcat para receber a shell na mesma porta especificada no código anterior.

Acessando o arquivo, recebemos nossa shell reversa.

![image](https://github.com/user-attachments/assets/dbbf0b9c-645c-4af7-bb27-c518dbffca7b)



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

Realizando uma varredura por diretórios, encontramos o diretório /files.

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


Ao acessá-lo, vemos que nosso código foi executado, retornando a mensagem "Hello, world" conforme esperado.


![image](https://github.com/user-attachments/assets/9ac82ef2-c709-4fa0-b2a9-22e2a3de2793)


Agora podemos repetir esse passo, mas dessa vez utilizando o código de um shell reverso.

Utilizei o código do PentestMonkey [https://github.com/pentestmonkey/php-reverse-shell] 

![image](https://github.com/user-attachments/assets/7f56b233-cf51-4cb6-9692-55226fb5be58)

Agora basta iniciar nosso listener no netcat para receber a shell na mesma porta especificada no código anterior.

Acessando o arquivo, recebemos nossa shell reversa.

![image](https://github.com/user-attachments/assets/dbbf0b9c-645c-4af7-bb27-c518dbffca7b)

Após uma estabilização básica inicial, enumeramos o diretório e vemos que nosso usário é dono de uma pasta -incidents- e um arquivo -recipe.txt- contendo o ingrediente especial que é: .... (1ª flag).

![image](https://github.com/user-attachments/assets/9225b84e-028d-4630-9e1f-f2d610ea1ab7)

## Obtendo user

Vamos ver o que tem dentro da pasta incidents:

Um arquivo pcapng - esse tipo de arquivo contém informações de capturas de tráfego de rede, então preferi transferir para minha máquina local para analisar mais facilmente.

![image](https://github.com/user-attachments/assets/672c85f1-79fc-4dac-aae6-b3e4301022b3)


Utilizando a ferramente de preferência (wireshark, tcpdump, tshark), podemos visualizar as informações de conexão armazenadas no arquivo pcapng. Utilizando o tcpdump podemos ver que algumas dessas transmissões de dados foram realizadas por protocolos não-criptografados, o que revela a senha de um dos usuários em texto claro.

Abertura do arquivo

![image](https://github.com/user-attachments/assets/385d489c-62a6-4f7c-bdc0-9019e47b5fd7)


![image](https://github.com/user-attachments/assets/a9e1dcb9-c77b-4b34-b785-20aba16bff48)

Vamos tentar usar essas credenciais para autenticar como o usuário lennie

![image](https://github.com/user-attachments/assets/c973d791-03e4-48b8-adee-aedec4e75059)

Sucesso. Obtivemos acesso de usuário na máquina, e a flag user.txt

## Obtendo a flag de root

Diretório suspeito - scripts

planner.sh -> Script com permissões de root, chamando um outro script com permissões do nosso usuário.\
print.sh -> Script com permissões do nosso usuário, nos permitindo fazer edição e alterando as operações que ele executa.

![image](https://github.com/user-attachments/assets/27b30cde-6351-488f-a6fa-440203e8a55a)

Para obtermos o conteúdo da flag do root, podemos simplesmente editar o script print.sh para copiar a flag e depois ler o seu conteúdo, e executar o planner.sh que irá fazer o chamado do nosso script malicioso.

![image](https://github.com/user-attachments/assets/754b4da6-d2fb-40d9-9722-f0b0f0e2feb8)




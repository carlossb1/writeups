# Room - Light - TryHackMe 

Level: Easy

Ao conectar no servidor, recebemos uma mensagem de ...

Inserimos o usuário que foi fornecido no enunciado e o servidor nos retorna a senha dele.

A primeira ideia foi tentar conectar via SSH com essas credenciais, mas não foi possível.

Como o enunciado sugere que é um sistema de banco de dados, a segunda aproximação envolveu verificar se o sistema é vulnerável a ataques de SQL Injection.

Utilizando alguns dos payloads encontrados no repo https://github.com/payloadbox/sql-injection-payload-list, e baseado nas mensagens de erro, foi possível identificar que o engine usado no banco de dados era o SQLite

Testando o payload ' UNION SELECT 1+1' foi exibida uma mensagem indicando que existem filtros para algumas expressões e caracteres.

Felizmente as expressões do SQLite não são case-sensitive, então ao tentar alterar os caracteres entre maiúsculos e minúsculos, conseguimos bypassar o filtro e executar as operações normalmente.

' UnIoN SeLeCt 1+1 '

retornou o resultado: 2, indicando que o código estava sendo de fato executado pelo banco de dados.

A partir daí, o foco é em enumerar as informações das tabelas. Para isso, vamos prosseguir com o método de ataque utilizando as expressões UNION 
https://portswigger.net/web-security/sql-injection/union-attacks

Conforme a documentação do SQLite, disponível em https://www.sqlite.org/schematab.html Em todos os bancos de dados que utilizam essa engine, vai existir uma tabela que contém algumas 
informações sobre todas as outras tabelas.

CREATE TABLE sqlite_schema(
  type text,
  name text,
  tbl_name text,
  rootpage integer,
  sql text
);

Podendo receber esses nomes alternativos: 
    sqlite_master
    sqlite_temp_schema
    sqlite_temp_master 


Seguindo nosso procedimento para conseguir as informações, podemos utilizar o payload
' UNiON SeLect tbl_name FROM sqlite_master '

Descobrimos a tabela admintable

Agora podemos fazer o mesmo processo dentro dessa tabela.
Para descobrir o nome das colunas, podemos realizar a query exemplificada nesse post do fórum do SQLite https://sqlite.org/forum/info/9add3c3898aed7c4

' UnIoN SeLect name from pragma_table_info('admintable') '
Primeira coluna: id

' UnIoN SeLect name from pragma_table_info('admintable') where name != 'id
Segunda coluna: password

' UnIon SeLect name from pragma_table_info('admintable') where name != 'id' and name != 'password
Terceira coluna: username

# Verificando os usernames
' UnIon SeLect username from admintable ' 
*TryHackMeAdmin*

' UnIoN SeLeCt password from admintable where username = 'TryHackMeAdmin
*mamZtAuMlrsEy5bp6q17*

Vamos tentar realizar o acesso via SSH com essas credenciais, mas novamente, não foi possível.

Realizando uma nova consulta ao banco de usuários 
' UnIon SeLect username from admintable where username != 'TryHackMeAdmin

Olha ela aí!, encontramos o usuário *flag* agora vamos ver se a flag está na senha 
' UnIoN SeLeCt password from admintable where username = 'flag

E Foi!
Encontramos a flag
THM{SQLit3_InJ3cTion_is_SimplE_nO?}


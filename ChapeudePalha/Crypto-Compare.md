Room: Crypto Compare \
Level: Easy \
Categoria: Web

## Introdução

Ao entrarmos na room, somos redirecionados à uma página que exibe o seguinte código PHP:

![image](https://github.com/user-attachments/assets/9afdf489-18ed-40be-aabf-888c456b43af)


Analisando o código, vemos que ele funciona da seguinte maneira:
- Recebe 2 parâmetros: 'shell' e 'pwn',
- Verifica se os dois parâmetros são iguais,
- Realiza a comparação dos valores das hashes MD5 desses parâmetros,
- Caso os dois valores sejam diferentes, mas possuam a mesma hash MD5, exibe a flag.

## Exploração

O truque para explorar essa comparação consiste em uma fraqueza na função hash MD5, onde é possível produzir colisões entre duas strings diferentes. 

### Mas o que é uma Hash?

>Um hash (ou escrutínio) é uma sequência de bits geradas por um algoritmo de dispersão, em geral representada em base hexadecimal, que permite a visualização em letras e números (0 a 9 e A a F), representando um nibble cada. O conceito teórico diz que "hash é a transformação de uma grande quantidade de dados em uma pequena quantidade de informações".

>Essa sequência busca identificar um arquivo ou informação unicamente. Por exemplo, uma mensagem de correio eletrônico, uma senha, uma chave criptográfica ou mesmo um arquivo. É um método para transformar dados de tal forma que o resultado seja (quase) exclusivo. Além disso, funções usadas em criptografia garantem que não é possível a partir de um valor de hash retornar à informação original.

>Como a sequência do hash é limitada, muitas vezes não passando de 512 bits, existem colisões (sequências iguais para dados diferentes). Quanto maior for a dificuldade de se criar colisões intencionais, melhor é o algoritmo. 

Fonte: [wikipedia](https://pt.wikipedia.org/wiki/Fun%C3%A7%C3%A3o_hash)

### MD5
>O algoritmo de sintetização de mensagem MD5 é uma função hash amplamente utilizada que produz um valor de hash de 128 bits expresso em 32 caracteres.[1] Embora o MD5 tenha sido projetado inicialmente para ser usado como uma função hash criptográfica, foi constatado que ele sofre de extensas vulnerabilidades. Ele ainda pode ser usado como uma soma de verificação para checar a integridade de dados,[2] mas apenas contra corrupção não intencional. Ele permanece adequado para outros fins não criptográficos, por exemplo, para determinar a partição para uma chave específica em um banco de dados particionado.[3]

Fonte: [wikipedia](https://pt.wikipedia.org/wiki/MD5)

### Exploit

Agora que entendemos um pouco mais sobre como funciona esse tipo de algoritmo, vamos ver se encontramos uma forma de produzir essa colisão.

Para nossa sorte, conseguimos encontrar um exemplo desse tipo de colisão nesse [post](https://www.johndcook.com/blog/2024/03/20/md5-hash-collision/)

Conforme mostrado pelo post no blog, as duas strings:

`TEXTCOLLBYfGiJUETHQ4hAcKSMd5zYpgqf1YRDhkmxHkhPWptrkoyz28wnI9V0aHeAuaKnak`

e

`TEXTCOLLBYfGiJUETHQ4hEcKSMd5zYpgqf1YRDhkmxHkhPWptrkoyz28wnI9V0aHeAuaKnak`

produzem a mesma hash md5.

Então podemos usar esse payload para obter a flag:

`https://crypto-compare.chapeudepalhahacker.club/?shell=TEXTCOLLBYfGiJUETHQ4hAcKSMd5zYpgqf1YRDhkmxHkhPWptrkoyz28wnI9V0aHeAuaKnak&pwn=TEXTCOLLBYfGiJUETHQ4hEcKSMd5zYpgqf1YRDhkmxHkhPWptrkoyz28wnI9V0aHeAuaKnak`

![image](https://github.com/user-attachments/assets/1cfc0f1b-6294-406f-bf6b-41d82b1b87c1)


## Agradecimento
Não poderia deixar de agradecer ao [@calilkhalil](https://github.com/calilkhalil) pela ajuda nesse e em outros desafios. Me ensinou muita coisa, e pra galera que curte CTF, vale a pena demais dar uma conferida nos repos dele.

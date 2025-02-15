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

Podemos encontrar um exemplo desse tipo de colisão nesse [post](https://www.johndcook.com/blog/2024/03/20/md5-hash-collision/)

Conforme mostrado pelo post no blog, as duas strings:

`TEXTCOLLBYfGiJUETHQ4hAcKSMd5zYpgqf1YRDhkmxHkhPWptrkoyz28wnI9V0aHeAuaKnak`

e

`TEXTCOLLBYfGiJUETHQ4hEcKSMd5zYpgqf1YRDhkmxHkhPWptrkoyz28wnI9V0aHeAuaKnak`

produzem a mesma hash md5.

Então podemos usar esse payload para obter a flag:

`https://crypto-compare.chapeudepalhahacker.club/?shell=TEXTCOLLBYfGiJUETHQ4hAcKSMd5zYpgqf1YRDhkmxHkhPWptrkoyz28wnI9V0aHeAuaKnak&pwn=TEXTCOLLBYfGiJUETHQ4hEcKSMd5zYpgqf1YRDhkmxHkhPWptrkoyz28wnI9V0aHeAuaKnak`

![image](https://github.com/user-attachments/assets/1cfc0f1b-6294-406f-bf6b-41d82b1b87c1)


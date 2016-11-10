# hybrid-rs-trainner #

##Afinal, do que se trata esse repositório?

Essse repositório contém um conjunto de scripts com a finalidade de treinar um Sistema de Recomendação Híbrido -Collaborative Filtering (CF) e Content-Based Filtering (CBF)-  

Desse modo, é possível fazer recomendações de eventos (seja item, filme, ou whatever. Isso depende da modelagem) conhecidos (no futuro será 
possível gerar recomendações para novos eventos)
para usuários (também será possível gerar recomendações para novos usuários).

## O que é Colaborative Filtering (CF)?
É uma das taxonomias (bem comum) utilizadas para distinguir os Sistemas de Recomendação. A premissa básica por trás da CF é a de que se um usuário `u1` é semelhante a um usuário `u2`, então pode-se gerar recomendações para o usuário `u2` com base no usuário `u1`.

Para explicar melhor, imagina-se a seguinte situação:
 - Usuário `u1` tem 18 anos e solteiro
 - Usuário `u2` tem 33 anos e é casado
 - Usuário `u3` tem 21 anos e é solteiro
 - Usuário `u4` tem 45 anos e é casado
 
 - `u1` assiste os filmes `Mercenários`, `Mercenários 2`,  `Mercenários 3` e `Atração Perigosa`, `Rambo`
 - `u2` assiste os filmes `Mercenários`, `Mercenários 2`, `American PIE` e `Velozes e Furiosos`, `Se beber, não case`
 - `u3` assiste os filmes `American PIE`, `Mercenários 2`, `Mercenários 3`, `Atração Perigosa`
 - `u4` não assiste nenhum filme
 
Fica claro que o `u3` é semelhante ao `u1`, pois eles __assistiram 3 filmes iguais__. Seguindo a premissa da CF, um dos filmes recomendados para o usuário `u3` seria `Mercenários`. 

## O que é Content-Based Filterging (CBF)?
Assim como a CF é uma taxonomia para distinguir os Sistemas de Recomendação. Esta, por sua vez, faz o estudo de ténicas para gerar recomendações para usuários com base nas características dos mesmos.
Geralmente é utilizada quando não há informações colaborativas (diga-se coletivas) a respeito de um item ou usuário, já que, estas geralmente são mais efetivas (para gerar recomendações) do que as anteriores.
Desse modo, para `u4` seria recomendado os filmes que `u2`assistiu, pois o `u2` é o mais mais semelhante ao `u4`.

## Como funciona?


## Algoritmos Suportados
  * KNarest Neighborh (instance-based ou lazy learning)
  
## Como é gerado uma recomendação?
Para um cliente `c` encontram-se os `k`vizinhos mais próximos com base no faturamento. 

## Como o algoritmo funciona?
Nessa primeira versão é realizada CF com base nos faturamentos (cliente `c` comprou item `i`).

Utilizam-se as implementações da técnica do vizinho mais próximo (KNN) disponíveis na biblioteca do `scikit-learn`(http://scikit-learn.org/stable/modules/neighbors.html), juntamente com seus parâmetros,
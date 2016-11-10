# hybrid-rs-trainner #

##Afinal, do que se trata esse repositório?

Essse repositório contém um conjunto de scripts com a finalidade de treinar um Sistema de Recomendação Híbrido -Collaborative Filtering (CF) e Content-Based Filtering (CBF)-  

Desse modo, é possível fazer recomendações de eventos (seja item, filme, ou whatever. Isso depende da modelagem) conhecidos (no futuro será 
possível gerar recomendações para novos eventos)
para usuários (também será possível gerar recomendações para novos usuários).

## O que é Filtragem Colaborativa?
É uma das taxonomias (bem comum) utilizadas para distinguir os Sistemas de Recomendação. A premissa básica por trás da filtragem colaborativa é a de que se um usuário `u1` é semelhante a um usuário `u2`, então pode-se gerar recomendações para o usuário `u2` com base no usuário `u1`.

Para explicar melhor, imagina-se a seguinte situação:
 
 - Um usuário `u1` assiste os filmes `Mercenários`, `Mercenários 2`,  `Mercenários 3` e `Atração Perigosa`
 - Um usuário `u2` assiste os filmes `Mercenários`, `Mercenários 2`, `American PIE` e `Velozes e Furiosos`
 - Um usuário `u3` assiste os filmes `Homens de Honra`, `Mercenários 2`, `Mercenários 3`, `Atração Perigosa`
 
Fica claro que o `u3` é semelhante ao `u1`, pois eles assistiram 3 filmes iguais. Seguindo a premissa da filtragem colaborativa, um dos filmes recomendados para o usuário `u3` seria `Mercenários`. 
 

## Como funciona?


## Algoritmos Suportados
  * KNarest Neighborh (instance-based ou lazy learning)
  
## Como é gerado uma recomendação?
Para um cliente `c` encontram-se os `k`vizinhos mais próximos com base no faturamento. 

## Como o algoritmo funciona?
Nessa primeira versão é realizada CF com base nos faturamentos (cliente `c` comprou item `i`).

Utilizam-se as implementações da técnica do vizinho mais próximo (KNN) disponíveis na biblioteca do `scikit-learn`(http://scikit-learn.org/stable/modules/neighbors.html), juntamente com seus parâmetros,

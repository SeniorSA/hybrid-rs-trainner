# hybrid-rs-trainner #

##Afinal, do que se trata esse repositório?

Essse repositório contém um conjunto de scripts com a finalidade de treinar um Sistema de Recomendação Híbrido -Collaborative Filtering (CF) e Content-Based Filtering (CBF)- genérico o suficiente para fazer recomendações para de itens para usuários (conhecidos ou novos).  

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
Geralmente é utilizada quando não há informações colaborativas (diga-se coletivas) a respeito de um item ou usuário. Desse modo, para `u4` seria recomendado os filmes que `u2` assistiu, pois __com base nas características dos usuários__ (idade e estado civil) o `u2` é o mais mais semelhante ao `u4`

## O que é Hybrid Filtering?
Os Sistemas de Recomendação Híbridos fazem uso tanto de técnicas presentes em CF, quanto em CBF. Na verdade, na maioria das vezes, tomam-se como prioridade as técnicas utilizadas na CF, e caso não haja informações a respeito (usuário ou item novo) utilizam-se técnicas de CBF.

Assim, um Sistema de Recomendação Híbrido seria capaz de gerar recomendações para todos os usuários disponíveis (`u1`, `u2`, `u3`, `u4`). Para o `u3`, por exemplo, seria recomendado `Mercenários`, e para o `u4` seria recomendado os filmes que o `u2` assistiu. Os Híbridos geralmente (almost like everything, não é há convenção na literatura) geram suas recomendações com base nas técnicas de CF, pois estas são mais efetivas (geramente), e caso não haja informações colaborativas, então usam-se técnicas de CBF.

## Qual é a principal diferença entre essas taxonomias?
Diferentes técnicas de Inteligência Artificial (IA) são utilizadas para tratar esses problemas - em alguns casos é utilizado a mesma técnica em CF e CBF. O exemplo mais clássico disso é o uso de algoritmo KNearestNeighbor -.
A principal distinção entre elas está no uso dos dados para gerar as recomendações - CF usa dados colaborativos para determinar a similaridade e gerar recomendações com base nos itens ou usuários mais similares, enquanto que CBF usa dados individuais para determinar as recomendações para os itens ou usuários mais similares -.

## Como definir qual técnica utilizar para treinar o modelo e gerar as recomendações?
Evidentemente não há uma solução para comum para todos os casos. Cada problema é um problema, e como tal, deve ser tratado de forma singular. Portanto, para determinar qual técnica é melhor para um conjunto de dados (domínio), deve-se fazer uma análise dos dados e posteriormente a elaboração e validação de hipóteses.

Na verdade, o problema de recomendação tem sido tratamento como problema de agrupamento, etc. -, como problema de classificação, como problema de regressão, como problema de regras de associação

## Algoritmos Suportados
  * KNarest Neighborh (instance-based ou lazy learning)
  
## Como é gerado uma recomendação?
Para um cliente `c` encontram-se os `k`vizinhos mais próximos com base no faturamento. 

## Como o algoritmo funciona?
Nessa primeira versão é realizada CF com base nos faturamentos (cliente `c` comprou item `i`).

Utilizam-se as implementações da técnica do vizinho mais próximo (KNN) disponíveis na biblioteca do [scikit-learn](http://scikit-learn.org/stable/modules/neighbors.html), juntamente com seus parâmetros,

## Como fazer o treinamento do algoritmo?
Dentro do mesmo diretório onde o projeto foi clonado, basta digitar o comando `python train_classifier.py` passando os parâmetros disponíveis. Os parâmetros disponíveis são:
 - --distance-metric [metrica escolhida]. As métricas estão disponíveis [aqui](http://scikit-learn.org/stable/modules/generated/sklearn.neighbors.DistanceMetric.html)
 - --kfold [inteiro descrevendo o número de folds usado na validação cruzada] 
 - --alg [o algoritmo utilizado para fazer o cálculo dos k vizinhos mais próxixos] disponível [em](http://scikit-learn.org/stable/modules/neighbors.html#nearest-neighbor-algorithms)
 - --n-neighbors [inteiro descrevendo o número de vizinhos mais próximos]
 - --top-items [número descrevendo o número dos top items para um usuário de acordo com sua relevância] (AINDA NÃO É SUPORTADO)
 - --leaf-size [inteiro que determina o número de nó folhas utilizado na poda] default: 30. Parâmetro só é utilizado quando quando --alg=kn_tree ou --alg=ball_tree
 - --weights [string definindo a função de peso utilizada na predição] default: 'uniform'. [Mais informações](http://scikit-learn.org/stable/modules/neighbors.html#nearest-neighbor-algorithms)
 - --p [inteiro definindo a potência utilizada para fazer o cálculo da distância] [mais informações](http://scikit-learn.org/stable/modules/neighbors.html#nearest-neighbor-algorithms)
 
Se for nas configurações padrões (sem alterar os parâmetros), a implementação da técnica do vizinho mais próximo utilizada será a 'brute'. A métrica de distância será a menor distância entre dois pontos (distância euclidiana), o número de vizinho será 12 e o número de estraticações utilizada para fazer a validação cruzada será igual a 10.

Após o término do treinamento, será escolhido a versão com as melhores métricas e será salvo em disco. O nome do arquivo será `user_user_cf_knn-[dia-mes-ano-hora-minuto-segundo].pkl`.
Além disso, também será gerado um log com as métricas coletadas durante o treinamento dos k modelos (kfolds).


## REFERÊNCIAS
 * [Recommender systems survey](http://romisatriawahono.net/lecture/rm/survey/information%20retrieval/Bobadilla%20-%20Recommender%20Systems%20-%202013.pdf)
 * [An Empirical Analysis of Design Choices in Neighborhood](https://www.researchgate.net/profile/Jon_Herlocker/publication/226021885_An_Empirical_Analysis_of_Design_Choices_in_Neighborhood-Based_Collaborative_Filtering_Algorithms/links/00b7d539756e3b1c49000000.pdf)
 * [Recommender Systems Handbook]()
 * [Recommendation Systems](http://infolab.stanford.edu/~ullman/mmds/ch9.pdf)
 * [Similarity and recommender systems](http://www.inf.ed.ac.uk/teaching/courses/inf2b/learnnotes/inf2b-learn-note02-2up.pdf)
 * [Semi-Supervised Learning for Personalized Web Recommender](http://cai.type.sk/content/2010/4/semi-supervised-lear\ning-for-personalized-web-recommender-system/11052.pdf)
 * [Learning From Labeled And Unlabeled Data: An Empirical Study Across Techniques And Domains](https://www.jair.org/media/1509/live-1509-2348-jair.pdf)
 * [Is trust robuts? An Analysis of Trust-Based Recommendation](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.476.7184&rep=rep1&type=pdf)
 

# -*- coding: utf-8 -*-

import pandas as pd

#Carregando os dados
dados = pd.read_csv("https://raw.githubusercontent.com/alura-cursos/alura-clustering-validation/base-de-dados/CC%20GENERAL.csv")

#Primeira visualização dos dados
dados.columns.tolist() 
dados.shape #(8950, 18)
dados.info() #apenas uma coluna com valores faltantes (MINIMUM_PAYMENTS)

#CUSTID : Identification of Credit Card holder (Categorical)
#BALANCE : Balance amount left in their account to make purchases (
#BALANCEFREQUENCY : How frequently the Balance is updated, score between 0 and 1 (1 = frequently updated, 0 = not frequently updated)
#PURCHASES : Amount of purchases made from account
#ONEOFFPURCHASES : Maximum purchase amount done in one-go
#INSTALLMENTSPURCHASES : Amount of purchase done in installment
#CASHADVANCE : Cash in advance given by the user
#PURCHASESFREQUENCY : How frequently the Purchases are being made, score between 0 and 1 (1 = frequently purchased, 0 = not frequently purchased)
#ONEOFFPURCHASESFREQUENCY : How frequently Purchases are happening in one-go (1 = frequently purchased, 0 = not frequently purchased)
#PURCHASESINSTALLMENTSFREQUENCY : How frequently purchases in installments are being done (1 = frequently done, 0 = not frequently done)
#CASHADVANCEFREQUENCY : How frequently the cash in advance being paid
#CASHADVANCETRX : Number of Transactions made with "Cash in Advanced"
#PURCHASESTRX : Numbe of purchase transactions made
#CREDITLIMIT : Limit of Credit Card for user
#PAYMENTS : Amount of Payment done by user
#MINIMUM_PAYMENTS : Minimum amount of payments made by user
#PRCFULLPAYMENT : Percent of full payment paid by user
#TENURE : Tenure of credit card service for user

#Removendo colunas
dados.drop(columns = ['CUST_ID','TENURE'], inplace = True)

#Substituindo valores faltantes
dados.fillna(dados.median(), inplace = True)

#Colocando todos os valores entre 0 e 1
from sklearn.preprocessing import Normalizer
values = Normalizer().fit_transform(dados.values)

#ajustado o cluster
from sklearn.cluster import KMeans
kmeans = KMeans(n_clusters = 5, n_init = 10, max_iter = 300)
y_pred = kmeans.fit_predict(values)

#Coeficiente de Silhouette
#indica o quanto estão separados os clusters
from sklearn import metrics
labels = kmeans.labels_
silhouette = metrics.silhouette_score(values, labels, metric= 'euclidean')
#vai de [-1,1]
# se o valor é posivito já é bom
print(silhouette)


#Davies-Bouldin
#Quanto menor, melhor
dbs = metrics.davies_bouldin_score(values, labels)
print(dbs)

#Calinski
caliski = metrics.calinski_harabasz_score(values, labels)
print(caliski)

#definindo funcao
def clustering_alg(n_clusters, dataset):
    kmeans = KMeans(n_clusters=n_clusters, n_init = 10, max_iter=300)
    labels = kmeans.fit_predict(dataset)
    s = metrics.silhouette_score(dataset, labels, metric = "euclidean")
    dbs = metrics.davies_bouldin_score(dataset, labels)
    caliski = metrics.calinski_harabasz_score(dataset, labels)
    return s, dbs, caliski

#Calculando estatísticas para cada determinado tipo de número de clusters
s1, dbs1, caliski1 = clustering_alg(2, values)
df = pd.DataFrame({ "i":[2], "s": [s1], "d":[dbs1], "c":[caliski1]})
for i in range(3,10):
    s1, dbs1, caliski1 = clustering_alg(i, values)
    df2 = pd.DataFrame({ "i":[i], "s": [s1], "d":[dbs1], "c":[caliski1]})
    df = df.append(df2)
    
print(df)

#Vendo a estabilidade e estrutura
import numpy as np

#vendo  se há uma diferenca das estatísticas com os nossos dados e dados aleatorios
random_df = np.random.rand(8950,16)
s, dbs, caliski = clustering_alg(5, random_df)
s1, dbs1, caliski1 = clustering_alg(5, values)
print(s, dbs, caliski)
print(s1, dbs1, caliski1)

#vendo a estabilidade  do modelo
set1, set2, set3 = np.array_split(values,3)

s1, dbs1, caliski1 = clustering_alg(5, set1)
s2, dbs2, caliski2 = clustering_alg(5, set2)
s3, dbs3, caliski3 = clustering_alg(5, set3)

print(s1, dbs1, caliski1)
print(s2, dbs2, caliski2)
print(s3, dbs3, caliski3)

#Gráfico
import matplotlib.pyplot as plt

plt.scatter(dados['PURCHASES'],dados['PAYMENTS'], c = labels, s = 5, cmap = 'rainbow')
plt.xlabel("Valor total pago")
plt.ylabel("Valor total gasto")

#seaborn
#não dá pra visualizar
import seaborn as sns

dados['cluster'] = labels
sns.pairplot(dados[0:], hue = 'cluster')

#alternativa a gráfico
dados.groupby('cluster').describe()

centroids = kmeans.cluster_centers_
max = len(centroids[0])
for i in range(max):
    print(dados.columns[i], round(centroids[:, i].var(), 6))
    
#selecionando atributos específicos que apresentaram maior variância
descripition = dados.groupby('cluster')['BALANCE','PURCHASES','CASH_ADVANCE','CREDIT_LIMIT','PAYMENTS'].describe()
n_clients = dados['cluster'].value_counts()
print(descripition.mean)
descripition['n_clients'] = n_clients
print(descripition)

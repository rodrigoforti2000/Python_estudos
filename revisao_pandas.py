# -*- coding: utf-8 -*-

#Pandas
import pandas as pd
import rope

#definindo DF
dados = {'nome' : ['Rodrigo','Julia'],
         'sobrenome': ['Forti','Godoy'],
         'idade': [20, 21]}
df_dados = pd.DataFrame(dados)
df_dados
df_dados["nome"] == "Rodrigo"
df_dados.head(1)
df_dados.tail(1)

#Importando Dados
#mudar barras
df_votacao = pd.read_csv("C:/Users/Windows 10/Desktop/ESTUDOS/votacao_agg_estado.csv")
df_votacao.head(5)

#colunas bonitinho
df_votacao.columns.tolist()

#dimensão
df_votacao.shape

#utilitarios
#valores faltante, tipo (object = string)
df_votacao.info()
df_votacao.dtypes['ano_eleicao']

#navegar
#df[coluna][linha]
df_votacao['nome'][0:10]

#pegar toda linha
df_votacao.iloc[0]
#df[col][3] = df.iloc[3][col]

#filtro
filtro = [True, False]
df_dados[filtro]
filtro = df_dados['idade'] >= 21
df_dados[filtro]
df_dados[df_dados['nome']=='Rodrigo']
filtro_composto = (df_dados['idade'] == 20) & (df_dados['nome']=='Rodrigo')
df_dados[filtro_composto]
df_dados.where(filtro_composto)
df_dados.where(filtro_composto).dropna(how = 'all')

filtro_votacao = df_votacao['sigla_partido'] == 'PSOL'
df_votacao[filtro_votacao]['nome']

#Manipulacao
#criacao de coluna
df_dados['sabe_cafe'] = [False,True]
df_dados
#inplace = True altera o objeto
#ou df_dados = df_dados (favorito)
df_dados.rename(columns = {'sabe_cafe':'fazer_cafe'}, inplace = True)

#Deletar coluna
df_dados['tem_dinheiro'] = False
del df_dados['tem_dinheiro']

#Unique
#Lista dos distintos
df_votacao['sigla_partido'].unique()
df_votacao['sigla_partido'].nunique()

df_vot_2018 = df_votacao[df_votacao['ano_eleicao'] == 2018]
print(df_vot_2018['numero_sequencial'].nunique(), "candidatos distintos em 2018")

#Transformações, conversões e remoções
import numpy as np

np.log(df_votacao['total_votos'])

def sigla_cafe(x):
    if x == True:
        return 'sabe fazer cafe'
    else:
        return 'nao sabe fazer cafe'

#apply
df_dados['fazer_cafe'].apply(sigla_cafe)

#Bolsonarao com like
def is_bolsonaro(x):
    return 'BOLSONARO' in x  

def like(x, like_what=""):
    return like_what in x

#erro
df_vot_2018[df_vot_2018['nome'].apply(like, args = 'GODOY')]['nome']

#funçoes anonimas
df_vot_2018[df_vot_2018['nome'].apply(lambda x: "GODOY" in x)]['nome']

#pego o primeiro nome e deixa a primeira maiuscula
"Rodrigo Forti".split(" ")[0].title()
df_votacao['nome'].apply(lambda x: x.split(" ")[0].title()) 

#Group by
df_dados['sobrenome'].value_counts()

df_dados.groupby('sobrenome')['idade'].mean()
df_dados.groupby('sobrenome').describe()

agg_columns = ['ano_eleicao','numero_turno','sigla_partido']
df_group = df_votacao.groupby(agg_columns)['total_votos'].sum()
#transfromando uma serie em df
df_group = df_group.reset_index()

df_group.sort_values(by = ['ano_eleicao','total_votos'], ascending = [True,False])


#merge
df_join = df_votacao.merge(df_group, on=['ano_eleicao','numero_turno','sigla_partido'],
                 how = 'left', suffixes=["","_partido"])

df_join['representacao_partido'] = df_join['total_votos']/df_join['total_votos_partido']
df_join.sort_values('representacao_partido', ascending = False)[['nome','sigla_partido','representacao_partido']]

#explode abre listas em várias linhas
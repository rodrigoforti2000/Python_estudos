# -*- coding: utf-8 -*-

#importação de pacotes
import numpy as np
import pandas as pd
import pyDOE2 as doe
import seaborn as sns

#Duas formas
ensaios = np.array ([[-1,-1],[1,-1],[-1,1],[1,1]])
ensaios = doe.ff2n(2)

#Dataframe do experimento
experimento = pd.DataFrame(ensaios, columns=['farinha','chocolate'])
experimento['porcoes'] = [19,37,24,49]

#Gráficos
sns.set_palette('terrain')
sns.set_style('darkgrid')

ax1 = sns.lmplot(data = experimento, x = 'farinha', y = 'porcoes', ci = None, hue = 'chocolate')
ax1.set(xticks = (-1,1))

ax1 = sns.lmplot(data = experimento, x = 'chocolate', y = 'porcoes', ci = None, hue = 'farinha')
ax1.set(xticks = (-1,1))

#Modelo
import statsmodels.api as sm
import statsmodels.formula.api as sfm

modelo = sfm.ols(data = experimento, formula = 'porcoes ~ farinha + chocolate + farinha:chocolate')
modelo_ajustado = modelo.fit()

print(modelo_ajustado.summary())


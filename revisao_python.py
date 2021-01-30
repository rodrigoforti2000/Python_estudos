# -*- coding: utf-8 -*-

#strigs 
nome = 'Rodrigo Forti'
nome.upper()
nome.lower()
nome[:3]
nome[-5:-1]
nome[::-1] #inverter

#numérico
type(1) #int
type(1.) #float
9//2 #divisão inteira
9%2 #resto da divisão

#listas
minha_lista = ['Rodrigo', 28, ['Julia','Maria'], True]
len(minha_lista)
minha_lista[-1]
minha_lista[0]
minha_lista[::-1]
minha_lista[2][1]

#if
idade = input('Entre com sua idade:')
idade = int(idade)

if idade < 18:
    print('Novinho')
elif idade <= 65:
    print('pode beber')
else:
    print("Cuidado, sua idade é avançada")

#for e While
for i in range(1,11):
    if i%2 == 0:
        print(i, 'é par')
    else:
        print(i, 'é impar')
        
i = 1
while True:
    print(i)
    if i == 10:
        break
    i += 1
    
# funçoes
def calc_cubo(x):
    return x ** 3

calc_cubo(3)

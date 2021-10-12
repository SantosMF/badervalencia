#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  20 20:59:19 2021
@author: marcio
mpraquedista@gmail.com
"""
import sys
import readline
readline.parse_and_bind('tab: complete')
valence = {} ## lista para os cell_parameters
atomos = []## lista para os simbolos dos atomos do Atomic_positions
nat = 0 ## número de átomos na célula ## variável global (tem o valor modificado)
ntp = 0 ## número de tipos de átomos ## variável global (tem o valor modificado)
#-------------------início da leitura do arquivo outscf.out------------------
with open(str(input("Insira o arquivo scf.out\n>> ")),"r") as outscf:
    for lines in outscf: # lê o arquivo a partir da linha 'Begin final coordinates'
        if 'number of atoms/cell' in lines:
            nat += int(lines[40:45]) ## modifica o valor da variável nat
            ntp += int((outscf.readline().rstrip().split('='))[1]) # modifica ntp
        if 'valence' in lines: ## busca os tipos de átomos
            for i in range(0, ntp):
                key = outscf.readline().split()
                valence[key[0]] = key[1] # chave = símbolo: valor = valencia  do átomo
            break
    for lines in outscf:
        if 'Cartesian axes' in lines:
            outscf.readline(), outscf.readline()
            break
    try:
        for lines in outscf:
            dados = lines.split()
            atomos.append(dados[1]) # armazena os símbolos dos átomos
            if 'number of k points' in lines:
                break
    except:
        pass
##--------------término da leitura do arquivo outscf.out----------------------
if len(atomos) != 0:
#---------------abrir arquivo ACF.dat gerado pelo programa bader--------------
    with open(str(input("Insira o arquivo ACF.dat\n>> ")),"r") as ACF:
        ACF.readline(), ACF.readline() #remove as duas primeiras linhas
        carga = []
        try:
            for lines in ACF:
                numero, X, Y, Z, CHARGE, MIN_DIST, ATOMIC_VOL = lines.split()
                carga.append(CHARGE) #armazena as cargas de bader
        except:
            pass ## ignora as quatro últimas linhas
    out_file = str(input("Salvar dados como?\n>>"))
    with open (out_file,'w')as out_date:
        for atomic_symbol, charge_bader in zip(atomos, carga):
            #função que obtém as cargas de bader
            badervalence = (float(valence[atomic_symbol]) - float(charge_bader))
            out_date.write(('{}{}{:^10.6f}{}'.format(atomic_symbol,'\t', badervalence,'\n')))
    print('\nDados Salvos!')
else:
    print("Erro!\nInsira o arquivo de saida do cálculo scf")
    sys.exit()

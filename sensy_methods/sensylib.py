
import sensyerror as se
from sensyutils import *

import os
import traceback
import pandas as pd
import numpy as np
from unicodedata import normalize
import plotly.graph_objs as go
import kaleido

from pptx import Presentation
from pptx.util import Inches

class SensoryBot:
    
    def __init__(self, projeto = None):
        
        self.projeto = projeto
        self.nome_xlsx = self.projeto.lower()
        
        self.configurar_marca_mdias()
        self.configurar_dados()
        self.configurar_atributos_de_lista()
        
        print('SensoryBot Pronto!')
        print('')
        print('Cidades:')
        for c in self.lista_de_cidades:
            print(' - {}'.format(c))
        
    
    # --------------------------------------------------------------------------------
    # - INICIALIZACAO
    # --------------------------------------------------------------------------------
    
    def configurar_marca_mdias(self):
        
        prm = pd.read_excel('./data/{}.xlsx'.format(self.nome_xlsx), sheet_name = 'PARAMETRO')
        prm = prm[prm.PROJETO == self.projeto].reset_index(drop = True)
        
        self.marca_mdias = {}
        for i in range(len(prm)):

            M = normalize('NFKD', prm.loc[i, 'MARCA_MDIAS']).encode('ASCII','ignore').decode('ASCII')
            C = normalize('NFKD', prm.loc[i, 'CIDADE']).encode('ASCII','ignore').decode('ASCII')
        
            self.marca_mdias[M] =  C
            
    def remover_acentos(self, x):
        return normalize('NFKD', x).encode('ASCII','ignore').decode('ASCII')
    

    def configurar_dados(self):
        
        self.lista_dataset = ['HEDONICA', 'USUARIO', 'ORDENACAO', 'CATA']
        self.dataset = {}
        
        for i in self.lista_dataset:
            temp = pd.read_excel('./data/{}.xlsx'.format(self.nome_xlsx), sheet_name = i)
            
            if i == 'USUARIO':
                temp['CIDADE'] = temp['CIDADE'].apply(lambda x: self.remover_acentos(x))
                
            else:
                temp['AMOSTRA'] = temp['AMOSTRA'].apply(lambda x: self.remover_acentos(x))
        
            self.dataset[i] = temp
            
                
    def configurar_atributos_de_lista(self):

        # Cidade dos usuarios
        self.cidade_usuario = {}
        
        df = self.criar_dataframe('USUARIO', False)
        for C in df['CIDADE'].unique():
            self.cidade_usuario[C] = list(df[df['CIDADE'] == C].ID_USUARIO.unique())
        
        # Cidades
        self.lista_de_cidades = []
        self.lista_de_cidades = list(self.cidade_usuario.keys())
        
        # Hedonicas
        self.lista_de_hedonicas = []
        self.lista_de_hedonicas_jar = []
        
        df = self.criar_dataframe('HEDONICA', False)
        for i in df.columns:
            if i not in ['ID_USUARIO', 'AMOSTRA'] and i.find('JAR') == -1 and i.find('COMPRA') == -1:
                self.lista_de_hedonicas.append(i)
                
            if i not in ['ID_USUARIO', 'AMOSTRA'] and i.find('JAR') != -1 and i.find('COMPRA') == -1:
                self.lista_de_hedonicas_jar.append(i)
                
        # Catas
        self.lista_de_catas = []
        df = self.criar_dataframe('CATA', False)
        for i in df.columns:
            if i not in ['ID_USUARIO', 'AMOSTRA']:
                self.lista_de_catas.append(i)
                
                
    def analisar_atributos(self):
        
        for i in self.lista_dataset:
            
            print('- {}'.format(i))
            print('-----------------------')
            print('Registros : {}'.format(len(self.dataset[i])))
            print('Colunas   : {}'.format(len(self.dataset[i].columns)))
            print('Nulos     : {}'.format(self.dataset[i].isna().sum().sum()))
            print('Usuarios  : {}'.format(len(self.dataset[i].ID_USUARIO.unique())))
            print('')
            
            
    def criar_dataframe(self, dataset, formatar_colunas = False):
    
        df = self.dataset[dataset].copy()
        if formatar_colunas == True:
            
            nome_colunas = []
            for i in cols:
                i = i.replace('_', ' ')
                k = ""
                for j in i.split(' '):
                    k = k + " " + j.capitalize() 
                nome_colunas.append(k.strip())
                
            df.columns = nome_colunas

        return df
    
    def grafico_pizza_atributos_usuario(self, atributo = None, cidade = None):

        caminho = './grafico/atributo_usuarios/{}_{}.png'.format(atributo.lower(), cidade.lower().replace(' ', '_'))

        df = self.criar_dataframe('USUARIO', False)
        df = df.dropna()
        df = df[df['CIDADE'] == cidade].reset_index(drop = True)
        
        if atributo == 'SEXO':
            df[atributo] = df[atributo].apply(lambda x: 'Masculino' if x.upper() == 'M' else 'Feminino')
            
        if atributo == 'FAIXA_ETARIA':
            df[atributo] = df[atributo].apply(lambda x: 'De ' + x.replace(' - ', ' a '))
            
        if atributo == 'ESCOLARIDADE':
            df[atributo] = df[atributo].apply(lambda x: x.replace(' /', ';<br>'))

        df = df.groupby(atributo)['ID_USUARIO'].nunique().reset_index()

        # Plot
        
        CONFIG = {
            'FAIXA_ETARIA'  : {'height' : 550, 'width' : 600},
            'CLASSE_SOCIAL' : {'height' : 550, 'width' : 600},
            'ESCOLARIDADE'  : {'height' : 650, 'width' : 750},
            'SEXO'          : {'height' : 550, 'width' : 600}
        }
        
        plot = exec_pizza_atributos_usuario(df, CONFIG[atributo]['height'], CONFIG[atributo]['width'])
        plot.write_image(
            caminho, 
            height = CONFIG[atributo]['height'], 
            width = CONFIG[atributo]['width'], 
            engine = 'kaleido'
        )
        
        return plot, df
    
    
    def grafico_nota_escala_hedonica(self, atributo = None, cidade = None):

        df = self.criar_dataframe('HEDONICA', False)
        
        if atributo == 'OVERALL_LIKING':
            
            caminho = './grafico/overall_liking/nota_hedonica/{}_{}.png'.format(atributo.lower(), cidade.lower().replace(' ', '_'))
            height = 400
            width = 600
            
        else:
            
            caminho = './grafico/atributo_hedonica/{}_{}.png'.format(atributo.lower(), cidade.lower().replace(' ', '_'))
            
            if atributo in ['TEXTURA', 'CROCANCIA', 'PROPORCAO_RECHEIO_CASQUINHA']:
                height = 225
                width = 775
            else:
                height = 180
                width = 800
        
        try:
            lista_usuarios = self.cidade_usuario[cidade]
        except:
            se.erro_grafico_parametro_cidade(df)
            return None
        
        if atributo not in df.columns:
            se.erro_grafico_parametro_atributo(df)
            return None
        
        
        df = df[df['ID_USUARIO'].isin(lista_usuarios)].reset_index(drop = True)
        df = df[['ID_USUARIO', 'AMOSTRA', atributo]]
        
        df['NOTA'] = np.where(
            (df[atributo] <= 4), '4 ou Menos', np.where((df[atributo] >= 7), '7 ou Mais', '5 ou 6'))
        
        df = df.groupby(['AMOSTRA', 'NOTA'])['ID_USUARIO'].count().reset_index()
        df.columns = ['AMOSTRA', 'NOTA', 'FREQ']
        df['FREQ_PERC'] = (df['FREQ'] / int(df['FREQ'].sum() / len(df['AMOSTRA'].unique())))
        
        
        plot = exec_nota_escala_hedonica(df, height, width)
        
        plot.write_image(
            caminho, 
            height = height,
            width = width,
            engine = 'kaleido'
        )

        return plot, df
    
    
    def grafico_histograma_escala_hedonica(self, atributo = None, cidade = None):

            caminho = './grafico/overall_liking/histograma/{}_{}.png'.format(
                atributo.lower(), cidade.lower().replace(' ', '_'))

            df = self.criar_dataframe('HEDONICA', False)

            try:
                lista_usuarios = self.cidade_usuario[cidade]
            except:
                se.erro_grafico_parametro_cidade(df)
                return None

            if atributo not in df.columns:
                se.erro_grafico_parametro_atributo(df)
                return None

            # PLOT
            
            temp = pd.DataFrame({atributo : list(range(1,10))})
            df = df[df['ID_USUARIO'].isin(lista_usuarios)].reset_index(drop = True)
            for A in df['AMOSTRA'].unique():

                aux = df[df['AMOSTRA'] == A].groupby(atributo)['ID_USUARIO'].nunique().reset_index()
                aux['ID_USUARIO'] = round(aux['ID_USUARIO'] / aux['ID_USUARIO'].sum(), 3)
                aux.columns = [atributo, A]
                temp = temp.merge(aux, on = atributo, how = 'left').fillna(0)

            
            plot = exec_histograma_escala_hedonica(temp, self.marca_mdias)     
            plot.write_image(
                caminho,
                height = 400,
                width = 600,
                engine = 'kaleido'
            )
            return plot, temp
        

    def grafico_medias_hedonicas_entre_marcas(self, cidade = None):

        caminho = './grafico/overall_liking/comparativo/{}.png'.format(cidade.lower().replace(' ', '_'))

        df = self.criar_dataframe('HEDONICA', False)

        try:
            lista_usuarios = self.cidade_usuario[cidade]
        except:
            se.erro_grafico_parametro_cidade(df)
            return None


        df = df[df['ID_USUARIO'].isin(lista_usuarios)].reset_index(drop = True)
        OL = dict(df.groupby('AMOSTRA')['OVERALL_LIKING'].mean())
        df = df[['ID_USUARIO', 'AMOSTRA'] + self.lista_de_hedonicas[1:]].pivot_table(
            columns = 'AMOSTRA', 
            values = self.lista_de_hedonicas[1:],
            aggfunc = 'mean',
            fill_value = 0).reset_index()

        df.rename({'index' : 'HEDONICA'}, axis = 1, inplace = True)
        for C in df.iloc[:, 1:].columns:
            df[C + 'OL'] = round(OL[C], 2)
            df[C] = round(df[C], 2)


        plot = exec_medias_hedonicas_entre_marcas(df, self.marca_mdias)
        plot.write_image(
            caminho, 
            height = 525,
            width = 1300,
            engine = 'kaleido'
        )
        return plot, df
    
    
    def grafico_marca_preferencia(self, cidade = None):
        
        caminho = './grafico/overall_liking/preferencia/{}.png'.format(cidade.lower().replace(' ', '_'))
        df = self.criar_dataframe('ORDENACAO', False)
        
        try:
            lista_usuarios = self.cidade_usuario[cidade]
        except:
            se.erro_grafico_parametro_cidade(df)
            return None

        df = df[df['ID_USUARIO'].isin(lista_usuarios)].reset_index(drop = True)
        df = df.pivot_table(
            columns = 'RESULTADOS', 
            index = 'AMOSTRA', 
            values = 'ID_USUARIO', 
            aggfunc = 'count', 
            fill_value = 0).reset_index()
        
        df.rename({1 : '1', 2 : '2', 3 : '3', 4 : '4'}, axis = 1, inplace = True)
        df['TOTAL'] = df.iloc[:, 1:].sum(axis = 1)
        for i in df.iloc[:, 1:].columns:
            df[i] = df[i] / df['TOTAL']

        df.drop('TOTAL', axis = 1, inplace = True)

        plot = exec_marca_preferencia(df)
        plot.write_image(
            caminho, 
            height = 500,
            width = 525,
            engine = 'kaleido'
        )

        return plot, df
    
    
    def grafico_histograma_escala_jar(self, atributo = None, cidade = None):

        caminho_plot = './grafico/atributo_jar/histograma/{}_{}.png'.format(
            atributo.lower(), cidade.lower().replace(' ', '_'))
        
        caminho_html = './grafico/atributo_jar/tabela/{}_{}.png'.format(
            atributo.lower(), cidade.lower().replace(' ', '_'))

        df = self.criar_dataframe('HEDONICA', False)

        try:
            lista_usuarios = self.cidade_usuario[cidade]
        except:
            se.erro_grafico_parametro_cidade(df)
            return None

        if atributo not in df.columns:
            se.erro_grafico_parametro_atributo(df)
            return None

        # HISTOGRAMA
        
        df = df[df['ID_USUARIO'].isin(lista_usuarios)].reset_index(drop = True)
        temp = pd.DataFrame({atributo : list(range(1,6))})
        
        for A in df['AMOSTRA'].unique():

            aux = df[df['AMOSTRA'] == A].groupby(atributo)['ID_USUARIO'].nunique().reset_index()
            aux['ID_USUARIO'] = round(aux['ID_USUARIO'] / aux['ID_USUARIO'].sum(), 3)
            aux.columns = [atributo, A]
            temp = temp.merge(aux, on = atributo, how = 'left').fillna(0)
            

        plot = exec_histograma_escala_jar(temp, self.marca_mdias)
        plot.write_image(
            caminho_plot, 
            height = 450,
            width = 600,
            engine = 'kaleido'
        )

        # TABELA

        tabela_html = pd.DataFrame()
        for A in df['AMOSTRA'].unique():
            
            tabela_html = tabela_html.append(pd.DataFrame({
                'AMOSTRA'    : [A.upper()], 
                'Mais Fraco' : [len(df[(df['AMOSTRA'] == A) & (df[atributo].isin([1, 2]))])], 
                'Ideal'      : [len(df[(df.AMOSTRA == A) & (df[atributo] == 3)])], 
                'Mais Forte' : [len(df[(df.AMOSTRA == A) & (df[atributo].isin([4, 5]))])]
            }))
            
        for i in ['Mais Fraco', 'Ideal', 'Mais Forte']:
            tabela_html[i] = (tabela_html[i] / len(df.ID_USUARIO.unique())).apply(lambda x: '{:0.1%}'.format(x))

        html = exec_tabela_escala_jar(tabela_html)
        html.write_image(
            caminho_html,
            height = 150,
            width = 500,
            engine = 'kaleido'
        )

        return plot, html


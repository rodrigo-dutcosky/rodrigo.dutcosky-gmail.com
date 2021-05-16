
def erro_grafico_parametro_atributo(df):
    
    print('ERRO: ATRIBUTO NAO RECONHECIDO.')
    print('')
    print('SUAS OPCOES DE PARAMETROS SAO:')
    print('------------------------------')
    
    for i in df.columns:
        if i not in ['ID_USUARIO', 'AMOSTRA'] and i.find('JAR') == -1:
            print('- {}'.format(i))
            
def erro_grafico_parametro_jar(df):
    
    print('ERRO: ESCALA JAR NAO PRECISA DESTE GRAFICO.')
    print('')
    print('CONTINUE COM UM DESTES PARAMETROS:')
    print('-----------------------------------')
    
    for i in df.columns:
        if i not in ['ID_USUARIO', 'AMOSTRA'] and i.find('JAR') == -1:
            print('- {}'.format(i))


def erro_grafico_parametro_cidade(df):
    
    print('ERRO: NENHUM USUARIO ENCONTRADO PARA ESTA CIDADE.')
    print('')
    print('CHEQUE SUA SINTAXE.')

    
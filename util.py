
import sys

def vazio(path):
    file = open(path, 'r')
    if len(file.read()) == 0:
        print('Arquivo Vazio - Criando arquivo baseado no template')
        file.close()
        file = open(path, 'w')
        file.write('date,value\n')
        file.close()
        return True
    print('File contains data')
    return False


def adicionar_in_file_data(path, value, data):

    try:
        file = open(path, 'a+')
        file.write('%s,%s\n' % ((data),str(value)))
        file.close()
        print('saved successfully in file')
    except:
        print("Error write in file - Unexpected error:", sys.exc_info()[0])
        return False
    return True

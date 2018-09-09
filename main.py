"""
autor: Marcos Vinícius
date: 8 set 2018

modulo de inicalização da GUI e primeiras opções
"""
from PyQt5.QtCore import *
import matplotlib.pylab as plt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *

from util import adicionar_in_file_data, vazio
import pandas as pd

import sys

class Janela_Principal(QDialog):

    # -- construtor da classe de interface principal - main window
    def __init__(self):
        super(Janela_Principal, self).__init__()
        self.createFormGroupBox()

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.formGroupBox)
        self.setLayout(self.mainLayout)

        self.setWindowTitle("Time-Series de Gastos")
        self.resize(400, 300)

    # -- cria as opções iniciais do programa
    def createFormGroupBox(self):

        self.btn_create = QPushButton("CRIAR")
        self.btn_open = QPushButton("ABRIR")
        self.btn_close = QPushButton("EXIT")

        self.formGroupBox = QGroupBox("Form layout")

        layout = QFormLayout()
        layout.addRow(self.btn_create)
        layout.addRow(self.btn_open)
        layout.addRow(self.btn_close)
        layout.setFormAlignment(Qt.AlignCenter)

        self.formGroupBox.setLayout(layout)

        # ações dos botoes
        self.btn_create.clicked.connect(self.criar_file_data)
        self.btn_open.clicked.connect(self.selecionar_file_data)
        self.btn_close.clicked.connect(self.sair)

    # -- scria o arquivo .csv de base de dados
    def criar_file_data(self):

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        name = QFileDialog.getSaveFileName(self, "Local para salvar a base de dados", "",
                                                  "CSV Files (*.csv)", options=options)

        # LOG - brindar o nome do arquivo para selecionar se é csv

        # cria o arquivo
        file = open(name[0], 'w')
        file.close()

        vazio(name[0])

        # crama a outra janela e encerra a atual
        self.interface_principal(name[0])

    # -- seleciona o arquivo .csv de base de dados
    def selecionar_file_data(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        nome, _ = QFileDialog.getOpenFileName(self, "Selecionar Base de dados .csv()", "",
                                                  "csv Files (*.csv)", options=options)
        if nome:
            print(nome)
            # troca de interface para tabls
            self.interface_principal(nome)


    # -- interface para manipulação dos dados do arquivo .csv
    def interface_principal(self, name_file):
        print('em implementação.')

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab_create = QWidget()
        self.tab_view = QWidget()
        self.tab_plot = QWidget()
        self.tabs.resize(500, 400)

        # Add tabs
        self.tabs.addTab(self.tab_create, "Create")
        self.tabs.addTab(self.tab_view, "View")
        self.tabs.addTab(self.tab_plot, "Plot")


        # -------------------------- TAB CREATE ---------------------------
        self.tab_create.layout = QVBoxLayout(self)
        self.createFormGroupBox_CREATE(name_file)
        self.tab_create.layout.addWidget(self.formGroupBox_create)
        self.tab_create.setLayout(self.tab_create.layout)
        # -----------------------------------------------------------------


        # -------------------------- TAB VIEW ---------------------------
        self.tablew_view_csv(name_file)
        # -----------------------------------------------------------------

        # -------------------------- PLOTAR SERIE ---------------------------
        self.gernerate_plot(name_file)
        # -----------------------------------------------------------------

        # adicionando e redimensionado QTabWidget() in main layout

        self.mainLayout.removeWidget(self.formGroupBox)

        self.mainLayout.addWidget(self.tabs)

        self.resize(self.tabs.width(), self.tabs.height())

    # -- cria as opções iniciais do programa
    def createFormGroupBox_CREATE(self, nome_file):


        self.textbox_valor = QLineEdit(self)
        self.date_edit = QDateEdit()
        self.date_edit.setDate(QDate.currentDate())
        self.name_file_data = nome_file

        self.btn_adicionar_info = QPushButton("Adicionar")

        self.formGroupBox_create = QGroupBox("Adicione as informações")
        layout = QFormLayout()
        layout.addRow(QLabel('FILE : '), QLabel(nome_file))
        layout.addRow(QLabel('Valor'), self.textbox_valor)
        layout.addRow(QLabel('Data'), self.date_edit)
        layout.addRow(self.btn_adicionar_info)

        #layout.setFormAlignment(Qt.AlignCenter)

        self.formGroupBox_create.setLayout(layout)


        # ações dos botoes
        self.btn_adicionar_info.clicked.connect(self.salvar_valores)


    def tablew_view_csv(self, nome_file):

        # A table is created with
        self.tableWidget = QTableWidget()

        # atualiza os componentes da tabela
        self.update_table(nome_file)

        self.tab_view.layout = QVBoxLayout(self)
        self.tab_view.layout.addWidget(self.tableWidget)
        self.tab_view.setLayout(self.tab_view.layout)

    # Atualizar valorres da tabela
    def update_table(self, nome_file):
        print('update_table()')

        data = pd.read_csv(nome_file)

        # set row count
        self.tableWidget.setRowCount(data.shape[0] + 1)

        # set column count
        self.tableWidget.setColumnCount(data.shape[1])

        print('Chaves : ', data.columns.values.tolist())

        # adicionando o nome das colunas
        for j, chave in enumerate(data.columns.values.tolist()):
            print('indice', j, ' =', chave)
            self.tableWidget.setItem(0, j, QTableWidgetItem(str(chave)))

        for i in range(1, data.shape[0] + 1):
            for col, chave in enumerate(data.columns.values.tolist()):
                self.tableWidget.setItem(i, col, QTableWidgetItem(str(data.iloc[i - 1][chave])))

        self.tableWidget.resizeColumnsToContents()

    def gernerate_plot(self, nome_file):

        nome_file_plot = 'grafico.png'

        dateparse = lambda dates: pd.datetime.strptime(dates, '%d/%m/%Y')
        data = pd.read_csv(nome_file, parse_dates=['date'], index_col='date', date_parser=dateparse)

        ts = data['value']

        plt.plot(ts)
        plt.savefig(nome_file_plot)

        # Create widget
        label_image = QLabel(self)
        pixmap = QPixmap(nome_file_plot)
        label_image.setPixmap(pixmap)

        self.resize(pixmap.width(),pixmap.height())

        # adiciona os elementos na interface
        self.tab_plot.layout = QVBoxLayout(self)
        self.tab_plot.layout.addWidget(label_image)
        self.tab_plot.setLayout( self.tab_plot.layout)







    # salvar valores de criar arquivo
    def salvar_valores(self):
        print('salvar_valores()')

        if adicionar_in_file_data(self.name_file_data, self.textbox_valor.text(), self.date_edit.text()):
            self.update_table(self.name_file_data)

    # sair da aplicação
    def sair(self):
        sys.exit(dialog.exec_())




if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = Janela_Principal()
    sys.exit(dialog.exec_()) # read in csv and plot with matplotlib in pyqt5
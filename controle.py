from PyQt5 import uic, QtWidgets  # ler  o arquivo ui e o qt para montar os elementos na tela
import sqlite3   # para trabalhar com sqlite

from reportlab.pdfgen import canvas  # para gerar PDF
from reportlab.lib.pagesizes import A4  # importar o tamanho da folha ex. A4

def botao_enviar():
    # o que for digitado no text box
    codigo = formulario.codigo_text.text()  # le o que foi digitado no formulario no codigo e armazena na linha1
    descricao = formulario.descricao_text.text()
    preco = formulario.preco_text.text()
    # o que for escolhido no radio button
    categoria = ""
    if formulario.radio_informatica.isChecked():  # verifica se o radio buttom foi cliclado
        categoria = "informatica"
    elif formulario.radio_alimentos.isChecked():  # elif é quando tem varias escolhas no if
        categoria = "alimentos"
    else:  # se nenhuma das opções acima for esclhida so resta essa
        categoria = "eletronicos"

    # conectando no banco
    try:
        conexao = sqlite3.connect("novo_banco.db")
        cursor = conexao.cursor()

        # inserindo dados no banco
        cursor.execute("INSERT INTO produtos (codigo, descricao, preco, categoria) VALUES (?,?,?,?)",
                       (codigo, descricao, preco, categoria))

        # salvando dados no banco
        conexao.commit()

        # fechando o banco
        conexao.close()
    except ValueError:
        print("Erro ao acessar banco de dados " + ValueError)

    formulario.codigo_text.setText("")
    formulario.descricao_text.setText("")
    formulario.preco_text.setText("")


def botao_listar():
    listar.show()  # chama a segunda tela ( listar_dados)
    try:
        conexao = sqlite3.connect("novo_banco.db")
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM produtos")
        lidos = cursor.fetchall()

        listar.tableWidget.setRowCount(len(lidos))  # exibe a quantidade de linhas contidas em lidos ( tableWidget é o nome do componente )
        listar.tableWidget.setColumnCount(4)  # exibe quantidade de colunas do banco

        for i in range(0, len(lidos)): # le a matriz
            for j in range(0,4):
                listar.tableWidget.setItem(i,j,QtWidgets.QTableWidgetItem(lidos[i][j])) # percorre a matriz e preenche o tableWidget com os dados do banco

        conexao.commit()
        conexao.close()
    except ValueError:
        print("Erro ao acessar banco de dados "+ValueError)

def botao_pdf():
    try:
        conexao = sqlite3.connect("novo_banco.db")
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM produtos")
        lidos = cursor.fetchall()
        y = 0 # cordenada para escrever no pdf , acho que é a linha

        # iniciar codigo para PDF
        pdf = canvas.Canvas("Produtos.pdf", pagesize=A4)  # o nome do arquivo que sera gerado
        pdf.setFont("Times-Bold", 25)  # tipo de letra e tamanho
        pdf.drawString(200, 800, " Produtos Cadastrados :")
        pdf.setFont("Times-Bold", 18)
        pdf.drawString(10, 750, "CODIGO ")
        pdf.drawString(110, 750, "DESCRIÇÃO")
        pdf.drawString(275, 750, "PREÇO")
        pdf.drawString(390, 750, "CATEGORIA")
        for i in range(0,len(lidos)):
            y = y + 50
            pdf.drawString(10, 750 - y, lidos[i][0])
            pdf.drawString(110, 750 - y, lidos[i][1])
            pdf.drawString(275, 750 - y, lidos[i][2])
            pdf.drawString(390, 750 - y, lidos[i][3])

        pdf.save()  # salva o pdf e finaliza o arquivo
        conexao.commit()
        conexao.close()
    except ValueError:
        print("Erro ao acessar banco de dados "+ValueError)




def botao_excluir():
    linha = listar.tableWidget.currentRow() # metodo para saber qual linha foi selecionada na tela grafica gerada
    listar.tableWidget.removeRow(linha)  # remove a linha selecionada ( apenas da parte grafica , nao do banco )
    try:
        conexao = sqlite3.connect("novo_banco.db")
        cursor = conexao.cursor()
        cursor.execute("SELECT codigo FROM produtos")
        lidos = cursor.fetchall()
        valor_id = lidos[linha][0]
        print("Registro :",valor_id)
        print("lidos: ",lidos)
        cursor.execute("DELETE FROM produtos WHERE codigo="+valor_id)

    except ValueError:
        print("Erro ao acessar banco de dados "+ValueError)


def botao_alterar():
    print("Atlerar")


#=============================================================================================

app = QtWidgets.QApplication([])  # obejeto app para criar a aplicação
formulario = uic.loadUi("formulario.ui")  # objeto formulario para carregar o arquivo de tela criado
listar = uic.loadUi("listar_dados.ui")  # objeto listar_dados para carregar a segunda tela listar_dados

# botoes
formulario.botao_enviar.clicked.connect(
    botao_enviar)  # objeto criado para quando clicar no botão -> executar a função ( não pode ter os "()" no fim .
formulario.botao_listar.clicked.connect(botao_listar)
listar.botao_pdf.clicked.connect(botao_pdf)
listar.botao_excluir.clicked.connect(botao_excluir)
listar.botao_alterar.clicked.connect(botao_alterar)

formulario.show()
app.exec()

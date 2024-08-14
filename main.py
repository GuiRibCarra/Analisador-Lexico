import tkinter.filedialog
import tkinter.messagebox
from tkinter import *


def abrir_arq():
    bloco.delete('0.0',END)
    tabela.delete(0,END)
    arq = tkinter.filedialog.askopenfilename()

    if('.txt' in arq):
        arq_a = open(arq,'r')
        conteudo = arq_a.read()
        bloco.insert(END,conteudo)

    else:
        tkinter.messagebox.showerror(title="ERROR",message="Tipo de Arquivo selecinado não é .txt, selecione novamente")
        print('erro')

def salvar_arq():
    tabela.delete(0, END)
    tipo = [('.txt', '*.txt')]
    arq = tkinter.filedialog.asksaveasfile(mode='w',filetypes=tipo,defaultextension=".txt")
    arq.write(bloco.get('0.0',END))


def numeros_I_R(texto,posicao):
  tamanho = len(texto)-1
  if posicao == tamanho:
      numero = texto[posicao]
      tipo = 'NUMERO_INTEIRO'
      return numero,posicao,tipo

  tamanho_max = 15
  tamanho_n = 1
  tamanho_c = 1
  for i in range(posicao,tamanho):
    if texto[i] in numeros:
      numero = texto[i]
      j = i+1
      while texto[j] in numeros:
        numero = numero + texto[j]
        j = j+1
        tamanho_n = tamanho_n + 1
        if j == tamanho:
          numero = numero + texto[j]
          break
      if texto[j] == '.':
        numero = numero + texto[j]
        k = j+1
        while texto[k] in numeros:
          numero = numero + texto[k]
          k = k+1
          tamanho_c = tamanho_c + 1
        if tamanho_c > tamanho_max or tamanho_n > tamanho_max:
            tipo = 'NUMERO MAIOR QUE O LIMITE'
            return numero, k, tipo
        tipo = 'NUMERO_REAL'
        return numero,k,tipo
      if tamanho_n > tamanho_max:
          tipo = 'NUMERO MAIOR QUE O LIMITE'
          return numero, j, tipo
      tipo = 'NUMERO_INTEIRO'
      return numero,j,tipo

def especiais(texto,posicao):
  tamanho = len(texto)
  for i in range(posicao,tamanho):
    if texto[i] in c_especiais:
      if texto[i] == '(':
        tipo = 'ABRE_PARENTESES'
        especi = '('
        return especi,i,tipo
      if texto[i] == ')':
        tipo = 'FECHA_PARENTESES'
        especi = ')'
        return especi,i,tipo
      if texto[i] == '+':
        tipo = 'OP_SOMA'
        especi = '+'
        return especi,i,tipo
      if texto[i] == '-':
        tipo = 'OP_SUBTRACAO'
        especi = '-'
        return especi,i,tipo
      if texto[i] == '*':
        tipo = 'OP_MULTIPLICACAO'
        especi = '*'
        return especi,i,tipo
      if texto[i] == '/':
        tipo = 'OP_DIVISAO'
        especi = '/'
        return especi,i,tipo
      if texto[i] == '.':
        tipo = 'PONTO_MAL_USADO'
        especi = '.'
        return especi,i,tipo
  return None, None, None

def imprimirAnalise():
    tabela.delete(0,END)
    texto = bloco.get('1.0',END)
    terminou = False
    i = 0
    linha = 1
    while terminou == False:
        if i == len(texto):
            terminou = True
            break
        if texto[i] == ' ':
            i = i + 1
        elif texto[i] == '\n':
            i = i + 1
            linha = linha + 1
        elif texto[i] == ',' and texto[i-1] in numeros and texto[i+1] in numeros:
            tabela.insert(END,'Utilize o "." ao invés da "virgula "'+' -> LINHA:'+str(linha))
            tabela.itemconfig(END, {'bg': 'yellow'})
            i = i + 1
        elif texto[i] not in numeros and texto[i] not in c_especiais:
            tabela.insert(END,texto[i] + ' ->  ERROR_NÃO_ESTA_NO_ALFABETO'+' -> LINHA:'+str(linha))
            tabela.itemconfig(END, {'bg':'red'})
            i = i + 1
        elif texto[i] in numeros:
            numero, j, tipo = numeros_I_R(texto, i)
            tabela.insert(END,numero + ' -> ' + tipo+' -> LINHA:'+str(linha))
            if tipo == 'NUMERO MAIOR QUE O LIMITE':
                tabela.itemconfig(END, {'bg': 'yellow'})
            else:
                tabela.itemconfig(END, {'bg': '#00FF7F'})
            i = j
        elif texto[i] in c_especiais:
            numero, k, tipo = especiais(texto, i)
            i = k + 1
            tabela.insert(END,numero + ' -> ' + tipo+' -> LINHA:'+str(linha))
            tabela.itemconfig(END, {'bg': '#00FF7F'})

numeros=['0','1','2','3','4','5','6','7','8','9']
c_especiais = ['(',')','+','-','*','/','.']

janela = Tk()
janela.title("Analisador Lexico")
janela.geometry("900x400")
janela.config(background='#BA55D3')

bloco = Text(janela, width=60, height=20)
bloco.grid(column=0,row=0,padx=5,pady=5)

numeracao = Text(janela,)

tabela = Listbox(janela,height=20,width=60)
tabela.grid(column=1,row=0,padx=5,pady=5)


botao = Button(janela, text="Analisar", command = imprimirAnalise)
botao.grid(column=1, row=1, padx=0, pady=0)

menu = Menu(janela)
menu_arq = Menu(menu)
menu_arq.add_command(label='Abrir .txt',command=abrir_arq)
menu_arq.add_command(label='Salvar .txt',command=salvar_arq)
menu.add_cascade(label='Arquivo',menu=menu_arq)

janela.config(menu = menu)
janela.mainloop()
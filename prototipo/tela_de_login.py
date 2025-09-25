import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class Tela:
    def __init__(self, master):
        self.janela = master
        self.janela.geometry("500x300")
        self.janela.title('Tela de Login com layout grid')

        self.lbl_usuario = ttk.Label(self.janela, text="Usuário:")
        self.lbl_usuario.grid(column=0, row=0, sticky=W, padx=5, pady=5)

        self.ent_usuario = ttk.Entry(self.janela)
        self.ent_usuario.grid(column=1, row=0, sticky=E, padx=5, pady=5)

        self.lbl_senha = ttk.Label(self.janela, text="Senha:")
        self.lbl_senha.grid(column=0, row=1, sticky=W, padx=5, pady=5)

        self.ent_senha = ttk.Entry(self.janela, show="*")
        self.ent_senha.grid(column=1, row=1, sticky=E, padx=5, pady=5)

        # Cria um Frame para agrupar os botões
        self.frm_botoes = ttk.Frame(self.janela)
        self.frm_botoes.grid(column=1, row=2, columnspan=2, pady=5)

        # Botão de Login dentro do Frame
        self.btn_login = ttk.Button(self.frm_botoes, text="Entrar", bootstyle="primary")
        self.btn_login.pack(side=LEFT, padx=5)

        # Botão de Cadastrar ao lado do botão de Login
        self.btn_cadastrar = ttk.Button(self.frm_botoes, text="Cadastrar", bootstyle="primary")
        self.btn_cadastrar.pack(side=LEFT)



        self.centraliza(self.janela)
    def centraliza(self, master):
        # Criar uma forma de centralizar a janela

        largura_monitor = master.winfo_screenwidth()
        altura_monitor = master.winfo_screenheight()
        master.update_idletasks()
        largura_janela = master.winfo_width()
        altura_janela = master.winfo_height()
        x = largura_monitor // 2 - largura_janela // 2
        y = altura_monitor //2 - altura_janela // 2
        master.geometry(f'{largura_janela}x{altura_janela}+{x}+{y}')

app = ttk.Window(themename='darkly')
Tela(app)
app.mainloop()
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
#import control

class Tela:
    def __init__(self, master):
        self.janela = master
        self.janela.geometry("240x110")
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
        
        self.btn_remover = ttk.Button(self.frm_botoes, text="remover", bootstyle="primary")
        self.btn_remover.pack(side=LEFT)
        
        self.btn_pesquisar = ttk.Button(self.frm_botoes, text="pesquisar", bootstyle="primary")
        self.btn_pesquisar.pack(side=LEFT)

app = ttk.Window(themename='darkly')
Tela(app)
app.mainloop()
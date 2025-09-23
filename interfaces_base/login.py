import tkinter as tk
janela = tk.Tk()
janela.geometry("240x110")
janela.title('Tela de Login com layout grid')
janela.resizable(0, 0)

lbl_usuario = tk.Label(janela, text="Usuário:")
lbl_usuario.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)

ent_usuario = tk.Entry(janela)
ent_usuario.grid(column=1, row=0, sticky=tk.E, padx=5, pady=5)

lbl_senha = tk.Label(janela, text="Senha:")
lbl_senha.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)

ent_senha = tk.Entry(janela, show="*")
ent_senha.grid(column=1, row=1, sticky=tk.E, padx=5, pady=5)

btn_login = tk.Button(janela, text="Entrar")
btn_login.grid(column=1, row=2, sticky=tk.W, padx=5, pady=5)

janela.mainloop()
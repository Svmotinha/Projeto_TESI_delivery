import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import sqlite3
import json

class TelaPedidosAdmin:
    def __init__(self, master, conn, cursor):
        self.janela = master
        self.conn = conn
        self.cursor = cursor
        self.janela.title("Gerenciamento de Pedidos")
        self.janela.geometry("900x600")
        self.janela.grab_set()

        self.main_frame = ttk.Frame(self.janela)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.frm_lista = ttk.Labelframe(self.main_frame, text="Pedidos Ativos")
        self.frm_lista.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        self.frm_detalhes = ttk.Labelframe(self.main_frame, text="Detalhes e Ações")
        self.frm_detalhes.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        self.tree = ttk.Treeview(self.frm_lista, columns=('ID', 'Cliente', 'Data', 'Total', 'Status'), show='headings', bootstyle="info")
        self.tree.heading('ID', text='ID')
        self.tree.heading('Cliente', text='Cliente')
        self.tree.heading('Data', text='Data')
        self.tree.heading('Total', text='Total (R$)')
        self.tree.heading('Status', text='Status')

        self.tree.column('ID', width=40, anchor=CENTER)
        self.tree.column('Cliente', width=150)
        self.tree.column('Data', width=130)
        self.tree.column('Total', width=80, anchor=E)
        self.tree.column('Status', width=100)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind('<<TreeviewSelect>>', self.mostrar_detalhes)
        
        self.criar_widgets_detalhes()
        self.carregar_pedidos()
        self.centraliza(self.janela)

    def criar_widgets_detalhes(self):
        self.detalhes_texto = tk.Text(self.frm_detalhes, height=10, state=tk.DISABLED, font=("Courier", 9))
        self.detalhes_texto.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.frm_acoes = ttk.Frame(self.frm_detalhes)
        self.frm_acoes.pack(fill=tk.X, padx=10, pady=10)

        self.lbl_mudarStatus = ttk.Label(self.frm_acoes, text="Mudar status para:")
        self.lbl_mudarStatus.pack(side=tk.LEFT)
        
        self.status_var = tk.StringVar()
        self.combobox_status = ttk.Combobox(self.frm_acoes, textvariable=self.status_var, state='readonly',
                                            values=["Em produção", "Saiu para entrega", "Finalizado"])
        self.combobox_status.pack(side=tk.LEFT, padx=5)
        
        self.btn_atualizar = ttk.Button(self.frm_acoes, text="Atualizar Status", bootstyle="success", command=self.atualizar_status, state=tk.DISABLED)
        self.btn_atualizar.pack(side=tk.LEFT)

        self.btn_historico = ttk.Button(self.frm_detalhes, text="Ver Pedidos Finalizados", bootstyle="secondary", command=self.abrir_historico_admin)
        self.btn_historico.pack(pady=10)

    def carregar_pedidos(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        try:
            sql = """
                SELECT p.id, u.nome, p.data_pedido, p.total, p.status
                FROM pedidos p
                JOIN usuarios u ON p.usuario_id = u.id
                WHERE p.status != 'Finalizado'
                ORDER BY p.id ASC
            """
            self.cursor.execute(sql)
            for p in self.cursor.fetchall():
                self.tree.insert('', tk.END, values=(p[0], p[1], p[2], f"{p[3]:.2f}", p[4]))
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível carregar os pedidos: {e}", parent=self.janela)
    
    def mostrar_detalhes(self, event):
        item_selecionado = self.tree.selection()
        if not item_selecionado: 
            self.btn_atualizar.config(state=tk.DISABLED)
            self.status_var.set('')
            return

        self.btn_atualizar.config(state=tk.NORMAL)
        valores = self.tree.item(item_selecionado, 'values')
        pedido_id = valores[0]
        status_atual = valores[4]
        self.status_var.set(status_atual)
        
        self.detalhes_texto.config(state=tk.NORMAL)
        self.detalhes_texto.delete('1.0', tk.END)
        try:
            self.cursor.execute("SELECT produtos FROM pedidos WHERE id=?", (pedido_id,))
            produtos_json = self.cursor.fetchone()[0]
            produtos_dict = json.loads(produtos_json)

            texto_detalhes = ""
            for prod_id, detalhes in produtos_dict.items():
                nome = detalhes.get('nome', 'N/A')
                qtd = detalhes.get('qtd', '?')
                texto_detalhes += f"{nome:<30} Qtd: {qtd}\n"

            self.detalhes_texto.insert('1.0', texto_detalhes)
        except Exception as e:
            self.detalhes_texto.insert('1.0', f"Erro ao carregar detalhes: {e}")
        self.detalhes_texto.config(state=tk.DISABLED)

    def atualizar_status(self):
        item_selecionado = self.tree.selection()
        if not item_selecionado:
            messagebox.showwarning("Aviso", "Nenhum pedido selecionado.", parent=self.janela)
            return

        pedido_id = self.tree.item(item_selecionado, 'values')[0]
        novo_status = self.status_var.get()
        if not novo_status:
            messagebox.showwarning("Aviso", "Selecione um status.", parent=self.janela)
            return
            
        try:
            self.cursor.execute("UPDATE pedidos SET status=? WHERE id=?", (novo_status, pedido_id))
            self.conn.commit()
            messagebox.showinfo("Sucesso", "Status do pedido atualizado!", parent=self.janela)
            self.carregar_pedidos()
            
            self.detalhes_texto.config(state=tk.NORMAL)
            self.detalhes_texto.delete('1.0', tk.END)
            self.detalhes_texto.config(state=tk.DISABLED)
            self.status_var.set('')
            self.btn_atualizar.config(state=tk.DISABLED)

        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível atualizar o status: {e}", parent=self.janela)

    def abrir_historico_admin(self):
        top_historico = ttk.Toplevel(self.janela)
        TelaHistoricoAdmin(top_historico, self.conn, self.cursor)

    def centraliza(self, master):
        largura_monitor = master.winfo_screenwidth()
        altura_monitor = master.winfo_screenheight()
        master.update_idletasks()
        largura_janela = master.winfo_width()
        altura_janela = master.winfo_height()
        x = largura_monitor // 2 - largura_janela // 2
        y = altura_monitor // 2 - altura_janela // 2
        master.geometry(f'{largura_janela}x{altura_janela}+{x}+{y}')

class TelaHistoricoAdmin:
    def __init__(self, master, conn, cursor):
        self.janela = master
        self.conn = conn
        self.cursor = cursor
        self.janela.title("Histórico de Pedidos Finalizados")
        self.janela.geometry("800x500")
        self.janela.grab_set()

        self.lbl_titulo = ttk.Label(self.janela, text="Pedidos Finalizados", font=("Arial", 16, "bold"))
        self.lbl_titulo.pack(pady=10)

        self.tree = ttk.Treeview(self.janela, columns=('ID', 'Cliente', 'Data', 'Total'), show='headings', bootstyle="success")
        self.tree.heading('ID', text='ID')
        self.tree.heading('Cliente', text='Cliente')
        self.tree.heading('Data', text='Data')
        self.tree.heading('Total', text='Total (R$)')
        
        self.tree.column('ID', width=50, anchor=CENTER)
        self.tree.column('Cliente', width=200)
        self.tree.column('Data', width=150)
        self.tree.column('Total', width=100, anchor=E)
        
        self.tree.pack(fill=BOTH, expand=True, padx=10, pady=10)

        self.carregar_pedidos_finalizados()
        self.centraliza(self.janela)

    def carregar_pedidos_finalizados(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        try:
            sql = """
                SELECT p.id, u.nome, p.data_pedido, p.total
                FROM pedidos p
                JOIN usuarios u ON p.usuario_id = u.id
                WHERE p.status = 'Finalizado'
                ORDER BY p.id DESC
            """
            self.cursor.execute(sql)
            for p in self.cursor.fetchall():
                self.tree.insert('', END, values=(p[0], p[1], p[2], f"{p[3]:.2f}"))
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível carregar o histórico: {e}", parent=self.janela)

    def centraliza(self, master):
        largura_monitor = master.winfo_screenwidth()
        altura_monitor = master.winfo_screenheight()
        master.update_idletasks()
        largura_janela = master.winfo_width()
        altura_janela = master.winfo_height()
        x = largura_monitor // 2 - largura_janela // 2
        y = altura_monitor // 2 - altura_janela // 2
        master.geometry(f'{largura_janela}x{altura_janela}+{x}+{y}')

# --- Bloco para Teste (pode ser removido ao integrar) ---
if __name__ == '__main__':
    app = ttk.Window(themename="darkly")
    app.title("Teste do Painel de Pedidos Admin")
    
    # Simula a conexão com o banco de dados
    try:
        conn = sqlite3.connect("Entregai.db")
        cursor = conn.cursor()

        # Botão para abrir a tela de gerenciamento de pedidos
        btn_abrir_pedidos = ttk.Button(app, text="Abrir Gerenciador de Pedidos", 
                                       command=lambda: TelaPedidosAdmin(ttk.Toplevel(app), conn, cursor))
        btn_abrir_pedidos.pack(pady=50, padx=50)

    except Exception as e:
        lbl_erro = ttk.Label(app, text=f"Erro ao conectar ao DB: {e}")
        lbl_erro.pack(pady=50, padx=50)

    app.mainloop()

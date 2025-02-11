import tkinter as tk
from tkinter import ttk, messagebox
import threading
import os
from PIL import Image, ImageTk
from tkinterdnd2 import DND_FILES, TkinterDnD
import sys
import core as c
from logger import logger

class CustomButton(tk.Button):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(relief=tk.FLAT, bg="#FD9E40", activebackground="#fa8b1e", bd=0.3)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, event=None):
        self.configure(bg="#fa8b1e")

    def on_leave(self, event=None):
        self.configure(bg="#FD9E40")

class Application(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()
        self.title("Syncatalog - CGU")
        self.setup_window()
        #self.load_images()
        self.create_widgets()
        #self.setup_drag_and_drop()
        
        self.utils = c.utils()
        self.send = c.send()
        self.log = logger()
        self.filepath = ""
        self.loading_window = None
        #self.existing_data = self.get_existing_data()

    def setup_window(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width, window_height = 280, 150
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.resizable(False, False)
        self.configure(bg='#FFBF48')
        #messagebox.showinfo("s", os.path.join(os.path.abspath("."), "logo_sr.ico"))
        #self.iconbitmap(os.path.join(os.path.abspath("."), "logo_sr.ico"))
        

    def load_images(self):
        self.square_photo = self.load_image("logo_sr.png")

    def load_image(self, filename):
        return ImageTk.PhotoImage(Image.open(self.resource_path(filename)))

    def create_widgets(self):
        #self.create_labels()
        self.create_buttons()

    def create_labels(self):

        self.label = tk.Label(
            self, 
            text="Sincronizar clientes",
            font=("Arial", 12),
            bg="#FFBF48"
        )
        self.label.place(relx=0.05, rely=0.1)

    def create_buttons(self):
        self.btn_clientes = CustomButton(
            self, 
            text="Sincronizar Clientes", 
            command=self.clients, 
            font=("Arial", 12)
        )
        self.btn_clientes.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.3)

        # self.btn_productos = CustomButton(
        #     self, 
        #     text="Sincronizar Productos", 
        #     command=self.products, 
        #     font=("Arial", 12)
        # )
        # self.btn_productos.place(relx=0.1, rely=0.5, relwidth=0.8, relheight=0.3)

    def products(self):

        self.show_loading_window()
        #self.btn_productos.config(state="disabled")
        self.btn_clientes.config(state="disabled")
        #self.btn_imagen.config(state="disabled")
        threading.Thread(target=self.run_process, daemon=True).start()
    
    def clients(self):
        self.show_loading_window()
        self.btn_clientes.config(state="disabled")
        #self.btn_productos.config(state="disabled")
        #self.btn_imagen.config(state="disabled")
        threading.Thread(target=self.run_processclient, daemon=True).start()

    def show_loading_window(self):
        self.loading_window = tk.Toplevel(self)
        self.loading_window.title("Enviando")
        self.loading_window.geometry("200x100")
        #self.loading_window.iconbitmap(self.resource_path("logo_sr.ico"))
        self.loading_window.resizable(False, False)
        self.loading_window.configure(bg='#FFBF48')
        self.center_window(self.loading_window, 200, 50)
        self.loading_window.transient(self)
        self.loading_window.grab_set()
        
        self.progress_bar = ttk.Progressbar(self.loading_window, mode='indeterminate')
        self.progress_bar.pack(expand=True, padx=10, pady=15)
        self.progress_bar.start()

    def center_window(self, window, width, height):
        x = self.winfo_x() + (self.winfo_width() - width) // 2
        y = self.winfo_y() + (self.winfo_height() - height) // 2
        window.geometry(f"{width}x{height}+{x}+{y}")

    def run_process(self):
        try:
            self.send.process()
            #self.existing_data = self.get_existing_data()
        except Exception as e:
            self.log.write_to_log(f"(run_process) - Se produjo un error: {str(e)}")
        finally:
            self.after(0, self.reset_ui)
    
    def run_processclient(self):
        try:
            self.send.processclient()
            #self.existing_data = self.get_existing_data()
        except Exception as e:
            self.log.write_to_log(f"(run_processclient) - Se produjo un error: {str(e)}")
        finally:
            self.after(0, self.reset_ui)

    def reset_ui(self):
        if hasattr(self, 'progress_bar'):
            self.progress_bar.stop()
        if hasattr(self, 'loading_window'):
            self.loading_window.destroy()
        # self.label.config(text="\n\n\n\nArrastra y suelta archivos aquí")
        # self.filepath = ""
        #self.btn_productos.config(state="normal")
        self.btn_clientes.config(state="normal")
        # self.btn_imagen.config(state="normal")

    # def open_grid_window(self):
    #     self.grid_window = tk.Toplevel(self)
    #     self.grid_window.title("Editar Grilla")
    #     self.grid_window.resizable(False, False)
    #     self.grid_window.configure(bg='#FFBF48')

    #     width, height = 250, 300
    #     self.center_window(self.grid_window, width, height)
        
    #     self.grid_window.transient(self)
    #     self.grid_window.grab_set()
        
    #     self.setup_treeview_style()
    #     self.create_treeview()
    #     self.create_save_button()
        
    #     self.load_existing_data()

    # def setup_treeview_style(self):
    #     style = ttk.Style()
    #     style.theme_use("default")
    #     style.configure(
    #         "Custom.Treeview",
    #         background="#ffffff",
    #         foreground="black",
    #         rowheight=25,
    #         fieldbackground="#ffffff",
    #         bordercolor="#999999",
    #         borderwidth=1
    #     )
    #     style.map('Custom.Treeview', 
    #               background=[('selected', '#dbd7d7')], 
    #               foreground=[('selected', 'black')])
    #     style.configure(
    #         "Custom.Treeview.Heading",
    #         background="#b3b1b1",
    #         foreground="black",
    #         font=("Arial", 12, "bold"),
    #         relief="flat"
    #     )
    #     style.map("Custom.Treeview.Heading",
    #               relief=[('active', 'groove'), ('pressed', 'sunken')])

    # def create_treeview(self):
    #     self.tree = ttk.Treeview(
    #         self.grid_window, 
    #         columns=("EXCEL", "SOFT"), 
    #         show='headings', 
    #         style="Custom.Treeview"
    #     )
    #     for col in ("EXCEL", "SOFT"):
    #         self.tree.heading(col, text=col)
    #         self.tree.column(col, width=100, anchor='center')
    #     self.tree.pack(expand=True, fill='both', padx=10)
    #     self.tree.bind("<Double-1>", self.on_double_click)
    #     self.tree.bind("<Return>", self.on_return)
    #     self.tree.bind("<FocusOut>", self.on_focus_out)

    # def load_existing_data(self):
    #     if self.existing_data:
    #         for item in self.existing_data:
    #             status = "nuevo" if item['bd'] != "viejo" else item['bd']
    #             self.tree.insert('', 'end', values=(item['excel'], item['soft'], status))
    #     self.tree.insert('', 'end', values=("", "", "nuevo"))

    # def get_existing_data(self):
    #     try:
    #         return self.send.getCodigobalanza()
    #     except AttributeError:
    #         self.log.write_to_log("Error: self.send.getCodigobalanza() no está disponible")
    #         return []
    #     except Exception as e:
    #         self.log.write_to_log(f"Error al obtener datos preexistentes: {str(e)}")
    #         return []
        
    # def create_save_button(self):
    #     self.btn_guardar = CustomButton(self.grid_window, text="Aceptar", command=self.save_values)
    #     self.btn_guardar.pack(pady=2)

    # def on_double_click(self, event):
    #     region = self.tree.identify("region", event.x, event.y)
    #     if region == "cell":
    #         column = self.tree.identify_column(event.x)
    #         row = self.tree.identify_row(event.y)
    #         item = self.tree.item(row)
    #         values = item['values']
    #         if len(values) > 2 and values[2] == "nuevo":
    #             self.edit_cell(row, column)
    #         else:
    #             print("No se puede editar esta fila.")

    # def edit_cell(self, row, column):
    #     x, y, width, height = self.tree.bbox(row, column)
    #     value = self.tree.set(row, column)
        
    #     self.entry = ttk.Entry(self.tree, width=width)
    #     self.entry.place(x=x, y=y, width=width, height=height)
    #     self.entry.insert(0, value)
    #     self.entry.focus_set()
    #     self.entry.bind("<Return>", lambda e: self.set_cell_value(e, row, column))
    #     self.entry.bind("<FocusOut>", lambda e: self.set_cell_value(e, row, column))

    # def set_cell_value(self, event, row, column):
    #     value = self.entry.get()
    #     self.tree.set(row, column, value)
    #     self.entry.destroy()
    #     self.check_and_add_row()

    # def check_and_add_row(self):
    #     last_item = self.tree.get_children()[-1]
    #     values = self.tree.item(last_item)['values']
    #     if values and all(values):
    #         self.tree.insert('', 'end', values=("", "", "nuevo"))

    # def on_return(self, event):
    #     row_id = self.tree.focus()
    #     column = self.tree.identify_column(event.x)
    #     self.edit_cell(row_id, column)

    # def on_focus_out(self, event):
    #     if hasattr(self, 'entry') and self.entry.winfo_exists():
    #         self.entry.destroy()

    # def save_values(self):
    #     self.existing_data = self.send.guardar_valores(self.tree)
    #     self.grid_window.destroy()

    @staticmethod
    def resource_path(relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)
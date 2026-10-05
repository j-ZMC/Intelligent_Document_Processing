#Libreria de interfaz grafica: https://customtkinter.tomschimansky.com/documentation/
import customtkinter as ctk
#Documentos Locales
from graphical_interface.home import pagina_principal

# Crea la ventana principal, asigna el tamano inicial, nombre de la ventana
# Crea una ventana place holder, llama a la ventana home, mantiene la ventana revisando los inputs
root = ctk.CTk()
root.geometry("1920x1080")
root.title("Intelligent Document Processing")
frame = ctk.CTkFrame(master=root)

pagina_principal(root, frame)

root.mainloop()

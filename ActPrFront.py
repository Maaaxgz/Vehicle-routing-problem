import tkinter as tk
from tkinter import filedialog
import ActPr as backend

def ver_mapa():
    backend.mostrar_mapa()

def ver_ruta_inicial():
    backend.mostrar_ruta_i()

def ver_ruta_final():
    backend.mostrar_ruta_f()

def main():
    global boton__ruta_i, boton_ruta_f
    winPrin = tk.Tk()
    winPrin.title("Proyecto - VRP Solver")
    winPrin.geometry('500x300+600+200')
    winPrin['background'] = '#2C3639'
    winPrin.resizable(False, False)

    texto = tk.Label(winPrin, text="Problema del Enrutamiento del Vehículo", font="arial 14 bold", bg='#2C3639', fg='#DCD7C9')
    texto.pack(padx=20,pady=20)
    texto = tk.Label(winPrin, text="¿Qué quieres hacer?", font="arial 11 bold italic", bg='#2C3639', fg='#DCD7C9')
    texto.pack(pady=10)

    boton_ver = tk.Button(winPrin, text="Ver mapa a utilizar", font="arial 11" , bg="#A27B5C", fg="white" ,command=ver_mapa)
    boton_ver.pack(pady=7)
    boton_ruta_i = tk.Button(winPrin, text="Generar ruta inicial", font="arial 11" , bg="#A27B5C", fg="white", command=ver_ruta_inicial)
    boton_ruta_i.pack(pady=7)
    boton_ruta_f = tk.Button(winPrin, text="Generar ruta final", font="arial 11" , bg="#A27B5C", fg="white", command=ver_ruta_final)
    boton_ruta_f.pack(pady=7)

    winPrin.mainloop()

    boton_ruta_i, boton_ruta_f = None, None

if __name__ == "__main__":
    main()

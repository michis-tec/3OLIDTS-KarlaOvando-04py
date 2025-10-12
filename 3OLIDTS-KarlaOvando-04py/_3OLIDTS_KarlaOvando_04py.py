import tkinter as tk
from tkinter import messagebox
import re
import mysql.connector

def insertarRegistro(nombre, apellidos, edad, telefono, estatura, genero):
    try:
        conexion = mysql.connector.Connect(
            host="Localhost",
            user="root",
            password="1234",
            database="Formulario",
            port="3306"
            )
        cursor= conexion.cursor()
        stringQuery = "INSERT INTO resgistros (nombre, apellidos, estatura, edad, telefono, genero) VALUES (%s, %s, %s, %s, %s, %s)"
        valores = nombre, apellidos, telefono, estatura, edad, genero
        cursor.execute(stringQuery,valores)
        conexion.commit()
        cursor.close()
        messagebox.showinfo("insercion correcta", "datos guardados con exito")
    except mysql.connector.Error as err:
        messagebox.showerror("error en la conexion", f"error al insertar datos: {err}")

def limpiar_campos():
    entry_nombres.delete(0, tk.END)
    entry_apellidos.delete(0, tk.END)
    entry_edad.delete(0, tk.END)
    entry_estatura.delete(0, tk.END)
    entry_telefono.delete(0, tk.END)
    var_genero.set(0)

def borrar_campos():
    limpiar_campos()

def guardar_datos():
    #obtener los datos de los campos
    nombres = entry_nombres.get()
    apellidos = entry_apellidos.get()
    edad = entry_edad.get()
    estatura = entry_estatura.get()
    telefono = entry_telefono.get()


    #obtener el genero seleccionado
    genero = ""
    if var_genero.get() == 1:
        genero = "Hombre"
    elif var_genero.get() == 2:
        genero = "Mujer"

    #validar que los campos tengan el formato correcto
    if (es_entero_valido(edad) and es_decimal_valido(estatura) and
        es_entero_valido_de_10_digitos(telefono) and es_texto_valido(nombres) and es_texto_valido(apellidos)):
        #crear una cadena con los datos
        datos = f"Nombres: {nombres}\nApellidos: {apellidos}\nEdad: {edad} anos\nEstatura: {estatura} cm\nTelefono: {telefono}\nGenero: {genero}"

        #guardar los datos en un archivo de texto
        with open("datos.txt", "a") as archivo:
            archivo.write(datos + "\n\n")
            insertarRegistro(nombres, apellidos, edad, estatura, telefono, genero)
            messagebox.showinfo("informacion", "datos guadados con exito: \n\n"+datos)
            limpiar_campos()
    else:
        messagebox.showerror("Error", "algunos de los campos tienen formato equivocado")


def es_entero_valido(valor):
    try:
        int(valor)
        return True
    except ValueError:
        messagebox.showerror("Error edad", "valor de edad equivocado")
        return False

def es_decimal_valido(valor):
    try:
        float(valor)
        return True
    except ValueError:
        return False

def es_entero_valido_de_10_digitos(valor):
    return valor.isdigit() and len(valor) == 10

def es_texto_valido(valor):
    return bool(re.match("^[a-zA-Z\s]+$", valor))

#crear la ventana principal
ventana = tk.Tk()
ventana.title("Formulario vr.003")
ventana.geometry("300x400")

#crear variables paraa los radiobutton
var_genero = tk.IntVar()

#crear etiquetas y campos de entrada
label_nombres = tk.Label(ventana, text="Nombres:")
label_nombres.pack()
entry_nombres = tk.Entry(ventana)
entry_nombres.pack()

label_apellidos = tk.Label(ventana, text="Apellidos:")
label_apellidos.pack()
entry_apellidos = tk.Entry(ventana)
entry_apellidos.pack()

label_edad = tk.Label(ventana, text="Edad:")
label_edad.pack()
entry_edad = tk.Entry(ventana)
entry_edad.pack()

label_estatura = tk.Label(ventana, text="Estatura:")
label_estatura.pack()
entry_estatura = tk.Entry(ventana)
entry_estatura.pack()

label_telefono = tk.Label(ventana, text="Telefono:")
label_telefono.pack()
entry_telefono = tk.Entry(ventana)
entry_telefono.pack()

label_genero = tk.Label(ventana, text="Genero: ")
label_genero.pack()

rb_hombre = tk.Radiobutton(ventana, text="Hombre", variable=var_genero, value=1)
rb_hombre.pack()

rb_mujer = tk.Radiobutton(ventana, text="Mujer", variable=var_genero, value=2)
rb_mujer.pack()

#boton para guaradr datos
btn_guardar = tk.Button(ventana, text="Guardar", command=guardar_datos)
btn_guardar.pack()

#boton para borrar campos
btn_borrar = tk.Button(ventana, text="Borrar campos", command=limpiar_campos)
btn_borrar.pack()

#iniciar la aplicacion
ventana.mainloop()
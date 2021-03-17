#CREANDO INTERFAZ USUARIO CON TKINTER Y SOCKETS
#JULIAN GIRALDO CARDONA - LUIS ZULUAGA - JUAN DAVID ALVAREZ
###################UTP###############################

#IMPORTAMOS LIBRERÍAS NECESARIAS.
from Tkinter import *
import os
import socket


#CREAMOS VENTANA PRINCIPAL.
def ventana_inicio():
    global ventana_principal#DEFINIMOS VENTANA PRINCIPAL
    global sala#CREAMOS VARIABLE GLOBAL PARA ETIQUETAR UNA SALA
    sala='lobby'#LA SALA PRINCIPAL SE LLAMA LOBBY
    pestas_color="LightBlue"#SE DEFINE EL COLOR DE CADA PESTAÑA
    ventana_principal=Tk()#SE INICIALIZA LA VENTANA PRINCIPAL CON TKINTER
    ventana_principal.geometry("300x250")#DIMENSIONES DE LA VENTANA
    ventana_principal.title("Chat Online")#TITULO DE LA VENTANA
    Label(text="Chat Online \n Julian G | Juan Alvarez | Luis Zuluaga", bg="BlueViolet", width="300", height="2", font=("Calibri", 13)).pack() # SE CREA UN TITULO
    Label(text="").pack()#EL METODO PACK() PARA ORGANIZAR AUTOMATICAMENTE DICHO OBJETO EN LA VENTANA
    Button(text="Acceder", height="2", width="30", bg=pestas_color, command=login).pack() #BOTÓN "Acceder"
    Label(text="").pack()
    Button(text="Registrarse", height="2", width="30", bg=pestas_color, command=registro).pack() #BOTÓN "Registrarse".
    Label(text="").pack()
    ventana_principal.mainloop()#SE DEFINE COMO EL MAIN

#CREAMOS VENTANA PARA REGISTRO.
def registro():
    global ventana_registro
    ventana_registro = Toplevel(ventana_principal)#INDICA QUE DEPENDE DE LA VENTANA PRINCIPAL
    ventana_registro.title("Registro")#NOMBRE DE LA VENTANA
    ventana_registro.geometry("300x250")#DIMENSIONES DE LA VENTANA
 
    global nombre_usuario#ESTABLECEMOS LA ENTRADA PARA EL NOMBRE DE USUARIO QUE INGRESE EL CLIENTE POR MEDIO DE LA CASILLA DE TEXTO
    global clave#ESTABLECEMOS LA VARIABLE CLAVE 
    global entrada_nombre#ESTABLECEMOS LAS ENTRADAS
    global entrada_clave
    nombre_usuario = StringVar() #DECLARAMOS "string" COMO TIPO DE DATO PARA "nombre_usuario"
    clave = StringVar() #DECLARAMOS "sytring" COMO TIPO DE DATO PARA "clave"
 
    Label(ventana_registro, text="Introduzca datos", bg="BlueViolet").pack()
    Label(ventana_registro, text="").pack()
    etiqueta_nombre = Label(ventana_registro, text="Nombre de usuario * ")
    etiqueta_nombre.pack()
    entrada_nombre = Entry(ventana_registro, textvariable=nombre_usuario) #ESPACIO PARA INTRODUCIR EL NOMBRE.
    entrada_nombre.pack()
    etiqueta_clave = Label(ventana_registro, text="Contraseña * ")
    etiqueta_clave.pack()
    entrada_clave = Entry(ventana_registro, textvariable=clave, show='*') #ESPACIO PARA INTRODUCIR LA CONTRASEÑA.
    entrada_clave.pack()
    Label(ventana_registro, text="").pack()
    Button(ventana_registro, text="Registrarse", width=10, height=1, bg="BlueViolet", command = registro_usuario).pack() #BOTÓN "Registrarse"
    #EL BOTÓN LLAMA AL METODO REGISTRO USUARIO

#CREAMOS VENTANA PARA LOGIN.

def login():
    global ventana_login#SE DEFINE LA VENTANA DE MANERA GLOBAL
    ventana_login = Toplevel(ventana_principal)
    ventana_login.title("Acceso a la cuenta")#TITULO DE LA VENTANA
    ventana_login.geometry("300x250")#DIMENSIONES
    Label(ventana_login, text="Introduzca nombre de usuario y contraseña").pack()
    Label(ventana_login, text="").pack()
 
    global verifica_usuario
    global verifica_clave
 
    verifica_usuario = StringVar()
    verifica_clave = StringVar()
 
    global entrada_login_usuario
    global entrada_login_clave
 
    Label(ventana_login, text="Nombre usuario * ").pack()
    entrada_login_usuario = Entry(ventana_login, textvariable=verifica_usuario)
    entrada_login_usuario.pack()
    Label(ventana_login, text="").pack()
    Label(ventana_login, text="Contraseña * ").pack()
    entrada_login_clave = Entry(ventana_login, textvariable=verifica_clave, show= '*')
    entrada_login_clave.pack()
    Label(ventana_login, text="").pack()
    Button(ventana_login, text="Acceder", width=10, height=1, bg="BlueViolet", command = verifica_login).pack()#EL BOTÓN LLAMA AL METODO VERIFICA_LOGIN

#VENTANA "VERIFICACION DE LOGIN CON SOLICITUD AL SERVIDOR".

def verifica_login():
    s = socket.socket()#SE CONECTA EL SOCKET
    s.connect(('34.235.104.230', 6030))#INDICAMOS LA DIRECCIÓN Y EL HOST
    bandera=0
    usuario_info = verifica_usuario.get()#OBTIENE EL NOMBRE DE USUARIO
    clave_info = verifica_clave.get()#OBTIENE LA CONTRASEÑA
    datos=[usuario_info, clave_info,'2']#AGRUPA LOS DATOS PARA SER ENVIADOS AL SERVIDOR 
    print (datos)#MUESTRA LOS DATOS
    for i in datos:#LA VARIABLE I VA TOMANDO EL VALOR DE CADA DATO
         s.send(i)#SE ENVIA "i" AL SERVIDOR EN CADA INSTANCIA
    bandera=s.recv(1024)#RECIBE LA RESPUESTA DEL SERVIDOR LUEGO DE TERMINAR DE ENVIAR TODOS LOS DATOS
    print (bandera)#MUESTRA QUE TIPO DE RESPUESTA RECIBIO
    if bandera == '0':#SI LA RESPUESTA ES '0' ENTONCES EJECUTA EL EXITO DE LOGIN
        exito_login(sala)
            
       #SI LA BANDERA ES '1' SIGNIFICA QUE LA CLAVE ES INCORRECTA
    if bandera == '1':
        no_clave()
    #SI LA BANDERA ES '2' SIGNIFICA QUE EL NOMBRE DE USUARIO NO EXISTE
    if bandera == '2':
        no_usuario() 


# VENTANA "Login finalizado con exito".
# VENTANA DEL CHAT
 
def exito_login(sala):
    global ventana_exito
    global entrada_mensaje
    global mensaje
    global muestra_mensajes
    global codsala #DEFINIMOS VARIABLE GLOBAL PARA EL NOMBRE DE LA SALA
    codsala=sala
    mensaje = StringVar()
    ventana_exito = Toplevel(ventana_login)
    ventana_exito.title(sala)
    ventana_exito.geometry("400x300")
    Label(ventana_exito, text=sala, bg="BlueViolet", width="300", height="2", font=("Calibri", 13)).pack() # Create a text label
    Label(text="").pack()
    scrollbar=Scrollbar(ventana_exito)#DEFINIMOS UN SCROLLBAR PARA ASÍ OBSERVAR GRANDES CANTIDADES DE TEXTO
    scrollbar.pack(side = RIGHT, fill = Y)
    muestra_mensajes=Listbox(ventana_exito, yscrollcommand = scrollbar.set, width="280")
    muestra_mensajes.pack()
    scrollbar.config(command = muestra_mensajes.yview)
    etiqueta_mensaje = Label(ventana_exito, text="Introduce mensaje, o bien, puedes unirte a una sala o crear una")
    etiqueta_mensaje.pack()
    entrada_mensaje = Entry(ventana_exito, textvariable=mensaje) #ESPACIO PARA INTRODUCIR EL MENSAJE.
    entrada_mensaje.pack()
    Label(ventana_exito, text="").pack()
    Button(ventana_exito, text="Enviar mensaje", width=15, height=1, bg="BlueViolet", command = envio_mensaje).pack(side=LEFT)#SE EJECUTA EL METODO envio_mensaje
    Button(ventana_exito, text="Hacer un comando", width=30, height=1, bg="BlueViolet", command = comandos).pack(side=RIGHT)#SE EJECUTA EL METODO comandos
 
#VENTANA DE "Contraseña incorrecta".
 
def no_clave():
    global ventana_no_clave
    ventana_no_clave = Toplevel(ventana_login)
    ventana_no_clave.title("ERROR")
    ventana_no_clave.geometry("150x100")
    Label(ventana_no_clave, text="Contraseña incorrecta ").pack()
    Button(ventana_no_clave, text="OK", command=borrar_no_clave).pack() #EJECUTA "borrar_no_clave()".
 
#VENTANA DE "Usuario no encontrado".
 
def no_usuario():
    global ventana_no_usuario
    ventana_no_usuario = Toplevel(ventana_login)
    ventana_no_usuario.title("ERROR")
    ventana_no_usuario.geometry("150x100")
    Label(ventana_no_usuario, text="Usuario no encontrado").pack()
    Button(ventana_no_usuario, text="OK", command=borrar_no_usuario).pack() #EJECUTA "borrar_no_usuario()"
    
#VENTAN DE "Usuario existente".
def usuario_existente():
    Label(ventana_registro, text="Nombre de usuario ya elegido", fg="IndianRed", font=("calibri", 11)).pack()

#CERRADO DE VENTANAS

def borrar_exito_login():
    ventana_exito.destroy()
 
 
def borrar_no_clave():
    ventana_no_clave.destroy()
 
 
def borrar_no_usuario():
    ventana_no_usuario.destroy()

def comandos():
    global ventana_comandos
    global sala_nueva
    global entrada_sala_nueva
    global entrada_unirse_sala
    global unirse_sala
    global entrada_mensaje_priv
    global mensaje_priv
    sala_nueva=StringVar()
    unirse_sala=StringVar()
    mensaje_priv=StringVar()
    ventana_comandos = Toplevel(ventana_exito)
    ventana_comandos.title("Comandos")
    ventana_comandos.geometry("400x400")
    Label(ventana_comandos, text="Elige un comando", bg="BlueViolet", width="300", height="2", font=("Calibri", 13)).pack() # Create a text label
    Label(text="").pack()
    entrada_sala_nueva = Entry(ventana_comandos, textvariable=sala_nueva) #ESPACIO PARA INTRODUCIR EL NOMBRE DE SALA
    entrada_sala_nueva.pack()
    Button(ventana_comandos, text="#cR", command=nueva_sala).pack()
    entrada_unirse_sala = Entry(ventana_comandos, textvariable=unirse_sala) #ESPACIO PARA INTRODUCIR EL NOMBRE DE SALA
    entrada_unirse_sala.pack()
    Button(ventana_comandos, text="#gR", command=unirse_sala_nueva).pack()
    Button(ventana_comandos, text="#eR", command=volver_lobby).pack()
    Button(ventana_comandos, text="#exit", command=salir_chat).pack()
    Button(ventana_comandos, text="#IR", command=borrar_no_usuario).pack()
    Button(ventana_comandos, text="#show users", command=borrar_no_usuario).pack()
    entrada_mensaje_priv = Entry(ventana_comandos, textvariable=mensaje_priv) #ESPACIO PARA INTRODUCIR EL NOMBRE DE USUARIO
    entrada_mensaje_priv.pack()
    Button(ventana_comandos, text="#\private", command=borrar_no_usuario).pack()
    
#AL EJECUTAR EL BOTÓN "#cR"
def nueva_sala():
    ventana_comandos.destroy()
    ventana_exito.destroy()
    exito_login(sala_nueva.get())

#AL EJECTURAR EL BOTÓN "#gR"
def unirse_sala_nueva():
    ventana_comandos.destroy()
    ventana_exito.destroy()
    exito_login(unirse_sala.get())

#AL EJECUTAR EL BOTÓN "#exit"
def salir_chat():
    ventana_principal.destroy()

#AL EJECUTAR EL BOTÓN "#eR"
def volver_lobby():
    ventana_comandos.destroy()
    ventana_exito.destroy()
    comando='lobby'
    exito_login(comando)


    
#ENVIAR MENSAJE AL SERVIDOR Y RECIBIR
    
def envio_mensaje():
    info_mensaje=[]
    recibido=[]
    s = socket.socket()#NOS CONECTAMOS
    s.connect(('34.235.104.230', 6030))
    nombre=verifica_usuario.get()
    envio_mensaje=nombre+": "+mensaje.get()#UNIFICAMOS EL MENSAJE CON EL NOMBRE DE USUARIO
    datos=[envio_mensaje, '3',codsala]#AGRUPAMOS LOS DATOS QUE SERÁN ENVIADOS
    print (datos)#MOSTRAMOS LOS DATOS
    for i in datos:#INGRESAMOS A LOS DATOS
        print (i)
        s.send(i)#SE ENVIA EL DATO EN ESA INSTANCIA
    for u in range(3):#SE TIENE PLANEADO RECIBIR 3 DATOS
        info_mensaje.append(s.recv(1024))#VAMOS AGREGANDO LOS DATOS A MEDIDA QUE SE RECIBEN DESDE EL SERVIDOR
        
    print (info_mensaje)#SE MUESRAN LOS DATOS RECIBIDOS
    
    if info_mensaje[1] == codsala:#SI LA SALA CORRESPONDE CON LA SALA DE ORIGEN DEL MENSAJE SE PUEDE MOSTRAR
        muestra_mensajes.insert(END,info_mensaje[0])#SE INSERTA EL MENSAJE A LA CASILLA DE TEXTO DE LA VENTANA exito_login

#REGISTRAR USUARIO
    
def registro_usuario():
    s = socket.socket()#NOS CONECTAMOS POR MEDIO DEL SOCKET
    s.connect(('34.235.104.230', 6030))
    bandera=0
    usuario_info = nombre_usuario.get()#OBTENEMOS EL NOMBRE DE USUARIO
    clave_info = clave.get()#OBTENEMOS LA CLAVE
    datos=[usuario_info, clave_info,'1']#AGRUPAMOS LOS DATOS CON LA ETIQUETA '1'
    print (datos)#MOSTRAMOS LOS DATOS
    for i in datos:#DESCOMPONEMOS LA LISTA DE DATOS PARA IR ENVIANDO UNO POR UNO 
         s.send(i)#ENVIAMOS CADA DATO
    recibido=s.recv(1024)#RECIBIMOS LA RESPUESTA DEL SERVIDOR
    bandera=int(recibido)#GUARDAMOS DICHA RESPUESTA EN VARIABLE INT
    if bandera== 1:#SI LA RESPUESTA FUE 1 ENTONCES
        usuario_existente()
    if bandera == 0:#SI LA RESPUESTA FUE 2 ENTONCES
        entrada_nombre.delete(0, END)
        entrada_clave.delete(0, END)
 
        Label(ventana_registro, text="Registro completado con éxito", fg="green", font=("calibri", 11)).pack()
 
ventana_inicio()  #EJECUCIÓN DE LA VENTANA DE INICIO

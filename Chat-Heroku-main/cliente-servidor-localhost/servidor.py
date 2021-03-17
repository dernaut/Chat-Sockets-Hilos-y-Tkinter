
import threading
import os
import socket

#PRESENTADO POR JULIAN GIRALDO, LUIS ZULUAGA, JUAN DAVID ALVAREZ
#UTP / SISTEMAS DISTRIBUIDOS
class Client(threading.Thread):

    def __init__(self, conn, addr):
        # Inicializar clase padre.
        super(Client, self).__init__()
        self.conn = conn
        self.addr = addr

    def Guardar_datos(self, nombre, contra):
        #SE CREA UNA ETIQUETA PARA ENVIAR AL CLIENTE DEPENDE DEL RESULTADO DEL GUARDADO DE DATOS
        bandera=0
        #SE INICIALIZA UNA LISTA CON DIRECCIÓN LOCAL
        lista_archivos = os.listdir('.')
        #PREGUNTA SI EL NOMBRE DE USUARIO ESTÁ EN LA LISTA
        if nombre in lista_archivos:
            #SI ES CIERTO ENTONCES LA BANDERA CAMBIA SU VALOR A 1 PARA ASÍ SER ENVIADA AL CLIENTE
            bandera=1
        #SI ESE NOMBRE NO ESTÁ EN USO ENTONCES EL SERVIDOR PROCEDE A CREAR USUARIO
        if bandera == 0:
            file = open(nombre, "w") #CREACION DE ARCHIVO CON "nombre" y "clave"
            file.write(nombre + "\n")#ESCRITURA EN EL ARCHIVO
            file.write(contra)
            file.close()#CIERRE ARCHIVO
            print("%s se ha registrado." % nombre) #INDICADOR EN CONSOLA SERVIDOR DE REGISTRO
        self.conn.send(str(bandera))#SE ENVIA EL VALOR DE LA BANDERA PARA CLIENTE
    def verificacion_usuario(self, nombre, contra):
        #SE INICIALIZA BANDERA STRING
        bandera=''
        #SE INICIALIZA UNA LISTA CON DIRECCIÓN LOCAL
        lista_archivos = os.listdir('.') #GENERA LISTA DE ARCHIVOS UBICADOS EN EL DIRECTORIO.
        #SI EL NOMBRE SE ENCUENTRA EN LA LISTA DE ARCHIVOS..
        if nombre in lista_archivos:
            archivo1 = open(nombre, "r") #APERTURA DE ARCHIVO EN MODO LECTURA
            verifica = archivo1.read().splitlines() #LECTURA DEL ARCHIVO QUE CONTIENE EL nombre Y contraseña.
            #SI LA CONTRASEÑA INTRODUCIDA SE ENCUENTRA EN EL ARCHIVO...
            if contra in verifica:
                bandera='0' #BANDERA CAMBIA EL VALOR PARA ENVIARSE A CLIENTE
                self.conn.send(bandera)#SE ENVIA LA BANDERA
                lista_usuarios.append(nombre)#SE ANEXA EL NOMBRE DE DICHO USUARIO PARA LLEVAR REGISTRO DE TODOS LOS CLIENTES
                print("Inicio correcto")#MUESTREO EN CONSOLA PARA VERIFICAR QUE INICIÓ SESIÓN CORRECTAMENTE
                
            else:
                #SI LA CONTRASEÑA ES INCORRECTA
                bandera='1' #BANDERA CAMBIA VALOR PARA ENVIARSE A CLIENTE
                self.conn.send(str(bandera))#SE ENVIA LA BANDERA
                print ("Clave incorrecta")#MUESTRA EN CONSOLA SERVIDOR
        #SI EL NOMBRE INTRODUCIDO NO SE ENCUENTRA EN EL DIRECTORIO...
        else:
            bandera='2' #BANDERA SE CODIFICA
            self.conn.send(str(bandera))#SE ENVIA LA BANDERA
            print ("Usuario no encontrado")#MUESTRA EN CONSOLA SERVIDOR
    def envio_mensaje_chat(self, mensaje, sala):#METODO ENVIO DE MENSAJE, SE EJECUTA CUANDO SE RECIBE LA PETICIÓN DE CLIENTE
        #print(mensaje)
        lista_salas.append(sala)#EN EL MOMENTO EN QUE SE RECIBE UNA SALA NUEVA SE AGREGA
        mensaje_env=[mensaje, sala, '']#SE AGRUPAN LOS DATOS QUE SE VAN A REENVIAR
        #print (mensaje_env)
        for e in clientes:#INGRESAMOS A LOS CLIENTES CONECTADOS
            for i in mensaje_env:#SEPARAMOS LOS DATOS DE LA LISTA
                self.conn.send(i)#EN CADA INSTANCIA DEL CICLO ENVIAMOS DATO POR DATO AL CLIENTE
    def mostrar_usuarios(self):#METODO PARA ENVIAR TODOS LOS USUARIOS 
        for e in clientes:#INGRESAMOS A LOS CLIENTES CONECTADOS
            for i in lista_usuarios:#OBTENEMOS CADA UNO DE LOS DATOS DE LISTA DE USUARIOS
                self.conn.send(i)#ENVIAMOS DATO POR DATO AL CLIENTE
                
    def mostrar_salas(self):#METODO PARA ENVIAR TODAS LAS SALAS
        for e in clientes:#INGRESAMOS A LOS CLIENTES CONECTADOS
            for i in lista_salas:#OBTENEMOS CADA UNO DE LOS DATOS DE LISTA SALAS
                self.conn.send(i)#ENVIAMOS DATO POR DATO AL CLIENTE

                
    def run(self):#METODO RUN, DONDE SE EJECUTA CADA HILO Y TAMBIÉN TODAS LAS PETICIONES DEL SERVIDOR
        datos=[]#SE INICIALIZA UNA VARIABLE PARA REGISTRAR CADA UNO DE LOS DATOS QUE SE RECIBEN POR PARTE DEL CLIENTE
        for u in range (3):#ESTABLECEMOS QUE LOS DATOS MAXIMOS QUE PUEDE RECIBIR ES 3 POR LLAMADO
            datos.append(self.conn.recv(1024))#RECIBE CADA UNO DE LOS DATOS DESDE LA CONEXION DEL CLIENTE  Y LOS GUARDA EN LA LISTA
        nombre=str(datos[0])#ASIGNA VARIABLE NOMBRE
        contra=str(datos[1])#ASIGNA VARIABLE CONTRASEÑA
        print (datos)#MUESTRA LOS DATOS EN CONSOLA SERVIDOR
        #print (clientes)
        if datos[2] == '1':#EL SERVIDOR RECIBE UNA ETIQUETA Y GRACIAS A ESTO PUEDE INTERPRETAR CUAL SOLICITUD SE HACE
            #SI LA ETIQUETA ES '1' ENTONCES EL CLIENTE QUIERE REGISTRARSE
            print("%s registrandose." % datos[0])
            print(datos)
            self.Guardar_datos(nombre,contra)#SE EJECUTA EL METODO GUARDAR DATOS
        if datos[2] == '2':
            #SI LA ETIQUETA ES '2' ENTONCES EL CLIENTE ESTÁ QUERIENDO INICIAR SESIÓN
            print(("%s iniciando sesion." % datos[0]))
            self.verificacion_usuario(nombre, contra)#SE EJECUTA EL METODO VERIFICACIÓN USUARIO
        if datos[1] == '3':
            #SI LA ETIQUETA ES '3' ENTONCES EL CLIENTE ESTÁ QUERIENDO ENVIAR UN MENSAJE Y DEL MISMO MODO RECIBIRLO
            print ("se ha recibido un mensaje")
            self.envio_mensaje_chat(datos[0], datos[2])#SE EJECUTA EL METODO ENVIO MENSAJE CHAT
        if datos[2]== '4':
            #SI LA ETIQUETA ES '4' ENTONCES EL CLIENTE ESTÁ SOLICITANDO MOSTRAR TODOS LOS USUARIOS
            print ("comando mostrar usuarios")
            self.mostrar_usuarios()#LLAMA AL METODO MOSTRAR USUARIOS
        if datos[2]== '5':
            #SI LA ETIQUETA ES '5' ENTONCES EL CLIENTE SOLICITA MOSTRAR TODAS LAS SALAS DISPONIBLES
            print ("comando mostrar salas")
            self.mostrar_salas()#LLAMA AL METODO MOSTRAR SALAS
        #s.close()
                    
def main():
    global lista_usuarios#LISTA GOBLAL PARA GUARDAR TODOS LOS CLIENTES CON NOMBRE DE USUARIO
    global lista_salas#LISTA GLOBAL PARA GUARDAR TODAS LAS SALAS
    lista_salas=[]#SE INICIALIZA
    lista_usuarios=[]#SE INICIALIZA
    s = socket.socket()#SE CREA EL SOCKET
    
    # Escuchar peticiones en el puerto 6030.
    s.bind(('localhost', 6030))#ESTABLECEMOS DIRECCION LOCAL EN ESTE CASO
    s.listen(1)#EL SOCKET RECIBE PETICIONES POR EL CANAL 1
    global clientes#SE CREA LISTA GLOBAL DE CLIENTES PARA ALMACENAR EL HILO
    clientes=[]#INICIALIZAMOS
    while True:
        conn, addr = s.accept()#ACEPTAMOS LA CONEXION DEL CLIENTE
        c = Client(conn, addr)#CREAMOS EL CLIENTE CON LA VARIABLE C
        clientes.append(c)#AGREGAMOS CADA CLIENTE A LA LISTA CLIENTES PARA LUEGO ACCEDER A ELLOS
        c.start()#EJECUTAMOS RUN()
    s.close()#CERRAMOS LA CONEXIÓN SI DEJAN DE INGRESAR CLIENTES
if __name__ == "__main__":
    print ('Servidor abierto')#MUESTREO PARA CONSOLA SERVIDOR
    main()#EJECUTAMOS MAIN


#s.close()

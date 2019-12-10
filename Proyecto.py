"""
PROYECTO SCRABBLE
Editores:   Salvador Galindo
            Facundo
            Juan
DOCUMENTO: https://docs.google.com/document/d/19qLfRDQjicCGriPfUQGNLpU69WttZMfHk9bWYa6U6Qg/edit


ANOTACIONES:
casillas=[i][j]=[num][letra] --> casillas=[[fila1][fila2]...[fila15]]
Tenemos en cuenta que num1=0 (posicion 0) y A=0 (posicion 0)
Para editar la puntuación de un jugador:
jugadores={0:datos1, 1:datos2, 2:datos3, 3:datos4} por lo tanto accedemos al valor de la clave
datosx=[puntuación, [palabras compuestas por el jugador]]
"""

"""
--------------LISTAS, VARIABLES, CONSTANTES:----------------------
"""
#Letras para imprimir en el tablero
letras=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O"]
#Diccionario que contiene las letras y sus respectivas puntuaciones
puntuacion = {"A": 1 , "B": 3 , "C": 3 , "D": 2 ,
             "E": 1 , "F": 4 , "G": 2 , "H": 4 ,
             "I": 1 , "J": 8 , "K": 5 , "L": 1 ,
             "M": 3 , "N": 1 , "O": 1 , "P": 3 ,
             "Q": 10, "R": 1 , "S": 1 , "T": 1 ,
             "U": 1 , "V": 4 , "W": 4 , "X": 8 ,
             "Y": 4 , "Z": 10}
#Casillas: individual y listas (tablero)
casilla="■"
casillas=[]
#Anchura y altura del tablero
HORIZONTAL=15
VERTICAL=15
#Declaración de valores globales
jugadores = dict()
turnoactual=0
detectadasTotal=[]
#CREAMOS LA LISTA DE CASILLAS CON CASILLAS
for i in range(VERTICAL):
    casillashorizontal=[]
    for j in range(HORIZONTAL):
        casillashorizontal.append(casilla)
    casillas.append(casillashorizontal)

    
"""
--------------------PROCEDIMIENTOS:-------------------------------
"""

""" Pintar tablero"""
def pintarTablero():
    print()
    #IMPRIME LAS LETRAS SUPERIORES
    for k in range(len(letras)):
        if(k==14):
            print(letras[k])
        elif(k==0):
            print("  ",letras[k],end="  ")
        else:
            print(letras[k],end="  ")
            
    #IMPRIME EL TABLERO
    for i in range(17):
        #IMPRIME LA PRIMERA Y ÚLTIMA FILA (║═════║)    
        if(i==0 or i==16):
            print("  ║",end="")
            for j in range(15):
                if(j==14):
                    print("═",end="")
                    print("║")
                else:
                    print("═══",end="")
        #IMPRIME LAS FILAS DEL INTERIOR  (1.║   E  ║)
        else:
            #IMPRIME LAS FILAS VACÍAS ENTRE NÚMEROS
            if(i!=1):
                print("  ║",end="")
                for j in range(15):
                    if(j==14):
                        print(" ",end="")
                        print("║")
                    else:
                        print("   ",end="")
            #IMPRIME LOS NUMEROS LATERALES
            if(0<i<10):
                print("",i,end="")
            else:
                print(i,end="")
            #IMPRIME BARRAS LATERALES, CARACTERES EN LAS FILAS DE NÚMEROS
            #Y NÚMEROS IZQUIERDA
            print("║",end="")
            for j in range(15):
                if(j==14):
                    print(devolverCasilla(i-1,j),end="")
                    print("║",end="")
                    print(i)
                else:
                    print(devolverCasilla(i-1,j)," ",end="")
    #IMPRIME LAS LETRAS INFERIORES
    for k in range(len(letras)):
        if(k==14):
            print(letras[k])
        elif(k==0):
            print("  ",letras[k],end="  ")
        else:
            print(letras[k],end="  ")
                    
    #CASILLAS ESPECIALES (pasar a for)
        #casilla inicial (centro)
            #casillas[7][7]="1"
        #casilla x2
            #casillas[6][6]="2"
            #casillas[6][8]="2"
            #casillas[8][6]="2"
            #casillas[8][8]="2"
        #casilla x3
            #casillas[][6]="3

""" Crear Jugadores:"""
def crearJugadores(numJugadores):
    #Variables globales
    #Diccionario jugadores que contiene las puntuaciones respectivas
    global jugadores
    
    puntuacion=0
    #Lista: contiene [puntuación, [palabras del jugador]]
    datosJugador=[puntuacion]
    #Bucle constructor del diccionario
    for i in range(numJugadores):
        jugadores[i]=datosJugador
    
""" Mostrar Turnos:"""
def mostrarTurnos(ordenJugadores):
    #Variables globales
    global turnoactual
    
    orden=["primer","segundo","tercer","cuarto"]
    print()
    for i in range(len(ordenJugadores)):
        print("El",orden[i],"jugador es: J",end="")
        print(ordenJugadores[i])
    print("El turno actual es del jugador J",end="")
    print(turnoactual)
    
""" Escribir: permite al jugador escribir una palabra en el tablero y ganar puntos"""
def escribir():
    #Pide los datos: palabra, número y letra
    palabra=(input("¿Qué deseas escribir?: ")).upper()
    print("¿En qué posición deseas escribirla? (Número, Letra, Sentido)")
    posNum=int(input("Introduce un número: "))-1
    letra=(input("Introduce una letra: ")).upper()
    sentido=int(input("Escribe un sentido (1. Derecha/2. Abajo): "))
    
    palabraLista=list(palabra)
    posLetra=posicionLetra(letra)
    #Insertamos los datos y comprobamos si se puede introducir en el tablero:
    colocar=comprobarTablero(palabraLista,posNum,posLetra,sentido)
    #
    if(colocar==False):
        print("Error. La palabra no se puede colocar.\n")
    else:
        for posCasilla in range(len(palabraLista)):
            if(palabraLista[posCasilla]==""):
                if(sentido==1):
                    posLetra+=1
                if(sentido==2):
                    posNum+=1
            else:
                casillas[posNum][posLetra]=palabraLista[posCasilla]
                if(sentido==2):
                    posNum+=1
                if(sentido==1):
                    posLetra+=1
        #La palabra se ha escrito. Sumamos los puntos:
        sumarPuntos(palabra)
        #Y pintamos el tablero:
        pintarTablero()
        
""" Instrucciones"""
def instrucciones():
    print('1.Se reparten 7 letras a cada jugador.\n2.Cada jugador debe formar una'
          ' palabra de dos o más letras que deberá colocar horizontal o verticalmente'
          ' en el tablero.\n3.El juego finaliza al acabarse las letras a repartir.\n'
          '4.Ganará el juagdor que tenga más puntos al finalizar el juego.')

""" Mostrar palabras:"""
def mostrarPalabras():
    palabrasTotal=detectarPalabras()
    print(palabrasTotal)
    print()
    if(palabrasTotal==[]):
        print("No hay palabras en el tablero.")
    else:
        for i in range(len(palabrasTotal)):
            for j in range(len(palabrasTotal[i])):
                if(j==len(palabrasTotal[i])-1):
                    print(palabrasTotal[i][j])
                else:
                    print(palabrasTotal[i][j],end="")
        print("En total hay",len(palabrasTotal),"palabras.")

""" Mostrar letras:"""
def mostrarLetras():
    letrasJugador=getLetras(letrasJugador)
    print(letrasJugador)

""" Sumar puntos:"""
def sumarPuntos(palabra):
    #Variables globales
    global turnoactual
    
    jugador=turnoactual
    

""" Menú jugador:"""
def menuJugador(numJugadores):
    #Se pinta el tablero inicial
    print("\n Este es el tablero:")
    pintarTablero()
    #Se crean los jugadores necesarios
    crearJugadores(numJugadores)
    #Se designan el orden de los jugadores
    ordenJugadores=turnoJugadores(numJugadores)
    #Y se muestra en pantalla
    mostrarTurnos(ordenJugadores)
    #Comienza el juego
    print("\nComienza el juego!!!")
    salir=True
    while(salir):
        print("\nMenú de juego:")
        print("\n1. Escribir una palabra.")
        print("2. Pasar turno.")
        print("3. Ver Tablero.")
        print("4. Ver palabras en el tablero.")
        print("5. Ver letras disponibles.")
        print("6. Ver el orden de juego y a cual es el turno actual.")
        print("0. Salir.")
        opcion=int(input("Elige que hacer: "))

        if(opcion==1):
            escribir()
        if(opcion==2):
            pasarTurno()
        if(opcion==3):
            pintarTablero()
        if(opcion==4):
            mostrarPalabras()
        if(opcion==5):
            mostrarLetras()
        if(opcion==6):
            mostrarTurnos(ordenJugadores)
        if(opcion==0):
            salir=False
    
"""
--------------------FUNCIONES:----------------------------
"""
""" Devolver casilla: devuelve el carácter de la casilla: un espacio o una letra:"""
def devolverCasilla(i,j):
    return casillas[i][j]

""" Comprobar tablero: comprueba si la palabra escrita se puede insertar en la posición
    especificada. Parámetros: posNum, posLetra, palabraLista y sentido.
    Devuelve True si la palabra se puede escribir, False si no se puede escribir. """
def comprobarTablero(palabraLista,posNum,posLetra,sentido):
    if(posNum+len(palabraLista)>16 or posLetra+len(palabraLista)>16):
        return False
    else:
        for posCasilla in range(len(palabraLista)):
            if(casillas[posNum][posLetra]=="■"):
                pass
            elif(casillas[posNum][posLetra]==palabraLista[posCasilla]):
                #palabraLista.remove(casillas[posNum][posLetra])
                palabraLista[posCasilla]=""
                posCasilla-=1
            else:
                return False
            if(sentido==1):
                posLetra+=1
            if(sentido==2):
                posNum+=1
    return palabraLista

""" Posicion de la letra: obtenemos la posicion de una letra que insertamos como parámetro
    y nos devuelve la posición en el abecedario"""
def posicionLetra(letra):
    posLetra=0
    while(letra!=letras[posLetra]):
        posLetra+=1
    return posLetra

""" Detectar palabras: detecta palabras en el tablero y las suma a una lista
    palabrasTotales."""
def detectarPalabras():
    #Variables globales
    global detectadasTotal

    detectadas=[]
    detHorizontal=[]
    detVertical=[]
    #Detecta palabras horizontales
    for i in range(VERTICAL):
        for j in range(HORIZONTAL):
            if(casillas[i][j]!="■"):
                detHorizontal.append(casillas[i][j])
                if(j==HORIZONTAL-1 or casillas[i][j+1]=="■"):
                    if(len(detHorizontal)>1):
                        detectadas.append(detHorizontal)
                    detHorizontal=[]
    #Detecta palabras verticales
    for j in range(HORIZONTAL):
        for i in range(VERTICAL):
            if(casillas[i][j]!="■"):
                detVertical.append(casillas[i][j])
                if(j==VERTICAL-1 or casillas[i+1][j]=="■"):
                    if(len(detVertical)>1):
                        detectadas.append(detVertical)
                    detVertical=[]
    #Detectadas toma el valor de palabras nuevas en el tablero
    #detectadas=detectadastotal-detectadas
    
    detectadasTotal=detectadas
    return detectadas

""" Get Letras: devuelve un número determinado de letras al jugador""" 
def getLetras(letrasJugador):
    import random
    restantes=7-len(letrasJugador)
    for i in range(restantes):
        secreto=random.randint(0,14)
        letrasJugador.append(letras[secreto])
    return letrasJugador

""" Orden jugadores:"""
def turnoJugadores(numJugadores):
    #Variables globales
    global turnoactual
    
    import random
    ordenJugadores=[]
    i=1
    while(i<numJugadores+1):
        secreto=random.randint(1,numJugadores)
        if(secreto in ordenJugadores):
            i=i-1
            ordenJugadores.pop()
        else:
            ordenJugadores.append(secreto)
            i+=1
    turnoactual=ordenJugadores[0]
    return ordenJugadores

"""
------------------------INICIO:---------------------------
"""

def menuPrincipal():
    salir=True
    while(salir):
        print("\nMenú principal:")
        print("\n1. Jugar al SCRUBBLE.")
        print("2. Ver las instrucciones de juego.")
        print("0. Salir.")
        opcion=int(input("\nElige que hacer: "))

        if(opcion==1):
            numJugadores=int(input("\n¿Cuántos jugadores van a jugar? (2-4)?"))
            menuJugador(numJugadores)
        if(opcion==2):
            instrucciones()
        if(opcion==0):
            salir=False
            
letrasJugador=['A','E']
menuPrincipal()

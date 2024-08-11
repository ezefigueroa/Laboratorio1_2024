import csv
import os

class Tarea: #Se crea la clase Tarea
    def __init__(self, id, descripcion, prioridad, categoria="General"): #Con el constructor init se inicializan los parámetros que van a definir el objeto tarea con self, un id, descripción, prioridad y categoria. En el caso que el usuario no ingrese categoría por defecto se le asigna "General"
        self.id = id                   #cada objeto tarea tendrá un identificador único
        self.descripcion = descripcion #cada objeto tarea tendrá una descripción ingresada por el usuario especificando a que hace referencia la tarea
        self.prioridad = prioridad     #cada objeto tarea tendrá una prioridad que el usuario ingresará según opciones 1 prioridad baja, 2 prioridad media y 3 prioridad alta
        self.completada = False        #cada objeto tarea inicialmente no estará completada por lo tanto se le asigna False
        self.categoria = categoria     #cada objeto tarea pertenecerá a una categoria ingresada por el usuario, si el usuario no la ingresa por defecto pertenecerá a la categoria general.
     
class Nodo: #Se crea la clase Nodo para almacenar las tareas
    def __init__(self, tarea): #se define el constructor init con dos parámetros, el objeto mismo y tarea
        self.tarea = tarea     #se define tarea para almacenar el objeto tarea con las caracteristicas que ingrese el usuario
        self.siguiente = None  #se define siguiente para apuntar al siguiente nodo en la lista enlazada. Inicialmente inicializa con None.
        
    def __str__ (self): # El metodo str hace posible que podamos imprimir la instancia del objeto
        estado = "Completada" if self.tarea.completada else "Pendiente" # en esta linea tenemos un version simplificada del condicional if que guarda en la variable estado el string completado o pendiente dependindo del valor que este guardado en la variable self.completada.
        return(f"ID: {self.tarea.id}, Descripción: {self.tarea.descripcion}, Prioridad: {self.tarea.prioridad}, Categoría: {self.tarea.categoria}, Estado: {estado}") # esta linea retorna las variables de la clase que queremos que se impriman.
            
class ListaEnlazada:  #Se crea la clase ListaEnlazada para recorrer la lista
    def __init__(self): #se define el constructor init que tiene cómo parámetro de self, objeto en sí mismo
        self.cabeza = None # se define cabeza para apuntar al primer nodo de la listaenlazada. Se inicializa con None
        self.id_actual = 1 #se define el id_actual para nuevas tareas inicializando desde el 1.
        self.cantidad_tareas = 0 # se define cantidad_tareas donde vamos a contar la cantidad de tareas nuevas.
        self.categorias_pendientes = {} # se crea un diccionario para poder contar las cantidad de tareas pendientes por categoria.
    
    def esta_vacia(self):   #se define un método llamado esta_vacia
        return self.cabeza is None #este método devuelve True si la lista está vacía o False en caso contrario

    def agregar_tarea(self, descripcion, prioridad, categoria): #se define un método llamado agregar_tarea que toma como parámetros el objeto mismo self, descripción de la tarea, la prioridad y categoria de la misma, para agregar una tarea a la lista enlazada.
        
        tarea = Tarea(self.id_actual, descripcion, prioridad, categoria) #se define tarea que corresponde a una instancia de la clase tarea
        
        if not self.buscar_tarea_descripcion(descripcion): # esta condicion llama al metodo buscar_tareas para verificar si existe una tarea actualmente con la misma descripcion.
            nuevo_nodo = Nodo(tarea)  # se crea un variable donde le asignamos un nodo nuevo con la instancia de tarea.
            self.id_actual += 1 #ante esta nueva tarea se suma 1 al id_actual
            self.cantidad_tareas +=1 # suma el valor de 1 a cantidad de tareas. sirve para contar la cantidad de tareas pendientes.

            if self.esta_vacia() or tarea.prioridad > self.cabeza.tarea.prioridad: #se utiliza un condicional if para comprobar si la lista está vacpia o si la prioridad de la nueva tarea es mayor que la prioridad de la tarea que está en la cabeza de la lista. Si la prioridad es mayor, la tarea debe ir al principio de la lista.
                nuevo_nodo.siguiente = self.cabeza  #se actualiza la referencia del nuevo nodo, asignando que el siguiente nodo del nuevo nodo sea el actual nodo en la cabeza de la lista
                self.cabeza = nuevo_nodo #se actualiza la cabeza de la lista donde nuevo_nodo será la nueva cabeza de la lista (colocando la tarea con amyor prioridad en la parte superior de la lista)
            
            else:  #en caso contrario (en que la tarea no debe ir en la cabeza de la lista porque no tiene la mayor prioridad, se buca la ubicación para insertar el nuevo nodo en la lista)
                actual = self.cabeza  #actual es self.cabeza
                while actual.siguiente is not None and actual.siguiente.tarea.prioridad >= tarea.prioridad: #recorre la lista hasta encontrar el lugar en donde va a insertar el nuevo nodo
                    actual = actual.siguiente #el nuevo nodo se inserta despues del nodo actual si la prioridad de la tarea siguiente en la lista es mayor o igual a la prioridad de la nueva tarea
                
                nuevo_nodo.siguiente = actual.siguiente #se actualiza la referencia del nuevo_ nodo y el siguiente del nuevo nodo será el nodo que estaba despues del nodo actual
                actual.siguiente = nuevo_nodo #se agrega el nuevo nodo a la lista, el nodo siguiente del nodo actual será el nuevo nodo insertandolo en la posición correcta
            
            if not tarea.completada: # verifica si la tarea fue completada.
                if tarea.categoria in self.categorias_pendientes: # verifica si la categoria de la tarea esta dentro del diccionario categoria_pendientes
                    self.categorias_pendientes[tarea.categoria] += 1 # si categoria pertence al diccionario se le suma 1 al valor
                else: # si la tarea no forma parte del diccionario categoria_pendientes
                    self.categorias_pendientes[tarea.categoria] = 1 # se crea una clave nueva y se le asigna el valor 1

            print("Tarea agregada con éxito.") # imprime que la tarea fue agregada correctamente
            
        else: # este else pertenece al primer if donde verificamos con el metodo buscar_tarea_descripcion
            print("No se pudo cargar la tarea. La tarea ya existe") # imprime que no se pudo cargar la tarea.
        

    def buscar_tarea_descripcion(self,descripcion)->bool: # Este metodo se utiliza para saber si existe una tarea con esa misma descripcion
        actual = self.cabeza # se crea una variable actual con el valor de self.cabeza
        while actual != None: # mientras la variable actual no sea None se ejecutara el bloque
            if actual.tarea.descripcion == descripcion: # La condicion nos permite comprobar si la descripcion de la variable actual es igual a la ingresada por el usuario, al querer crear una tarea nueva.
                return True    # retorna True en caso de que sea igual  y finaliza la funcion  
            actual = actual.siguiente # reccorremos la lista enlazada apuntando siempre al sieguiente
        return False # retorna False cuando no se encontro la misma descripcion.

    
    def completar_tarea(self, id): # este metodo nos permite completar una tarea osea cambiar el valor de completada a True
        actual = self.cabeza # asignamos self.cabeza a la variable actual.
                
        while actual is not None: # ingresamos al bucle si actual tiene alguna instancia de tarea.
            if actual.tarea.id == id: #comparamos el id de la tarea existente con el id ingresado por el usuario.
                if not actual.tarea.completada: # comprobamos que la tarea no haya sido completada anteriormente
                    actual.tarea.completada = True # cambiamos el valor de la variable completada.
                    print("Se completo la tarea") # se imprime que se completo la tarea
                    self.cantidad_tareas -=1 # se resta al contado cantidad_tareas el valor -1
                    if actual.tarea.categoria in self.categorias_pendientes: # verificamos si hay una categoria igual en el diccionario
                        self.categorias_pendientes[actual.tarea.categoria] -= 1 # si hay una categoria igual le restamos el valor 1
                        if self.categorias_pendientes[actual.tarea.categoria] == 0: # verificamos si el valor de la clave del diccionario es 0
                            del self.categorias_pendientes[actual.tarea.categoria] # si el valor era cero eliminamos la clave del diccionario.
                    return # finalizamos el metodo
                else: # este bloque se ejecuta si la tarea ya habia sido completada
                    print("Error: La tarea ya fue completada") # se imprime en pantalla la tarea fue completada.
                    return #finaliza el metodo
            actual = actual.siguiente # si el id verificado en el primer if no era igual se apunta la variable actual al valor siguiente del nodo
        print ("No hay tareas con ese numero de ID") # se imprime en pantalla que no hay tareas con ese numero de id luego de recorrer toda la lista enlazada.   
            

    def eliminar_tarea(self, id): #se define el método eliminar tarea que toma cómo parámetro el objeto mismo y el id de la tarea
        actual = self.cabeza #actual corresponde a self.cabeza
        previo = None #previo es None
        while actual is not None: #con este while, ingresará si se cumple esta condicion: mientras actual no este en None...
            if actual.tarea.id == id: #ingresa a esta condición si el id de la tarea actual es igual al id que ingresa el usuario de la tarea a eliminar
                if previo is None: #ingresa a esta condición si previo es None
                    self.cabeza = actual.siguiente#ahora cabeza es el siguiente de actual
                else: #en caso contrario (que previo no sea None)
                    previo.siguiente = actual.siguiente #ahora siguiente de previo es siguiente de actual
                
                print(f"Tarea eliminada: {actual}")#se muestra el mensaje "Tarea eliminada y la descripción de la misma"
                if not actual.tarea.completada: # se verifica si la tarea fue completada para poder llevar el conteo de las tareas pendientes por categorias
                    if actual.tarea.categoria in self.categorias_pendientes: # se verifica si la categoria pertenece al diccionario categorias_pendientes
                        self.categorias_pendientes[actual.tarea.categoria] -= 1 # si pertenece se le resta el valor de 1
                        if self.categorias_pendientes[actual.tarea.categoria] == 0: # se verifica si el valor de  la clave quedo en cero
                            del self.categorias_pendientes[actual.tarea.categoria] # si el valor quedo en cero se elimina del diccionario
                self.cantidad_tareas -= 1 # se le resta el valor de uno al contador total de tareas pendietes
                return #finaliza el metodo
            previo = actual #ahora previo es actual
            actual = actual.siguiente #actual es su siguiente
        print(f"Tarea con ID {id} no encontrada.") #En caso que no entre el while, se muestra el mensaje "Tarea con el ID taal, no encontrada"
        
    def mostrar_tareas(self): # este metodo nos muestra en pantalla el listado de todas las tareas.
        actual = self.cabeza # asignamos el valor self.cabeza a la variable actual
        if actual is None: # verificamos si actual es none.
            print("No hay tareas agregadas") # si actual es none , se imprime en pantalla no hay tareas agregadas.
            return # finaliza el metodo
        while actual is not None: # mientras actual no sea none
            print (actual) # se imprime las tareas que pasen por la variable actual
            actual = actual.siguiente # se recorre la lista enlazada otorgandole el valor de su siguiente a actual.       

    def mostrar_tareas_pendientes(self): # se muestran las tareas pendientes.
        actual = self.cabeza # se le asigna el valor self.cabeza a la variable actual.
        if actual is None: # se verifica si actual es none
            print("No hay tareas agregadas") # si actual es none se imprime en pantalla que no hay tareas pendientes
            return # se finaliza el metodo
        tareas_pendientes = False # se crea una variable tareas_pendientes con el valor false
        while actual is not None: # si el valor de actual no es none se ingresa al bucle
            if not actual.tarea.completada:  #se verifica que la tarea no haya sido completada
                tareas_pendientes = True # el valor de la variable tareas_pendientes pasa a ser true
                print(actual) # se imprime las tareas que esten pendientes.
            actual = actual.siguiente # se recorre la lista enlazada cambiando el valor de actual por el valor siguiente   
        if not tareas_pendientes: # se verifica el valor de la variable anteriormente creada tareas_pendientes que guarda el valor true si hay tareas pendientes y false en caso de no haya.
            print ("No hay tareas pendientes.") # se imprime en pantalla que no hay tareas pendientes.
            
    def mostrar_tareas_descripcion(self,text)->None: # este metodo nos muestra las tareas que coinciden con el texto ingresado por el usuario, se verifica si ese texto pertenece a una parte de la descripcion. 
        actual = self.cabeza # se le asigna el valor de self.cabeza a la variable actual.
        encontrado = False  # se crea una variable encontrado con el valor false
        while actual != None: # si el valor de actual no es none se ingresa al bucle
            if text in actual.tarea.descripcion: # se verifica si el texto forma parte de la descripcion con el comando in
                print (actual) # se imprime en pantalla las tareas que coincidan con ese texto
                encontrado = True # el valor de la variable enconrado cambia a True
            actual = actual.siguiente # se recorre la lista
        if not encontrado: # si no se encontraron coincidencias se imprime en pantalla que no se encontro tarea.
            print ("No se encontro una tarea con esa descripción")
    
    def mostrar_tareas_categorias(self,categoria)->None: # este metodo muestra las tareas en pantalla que coincidan con la categoria dada por el usuario
        actual= self.cabeza # se le asigna el valor self.cabeza a la variable actual
        encontrado = False # se crea la variable encontrado con el valor false
        while actual != None: # se ingresa al bucle cuando actual no sea none
            if actual.tarea.categoria == categoria: # se verifica que la categoria de actual sea igual a la ingresada por el usuario
                print (actual) # si la categoria era igual se imprime en pantalla las tareas
                encontrado = True # el valor de la variable encontrado pasa a ser true
            actual= actual.siguiente #se recorre la lista
        if not encontrado: # si no se encontro la misma caracteristica se imprime en pantalla.
            print ("No se encontro una tarea con esa caracteristica")
    
        
    # Funciones estadisticas:
    
    #def contar_tareas_pendientes_lineal(self)->int:
     #   actual = self.cabeza
      #  tareas_pendientes = 0
       # while actual is not None:
        #    if not actual.tarea.completada:
         #       tareas_pendientes += 1
          #  actual = actual.siguiente
        #return tareas_pendientes
          
    def contar_tareas_pendientes_cte (self) ->int: # este metodo sirve para contar de manera constante la cantidad de tareas pendientes.
        return self.cantidad_tareas # se retorna el valor de cantidad_tareas.
    
    def contar_tareas_completadas(self)-> int: # este metodo es una manera lineal de contar las tareas completadas.
        actual= self.cabeza # se crea la variable actual con el valor self.cabeza
        tareas_completadas = 0 # el contador de tareas esta en 0
        while actual is not None: # si actual no es none se ingresa al bucle
            if actual.tarea.completada: # se verifica si la tarea fue completada
                tareas_completadas +=1 # si la tarea fue completada se agrega uno a la variable tarea_completadas
            actual = actual.siguiente # se recorre la lista
        return tareas_completadas # se retorna el valor de la variable tareas_completadas
    
    def mostrar_estadisticas(self)->None: # este metodo nos muestra las estadisticas de las tareas.
        completadas = self.contar_tareas_completadas() # se crea la variable completadas y se le asigna el valor del metodo contar_tareas_completdas()
        pendientes = self.contar_tareas_pendientes_cte() #se crea la variable pendientes y se le asigna el valor del metodo contar_tareas_pendientes_cte()
        print(f"La cantidad de tareas pendientes por categoria son: {self.categorias_pendientes}") # se imprime la cantidad de tareas pendientes por categorias
        print(f"El total de tareas pendientes es: {pendientes}") # se imprime el total de tareas pendientes
        print(f"El total de tareas completadas es: {completadas}") # se imprime el total de tareas completadas.
        
    # Carga y guardado de archivos
    def guardar_en_csv(self, archivo):
        with open(archivo, mode='w', newline='') as file:
            writer = csv.writer(file)
            actual = self.cabeza
            while actual is not None:
                writer.writerow([actual.tarea.id, actual.tarea.descripcion, actual.tarea.prioridad, actual.tarea.categoria, actual.tarea.completada])
                actual = actual.siguiente
        print(f"Tareas guardadas en {archivo} con éxito.")

    def cargar_desde_csv(self, archivo):
        if not os.path.exists(archivo):
            print(f"Archivo {archivo} no encontrado.")
            return
        with open(archivo, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                id, descripcion, prioridad, categoria, completada = int(row[0]), row[1], int(row[2]), row[3], row[4] == 'True'
                tarea = Tarea(id, descripcion, prioridad, categoria)
                tarea.completada = completada
                self.agregar_tarea_existente(tarea)
            print(f"Tareas cargadas desde {archivo} con éxito.")

    def agregar_tarea_existente(self, tarea): # este metodo nos ayuda a cargar desde el archivo csv las tareas almacenadas.
        nuevo_nodo = Nodo(tarea) #se guarda la tarea (en nodo) cómo un nuevo_nodo que se agregará a la listaEnlazada
        #if not tarea.completada: #verificamos si la tarea fue completada.
        if not tarea.completada: # verificamos si la tarea fue completada
            self.cantidad_tareas = self.cantidad_tareas + 1  # se actualiza el valor del contador para llevar el conteo de las tareas pendientes.
        if self.esta_vacia() or tarea.prioridad > self.cabeza.tarea.prioridad: #se utiliza un condicional if para comprobar si la lista está vacpia o si la prioridad de la nueva tarea es mayor que la prioridad de la tarea que está en la cabeza de la lista. Si la prioridad es mayor, la tarea debe ir al principio de la lista.
            nuevo_nodo.siguiente = self.cabeza #se actualiza la referencia del nuevo nodo, asignando que el siguiente nodo del nuevo nodo sea el actual nodo en la cabeza de la lista
            self.cabeza = nuevo_nodo #se actualiza la cabeza de la lista donde nuevo_nodo será la nueva cabeza de la lista (colocando la tarea con amyor prioridad en la parte superior de la lista)
        else: #en caso contrario
            actual = self.cabeza # se crea la variable actual con el valor self.cabeza
            while actual.siguiente is not None and actual.siguiente.tarea.prioridad >= tarea.prioridad: #recorre la lista hasta encontrar el lugar en donde va a insertar el nuevo nodo
                actual = actual.siguiente # se recorre la lista
            nuevo_nodo.siguiente = actual.siguiente #se actualiza la referencia del nuevo_ nodo y el siguiente del nuevo nodo será el nodo que estaba despues del nodo actual
            actual.siguiente = nuevo_nodo #se agrega el nuevo nodo a la lista, el nodo siguiente del nodo actual será el nuevo nodo insertandolo en la posición correcta
        
        if not tarea.completada: #verifica si la tarea fue completada
                if tarea.categoria in self.categorias_pendientes: # se verifica si la categoria pertenece al diccionario categorias_pendientes
                    self.categorias_pendientes[tarea.categoria] += 1 # si la categoria pertenece a categorias_pendientes se le suma uno al valor 
                else:  # si la categoria no esta en categorias_pendientes se crea una clave y un valor nuevo en la linea siguiente
                    self.categorias_pendientes[tarea.categoria] = 1

        if tarea.id >= self.id_actual:   # se verifica si el id de la tarea es mayor o igual a self.id_actual
            self.id_actual = tarea.id + 1  # si el id es mayor se le suma 1 al valor de id de tareas.id, esto sirve para poder restablecer el numero de id una vez que cargamos las tareas del archivo csv.

def menu(): #se define el menu del sistema mostrando las opciones (funcionalidades)
    print("\nMenú:")
    print("1. Agregar tarea")
    print("2. Completar tarea")
    print("3. Eliminar tarea")
    print("4. Mostrar todas las tareas")
    print("5. Mostrar tareas pendientes")
    print("6. mostrar tareas por caracteristicas")
    print("7. Guardar tareas en archivo CSV")
    print("8. Cargar tareas desde archivo CSV")
    print("9. buscar tarea")
    print("10. Mostrar estadisticas")
    print("11. Salir")

def main(): #se define la funcion main 
    lista_tareas = ListaEnlazada() #se guarda la lista enlazada en lista de tareas
    archivo_csv = 'tareas.csv' 

    # Cargar tareas desde CSV si el archivo existe
    lista_tareas.cargar_desde_csv(archivo_csv)

    while True:
        menu() #se llama al metodo menu
        opcion = input("Seleccione una opción: ") #se guarda la opcion que ingrese el usuario en opcion
        
        if opcion == "1": #Si la opcion es igual a 1 entra a esta condicion
            descripcion = input("Ingrese la descripción de la tarea: ") #la descripcion se ingrese el usuario se guarda en descirpcion
            categoria = input("Ingrese la categoría de la tarea: ") #la categoria que ingrese el usuario se guarda en categoria
            try: #con este bloque se maneja excepciones y errores por si el usuario ingresa una opcion invalida
                prioridad =int(input("Ingrese la prioridad de la tarea (1 = baja, 2 = media, 3 = alta): ")) #se guarda la prioridad que ingrese el usuario en prioridad
                if prioridad in {1,2,3}: #is prioridad es 1, 2, 3
                    lista_tareas.agregar_tarea(descripcion, prioridad, categoria) #se llama al método de agregar tarea para agregar la tarea que ingresa el usuario
                else: #en caso cntrario que el usuario no ingresa 1, 2 o 3 e ingresa otro numero
                    print ("Prioridad invalida. Debe ser un numero del 1 al 3") #mostrara este mensaje
            except ValueError: #si ingresa otro tipo de dato como letra o simbolo
                print ("Entrada invalida. Debe ser un numero del 1 al 3") #mostrara este mensaje
                
        elif opcion == "2": #si la opcion es igual a 2 entra a esta condicion
            try: #con este bloque se maneja excepciones y errores por si el usuario ingresa una opcion invalida
                id_tarea = int(input("Ingrese el ID de la tarea a completar: ")) #el id que ingrese el usuario se guarda en id_tarea
                lista_tareas.completar_tarea(id_tarea) #se llama al método completar tarea para marcarla como completada
            except ValueError: #si ingresa otro tipo de dato como letra o simbolo
                print ("Entrada invalida. El ID es un numero") #mostrara este mensaje
                
        elif opcion == "3": #si la opcion es igual a 3 entra a esta condicion
            try: #con este bloque se maneja excepciones y errores por si el usuario ingresa una opcion invalida
                id_tarea = int(input("Ingrese el ID de la tarea a eliminar: ")) #el id que ingrese el usuario se guarda en id_tarea
                lista_tareas.eliminar_tarea(id_tarea) #se llama al método eliminar tarea para eliminarla  
            except ValueError: #si ingresa otro tipo de dato como letra o simbolo
                print("Entrada invalida. El ID es un numero") #mostrara este mensaje
            
        elif opcion == "4": #si la opcion es igual a 4 entra a esta condicion
            lista_tareas.mostrar_tareas() #se llama al método mostrar tareas para mostrar la lista de tareas
            
        elif opcion == "5": #si la opcion es igual a 5 entra a esta condicion
            lista_tareas.mostrar_tareas_pendientes() #se llama al método mostrar tareas pendientes para mostrar la lista de tareas pendientes
            
        elif opcion == "6": #si la opcion es igual a 6 entra a esta condicion
            categoria = input("ingrese una categoria: ") #la categoria que ingrese el usuario se guarda en la variable categoria
            lista_tareas.mostrar_tareas_categorias(categoria) #se llama al método mostrar tareas categorias para mostrar las tareas de la categoria que ingrese el usuario
        
        elif opcion == "7": #si la opcion es igual a 7 entra a esta condicion
            lista_tareas.guardar_en_csv(archivo_csv) #se llama al método guardar en csv para guardar el archivo
       
        elif opcion == "8": #si la opcion es igual a 8 entra a esta condicion
            
            lista_tareas.cargar_desde_csv(archivo_csv) #se llama al método cargar desde csv para cargar un archivo
            
        elif opcion == "9": #si la opcion es igual a 9 entra a esta condicion
            descripcion = input("ingrese descripcion de la tarea: ") #la descripcion que el usuario ingrese se almacena en la variable descripcion
            lista_tareas.mostrar_tareas_descripcion(descripcion) #se llama al metodo mostrar tareas descripcion para mostrar las taras segun la descripcion que ingrese el usuario
            
        elif opcion == "10": #si la opcion es igual a 10 entra a esta condicion
            lista_tareas.mostrar_estadisticas() #se llama al metodo mostrar estadisticas
            
        elif opcion == "11": #si la opcion es igual a 11 entra a esta condicion
            print("Saliendo del sistema de gestión de tareas.") #muestra este mensaje
            break #salida del bucle
        
        else: #pertenece al primer if (opcion 1) y en caso de que el usuario ingresa una opcion invalida, muestra el mensaje de la linea de abajo
            print("Opción no válida. Por favor, seleccione una opción válida.")

if __name__ == "__main__":
    main()

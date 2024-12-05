from funciones.opciones import *

opcion=0

while opcion!=9:
    menu()

    try:
        opcion = int(input("Ingrese la opcion que desee: "))
            
    
        #Mostrar
        if opcion==1:

            Mostrar_productos()
        
        #Alta productos
        elif opcion==2:
            AltaProducto()

        #Eliminar Productos
        elif opcion==3:

            print("\n1-Eliminar por nombre.\n2-Eliminar por id.")
            eleccion=int(input("\nSeleccione como desea buscar el producto a eliminar: "))
            
            if eleccion==1:
                Eliminar_productos()
            elif eleccion==2:
                Eliminar_productos_id()
            else:
                print("Opcion invalida")
        
        #Modificar Productos
        elif opcion==4:
            
            print("\n1-Modificar por nombre.\n2-Modificar por id.")
            eleccion=int(input("\nSeleccione como desea buscar el producto a modificar: "))
            
            if eleccion==1:
                Modificar_producto()
            elif eleccion==2:
                Modificar_producto_id()
            else:
                print("Opcion invalida")
        
        #Buscar Productos
        elif opcion==5:
            buscar_producto()
        
        #Productos bajo stock
        elif opcion==6:
            
            reporte_bajo_stock()
        
        elif opcion==9:
            
            print("\n\tSaliendo del programa")
            print("\tMuchas gracias, que tenga buen dia")
            conn.close()
        else:
            print("\n\tOpcion invalida")
    
    except ValueError:

        print("\nPor favor, ingrese un número entero válido.")

import sqlite3

conn=sqlite3.connect('inventario.db')

cursor= conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS productos (
id INTEGER PRIMARY KEY AUTOINCREMENT,
nombre TEXT NOT NULL,
descripcion TEXT NOT NULL,
cantidad INTEGER NOT NULL,
precio REAL NOT NULL,
categoria TEXT NOT NULL )
''')

#menu
def menu ():
    print("""
    \n\t********************** \n\t Menú de opciones \n\t**********************\n
    1. Consultar lista de productos.
    2. Agregar un producto.
    3. Eliminar producto.
    4. Modificar producto.
    5. Buscar producto.
    6. Productos bajo stock.
    9. Salir del programa.\n
    """)

#Funcion de carga de categorias
def categorias():
    
    lista=["Almacén","Bebidas","Lácteos","Congelados","Limpieza"]
    
    opcion = True
    while opcion:
        
        print("\nCategoría:\n\t1. Almacén.\n\t2. Bebidas.\n\t3. Lácteos.\n\t4. Congelados.\n\t5. Limpieza")
        categoria = int(input("\nIngrese la categoría del producto: "))
    
        

        if categoria in [1,2,3,4,5]:
        
            categoria = lista[categoria-1]
            opcion = False

        else:
            print("\nOpción inválida.")
            
    return categoria


#Mostrar todos los productos
def Mostrar_productos():

    cursor.execute("SELECT * FROM productos")
    productos=cursor.fetchall()
    
    if productos:
        for producto in productos:
            print(f"\nID:{producto[0]},\nNombre:{producto[1]},\nDescripción: {producto[2]},\nCantidad:{producto[3]} unidades,\nPrecio: ${producto[4]},\nCategoría:{producto[5]}")
    
    else:
        print("\nNo hay productos agregados en la base de datos.")


#Alta de productos
def AltaProducto():
    try:
        producto = str(input("\nIngrese un nuevo producto: ").lower())
        descripcion = str(input("\nIngrese una breve descripción del producto: ").lower())
        
        # Validación para que no se carguen campos vacíos
        if not producto or not descripcion:
            print("\nError: Debe ingresar un producto y una descripción.")
            return
        
        cantidad = int(input("\nIngrese la cantidad de stock del producto: "))
        precio = float(input("\nIngrese el precio del producto: "))

        categoria = categorias()
        
        cursor.execute("INSERT INTO productos (nombre, descripcion, cantidad, precio, categoria) VALUES (?, ?, ?, ?, ?)", (producto, descripcion, cantidad, precio, categoria))
        conn.commit()
        print("\nProducto agregado con éxito.")
        
    except ValueError:
        print("\nError: La cantidad y/o precio deben ser números.")



# Eliminar productos por nombre
def Eliminar_productos():
    
    cursor.execute("SELECT nombre FROM productos")
    productos = [producto[0].lower() for producto in cursor.fetchall()]

    prod = input("\nIngrese el producto que desea eliminar: ").lower()

    if prod in productos:
            
        while True:
            
            print(f"\n¡Se eliminarán TODOS los productos con el nombre {prod}!")
            pregunte = input(f"\n¿Está seguro de eliminar el producto {prod}? S=sí o N=no: ")
                
            if pregunte in ["S", "s"]:
                cursor.execute("DELETE FROM productos WHERE nombre = ?", (prod,))
                conn.commit()
                print("\nProducto eliminado con éxito.")
                break
                
            elif pregunte in ["N", "n"]:

                print("\nSe canceló la eliminación del producto.")
                break

            else:
                print("\nOpción inválida.")
    else:
        print("\nEl producto no existe en la base de datos.\n\nVolviendo al menú principal.")


#Eliminar producto por id
def Eliminar_productos_id():
    
    prod_id=int(input("\nIngrese el ID del producto que desea eliminar: "))
    cursor.execute("SELECT * FROM productos WHERE id = ?",(prod_id,))
    prod=cursor.fetchone()
        
    if prod!=None:
            
        while True:
            
            print("\nDatos del producto a eliminar:")
            print("\n\tID:",prod[0])
            print("\tNombre:",prod[1])
            print("\tDescripción:",prod[2])
            print("\tCantidad:",prod[3],"unidades")
            print("\tPrecio: $",prod[4])
            print("\tCategoría:",prod[5])
            pregunte = input(f"\n¿Está seguro de eliminar el producto {prod[1]}? S=si o N=no: ")

            if pregunte in ["S", "s"]:
                cursor.execute("DELETE FROM productos WHERE id = ?",(prod,))
                conn.commit()
                print("\nProducto eliminado con éxito.")
                break
                    
            elif pregunte in ["N", "n"]:

                print("\nSe canceló la eliminación del producto.")
                break

            else:
                print("\nOpción inválida.")
            
    else:
        print("\nProducto no encontrado.")


#Modificar producto por nombre
def Modificar_producto():

    cursor.execute("SELECT nombre FROM productos")
    productos=[producto[0].lower() for producto in cursor.fetchall()]
    print("\nSe modificara el primer producto que la aplicación encuentre con el nombre que seleccione.")
    prod=input("\nIndique que producto desea modificar: ").lower()
    
    if prod in productos:

        cursor.execute("SELECT * FROM productos WHERE nombre = ?",(prod,))
        producto_modificar=cursor.fetchone()
        
        while True:

            print("""\n\t1. Modificar nombre.\n\t2. Modificar descripcion. \n\t3. Modificar Stock. \n\t4. Modificar precio. \n\t5. Modificar categoria. \n\t6. Modicar todos los datos. \n""")

            try:
                eleccion = int(input("Ingrese la opción que desee: "))
                if eleccion not in [1, 2, 3, 4, 5, 6]:
                    print("\nOpción inválida. Por favor, ingrese una opción válida.\n")
                    continue
            except ValueError:
                print("\nError. Ingrese un número válido.\n")
                continue
            
            #Modificar nombre
            if eleccion==1:
                nombre=input("\nIngrese el nuevo nombre del producto: ").lower()
                cursor.execute("UPDATE productos SET nombre = ? WHERE id = ?",(nombre,producto_modificar[0]))
                conn.commit()
                print("\nNombre modificado con éxito.")
                break

            #Modificar descripcíon
            elif eleccion==2:
                descripcion=input("\nIngrese la nueva descripción del producto: ").lower()
                cursor.execute("UPDATE productos SET descripcion = ? WHERE id = ?",(descripcion,producto_modificar[0]))
                conn.commit()
                print("\nDescripción modificada con éxito.")
                break

                #Modificar stock
            elif eleccion==3:
                try:
                    stock=int(input("\nIngrese el nuevo stock del producto: "))
                    cursor.execute("UPDATE productos SET cantidad = ? WHERE id = ?",(stock,producto_modificar[0]))
                    conn.commit()
                    print("\nStock modificado con éxito.")
                    break
                except ValueError:
                    print("\nError. El stock debe ser un número entero.")

            #Modificar precio
            elif eleccion==4:
                try:
                    precio=float(input("\nIngrese el nuevo precio del producto: "))
                    cursor.execute("UPDATE productos SET precio = ? WHERE id = ?",(precio,producto_modificar[0]))
                    conn.commit()
                    print("\nPrecio modificado con éxito.")
                    break
                except ValueError:
                    print("\nError. El precio debe ser un número (ej: 1200.00).")
                
            #Modificar categoria
            elif eleccion==5:
                    
                print("\nSeleccione la nueva categoría del producto.")
                categoria=categorias()
                    
                cursor.execute("UPDATE productos SET categoría = ? WHERE id =?",(categoria,producto_modificar[0]))
                conn.commit()
                print("\nCategoría modificada con éxito.")
                break
                
            #Modificar todos los datos
            elif eleccion==6:
                try:
                    nombre=input("\nIngrese el nuevo nombre del producto: ").lower()
                    descripcion=input("\nIngrese la nueva descripción del producto: ").lower()
                    stock=int(input("\nIngrese el nuevo stock del producto: "))
                    precio=float(input("\nIngrese el nuevo precio del producto: "))
                        
                    categoria=categorias()

                    cursor.execute("UPDATE productos SET nombre =? ,descripcion = ? ,cantidad = ? ,precio = ?, categoria = ?  WHERE id = ? ",(nombre,descripcion,stock,precio,categoria,producto_modificar[0]))
                    conn.commit()
                    print("\nProducto modificado con éxito.")
                    break
                except ValueError:
                    print("\nError. El stock y/o precio deben ser números.")
        
    else:
        print("\nEl producto no existe en la base de datos.")

#Modificar producto por id
def Modificar_producto_id():

    prod = int(input("\nIndique el id del producto que desea modificar: "))
    cursor.execute("SELECT * FROM productos WHERE id = ?", (prod,))
    producto = cursor.fetchone()

    if producto:
        
        while True:

            print("\n\t1. Modificar nombre.\n\t2. Modificar descripcion.\n\t3. Modificar Stock\n\t4. Modificar precio.\n\t5. Modificar categoria.\n\t6. Modificar todos los datos.")

            try:
                eleccion = int(input("\nIngrese la opción que desee: "))
                if eleccion not in [1, 2, 3, 4, 5, 6]:
                    print("\nOpción inválida. Por favor, ingrese una opción válida.\n")
                    continue
            except ValueError:
                print("\nError. Ingrese un número válido.\n")
                continue

            # Modificar nombre
            if eleccion == 1:
                nombre = input("\nIngrese el nuevo nombre del producto: ").lower()
                cursor.execute("UPDATE productos SET nombre = ? WHERE id = ?", (nombre, producto[0]))
                conn.commit()
                print("\nNombre modificado con éxito.")
                break

            # Modificar descripción
            elif eleccion == 2:
                descripcion = input("\nIngrese la nueva descripción del producto: ").lower()
                cursor.execute("UPDATE productos SET descripcion = ? WHERE id = ?", (descripcion, producto[0]))
                conn.commit()
                print("\nDescripción modificada con éxito.")
                break

            # Modificar stock
            elif eleccion == 3:
                try:
                    stock = int(input("\nIngrese el nuevo stock del producto: "))
                    cursor.execute("UPDATE productos SET cantidad = ? WHERE id = ?", (stock, producto[0]))
                    conn.commit()
                    print("\nStock modificado con éxito.")
                    break
                except ValueError:
                    print("\nError. El stock debe ser un número entero.")
            
            # Modificar precio
            elif eleccion == 4:
                try:
                    precio = float(input("\nIngrese el nuevo precio del producto: "))
                    cursor.execute("UPDATE productos SET precio = ? WHERE id = ?", (precio, producto[0]))
                    conn.commit()
                    print("\nPrecio modificado con éxito.")
                    break
                except ValueError:
                    print("\nError. El precio debe ser un número (ej: 1200.00).")
            
            # Modificar categoría
            elif eleccion == 5:
                print("\nSeleccione la nueva categoría del producto.")
                categoria=categorias()
                cursor.execute("UPDATE productos SET categoria = ? WHERE id = ?", (categoria, producto[0]))
                conn.commit()
                print("\nCategoría modificada con éxito.")
                break

            # Modificar todos los datos
            elif eleccion == 6:
                try:
                    nombre = input("\nIngrese el nuevo nombre del producto: ").lower()
                    descripcion = input("\nIngrese la nueva descripción del producto: ").lower()
                    
                    #Validacion para que no se carguen campos vacios
                    if not producto or not descripcion:
                        print("\nError: Debe ingresar un producto y una descripción.")
                        return

                    stock = int(input("\nIngrese el nuevo stock del producto: "))
                    precio = float(input("\nIngrese el nuevo precio del producto: "))

                    print("\nSeleccione la nueva categoría del producto.")
                    categoria=categorias()

                    cursor.execute(
                        "UPDATE productos SET nombre = ?, descripcion = ?, cantidad = ?, precio = ?, categoria = ? WHERE id = ?",
                        (nombre, descripcion, stock, precio, categoria, producto[0])
                    )
                    conn.commit()
                    print("\nProducto modificado con éxito.")
                    break
                except ValueError:
                    print("\nError. El stock y/o precio deben ser números válidos.")

    else:
        print("\nEl producto no existe en la base de datos.")


#Buscar producto
def buscar_producto():
    opcion=True
    
    while opcion:
        
        producto_buscar=input("\nIngrese el nombre del producto a buscar: ").lower()
        cursor.execute("SELECT * FROM productos WHERE nombre = ?",(producto_buscar,))
        producto_buscar=cursor.fetchall()
        
        if producto_buscar:
            print("\nProducto encontrado:\n")
            for producto in producto_buscar:
                print("\tNombre:",producto[1])
                print("\tDescripción:",producto[2])
                print("\tCantidad:",producto[3],"unidades")
                print("\tPrecio: $",producto[4])
                print("\tCategoria:",producto[5],"\n")
            
        else:
            print("\nProducto no encontrado.")
        
        while True:
            consulta=input("\n¿Desea buscar otro producto? S:si o N:no : ")

            if consulta in ["S","s"]:
                break
            elif consulta in ["N","n"]:
                opcion=False
                break
            else:
                print("\nOpción no válida. Por favor, ingrese S o N.")



#Reporte bajo stock
def reporte_bajo_stock():
    try:
        reporte_min=int(input("\nIngrese el indice minimo de unidades que quiere que muestre el reporte: "))
        
        cursor.execute("SELECT * FROM productos WHERE cantidad <= ?",(reporte_min,))
        reporte_bajo_stock=cursor.fetchall()

        if reporte_bajo_stock:
            print(f"\n\nReporte de productos de {reporte_min} unidades o menos:")
            print("\t------------------------")
            print("\tProductos con stock bajo")
            print("\t------------------------")
            
            for reporte_final in reporte_bajo_stock:
                print(f"\n\t ID: {reporte_final[0]},\n\t Producto: {reporte_final[1]},\n\t Descripción: {reporte_final[2]},\n\t Cantidad: {reporte_final[3]} unidades,\n\t Precio: ${reporte_final[4]},\n\t Categoría: {reporte_final[5]}")
            print("\t------------------------\n")

        else:
            print("\nNo hay productos con stock bajo.")
    except ValueError:
        print("\nError, por favor ingrese un valor numerico.")

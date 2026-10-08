import sqlite3
from colorama import Fore, Back, Style  # type: ignore

def inventario_db():
    """
    Crea la base de datos y la tabla 'productos' si no existen.
    """
    try:
        # Conectar a la base de datos (se crea si no existe)
        conexion = sqlite3.connect('inventario.db')
        cursor = conexion.cursor()
        
        # Crear la tabla 'productos'
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                descripcion TEXT,
                cantidad INTEGER NOT NULL,
                precio REAL NOT NULL,
                categoria TEXT
            )
        ''')
        
        # Guardar los cambios y cerrar la conexión
        conexion.commit()
        print(Fore.GREEN + "Base de datos 'inventario.db' y tabla 'productos' creadas exitosamente." + Fore.RESET)
        
    except sqlite3.Error as error:
        print(Fore.RED + f"Error al crear la base de datos: {error}" + Fore.RESET)
        conexion.rollback()
    
    finally:
        if conexion:
            conexion.close()


def agregar_producto():
    """
    Permite agregar un nuevo producto.
    """
    conexion = sqlite3.connect("inventario.db")
    cursor = conexion.cursor()
    print("\nAlta de Producto\n")
    
    nombre = input("Ingrese el nombre del producto: ").strip()
    descripcion = input("Ingrese la descripcion del producto: ").strip()        
    cantidad = input("Ingrese la cantidad del producto: ").strip() 
    precio = input("Ingrese el precio del producto: ").strip() 
    categoria = input("Ingrese la categoría del producto: ").strip()

    if nombre == "" or descripcion == "" or cantidad == "" or precio == "" or categoria == "":
        print(Fore.RED + "Ningún campo puede estar vacío" + Fore.RESET)
        return
    
    else:
        try:
            cantidad = int(cantidad)
            precio = float(precio)
            
            cursor.execute("""
                           INSERT INTO productos (nombre, descripcion, cantidad, precio, categoria)
                           VALUES (?, ?, ?, ?, ?)
                           """, (nombre, descripcion, cantidad, precio, categoria))
            
            print(Fore.GREEN + "\n El producto fue agregado correctamente\n" + Fore.RESET)
            conexion.commit()
            
        except ValueError:
            print(Fore.RED + "La cantidad y/o precio deben ser valores numéricos" + Fore.RESET)
            conexion.rollback()
        except sqlite3.Error as error:
            print(Fore.RED + f"Error al agregar producto: {error}" + Fore.RESET)
            conexion.rollback()

    conexion.close()


def visualizar_productos():
    """
    Muestra todos los productos registrados en la base de datos.
    Verifica si la tabla esta vacia antes de intentar mostrar.
    """
    print(Fore.BLUE + "\n\t\t--- Lista de Productos ---\n" + Fore.RESET)
    conexion = sqlite3.connect('inventario.db')
    cursor = conexion.cursor()
        
    cursor.execute('SELECT * FROM productos')
    productos = cursor.fetchall()

    if not productos:
        print(Fore.RED + "No hay productos cargados." + Fore.RESET)
        return

    for producto in productos:
        print(f"""
              ID: {producto[0]}
              Nombre: {producto[1]}
              Descripción: {producto[2]}
              Cantidad: {producto[3]}
              Precio: ${producto[4]}
              Categoría: {producto[5]}
              ----------------------------
              """)
            
    conexion.close()
  
def verificar_id_existe(id_producto):
    """
    Verifica si un ID de producto existe en la base de datos.
    """
    try:
        conexion = sqlite3.connect('inventario.db')
        cursor = conexion.cursor()
        cursor.execute('SELECT id FROM productos WHERE id = ?', (id_producto,))
        producto = cursor.fetchone()
        conexion.close()
        return producto is not None
    except:
        return False

def cambio_de_nombre():
    """
    Actualiza solo el nombre de un producto por su ID.
    """
    try:
        id_producto = input("Ingrese el ID del producto: ").strip()
        if not id_producto.isdigit():
            print(Fore.RED + "El ID debe ser un número entero." + Fore.RESET)
            return
        
        id_producto = int(id_producto)
        
        # Verificar si el ID existe
        if not verificar_id_existe(id_producto):
            print(Fore.RED + f"No existe un producto con ID {id_producto}." + Fore.RESET)
            return
        
        nuevo_nombre = input("Ingresa el nuevo nombre para el producto: ").strip()
        if nuevo_nombre == "":
            print(Fore.RED + "El nombre no puede estar vacío" + Fore.RESET)
            return
        
        conexion = sqlite3.connect('inventario.db')
        cursor = conexion.cursor()
        
        cursor.execute('UPDATE productos SET nombre = ? WHERE id = ?', (nuevo_nombre, id_producto))
        conexion.commit()
        
        print(Fore.GREEN + "El nombre ha sido cambiado exitosamente." + Fore.RESET)

        # Mostrar el producto actualizado
        cursor.execute('SELECT * FROM productos WHERE id = ?', (id_producto,))
        producto_actualizado = cursor.fetchone()
        
        if producto_actualizado:
            print(Fore.BLUE + "\n Producto Actualizado" + Fore.RESET)
            print(f"ID: {producto_actualizado[0]}, Nombre: {producto_actualizado[1]}, Descripcion: {producto_actualizado[2]}")
            print(f"Cantidad: {producto_actualizado[3]}, Precio: {producto_actualizado[4]}, Categoria: {producto_actualizado[5]}")
        
        conexion.close()
        
    except sqlite3.Error as error:
        print(Fore.RED + f"Error al actualizar: {error}" + Fore.RESET)
    except Exception as error:
        print(Fore.RED + f"Error inesperado: {error}" + Fore.RESET)

def cambio_de_descripcion():
    """
    Actualiza la descripción del producto por ID.
    """
    try:
        id_producto = input("Ingrese el ID del producto: ").strip()
        if not id_producto.isdigit():
            print(Fore.RED + "El ID debe ser un número entero." + Fore.RESET)
            return
        
        id_producto = int(id_producto)
        
        # Verificar si el ID existe
        if not verificar_id_existe(id_producto):
            print(Fore.RED + f"No existe un producto con ID {id_producto}." + Fore.RESET)
            return
        
        nueva_descripcion = input("Ingresa la nueva descripcion para el producto: ").strip()
        
        conexion = sqlite3.connect('inventario.db')
        cursor = conexion.cursor()
        
        cursor.execute('UPDATE productos SET descripcion = ? WHERE id = ?', (nueva_descripcion, id_producto))
        conexion.commit()
        
        print(Fore.GREEN + "La descripcion ha sido cambiada exitosamente." + Fore.RESET)

        # Mostrar el producto actualizado
        cursor.execute('SELECT * FROM productos WHERE id = ?', (id_producto,))
        producto_actualizado = cursor.fetchone()
        
        if producto_actualizado:
            print(Fore.BLUE + "\n Producto Actualizado" + Fore.RESET)
            print(f"ID: {producto_actualizado[0]}, Nombre: {producto_actualizado[1]}, Descripcion: {producto_actualizado[2]}")
            print(f"Cantidad: {producto_actualizado[3]}, Precio: {producto_actualizado[4]}, Categoria: {producto_actualizado[5]}")
        
        conexion.close()
        
    except sqlite3.Error as error:
        print(Fore.RED + f"Error al actualizar: {error}" + Fore.RESET)
    except Exception as error:
        print(Fore.RED + f"Error inesperado: {error}" + Fore.RESET)

def cambio_de_cantidad():
    """
    Actualiza la cantidad en stock y emite alerta si queda por debajo del umbral.
    """
    try:
        id_producto = input("Ingrese el ID del producto: ").strip()
        if not id_producto.isdigit():
            print(Fore.RED + "El ID debe ser un número entero." + Fore.RESET)
            return
        
        id_producto = int(id_producto)
        
        # Verificar si el ID existe
        if not verificar_id_existe(id_producto):
            print(Fore.RED + f"No existe un producto con ID {id_producto}." + Fore.RESET)
            return
        
        numero_cantidad = input("Ingresa la nueva cantidad para el producto: ").strip()
        if not numero_cantidad.isdigit():
            print(Fore.RED + "La cantidad debe ser un número entero." + Fore.RESET)
            return
        
        nueva_cantidad = int(numero_cantidad)
        UMBRAL_STOCK_BAJO = 5
        
        conexion = sqlite3.connect('inventario.db')
        cursor = conexion.cursor()
        
        cursor.execute('UPDATE productos SET cantidad = ? WHERE id = ?', (nueva_cantidad, id_producto))
        conexion.commit()
        
        print(Fore.GREEN + "El stock ha sido actualizado exitosamente." + Fore.RESET)

        # ALERTA DE STOCK BAJO - Versión mejorada con más visibilidad
        if nueva_cantidad <= UMBRAL_STOCK_BAJO:
            cursor.execute('SELECT nombre, cantidad FROM productos WHERE id = ?', (id_producto,))
            producto_info = cursor.fetchone()
            if producto_info:
                nombre_producto = producto_info[0]
                cantidad_actual = producto_info[1]
                
                print("\n" + "!" * 60)
                print(Fore.RED + Back.YELLOW + " " * 20 + "⚠️  ALERTA: STOCK BAJO ⚠️" + " " * 20 + Style.RESET_ALL)
                print("!" * 60)
                print(Fore.RED + f"\nATENCIÓN: El producto '{nombre_producto}'")
                print(Fore.RED + f"tiene solo {cantidad_actual} unidades disponibles.")
                print(Fore.RED + f"Se recomienda reponer stock lo antes posible.\n")
                
                # Mostrar emojis visuales según el nivel de stock
                if cantidad_actual == 0:
                    print(Fore.RED + "🚫 STOCK AGOTADO - URGENTE REPONER 🚫")
                elif cantidad_actual <= 2:
                    print(Fore.RED + "🔴 STOCK MUY BAJO - REPONER INMEDIATAMENTE 🔴")
                elif cantidad_actual <= 5:
                    print(Fore.YELLOW + "🟡 STOCK BAJO - REPONER PRONTO 🟡")
                
                print(Style.RESET_ALL + "\n" + "-" * 60)

        # Mostrar el producto actualizado
        cursor.execute('SELECT * FROM productos WHERE id = ?', (id_producto,))
        producto_actualizado = cursor.fetchone()
        
        if producto_actualizado:
            print(Fore.BLUE + "\n Producto Actualizado" + Fore.RESET)
            print(f"ID: {producto_actualizado[0]}, Nombre: {producto_actualizado[1]}, Descripcion: {producto_actualizado[2]}")
            print(f"Cantidad: {producto_actualizado[3]}, Precio: {producto_actualizado[4]}, Categoria: {producto_actualizado[5]}")
        
        conexion.close()
        
    except sqlite3.Error as error:
        print(Fore.RED + f"Error al actualizar: {error}" + Fore.RESET)
    except Exception as error:
        print(Fore.RED + f"Error inesperado: {error}" + Fore.RESET)
    
def cambio_de_precio():
    """Actualiza el precio del producto por ID."""
    try:
        id_producto = input("Ingrese el ID del producto: ").strip()
        if not id_producto.isdigit():
            print(Fore.RED + "El ID debe ser un número entero." + Fore.RESET)
            return
        
        id_producto = int(id_producto)
        
        # Verificar si el ID existe
        if not verificar_id_existe(id_producto):
            print(Fore.RED + f"No existe un producto con ID {id_producto}." + Fore.RESET)
            return
        
        try:
            nuevo_precio = float(input("Ingresa el nuevo precio para el producto: "))
        except ValueError:
            print(Fore.RED + "El precio debe ser un número válido." + Fore.RESET)
            return
        
        conexion = sqlite3.connect('inventario.db')
        cursor = conexion.cursor()
        
        cursor.execute('UPDATE productos SET precio = ? WHERE id = ?', (nuevo_precio, id_producto))
        conexion.commit()
        
        print(Fore.GREEN + "El precio ha sido actualizado exitosamente." + Fore.RESET)

        # Mostrar el producto actualizado
        cursor.execute('SELECT * FROM productos WHERE id = ?', (id_producto,))
        producto_actualizado = cursor.fetchone()
        
        if producto_actualizado:
            print(Fore.BLUE + "\n Producto Actualizado" + Fore.RESET)
            print(f"ID: {producto_actualizado[0]}, Nombre: {producto_actualizado[1]}, Descripcion: {producto_actualizado[2]}")
            print(f"Cantidad: {producto_actualizado[3]}, Precio: {producto_actualizado[4]}, Categoria: {producto_actualizado[5]}")
        
        conexion.close()
        
    except sqlite3.Error as error:
        print(Fore.RED + f"Error al actualizar: {error}" + Fore.RESET)
    except Exception as error:
        print(Fore.RED + f"Error inesperado: {error}" + Fore.RESET)

def cambio_de_categoria():
    """Actualiza la categoría del producto por ID."""
    try:
        id_producto = input("Ingrese el ID del producto: ").strip()
        if not id_producto.isdigit():
            print(Fore.RED + "El ID debe ser un número entero." + Fore.RESET)
            return
        
        id_producto = int(id_producto)
        
        # Verificar si el ID existe
        if not verificar_id_existe(id_producto):
            print(Fore.RED + f"No existe un producto con ID {id_producto}." + Fore.RESET)
            return
        
        nueva_categoria = input("Ingresa la nueva categoria para el producto: ").strip()
        if nueva_categoria == "":
            print(Fore.RED + "La categoría no puede estar vacía" + Fore.RESET)
            return
        
        conexion = sqlite3.connect('inventario.db')
        cursor = conexion.cursor()
        
        cursor.execute('UPDATE productos SET categoria = ? WHERE id = ?', (nueva_categoria, id_producto))
        conexion.commit()
        
        print(Fore.GREEN + "La categoria ha sido actualizada exitosamente." + Fore.RESET)

        # Mostrar el producto actualizado
        cursor.execute('SELECT * FROM productos WHERE id = ?', (id_producto,))
        producto_actualizado = cursor.fetchone()
        
        if producto_actualizado:
            print(Fore.BLUE + "\n Producto Actualizado" + Fore.RESET)
            print(f"ID: {producto_actualizado[0]}, Nombre: {producto_actualizado[1]}, Descripcion: {producto_actualizado[2]}")
            print(f"Cantidad: {producto_actualizado[3]}, Precio: {producto_actualizado[4]}, Categoria: {producto_actualizado[5]}")
        
        conexion.close()
        
    except sqlite3.Error as error:
        print(Fore.RED + f"Error al actualizar: {error}" + Fore.RESET)
    except Exception as error:
        print(Fore.RED + f"Error inesperado: {error}" + Fore.RESET)

def actualizar_producto():
    """
    Menu para seleccionar que modificar de un producto.
    """
    while True:
        print(Fore.BLUE + "\n¿Qué dato desea modificar?\n" + Fore.RESET)
        print("1. Nombre")
        print("2. Descripcion")
        print("3. Cantidad")
        print("4. Precio")
        print("5. Categoria")
        print("6. Volver al Menu Principal")
        
        try:
            opcion = int(input("Ingrese la opción deseada: "))
        except ValueError:
            print(Fore.RED + "Error: Por favor, ingrese un número válido" + Fore.RESET)
            continue 
        
        if opcion == 1:
            cambio_de_nombre()
        elif opcion == 2:
            cambio_de_descripcion()
        elif opcion == 3:    
            cambio_de_cantidad()
        elif opcion == 4:
            cambio_de_precio()
        elif opcion == 5:
            cambio_de_categoria()
        elif opcion == 6:
            print("Volviendo al Menu Principal...")
            break
        else:
            print(Fore.RED + "Error: Ingresa una opcion valida del 1 al 6." + Fore.RESET)

def eliminar_por_id():
    """
    Elimina un producto por su ID.
    Usa rowcount para verificar si realmente se eliminó algo.
    """
    try:
        conexion = sqlite3.connect('inventario.db')
        cursor = conexion.cursor()
        id_producto = input("\nPor favor ingrese el ID del producto: ").strip()
        
        if not id_producto.isdigit():
            print(Fore.RED + "Error: Debe ingresar un número entero válido de ID." + Fore.RESET)
            return
            
        id_eliminar = int(id_producto)
        cursor.execute('DELETE FROM productos WHERE id = ?', (id_eliminar,))
        conexion.commit()
        
        if cursor.rowcount == 0:
            print(Fore.RED + f"No se ha encontrado el producto con ID '{id_eliminar}'" + Fore.RESET)
        else:
            print(Fore.GREEN + f"Producto con ID '{id_eliminar}' eliminado del inventario." + Fore.RESET)

    except sqlite3.Error as error:
        print(Fore.RED + f"Error al acceder a la base de datos: {error}" + Fore.RESET)
    except Exception as error:
        print(Fore.RED + f"Error inesperado: {error}" + Fore.RESET)
    finally:
        if conexion:
            conexion.close()

def eliminar_por_nombre():
    """
    Elimina un producto por su nombre.
    Usa rowcount para verificar si realmente se eliminó algo.
    """
    try:
        conexion = sqlite3.connect('inventario.db')
        cursor = conexion.cursor()
        nombre_producto = input("\nPor favor ingrese el nombre del producto: ").strip()
        
        cursor.execute('DELETE FROM productos WHERE nombre = ?', (nombre_producto,))
        conexion.commit()
        
        if cursor.rowcount == 0:
            print(Fore.RED + f"No se ha encontrado el producto '{nombre_producto}'" + Fore.RESET)
        else:
            print(Fore.GREEN + f"Producto '{nombre_producto}' eliminado del inventario." + Fore.RESET)

    except sqlite3.Error as error:
        print(Fore.RED + f"Error al acceder a la base de datos: {error}" + Fore.RESET)
    except Exception as error:
        print(Fore.RED + f"Error inesperado: {error}" + Fore.RESET)
    finally:
        if conexion:
            conexion.close()

def eliminar_por_categoria():
    """
    Elimina un producto por su categoria.
    Usa rowcount para verificar si realmente se eliminó algo.
    """
    try:
        conexion = sqlite3.connect('inventario.db')
        cursor = conexion.cursor()
        categoria_producto = input("\nPor favor ingrese la categoria del producto: ").strip()
        
        cursor.execute('DELETE FROM productos WHERE categoria = ?', (categoria_producto,))
        conexion.commit()
        
        if cursor.rowcount == 0:
            print(Fore.RED + f"No se ha encontrado la categoria '{categoria_producto}'" + Fore.RESET)
        else:
            print(Fore.GREEN + f"Productos de la categoria '{categoria_producto}' eliminados del inventario." + Fore.RESET)

    except sqlite3.Error as error:
        print(Fore.RED + f"Error al acceder a la base de datos: {error}" + Fore.RESET)
    except Exception as error:
        print(Fore.RED + f"Error inesperado: {error}" + Fore.RESET)
    finally:
        if conexion:
            conexion.close()

def buscar_producto():
    """
    Busca y muestra un producto por su ID.
    """
    conexion = None
    try:
        conexion = sqlite3.connect('inventario.db')
        cursor = conexion.cursor()
        print("Buscando...\n")
        producto_a_buscar = input("\nPor favor ingrese el ID del producto: ").strip()
        
        if not producto_a_buscar.isdigit():
            print(Fore.RED + "Error: Debe ingresar un número entero válido como ID." + Fore.RESET)
            return
            
        producto_id = int(producto_a_buscar)
        cursor.execute('SELECT * FROM productos WHERE id = ?', (producto_id,))
        producto_encontrado = cursor.fetchone()
        
        if producto_encontrado:
            print(Fore.BLUE + "\n Producto Encontrado" + Fore.RESET)
            print(f"ID: {producto_encontrado[0]}, Nombre: {producto_encontrado[1]}, Descripcion: {producto_encontrado[2]}")
            print(f"Cantidad: {producto_encontrado[3]}, Precio: {producto_encontrado[4]}, Categoria: {producto_encontrado[5]}")
        else:
            print(Fore.RED + f"\nNo se encontro ningun producto con el ID {producto_id}." + Fore.RESET)
        
    except sqlite3.Error as error:
        print(Fore.RED + f"Error al acceder a la base de datos: {error}" + Fore.RESET)
    except Exception as error:
        print(Fore.RED + f"Error inesperado: {error}" + Fore.RESET)
    finally:
        if conexion:
            conexion.close()

def mostrar_stock_bajo():
    """
    Muestra todos los productos con stock bajo (<= 5 unidades).
    """
    UMBRAL_STOCK_BAJO = 5
    
    try:
        conexion = sqlite3.connect('inventario.db')
        cursor = conexion.cursor()
        
        cursor.execute('SELECT * FROM productos WHERE cantidad <= ? ORDER BY cantidad ASC', (UMBRAL_STOCK_BAJO,))
        productos_bajo_stock = cursor.fetchall()
        
        if not productos_bajo_stock:
            print(Fore.GREEN + "\n✅ No hay productos con stock bajo." + Fore.RESET)
            return
        
        print("\n" + "="*70)
        print(Fore.RED + "📊 PRODUCTOS CON STOCK BAJO (≤ 5 unidades)" + Fore.RESET)
        print("="*70)
        
        for producto in productos_bajo_stock:
            id_producto, nombre, descripcion, cantidad, precio, categoria = producto
            
            # Determinar el color según la cantidad
            if cantidad == 0:
                color = Fore.RED
                estado = "AGOTADO"
                emoji = "🚫"
            elif cantidad <= 2:
                color = Fore.RED
                estado = "MUY BAJO"
                emoji = "🔴"
            else:
                color = Fore.YELLOW
                estado = "BAJO"
                emoji = "🟡"
            
            print(f"\n{emoji} {color}ID: {id_producto} - {nombre}{Fore.RESET}")
            print(f"   Cantidad: {color}{cantidad} unidades - {estado}{Fore.RESET}")
            print(f"   Categoría: {categoria}")
            print(f"   Precio: ${precio}")
            print(f"   Descripción: {descripcion}")
            print(f"   {'─'*60}")
        
        print(f"\n📈 {Fore.YELLOW}Total de productos con stock bajo: {len(productos_bajo_stock)}{Fore.RESET}")
        
        conexion.close()
        
    except sqlite3.Error as error:
        print(Fore.RED + f"Error al acceder a la base de datos: {error}" + Fore.RESET)

def eliminar_producto():
    """
    Menú para seleccionar cómo eliminar productos.
    """
    while True:
        print(Fore.BLUE + "\n¿Cómo desea identificar el producto a eliminar?\n" + Fore.RESET)
        print("1. Por ID")
        print("2. Por Categoría")
        print("3. Por Nombre")
        print("4. Volver al Menú Principal")
        
        try:
            opcion = int(input("Ingrese la opción deseada: "))
        except ValueError:
            print(Fore.RED + "Error: Por favor, ingrese un número válido" + Fore.RESET)
            continue
            
        if opcion == 1:
            eliminar_por_id()
        elif opcion == 2:
            eliminar_por_categoria()
        elif opcion == 3:    
            eliminar_por_nombre()
        elif opcion == 4:
            print("Volviendo al Menú Principal...")
            break
        else:
            print(Fore.RED + "Error: Ingrese una opción válida del 1 al 4." + Fore.RESET)

def menu_principal():
    """
    Muestra el menu principal del sistema.
    """
    print("\n" + "="*50)
    print("Sistema de Gestión Básica De Productos")
    print("="*50 + "\n")

    print("1. Agregar producto")
    print("2. Mostrar productos")
    print("3. Actualizar producto")
    print("4. Buscar producto")
    print("5. Eliminar producto")
    print("6. Ver productos con stock bajo")
    print("7. Salir\n")

### Programa Principal ###

# Inicializar la base de datos primero
inventario_db()

while True:
    menu_principal()
    
    try:
        opcion = int(input("Ingrese la opción deseada (1-7): "))
    except ValueError:
        print(Fore.RED + "Error: Por favor, ingrese un número válido." + Fore.RESET)
        continue
    
    if opcion == 1:
        agregar_producto()
    elif opcion == 2:
        visualizar_productos()
    elif opcion == 3:    
        actualizar_producto()
    elif opcion == 4:
        buscar_producto()
    elif opcion == 5:
        eliminar_producto()
    elif opcion == 6:
        mostrar_stock_bajo()
    elif opcion == 7:
        print("\n" + "="*50)
        print("Gracias por usar la aplicación")
        print("="*50)
        break
    else: 
        print(Fore.RED + "Error: Ingresó una opción incorrecta. Por favor, ingrese un número del 1 al 7." + Fore.RESET)
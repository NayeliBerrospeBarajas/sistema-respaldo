
import os
import shutil
from datetime import datetime






# Carpeta que queremos respaldar
CARPETA_ORIGEN = r"C:\Users\Neye\Documents\carpeta_a_respaldar"

# Carpeta donde se guardarán los respaldos
CARPETA_BACKUPS = r"C:\Users\Neye\Documents\respaldo"



# CREAR CARPETAS NECESARIAS


def preparar_carpetas():

    if not os.path.exists(CARPETA_ORIGEN):
        os.makedirs(CARPETA_ORIGEN)

    if not os.path.exists(CARPETA_BACKUPS):
        os.makedirs(CARPETA_BACKUPS)



# CREAR RESPALDO


def crear_backup():


    print("       CREACION DE RESPALDO")


    if not os.path.exists(CARPETA_ORIGEN):
        print("La carpeta de origen no existe.")
        return

    # Obtener fecha y hora actual
    fecha = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Nombre del respaldo
    nombre_backup = "backup_" + fecha

    # Ruta completa donde se guardará
    destino = os.path.join(CARPETA_BACKUPS, nombre_backup)

    try:

        shutil.copytree(CARPETA_ORIGEN, destino)

        print("\nRespaldo realizado correctamente.")
        print("Ubicacion:")
        print(destino)

    except Exception as error:

        print("\nOcurrio un error al crear el respaldo:")
        print(error)



# MOSTRAR RESPALDOS


def obtener_backups():

    if not os.path.exists(CARPETA_BACKUPS):
        return []

    backups = []

    for elemento in os.listdir(CARPETA_BACKUPS):

        ruta = os.path.join(CARPETA_BACKUPS, elemento)

        if os.path.isdir(ruta) and elemento.startswith("backup_"):
            backups.append(elemento)

    # Ordenar del más reciente al más antiguo
    backups.sort(reverse=True)

    return backups


def mostrar_backups():


    print("       RESPALDOS DISPONIBLES")


    backups = obtener_backups()

    if len(backups) == 0:
        print("No existen respaldos.")
        return

    for i, backup in enumerate(backups, start=1):
        print(f"{i}. {backup}")



# SELECCIONAR UN RESPALDO


def seleccionar_backup():

    backups = obtener_backups()

    if len(backups) == 0:
        print("\nNo existen respaldos disponibles.")
        return None

    print("\nRespaldos disponibles:")

    for i, backup in enumerate(backups, start=1):
        print(f"{i}. {backup}")

    while True:

        try:

            opcion = int(input("\nSelecciona un respaldo: "))

            if opcion >= 1 and opcion <= len(backups):

                return backups[opcion - 1]

            else:

                print("Opcion inválida.")

        except ValueError:

            print("Debes escribir un numero.")



# RECUPERACION TOTAL


def recuperar_total():

    print("\n======================================")
    print("       RECUPERACION TOTAL")
    print("======================================")

    backup = seleccionar_backup()

    if backup is None:
        return

    origen = os.path.join(CARPETA_BACKUPS, backup)

    print("\nEste proceso restaurara TODOS los archivos.")
    confirmar = input("¿Deseas continuar? (s/n): ")

    if confirmar.lower() != "s":
        print("Operacion cancelada.")
        return

    try:

        # Copiar todos los archivos del respaldo
        for elemento in os.listdir(origen):

            ruta_origen = os.path.join(origen, elemento)
            ruta_destino = os.path.join(CARPETA_ORIGEN, elemento)

            if os.path.isdir(ruta_origen):

                if os.path.exists(ruta_destino):
                    shutil.rmtree(ruta_destino)

                shutil.copytree(ruta_origen, ruta_destino)

            else:

                shutil.copy2(ruta_origen, ruta_destino)

        print("\nRecuperación total completada correctamente.")

    except Exception as error:

        print("\nError durante la recuperación:")
        print(error)



# RECUPERACIÓN DE CARPETA


def recuperar_carpeta():


    print("       RECUPERACION DE CARPETA")


    backup = seleccionar_backup()

    if backup is None:
        return

    ruta_backup = os.path.join(CARPETA_BACKUPS, backup)

    # Buscar carpetas dentro del respaldo
    carpetas = []

    for elemento in os.listdir(ruta_backup):

        ruta = os.path.join(ruta_backup, elemento)

        if os.path.isdir(ruta):
            carpetas.append(elemento)

    if len(carpetas) == 0:

        print("\nEl respaldo no contiene carpetas.")
        return

    print("\nCarpetas disponibles:")

    for i, carpeta in enumerate(carpetas, start=1):
        print(f"{i}. {carpeta}")

    try:

        opcion = int(input("\nSelecciona una carpeta: "))

        if opcion < 1 or opcion > len(carpetas):

            print("Opción invalida.")
            return

        carpeta_seleccionada = carpetas[opcion - 1]

        origen = os.path.join(ruta_backup, carpeta_seleccionada)
        destino = os.path.join(CARPETA_ORIGEN, carpeta_seleccionada)

        if os.path.exists(destino):

            shutil.rmtree(destino)

        shutil.copytree(origen, destino)

        print("\nCarpeta recuperada correctamente.")
        print("Carpeta:", carpeta_seleccionada)

    except ValueError:

        print("Debes escribir un numero.")

    except Exception as error:

        print("\nError durante la recuperacion:")
        print(error)


# ==========================================================
# RECUPERACION DE ARCHIVO INDIVIDUAL
# ==========================================================

def recuperar_archivo():

    print("       RECUPERACION DE ARCHIVO")


    backup = seleccionar_backup()

    if backup is None:
        return

    ruta_backup = os.path.join(CARPETA_BACKUPS, backup)

    # Buscar archivos dentro del respaldo
    archivos = []

    for raiz, carpetas, nombres_archivos in os.walk(ruta_backup):

        for archivo in nombres_archivos:

            ruta_completa = os.path.join(raiz, archivo)

            # Guardar ruta relativa
            ruta_relativa = os.path.relpath(
                ruta_completa,
                ruta_backup
            )

            archivos.append(ruta_relativa)

    if len(archivos) == 0:

        print("\nEl respaldo no contiene archivos.")
        return

    print("\nArchivos disponibles:")

    for i, archivo in enumerate(archivos, start=1):

        print(f"{i}. {archivo}")

    try:

        opcion = int(input("\nSelecciona un archivo: "))

        if opcion < 1 or opcion > len(archivos):

            print("Opcion invalida.")
            return

        archivo_seleccionado = archivos[opcion - 1]

        origen = os.path.join(
            ruta_backup,
            archivo_seleccionado
        )

        destino = os.path.join(
            CARPETA_ORIGEN,
            archivo_seleccionado
        )

        # Crear las carpetas necesarias
        carpeta_destino = os.path.dirname(destino)

        if not os.path.exists(carpeta_destino):

            os.makedirs(carpeta_destino)

        shutil.copy2(origen, destino)

        print("\nArchivo recuperado correctamente.")
        print("Archivo:", archivo_seleccionado)

    except ValueError:

        print("Debes escribir un numero.")

    except Exception as error:

        print("\nError durante la recuperacion:")
        print(error)



# MENÚ PRINCIPAL

def menu():

    preparar_carpetas()

    while True:

        print("\n")
        print("======================================")
        print("       SISTEMA DE RESPALDO")
        print("       Y RECUPERACION")
        print("======================================")

        print("\nCarpeta protegida:")
        print(CARPETA_ORIGEN)

        print("\n1. Crear respaldo")
        print("2. Ver respaldos")
        print("3. Recuperacion total")
        print("4. Recuperar una carpeta")
        print("5. Recuperar un archivo")
        print("6. Salir")

        opcion = input("\nSelecciona una opcion: ")

        if opcion == "1":

            crear_backup()

        elif opcion == "2":

            mostrar_backups()

        elif opcion == "3":

            recuperar_total()

        elif opcion == "4":

            recuperar_carpeta()

        elif opcion == "5":

            recuperar_archivo()

        elif opcion == "6":

            print("\nPrograma finalizado.")
            break

        else:

            print("\nOpción invalida.")

        input("\nPresiona ENTER para continuar...")



# INICIO DEL PROGRAMA


if __name__ == "__main__":

    menu()


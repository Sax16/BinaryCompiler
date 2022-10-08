from PyQt5 import QtWidgets, uic, QtTest
from time import sleep

# Iniciamos la app
app = QtWidgets.QApplication([])

# Cargamos archivos .ui
comp = uic.loadUi("generator.ui")

# Declarar nemonicos y sus valores en hexadecimal preestablecidos
NEMONICOS: dict[str, int] = {
    "NOT" : 0x00,
    "NAND, n" : 0x10,
    "ADD, n" : 0x20,
    "LDA, n" : 0x30,
    "OUTA" : 0x40,
    "OUTB" : 0x50,
    "INA" : 0x60,
    "RD" : 0x70,
    "RA" : 0x80,
    "LDRA" : 0x90,
    "JPI, n" : 0xc0,
    "JPC, n" : 0xd0,
    "JPZ, n" : 0xe0
}

# Declarando capacidad de memoria
CM: int = 256

# Creando las 255 direcciones de memoria incizializados en ceros -> [Valor_Nemonico, Operando]
direcciones: list[list[int]] = [[0x00, 0x00] for i in range(CM)]

def generar_file():
    # Obtenemos el nombre del archivo dado
    nombre_archivo = comp.namefile.text()

    # Manejando nombre vacio
    if nombre_archivo == "":
        nombre_archivo = "default.bin"
    # Comprobamos si el nombre termina en .bin sino le agregamos
    elif nombre_archivo[-4:] != ".bin":
        nombre_archivo += ".bin"
    
    # Crear archivo y escribir en binario todas las direcciones
    try:
        with open(nombre_archivo, 'wb') as f:
            # Agrupamos los 4 bits del nemonico y 4 bits del operando mediante una suma
            allBytes: list[int] = [sum(x) for x in direcciones]

            # Obtenemos todos los bytes
            allBytes: bytes = bytes(bytearray(allBytes))

            # Escribimos los bytes en el archivo
            f.write(allBytes)

            # Mensaje de exito
            comp.exito.setText("¡¡¡Archivo generado!!!")
            # Paramos ejecucion 2 segundos
            QtTest.QTest.qWait(3000)
            # Desaparecemos mensaje
            comp.exito.setText("")
    # Si ocurre algun error
    except Exception as e:
        # Mostramos mensaje de error
        comp.error.setText(f"Ocurrió un Error: {e}")
        # Paramos ejecucion 2 segundos
        QtTest.QTest.qWait(3000)
        # Desaparecemos mensaje
        comp.error.setText("")


def update_res(pos: int):
    try:
        # Validar Operando válido y generamos un error si este es mayor a 0xE a la vez dará error si no es un hexadevimal
        validadando_operando = f'''
if int(comp.ope_{pos}.text(), 16) > 0xF:
    raise ValueError
'''
        exec(validadando_operando)

        # Cambiar instruccion de operando en la direccion correspondiente
        cambiar_direccion = f'direcciones[{pos}][1] = int(comp.ope_{pos}.text(), 16)'
        exec(cambiar_direccion)

        # Generamos codigo para concatenar el valor del nemonico y del operando en el resultado en mayuscula
        actualizar_resultado = f'comp.res_{pos}.setText(hex(NEMONICOS[comp.nem{pos}.currentText()])[2].upper() + comp.ope_{pos}.text().upper())'
        exec(actualizar_resultado)
    except:
        # Generamos codigo para concatenar el valor del nemonico y del operando invalido con -
        actualizar_resultado = f'comp.res_{pos}.setText(hex(NEMONICOS[comp.nem{pos}.currentText()])[2].upper() + "-")'
        exec(actualizar_resultado)

def update_nem(value: str, pos: int):
    # Cambiar instruccion de nemonico en la direccion correspondiente
    direcciones[pos][0] = NEMONICOS[value]

    # Obtenemos en str el valor solo en hexadecimal del nemonico en Mayuscula
    valor_hex: str = hex(NEMONICOS[value])[2].upper()

    # Previniendo el error de operando vacio
    prev = f'''
if comp.ope_{pos}.text() == "":
    comp.ope_{pos}.setText("0")
'''
    exec(prev)

    # Generamos codigo para concatenar el valor del nemonico y del operando en el resultado
    actualizar_resultado = f'comp.res_{pos}.setText(valor_hex + comp.ope_{pos}.text().upper())'
    exec(actualizar_resultado)


# Evento de boton generar
comp.generarfile.clicked.connect(generar_file)

# Detectar los cambios de todos los operandos
for i in range(256):
    codigo_operandos: str = f"comp.ope_{i}.textChanged.connect(lambda: update_res({i}))"
    codigo_nemonicos: str = f"comp.nem{i}.currentTextChanged.connect(lambda value: update_nem(value, {i}))"
    exec(codigo_operandos)
    exec(codigo_nemonicos)

# Ejecutable
comp.show()
app.exec()
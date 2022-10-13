# Declarar nemonicos y sus valores en hexadecimal preestablecidos
NEMONICOS: dict[str, int] = {
    "NOT" : 0x00,
    "NAND" : 0x10,
    "ADD" : 0x20,
    "LDA" : 0x30,
    "OUTA" : 0x40,
    "OUTB" : 0x50,
    "INA" : 0x60,
    "RD" : 0x70,
    "RA" : 0x80,
    "LDRA" : 0x90,
    "JPI" : 0xc0,
    "JPC" : 0xd0,
    "JPZ" : 0xe0
}

# Declarando capacidad de memoria
CM: int = 256

# Creando las 255 direcciones de memoria incizializados en ceros -> [Valor_Nemonico, Operando]
direcciones: list[list[int]] = [[0x00, 0x00] for i in range(CM)]

def main() -> None:
    # Mostrar instruccones
    print_instruction()

    for i in range(CM):
        # Solicitar si desea ingresar una instruccion
        opcion: bool = add_instruction()

        # Desea ingresar una instruccion
        if opcion:
            # Solicitar nemonico
            nemonico: int = get_nemonico(i)

            # Evitar solicitar operando para los nemonicos q' lo ignoran
            if (nemonico == 0x00) or (nemonico >= 0x40 and nemonico <= 0x90):
                operando :int = 0x00
            else:
                # Solicitar operando
                operando: int = get_operando(i)
            
            # Cambiar la instruccion en el lugar correspondiente
            direcciones[i] = [nemonico, operando]

        # No desea ingresar otra instruccion
        else:
            break

    # Solicitar nombre del archivo
    nombre_archivo = input("\nIngrese nombre de archivo (.bin): ")
    # Previniendo entrada vacia
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

    except Exception as e:
        print("\nERROR AL CREAR EL ARCHIVO")
        print(e)

    input("\nPresiona Enter para salir...")


def print_instruction() -> None:
    print("""
╔═════════════════════════════════════════════════════════════════════════════════════════════════════════╗
▓                                          ##      ###                                                    ▓
▓                                                   ##                                                    ▓
▓     ####     ####    ##  ##   ######    ###       ##      ####    ######               ##  ##    ####   ▓
▓    ##  ##   ##  ##   #######   ##  ##    ##       ##     ##  ##    ##  ##              ##  ##   ##  ##  ▓
▓    ##       ##  ##   ## # ##   ##  ##    ##       ##     ######    ##        ===       ##  ##   ##      ▓
▓    ##  ##   ##  ##   ##   ##   #####     ##       ##     ##        ##        ===       ##  ##   ##  ##  ▓
▓     ####     ####    ##   ##   ##       ####     ####     #####   ####                  ######   ####   ▓
▓                               ####                                                                      ▓
╚═════════════════════════════════════════════════════════════════════════════════════════════════════════╝
╔═════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
| BIN |  HEX  |   Nemónico   |                       Descripción                           |     Observaciones    |
═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════
| 0   |   0   |     NOT      |           No hace nada, sirve para hacer delays             |  Ignora el operando  |
| 1   |   1   |    NAND      |            NAND entre operando y el acumulador              |                      |
| 10  |   2   |     ADD      |              Suma el operando al acumulador                 |                      |
| 11  |   3   |     LDA      |            Carga el operando en el acumulador               |                      |
| 100 |   4   |    OUTA      |   Coloca el valor del acumulador en el puerto de salida A   |  Ignora el operando  |
| 101 |   5   |    OUTB      |   Coloca el valor del acumulador en el puerto de salida B   |  Ignora el operando  |
| 110 |   6   |     INA      |   Carga el valor del puerto de entrada A en el acumulador   |  Ignora el operando  |
| 111 |   7   |     RD       | Coloca el valor del acumulador en el Registro D (dirección) |  Ignora el operando  |
| 1000|   8   |     RA       |       Coloca el valor del acumulador en el Registro A	   |  Ignora el operando  |
| 1001|   9   |    LDRA      |        Carga el valor de Registro A en el acumulador        |  Ignora el operando  |
| 1010|   A   |	             |                                                             |                      |
| 1011|   B   |              |                                                             |                      |
| 1100|   C   |    JPI       |       Salto incondicional a la posición RD+Operando         |                      |
| 1101|   D   |    JPC       |     Salto condicional (CARRY) a la posición RD+Operando     |                      |
| 1110|   E   |    JPZ       |      Salto condicional (ZERO) a la posición RD+Operando     |                      |
| 1111|   F   |              |                                                             |                      |
╚═════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝

Los valores permitidos en los operandos son entre 0 y F

===================================================================================================================

====== INICIANDO ======

""")


def add_instruction() -> bool:
    # Solicitar si ingresara mas instrucciones
    while True:
        opcion = input("Desea ingresar instrucción? (yes, no): ").upper()

        if opcion in ["Y", "YES"]:
            return True
        elif opcion in ["N", "NO"]:
            return False


def get_nemonico(i: int) -> int:
    while True:
        nemonico = input(f"[{i}] - Ingresar nemónico: ").upper()
        # Validar si es un nemonico válido
        if nemonico in NEMONICOS:
            return NEMONICOS[nemonico]


def get_operando(i: int) -> int:
    while True:
        try:
            # Pedir operando
            operando = input(f"[{i}] - Ingresar Operando: ")

            # Permitiendo entrada vacia "" como ceros
            if operando == '':
                return 0x00

            # Llevar a formato hexadecimal -> Esto puede generar un error si no se ingresa un valor hexadecimal
            operando = int(operando, 16)

            # Restringir a operandos entre 0 y A
            if operando > 0xF or operando < 0:
                raise ValueError
            
            return operando

        except:
            print("\nINGRESAR UN VALOR ENTRE 0 y 9!!!\n")


if __name__ == '__main__':
    main()

from datetime import datetime, timedelta
import sys  # Importamos sys para usar sys.exit() para cerrar el programa

class Productor:
    def __init__(self, nombre, telefono):
        self.nombre = nombre
        self.telefono = telefono


class TonelDePulpa:
    def __init__(self, sabor, fecha_venc, precio, productor):
        self.sabor = sabor
        self.fecha_venc = fecha_venc
        self.precio = precio
        self.productor = productor


class LoteDeNectar:
    def __init__(self, codigo, sabor, fecha_prod, precio_tonel):
        self.codigo = codigo
        self.sabor = sabor
        self.fecha_prod = fecha_prod
        self.fecha_venc = (datetime.strptime(fecha_prod, '%Y-%m-%d') + timedelta(days=3*365)).strftime('%Y-%m-%d')
        self.precio_lote = precio_tonel * 1.5 + 400
        self.precio_lata = self.precio_lote / 500


class Factura:
    def __init__(self, cliente, nit):
        self.cliente = cliente
        self.nit = nit
        self.detalle = []

    def agregar_detalle(self, descripcion, cantidad, precio):
        self.detalle.append({'descripcion': descripcion, 'cantidad': cantidad, 'precio': precio})

    def mostrar_factura(self):
        total = sum(item['cantidad'] * item['precio'] for item in self.detalle)
        print("\n--- FACTURA ---")
        print(f"Cliente: {self.cliente}")
        print(f"NIT: {self.nit}")
        for item in self.detalle:
            print(f"{item['descripcion']} x{item['cantidad']} @ Q{item['precio']:.2f}")
        print(f"Total: Q{total:.2f}\n")


class Inventario:
    def __init__(self):
        self.toneles = []
        self.lotes = []
        self.facturas = []

    def ingresar_tonel(self, tonel):
        self.toneles.append(tonel)
        print(f"Tonel de pulpa sabor {tonel.sabor} ingresado exitosamente.")

    def producir_lote(self, sabor, fecha_prod):
        toneles_disponibles = [t for t in self.toneles if t.sabor == sabor and t.fecha_venc >= fecha_prod]
        if not toneles_disponibles:
            print("No hay toneles disponibles para este sabor o están vencidos.")
            return

        tonel = toneles_disponibles.pop(0)
        self.toneles.remove(tonel)
        codigo = len(self.lotes) + 1
        lote = LoteDeNectar(codigo, sabor, fecha_prod, tonel.precio)
        self.lotes.append(lote)
        print(f"Lote {codigo} producido con éxito.")

    def venta_menor(self, sabor, cantidad, cliente, nit):
        lotes_disponibles = [l for l in self.lotes if l.sabor == sabor]
        if not lotes_disponibles:
            print("No hay lotes disponibles para este sabor.")
            return

        factura = Factura(cliente, nit)
        total_cantidad = cantidad

        while total_cantidad > 0 and lotes_disponibles:
            lote = lotes_disponibles[0]
            if total_cantidad <= 500:
                factura.agregar_detalle(f"Latas de néctar sabor {sabor}", total_cantidad, lote.precio_lata)
                self.lotes.remove(lote)
                print(f"Venta completada: {total_cantidad} latas de sabor {sabor}")
                break
            else:
                factura.agregar_detalle(f"Latas de néctar sabor {sabor}", 500, lote.precio_lata)
                total_cantidad -= 500
                self.lotes.remove(lote)

        self.facturas.append(factura)
        factura.mostrar_factura()

    def venta_mayor(self, sabor, cantidad_lotes, cliente, nit):
        lotes_disponibles = [l for l in self.lotes if l.sabor == sabor]
        if len(lotes_disponibles) < cantidad_lotes:
            print("No hay suficientes lotes disponibles para la venta.")
            return

        factura = Factura(cliente, nit)
        for _ in range(cantidad_lotes):
            lote = lotes_disponibles.pop(0)
            factura.agregar_detalle(f"Lote de néctares sabor {sabor}", 1, lote.precio_lote)
            self.lotes.remove(lote)

        self.facturas.append(factura)
        factura.mostrar_factura()

    def listar_toneles(self):
        print("\n--- Toneles Disponibles ---")
        if not self.toneles:
            print("No hay toneles disponibles en el inventario.")
        for tonel in self.toneles:
            print(f"Sabor: {tonel.sabor}, Vence: {tonel.fecha_venc}, Productor: {tonel.productor.nombre}, Tel: {tonel.productor.telefono}")

    def listar_lotes(self):
        print("\n--- Lotes Disponibles ---")
        if not self.lotes:
            print("No hay lotes disponibles.")
        for lote in self.lotes:
            print(f"Lote {lote.codigo}, Sabor: {lote.sabor}, Vence: {lote.fecha_venc}, Precio Lata: Q{lote.precio_lata:.2f}")

    def listar_facturas(self):
        print("\n--- Facturas Generadas ---")
        if not self.facturas:
            print("No hay facturas generadas.")
        for factura in self.facturas:
            factura.mostrar_factura()


# Función principal con menú interactivo
def main():
    inventario = Inventario()

    while True:
        print("\n--- Menú de Opciones ---")
        print("1. Ingresar tonel de pulpa")
        print("2. Producir lote de néctares")
        print("3. Venta al menor (por latas)")
        print("4. Venta al mayor (por lotes)")
        print("5. Listar toneles disponibles")
        print("6. Listar lotes disponibles")
        print("7. Listar facturas")
        print("8. Salir")

        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            sabor = input("Sabor de la pulpa: ")
            fecha_venc = input("Fecha de vencimiento (YYYY-MM-DD): ")
            precio = float(input("Precio del tonel: "))
            nombre = input("Nombre del productor: ")
            telefono = input("Teléfono del productor: ")
            productor = Productor(nombre, telefono)
            tonel = TonelDePulpa(sabor, fecha_venc, precio, productor)
            inventario.ingresar_tonel(tonel)

        elif opcion == "2":
            sabor = input("Sabor a producir: ")
            fecha_prod = input("Fecha de producción (YYYY-MM-DD): ")
            inventario.producir_lote(sabor, fecha_prod)

        elif opcion == "3":
            sabor = input("Sabor a vender: ")
            cantidad = int(input("Cantidad de latas: "))
            cliente = input("Nombre del cliente: ")
            nit = input("NIT del cliente: ")
            inventario.venta_menor(sabor, cantidad, cliente, nit)

        elif opcion == "4":
            sabor = input("Sabor a vender: ")
            cantidad_lotes = int(input("Cantidad de lotes: "))
            cliente = input("Nombre del cliente: ")
            nit = input("NIT del cliente: ")
            inventario.venta_mayor(sabor, cantidad_lotes, cliente, nit)

        elif opcion == "5":
            inventario.listar_toneles()

        elif opcion == "6":
            inventario.listar_lotes()

        elif opcion == "7":
            inventario.listar_facturas()

        elif opcion == "8":
            print("Saliendo del programa.")
            sys.exit()  # Cierra el programa

        else:
            print("Opción inválida. Intente de nuevo.")


if __name__ == "__main__":
    main()

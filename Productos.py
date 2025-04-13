import sys
import mysql.connector
from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QMessageBox
)

class ProductosCRUD(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Catalogo de Productos")
        self.setGeometry(100, 200, 500, 250)

        try:
            self.conn = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="mysql",
                database="Practica13_C22270660"
            )
            self.cursor = self.conn.cursor(dictionary=True)
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Error de conexión a la base", str(e))
            sys.exit(1)

        self.productos = []
        self.indice = -1

        self.layout = QVBoxLayout()
        form_layout = QVBoxLayout()
        btn_layout = QHBoxLayout()
        nav_layout = QHBoxLayout()

        self.tabla = QTableWidget()
        self.tabla.setColumnCount(4)
        self.tabla.setHorizontalHeaderLabels(["ID", "Nombre", "Formato", "Precio"])
        self.layout.addWidget(self.tabla)

        # Entradas
        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("ID")
        self.id_input.setReadOnly(True)

        self.nombre_input = QLineEdit()
        self.nombre_input.setPlaceholderText("Nombre")

        self.formato_input = QLineEdit()
        self.formato_input.setPlaceholderText("Formato de presentación")

        self.precio_input = QLineEdit()
        self.precio_input.setPlaceholderText("Precio")

        form_layout.addWidget(QLabel("ID Producto:"))
        form_layout.addWidget(self.id_input)
        form_layout.addWidget(QLabel("Nombre:"))
        form_layout.addWidget(self.nombre_input)
        form_layout.addWidget(QLabel("Formato de presentación:"))
        form_layout.addWidget(self.formato_input)
        form_layout.addWidget(QLabel("Precio:"))
        form_layout.addWidget(self.precio_input)

        # Botones CRUD
        self.btn_crear = QPushButton("Crear")
        self.btn_modificar = QPushButton("Modificar")
        self.btn_eliminar = QPushButton("Eliminar")
        self.btn_cargar = QPushButton("Cargar")

        self.btn_crear.clicked.connect(self.crear)
        self.btn_modificar.clicked.connect(self.modificar)
        self.btn_eliminar.clicked.connect(self.eliminar)
        self.btn_cargar.clicked.connect(self.cargar_productos)

        btn_layout.addWidget(self.btn_crear)
        btn_layout.addWidget(self.btn_modificar)
        btn_layout.addWidget(self.btn_eliminar)
        btn_layout.addWidget(self.btn_cargar)

        # Botones Navegación
        self.btn_anterior = QPushButton("← Atrás")
        self.btn_siguiente = QPushButton("Siguiente →")
        self.btn_anterior.clicked.connect(self.anterior)
        self.btn_siguiente.clicked.connect(self.siguiente)

        nav_layout.addWidget(self.btn_anterior)
        nav_layout.addWidget(self.btn_siguiente)

        self.layout.addLayout(form_layout)
        self.layout.addLayout(btn_layout)
        self.layout.addLayout(nav_layout)

        self.setLayout(self.layout)

    
    def cargar_productos(self):
        self.cursor.execute("SELECT * FROM Productos ORDER BY id_producto")
        self.productos = self.cursor.fetchall()
        self.indice = 0 if self.productos else -1
        self.mostrar_producto()

    # Mostrar en la tabla
        self.tabla.setRowCount(len(self.productos))
        for row_idx, producto in enumerate(self.productos):
         self.tabla.setItem(row_idx, 0, QTableWidgetItem(str(producto["id_producto"])))
        self.tabla.setItem(row_idx, 1, QTableWidgetItem(producto["nombre"]))
        self.tabla.setItem(row_idx, 2, QTableWidgetItem(producto["formato_presentacion"] or ""))
        self.tabla.setItem(row_idx, 3, QTableWidgetItem(str(producto["precio"])))


    def mostrar_producto(self):
        if 0 <= self.indice < len(self.productos):
            producto = self.productos[self.indice]
            self.id_input.setText(str(producto["id_producto"]))
            self.nombre_input.setText(producto["nombre"])
            self.formato_input.setText(producto["formato_presentacion"] or "")
            self.precio_input.setText(str(producto["precio"]))
        else:
            self.id_input.clear()
            self.nombre_input.clear()
            self.formato_input.clear()
            self.precio_input.clear()

    def crear(self):
        nombre = self.nombre_input.text()
        formato = self.formato_input.text()
        try:
            precio = float(self.precio_input.text())
        except ValueError:
            QMessageBox.warning(self, "Error en la simbologia", "Precio no válido.")
            return

        try:
            self.cursor.execute("INSERT INTO Productos (nombre, formato_presentacion, precio) VALUES (%s, %s, %s)",
                                (nombre, formato, precio))
            self.conn.commit()
            QMessageBox.information(self, "Éxito", "Producto creado.")
            self.cargar_productos()
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Error SQL", str(e))

    def modificar(self):
        try:
            id_producto = int(self.id_input.text())
        except ValueError:
            QMessageBox.warning(self, "Error", "ID inválido.")
            return

        nombre = self.nombre_input.text()
        formato = self.formato_input.text()
        try:
            precio = float(self.precio_input.text())
        except ValueError:
            QMessageBox.warning(self, "Error", "Precio no válido.")
            return

        try:
            self.cursor.execute("UPDATE Productos SET nombre=%s, formato_presentacion=%s, precio=%s WHERE id_producto=%s",
                                (nombre, formato, precio, id_producto))
            self.conn.commit()
            QMessageBox.information(self, "Éxito", "Producto modificado.")
            self.cargar_productos()
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Error SQL", str(e))

    def eliminar(self):
        try:
            id_producto = int(self.id_input.text())
        except ValueError:
            QMessageBox.warning(self, "Error", "ID inválido.")
            return

        try:
            self.cursor.execute("DELETE FROM Productos WHERE id_producto=%s", (id_producto,))
            self.conn.commit()
            QMessageBox.information(self, "Éxito", "Producto eliminado.")
            self.cargar_productos()
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Error SQL", str(e))

    def siguiente(self):
        if self.indice < len(self.productos) - 1:
            self.indice += 1
            self.mostrar_producto()

    def anterior(self):
        if self.indice > 0:
            self.indice -= 1
            self.mostrar_producto()

    def closeEvent(self, event):
        self.cursor.close()
        self.conn.close()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = ProductosCRUD()
    ventana.show()
    sys.exit(app.exec())

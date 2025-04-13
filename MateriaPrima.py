import sys
import mysql.connector
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QMessageBox,
    QTableWidget, QTableWidgetItem
)


class MateriaPrimaCRUD(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Catalo de la  Materia Prima")
        self.setGeometry(100, 100, 600, 400)

        try:
            self.conn = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="mysql",
                database="Practica13_C22270660"
            )
            self.cursor = self.conn.cursor(dictionary=True)
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Error de conexión", str(e))
            sys.exit(1)

        self.materias = []
        self.indice = -1

        self.layout = QVBoxLayout()
        form_layout = QVBoxLayout()
        btn_layout = QHBoxLayout()
        nav_layout = QHBoxLayout()

        self.id_input = QLineEdit()
        self.id_input.setReadOnly(True)
        self.nombre_input = QLineEdit()
        self.cantidad_input = QLineEdit()
        self.costo_input = QLineEdit()
        self.id_proveedor_input = QLineEdit()
        self.id_producto_input = QLineEdit()

        form_layout.addWidget(QLabel("ID Materia Prima:"))
        form_layout.addWidget(self.id_input)
        form_layout.addWidget(QLabel("Nombre:"))
        form_layout.addWidget(self.nombre_input)
        form_layout.addWidget(QLabel("Cantidad:"))
        form_layout.addWidget(self.cantidad_input)
        form_layout.addWidget(QLabel("Costo:"))
        form_layout.addWidget(self.costo_input)
        form_layout.addWidget(QLabel("ID Proveedor:"))
        form_layout.addWidget(self.id_proveedor_input)
        form_layout.addWidget(QLabel("ID Producto:"))
        form_layout.addWidget(self.id_producto_input)

        self.btn_crear = QPushButton("Crear")
        self.btn_modificar = QPushButton("Modificar")
        self.btn_eliminar = QPushButton("Eliminar")
        self.btn_cargar = QPushButton("Cargar")

        self.btn_crear.clicked.connect(self.crear)
        self.btn_modificar.clicked.connect(self.modificar)
        self.btn_eliminar.clicked.connect(self.eliminar)
        self.btn_cargar.clicked.connect(self.cargar_materias)

        btn_layout.addWidget(self.btn_crear)
        btn_layout.addWidget(self.btn_modificar)
        btn_layout.addWidget(self.btn_eliminar)
        btn_layout.addWidget(self.btn_cargar)

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

        self.tabla = QTableWidget()
        self.tabla.setColumnCount(6)
        self.tabla.setHorizontalHeaderLabels([
            "ID", "Nombre", "Cantidad", "Costo", "ID Proveedor", "ID Producto"
        ])
        self.layout.addWidget(self.tabla)
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(6)
        self.tabla.setHorizontalHeaderLabels([
            "ID", "Nombre", "Cantidad", "Costo", "ID Proveedor", "ID Producto"
        ])
        self.layout.addWidget(self.tabla)


    def cargar_materias(self):
        self.cursor.execute("SELECT * FROM MateriaPrima ORDER BY id_materia")
        self.materias = self.cursor.fetchall()
        self.indice = 0 if self.materias else -1
        self.mostrar_materia()
        self.llenar_tabla()

    def llenar_tabla(self):
        self.tabla.setRowCount(len(self.materias))
        for row_idx, materia in enumerate(self.materias):
            self.tabla.setItem(row_idx, 0, QTableWidgetItem(str(materia["id_materia"])))
            self.tabla.setItem(row_idx, 1, QTableWidgetItem(materia["nombre"]))
            self.tabla.setItem(row_idx, 2, QTableWidgetItem(str(materia["cantidad"])))
            self.tabla.setItem(row_idx, 3, QTableWidgetItem(str(materia["costo"])))
            self.tabla.setItem(row_idx, 4, QTableWidgetItem(str(materia["id_proveedor"]) if materia["id_proveedor"] else ""))
            self.tabla.setItem(row_idx, 5, QTableWidgetItem(str(materia["id_producto"]) if materia["id_producto"] else ""))


    def mostrar_materia(self):
        if 0 <= self.indice < len(self.materias):
            materia = self.materias[self.indice]
            self.id_input.setText(str(materia["id_materia"]))
            self.nombre_input.setText(materia["nombre"])
            self.cantidad_input.setText(str(materia["cantidad"]))
            self.costo_input.setText(str(materia["costo"]))
            self.id_proveedor_input.setText(str(materia["id_proveedor"]) if materia["id_proveedor"] else "")
            self.id_producto_input.setText(str(materia["id_producto"]) if materia["id_producto"] else "")
        else:
            self.id_input.clear()
            self.nombre_input.clear()
            self.cantidad_input.clear()
            self.costo_input.clear()
            self.id_proveedor_input.clear()
            self.id_producto_input.clear()

    def crear(self):
        nombre = self.nombre_input.text()
        try:
            cantidad = int(self.cantidad_input.text())
            costo = float(self.costo_input.text())
            id_proveedor = self.id_proveedor_input.text() or None
            id_producto = self.id_producto_input.text() or None
        except ValueError:
            QMessageBox.warning(self, "Error", "Verifica que cantidad y costo sean válidos o que los campos esten llenos.")
            return

        try:
            self.cursor.execute("""
                INSERT INTO MateriaPrima (nombre, cantidad, costo, id_proveedor, id_producto)
                VALUES (%s, %s, %s, %s, %s)
            """, (nombre, cantidad, costo, id_proveedor, id_producto))
            self.conn.commit()
            QMessageBox.information(self, "correcto", "Materia Prima creada.")
            self.cargar_materias()
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Error SQL", str(e))

    def modificar(self):
        try:
            id_materia = int(self.id_input.text())
            cantidad = int(self.cantidad_input.text())
            costo = float(self.costo_input.text())
            id_proveedor = self.id_proveedor_input.text() or None
            id_producto = self.id_producto_input.text() or None
        except ValueError:
            QMessageBox.warning(self, "Error", "Campos numéricos no válidos.")
            return

        nombre = self.nombre_input.text()

        try:
            self.cursor.execute("""
                UPDATE MateriaPrima
                SET nombre=%s, cantidad=%s, costo=%s, id_proveedor=%s, id_producto=%s
                WHERE id_materia=%s
            """, (nombre, cantidad, costo, id_proveedor, id_producto, id_materia))
            self.conn.commit()
            QMessageBox.information(self, "Éxito", "Materia modificada.")
            self.cargar_materias()
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Error SQL", str(e))

    def eliminar(self):
        try:
            id_materia = int(self.id_input.text())
        except ValueError:
            QMessageBox.warning(self, "Error", "ID inválido.")
            return

        try:
            self.cursor.execute("DELETE FROM MateriaPrima WHERE id_materia=%s", (id_materia,))
            self.conn.commit()
            QMessageBox.information(self, "correcto", "La Materia ha sido eliminada.")
            self.cargar_materias()
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Error SQL", str(e))

    def siguiente(self):
        if self.indice < len(self.materias) - 1:
            self.indice += 1
            self.mostrar_materia()

    def anterior(self):
        if self.indice > 0:
            self.indice -= 1
            self.mostrar_materia()

    def closeEvent(self, event):
        self.cursor.close()
        self.conn.close()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = MateriaPrimaCRUD()
    ventana.show()
    sys.exit(app.exec())

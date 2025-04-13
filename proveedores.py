import sys
import mysql.connector
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox
)

class ProveedoresCRUD(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Catalgo Proveedores ")
        self.setGeometry(50, 50, 600, 400)

        try:
            self.conn = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="mysql",
                database="Practica13_C22270660"
            )
            self.cursor = self.conn.cursor()
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Error de conexión", f"No se pudo conectar a la base de datos:\n{e}")
            sys.exit(1)

        self.layout = QVBoxLayout()

        self.id_input = QLineEdit()
        self.nombre_input = QLineEdit()
        self.materia_input = QLineEdit()

        form_layout = QHBoxLayout()
        form_layout.addWidget(QLabel("ID:"))
        form_layout.addWidget(self.id_input)
        form_layout.addWidget(QLabel("Nombre:"))
        form_layout.addWidget(self.nombre_input)
        form_layout.addWidget(QLabel("Materia Prima:"))
        form_layout.addWidget(self.materia_input)
        self.layout.addLayout(form_layout)

        # Botones
        btn_layout = QHBoxLayout()
        self.crear_btn = QPushButton("Crear")
        self.modificar_btn = QPushButton("Modificar")
        self.eliminar_btn = QPushButton("Eliminar")
        self.cargar_btn = QPushButton("Cargar el nuevo producto")

        self.crear_btn.clicked.connect(self.crear_proveedor)
        self.modificar_btn.clicked.connect(self.modificar_proveedor)
        self.eliminar_btn.clicked.connect(self.eliminar_proveedor)
        self.cargar_btn.clicked.connect(self.cargar_datos)

        btn_layout.addWidget(self.crear_btn)
        btn_layout.addWidget(self.modificar_btn)
        btn_layout.addWidget(self.eliminar_btn)
        btn_layout.addWidget(self.cargar_btn)
        self.layout.addLayout(btn_layout)

        # Tabla
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(3)
        self.tabla.setHorizontalHeaderLabels(["ID", "Nombre", "Materia Prima"])
        self.layout.addWidget(self.tabla)

        self.setLayout(self.layout)

    def cargar_datos(self):
        self.tabla.setRowCount(0)
        self.cursor.execute("SELECT * FROM Proveedores")
        resultados = self.cursor.fetchall()
        for row_index, (id_, nombre, materia) in enumerate(resultados):
            self.tabla.insertRow(row_index)
            self.tabla.setItem(row_index, 0, QTableWidgetItem(str(id_)))
            self.tabla.setItem(row_index, 1, QTableWidgetItem(nombre))
            self.tabla.setItem(row_index, 2, QTableWidgetItem(materia))

    def crear_proveedor(self):
        nombre = self.nombre_input.text()
        materia = self.materia_input.text()

        if not nombre or not materia:
            QMessageBox.warning(self, "Tienes un error", "Completa todos los campos,no cambie el ID.")
            return

        try:
            self.cursor.execute("INSERT INTO Proveedores (nombre, materia_prima) VALUES (%s, %s)", (nombre, materia))
            self.conn.commit()
            QMessageBox.information(self, "se a creado con exito", "Proveedor creado.")
            self.cargar_datos()
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Error SQL", str(e))

    def modificar_proveedor(self):
        try:
            id_ = int(self.id_input.text())
        except ValueError:
            QMessageBox.warning(self, "Error", "ID inválido.")
            return

        nombre = self.nombre_input.text()
        materia = self.materia_input.text()

        try:
            self.cursor.execute("UPDATE Proveedores SET nombre=%s, materia_prima=%s WHERE id_proveedor=%s",
                                (nombre, materia, id_))
            self.conn.commit()
            if self.cursor.rowcount == 0:
                QMessageBox.warning(self, "Aviso", f"No se encontró proveedor con ID {id_}.")
            else:
                QMessageBox.information(self, "Éxito", "Proveedor modificado.")
            self.cargar_datos()
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Error SQL", str(e))

    def eliminar_proveedor(self):
        try:
            id_ = int(self.id_input.text())
        except ValueError:
            QMessageBox.warning(self, "Error", "ID inválido.")
            return

        try:
            self.cursor.execute("DELETE FROM Proveedores WHERE id_proveedor=%s", (id_,))
            self.conn.commit()
            if self.cursor.rowcount == 0:
                QMessageBox.warning(self, "Aviso", f"No existe proveedor con ID {id_}.")
            else:
                QMessageBox.information(self, "Éxito", "Proveedor eliminado.")
            self.cargar_datos()
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Error SQL", str(e))

    def closeEvent(self, event):
        self.cursor.close()
        self.conn.close()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = ProveedoresCRUD()
    ventana.show()
    sys.exit(app.exec())

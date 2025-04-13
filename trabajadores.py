import sys
import mysql.connector
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox
)

class TrabajadoresCRUD(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestión de Trabajadores")
        self.setGeometry(100, 100, 600, 400)

        self.db = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="mysql",
            database="Practica13_C22270660"
        )
        self.cursor = self.db.cursor()

        self.layout = QVBoxLayout()

        # Formulario
        self.id_input = QLineEdit()
        self.nombre_input = QLineEdit()
        self.telefono_input = QLineEdit()

        form_layout = QHBoxLayout()
        form_layout.addWidget(QLabel("ID:"))
        form_layout.addWidget(self.id_input)
        form_layout.addWidget(QLabel("Nombre:"))
        form_layout.addWidget(self.nombre_input)
        form_layout.addWidget(QLabel("Teléfono:"))
        form_layout.addWidget(self.telefono_input)
        self.layout.addLayout(form_layout)

        # Botones
        button_layout = QHBoxLayout()
        self.agregar_btn = QPushButton("Crear")
        self.modificar_btn = QPushButton("Modificar")
        self.eliminar_btn = QPushButton("Eliminar")
        self.cargar_btn = QPushButton("Cargar")

        self.agregar_btn.clicked.connect(self.agregar_trabajador)
        self.modificar_btn.clicked.connect(self.modificar_trabajador)
        self.eliminar_btn.clicked.connect(self.eliminar_trabajador)
        self.cargar_btn.clicked.connect(self.cargar_datos)

        button_layout.addWidget(self.agregar_btn)
        button_layout.addWidget(self.modificar_btn)
        button_layout.addWidget(self.eliminar_btn)
        button_layout.addWidget(self.cargar_btn)
        self.layout.addLayout(button_layout)

        # Tabla
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(3)
        self.tabla.setHorizontalHeaderLabels(["ID", "Nombre", "Teléfono"])
        self.layout.addWidget(self.tabla)

        self.setLayout(self.layout)
        self.cargar_datos()

    def cargar_datos(self):
        self.tabla.setRowCount(0)
        self.cursor.execute("SELECT * FROM Trabajadores")
        for row_num, row_data in enumerate(self.cursor.fetchall()):
            self.tabla.insertRow(row_num)
            for col_num, data in enumerate(row_data):
                self.tabla.setItem(row_num, col_num, QTableWidgetItem(str(data)))

    def agregar_trabajador(self):
        id_ = self.id_input.text()
        nombre = self.nombre_input.text()
        telefono = self.telefono_input.text()

        try:
            self.cursor.execute(
                "INSERT INTO Trabajadores (id_trabajador, nombre, numero_telefono) VALUES (%s, %s, %s)",
                (id_, nombre, telefono)
            )
            self.db.commit()
            QMessageBox.information(self, "Éxito", "Trabajador agregado.")
            self.cargar_datos()
        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Error", str(err))

    def modificar_trabajador(self):
        id_ = self.id_input.text()
        nombre = self.nombre_input.text()
        telefono = self.telefono_input.text()

        try:
            self.cursor.execute(
                "UPDATE Trabajadores SET nombre = %s, numero_telefono = %s WHERE id_trabajador = %s",
                (nombre, telefono, id_)
            )
            self.db.commit()
            QMessageBox.information(self, "Éxito", "Trabajador modificado.")
            self.cargar_datos()
        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Error", str(err))

    def eliminar_trabajador(self):
        id_ = self.id_input.text()

        try:
            self.cursor.execute(
                "DELETE FROM Trabajadores WHERE id_trabajador = %s",
                (id_,)
            )
            self.db.commit()
            QMessageBox.information(self, "Éxito", "Trabajador eliminado.")
            self.cargar_datos()
        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Error", str(err))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = TrabajadoresCRUD()
    ventana.show()
    sys.exit(app.exec())

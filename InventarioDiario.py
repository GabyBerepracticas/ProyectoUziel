import sys
import mysql.connector
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QMessageBox
)

class TrabajadorCRUD(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestión de Trabajadores")
        self.setGeometry(200, 200, 400, 200)

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

        self.trabajadores = []
        self.indice = -1

        self.layout = QVBoxLayout()
        form_layout = QVBoxLayout()
        btn_layout = QHBoxLayout()
        nav_layout = QHBoxLayout()

        self.id_input = QLineEdit()
        self.nombre_input = QLineEdit()
        self.telefono_input = QLineEdit()

        form_layout.addWidget(QLabel("ID Trabajador:"))
        form_layout.addWidget(self.id_input)
        form_layout.addWidget(QLabel("Nombre:"))
        form_layout.addWidget(self.nombre_input)
        form_layout.addWidget(QLabel("Teléfono:"))
        form_layout.addWidget(self.telefono_input)

        self.btn_crear = QPushButton("Crear")
        self.btn_modificar = QPushButton("Modificar")
        self.btn_eliminar = QPushButton("Eliminar")
        self.btn_cargar = QPushButton("Cargar")

        self.btn_crear.clicked.connect(self.crear)
        self.btn_modificar.clicked.connect(self.modificar)
        self.btn_eliminar.clicked.connect(self.eliminar)
        self.btn_cargar.clicked.connect(self.cargar)

        btn_layout.addWidget(self.btn_crear)
        btn_layout.addWidget(self.btn_modificar)
        btn_layout.addWidget(self.btn_eliminar)
        btn_layout.addWidget(self.btn_cargar)

        
        self.btn_atras = QPushButton("← Atrás")
        self.btn_siguiente = QPushButton("Siguiente →")
        self.btn_atras.clicked.connect(self.anterior)
        self.btn_siguiente.clicked.connect(self.siguiente)

        nav_layout.addWidget(self.btn_atras)
        nav_layout.addWidget(self.btn_siguiente)

        
        self.layout.addLayout(form_layout)
        self.layout.addLayout(btn_layout)
        self.layout.addLayout(nav_layout)
        self.setLayout(self.layout)

    def cargar(self):
        self.cursor.execute("SELECT * FROM Trabajadores ORDER BY id_trabajador")
        self.trabajadores = self.cursor.fetchall()
        self.indice = 0 if self.trabajadores else -1
        self.mostrar()

    def mostrar(self):
        if 0 <= self.indice < len(self.trabajadores):
            t = self.trabajadores[self.indice]
            self.id_input.setText(str(t["id_trabajador"]))
            self.nombre_input.setText(t["nombre"])
            self.telefono_input.setText(t["numero_telefono"])
        else:
            self.id_input.clear()
            self.nombre_input.clear()
            self.telefono_input.clear()

    def crear(self):
        try:
            id_trabajador = int(self.id_input.text())
            nombre = self.nombre_input.text()
            telefono = self.telefono_input.text()
        except ValueError:
            QMessageBox.warning(self, "Error", "ID inválido.")
            return

        try:
            self.cursor.execute(
                "INSERT INTO Trabajadores (id_trabajador, nombre, numero_telefono) VALUES (%s, %s, %s)",
                (id_trabajador, nombre, telefono)
            )
            self.conn.commit()
            QMessageBox.information(self, "Éxito", "Trabajador creado.")
            self.cargar()
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Error SQL", str(e))

    def modificar(self):
        try:
            id_trabajador = int(self.id_input.text())
            nombre = self.nombre_input.text()
            telefono = self.telefono_input.text()
        except ValueError:
            QMessageBox.warning(self, "Error", "Datos inválidos.")
            return

        try:
            self.cursor.execute("""
                UPDATE Trabajadores SET nombre=%s, numero_telefono=%s
                WHERE id_trabajador=%s
            """, (nombre, telefono, id_trabajador))
            self.conn.commit()
            QMessageBox.information(self, "Éxito", "Trabajador actualizado.")
            self.cargar()
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Error SQL", str(e))

    def eliminar(self):
        try:
            id_trabajador = int(self.id_input.text())
        except ValueError:
            QMessageBox.warning(self, "Error", "ID inválido.")
            return

        try:
            self.cursor.execute("DELETE FROM Trabajadores WHERE id_trabajador=%s", (id_trabajador,))
            self.conn.commit()
            QMessageBox.information(self, "Éxito", "Trabajador eliminado.")
            self.cargar()
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Error SQL", str(e))

    def siguiente(self):
        if self.indice < len(self.trabajadores) - 1:
            self.indice += 1
            self.mostrar()

    def anterior(self):
        if self.indice > 0:
            self.indice -= 1
            self.mostrar()

    def closeEvent(self, event):
        self.cursor.close()
        self.conn.close()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = TrabajadorCRUD()
    ventana.show()
    sys.exit(app.exec())

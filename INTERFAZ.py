import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QComboBox, QLabel, QTableWidget, QMessageBox
import mysql.connector

class GestionDeTablas(QWidget):
    def __init__(self):
        super().__init__()
        print("Inicializando interfaz...")
        self.init_ui()
        self.conectar_base_datos()

    def conectar_base_datos(self):
        try:
            self.conn = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="mysql",
                database="Practica13_C22270660"
            )
            self.cursor = self.conn.cursor(dictionary=True)
            print("Conexión exitosa a la base de datos")
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Error de conexión a la base", str(e))
            sys.exit(1)

    def init_ui(self):
        self.setWindowTitle('Gestión de Tablas')
        self.setGeometry(100, 100, 600, 500)

        layout = QVBoxLayout()

        self.combo_tablas = QComboBox(self)
        self.combo_tablas.addItem('Trabajadores')
        self.combo_tablas.addItem('Proveedores')
        self.combo_tablas.addItem('Productos')
        layout.addWidget(QLabel('Selecciona una tabla:'))
        layout.addWidget(self.combo_tablas)

        boton_agregar = QPushButton('Agregar', self)
        boton_modificar = QPushButton('Modificar', self)
        boton_eliminar = QPushButton('Eliminar', self)
        boton_mostrar = QPushButton('Mostrar Datos', self)

        layout.addWidget(boton_agregar)
        layout.addWidget(boton_modificar)
        layout.addWidget(boton_eliminar)
        layout.addWidget(boton_mostrar)

        self.tabla = QTableWidget(self)
        layout.addWidget(self.tabla)

        self.setLayout(layout)

        boton_agregar.clicked.connect(self.agregar_dato)
        boton_modificar.clicked.connect(self.modificar_dato)
        boton_eliminar.clicked.connect(self.eliminar_dato)
        boton_mostrar.clicked.connect(self.mostrar_datos)

    def agregar_dato(self):
        print("Agregar datos")

    def modificar_dato(self):
        print("Modificar datos")

    def eliminar_dato(self):
        print("Eliminar datos")

    def mostrar_datos(self):
        tabla = self.combo_tablas.currentText()
        try:
            self.cursor.execute(f"SELECT * FROM {tabla}")
            resultados = self.cursor.fetchall()
            if resultados:
                columnas = list(resultados[0].keys())
                self.tabla.setColumnCount(len(columnas))
                self.tabla.setRowCount(len(resultados))
                self.tabla.setHorizontalHeaderLabels(columnas)
                for i, fila in enumerate(resultados):
                    for j, columna in enumerate(columnas):
                        self.tabla.setItem(i, j, QTableWidgetItem(str(fila[columna])))
            else:
                self.tabla.setRowCount(0)
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Error al mostrar datos", str(e))

from PyQt6.QtWidgets import QTableWidgetItem  # necesario para mostrar los datos

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = GestionDeTablas()
    ventana.show()
    sys.exit(app.exec())



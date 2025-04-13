import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
)

class VentanaTrabajadores(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Catálogo de Trabajadores")
        self.setGeometry(100, 100, 600, 400)

        self.trabajadores = []
        self.indice = -1

        layout_principal = QVBoxLayout()
        form_layout = QVBoxLayout()
        btn_layout = QHBoxLayout()
        nav_layout = QHBoxLayout()

        # Entradas
        self.id_input = QLineEdit()
        self.id_input.setReadOnly(True)
        self.nombre_input = QLineEdit()
        self.telefono_input = QLineEdit()

        form_layout.addWidget(QLabel("ID Trabajador:"))
        form_layout.addWidget(self.id_input)
        form_layout.addWidget(QLabel("Nombre:"))
        form_layout.addWidget(self.nombre_input)
        form_layout.addWidget(QLabel("Número de Teléfono:"))
        form_layout.addWidget(self.telefono_input)

        # Botones de acción
        self.btn_crear = QPushButton("Crear")
        self.btn_modificar = QPushButton("Modificar")
        self.btn_eliminar = QPushButton("Eliminar")
        self.btn_cargar = QPushButton("Cargar")

        self.btn_crear.clicked.connect(self.crear)
        self.btn_modificar.clicked.connect(self.modificar)
        self.btn_eliminar.clicked.connect(self.eliminar)
        self.btn_cargar.clicked.connect(self.cargar_trabajadores)

        btn_layout.addWidget(self.btn_crear)
        btn_layout.addWidget(self.btn_modificar)
        btn_layout.addWidget(self.btn_eliminar)
        btn_layout.addWidget(self.btn_cargar)

        # Botones de navegación
        self.btn_anterior = QPushButton("← Atrás")
        self.btn_siguiente = QPushButton("Siguiente →")
        self.btn_anterior.clicked.connect(self.anterior)
        self.btn_siguiente.clicked.connect(self.siguiente)

        nav_layout.addWidget(self.btn_anterior)
        nav_layout.addWidget(self.btn_siguiente)

        # Tabla
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['ID Trabajador', 'Nombre', 'Número de Teléfono'])

        layout_principal.addLayout(form_layout)
        layout_principal.addLayout(btn_layout)
        layout_principal.addLayout(nav_layout)
        layout_principal.addWidget(self.table)
        self.setLayout(layout_principal)

        self.indice = 0
        self.cargar_trabajadores()

    def cargar_trabajadores(self):
        self.table.setRowCount(0)
        for i, trabajador in enumerate(self.trabajadores):
            self.table.insertRow(i)
            self.table.setItem(i, 0, QTableWidgetItem(str(trabajador['id'])))
            self.table.setItem(i, 1, QTableWidgetItem(trabajador['nombre']))
            self.table.setItem(i, 2, QTableWidgetItem(trabajador['telefono']))
        self.mostrar_trabajador()

    def mostrar_trabajador(self):
        if 0 <= self.indice < len(self.trabajadores):
            trabajador = self.trabajadores[self.indice]
            self.id_input.setText(str(trabajador['id']))
            self.nombre_input.setText(trabajador['nombre'])
            self.telefono_input.setText(trabajador['telefono'])
        else:
            self.id_input.clear()
            self.nombre_input.clear()
            self.telefono_input.clear()

    def crear(self):
        nombre = self.nombre_input.text()
        telefono = self.telefono_input.text()

        if not nombre or not telefono:
            QMessageBox.warning(self, "Error", "Llene todos los campos.")
            return

        nuevo_id = self.trabajadores[-1]['id'] + 1 if self.trabajadores else 1
        self.trabajadores.append({'id': nuevo_id, 'nombre': nombre, 'telefono': telefono})
        QMessageBox.information(self, "Correcto", "Trabajador creado.")
        self.indice = len(self.trabajadores) - 1
        self.cargar_trabajadores()

    def modificar(self):
        if self.indice == -1:
            QMessageBox.warning(self, "Error", "No hay trabajador seleccionado.")
            return
        try:
            self.trabajadores[self.indice]['nombre'] = self.nombre_input.text()
            self.trabajadores[self.indice]['telefono'] = self.telefono_input.text()
            QMessageBox.information(self, "Correcto", "Trabajador modificado.")
            self.cargar_trabajadores()
        except IndexError:
            QMessageBox.critical(self, "Error", "Índice fuera de rango.")

    def eliminar(self):
        if self.indice == -1:
            QMessageBox.warning(self, "Error", "No hay trabajador seleccionado.")
            return
        del self.trabajadores[self.indice]
        QMessageBox.information(self, "Correcto", "Trabajador eliminado.")
        self.indice = max(0, self.indice - 1)
        self.cargar_trabajadores()

    def siguiente(self):
        if self.indice < len(self.trabajadores) - 1:
            self.indice += 1
            self.mostrar_trabajador()

    def anterior(self):
        if self.indice > 0:
            self.indice -= 1
            self.mostrar_trabajador()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaTrabajadores()
    ventana.show()
    sys.exit(app.exec())


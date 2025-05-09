from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton
import sys

class VentanaPrincipal(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Panel Administrativo")
        self.setGeometry(100, 100, 300, 300)

        layout = QVBoxLayout()

        btn_trabajadores = QPushButton("Trabajadores")
        btn_trabajadores.clicked.connect(self.abrir_trabajadores)
        layout.addWidget(btn_trabajadores)

        btn_proveedores = QPushButton("Proveedores")
        btn_proveedores.clicked.connect(self.abrir_proveedores)
        layout.addWidget(btn_proveedores)

        btn_productos = QPushButton("Productos")
        btn_productos.clicked.connect(self.abrir_productos)
        layout.addWidget(btn_productos)

        btn_materia = QPushButton("Materia Prima")
        btn_materia.clicked.connect(self.abrir_materia)
        layout.addWidget(btn_materia)

        self.setLayout(layout)

    def abrir_trabajadores(self):
        from InventarioDiario import TrabajadorCRUD
        self.ventana_trabajadores = TrabajadorCRUD()
        self.ventana_trabajadores.show()

    def abrir_proveedores(self):
        from proveedores import ProveedoresCRUD
        self.ventana_proveedores = ProveedoresCRUD()
        self.ventana_proveedores.show()

    def abrir_productos(self):
        from Productos_crud import ProductosCRUD
        self.ventana_productos = ProductosCRUD()
        self.ventana_productos.show()

    def abrir_materia(self):
        from MateriaPrima import MateriaPrimaCRUD
        self.ventana_materia = MateriaPrimaCRUD()
        self.ventana_materia.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec())

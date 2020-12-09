from PySide2.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QTableWidgetItem, QGraphicsScene
from PySide2.QtCore import Slot
from ui_mainwindow import Ui_MainWindow
from particula.particulas import Particulas
from particula.particula import Particula
from particula.algoritmos import distancia_euclidiana
from PySide2.QtGui import QPen, QColor, QTransform
from random import randint
from pprint import pprint
from pprint import pformat

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.particulas = Particulas()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.agregar_final_pushButton.clicked.connect(self.click_agregar_final)
        self.ui.agregar_inicio_pushButton.clicked.connect(self.click_agregar_inicio)
        self.ui.mostrar_pushButton.clicked.connect(self.click_mostrar)

        self.ui.actionAbrir.triggered.connect(self.action_abrir_archivo)
        self.ui.actionGuardar.triggered.connect(self.action_guardar_archivo)

        self.ui.mostrar_tabla_pushButton.clicked.connect(self.mostrar_tabla)
        self.ui.buscar_PushButton.clicked.connect(self.buscar_id)

        self.ui.dibujar.clicked.connect(self.dibujar)
        self.ui.limpiar.clicked.connect(self.limpiar)

        self.scene = QGraphicsScene()
        self.ui.graphicsView.setScene(self.scene)

        self.ui.actionPor_id.triggered.connect(self.ordenar_id)
        self.ui.actionPor_distancia.triggered.connect(self.ordenar_distancia)
        self.ui.actionPor_velocidad.triggered.connect(self.ordenar_velocidad)

        self.ui.actionMostrar_diccionario.triggered.connect(self.mostrar_diccionario)
        
        self.ui.actionRecorrido_en_Profundidad_Amplitud.triggered.connect(self.recorrido)

    @Slot()
    def recorrido(self):
        self.ui.salida.clear()

        origenes = (self.ui.origen_x_spinBox.value(), self.ui.origne_y_spinBox.value())
        recorrido = self.particulas.mostrar_recorrido(origenes)

        print ("Profundidad")

        self.ui.salida.insertPlainText("Profundidad" + '\n')
        for i in recorrido:
            self.ui.salida.insertPlainText(str(i) + '\n')
            print(i)
        
        recorrido_2 = self.particulas.mostrar_recorrido_2(origenes)

        print ("\nAmplitud")

        self.ui.salida.insertPlainText('\n'"Amplitud" + '\n')
        for i in recorrido_2:
            self.ui.salida.insertPlainText(str(i) + '\n')
            print(i)
        QMessageBox.information(
                self,
                "Exito",
                "Se imprimieron los recorridos ;) " 
            )

    @Slot()
    def mostrar_diccionario(self):
        self.ui.salida.clear()
        self.ui.salida.insertPlainText(self.particulas.mostrar_diccionario())
        QMessageBox.information(
                self,
                "Exito",
                "Se imprimio el diccionario " 
            )

    @Slot()
    def ordenar_id(self):
        self.particulas.ordenar_id()
        QMessageBox.information(
                self,
                "Exito",
                "Se ordeno el archivo por id " 
            )
   
    @Slot()
    def ordenar_distancia(self):
        self.particulas.ordenar_distancia()
        QMessageBox.information(
                self,
                "Exito",
                "Se ordeno el archivo por distancia " 
            )
   
    @Slot()
    def ordenar_velocidad(self):
        self.particulas.ordenar_velocidad()
        QMessageBox.information(
                self,
                "Exito",
                "Se ordeno el archivo por velocidad " 
            )

    def wheelEvent(self, event):
        if event.delta() > 0:
            self.ui.graphicsView.scale(1.2, 1.2)
        else:
            self.ui.graphicsView.scale(0.8, 0.8)

    @Slot()
    def dibujar(self):
        pen = QPen ()
        pen.setWidth(3)
        for particula in self.particulas:
            color = QColor(particula.red, particula.green ,particula.blue)
            pen.setColor(color)

            self.scene.addEllipse(particula.origen_x, particula.origen_y, 3, 3, pen)
            self.scene.addEllipse(particula.destino_x, particula.destino_y, 3, 3, pen)
            self.scene.addLine(particula.origen_x+3, particula.origen_y+3, particula.destino_x, particula.destino_y, pen)

    @Slot()
    def limpiar(self):
        self.scene.clear()

    @Slot()
    def buscar_id(self):
        id = self.ui.buscar_lineEdit.text()
        encontrado = False
        for particula in self.particulas:
            if id == str(particula.id):
                self.ui.tabla.clear()
                self.ui.tabla.setRowCount(1)
                id_widget = QTableWidgetItem(str(particula.id))
                origen_x_widget = QTableWidgetItem(str(particula.origen_x))
                origen_y_widget = QTableWidgetItem(str(particula.origen_y))
                destino_x_widget = QTableWidgetItem(str(particula.destino_x))
                destino_y_widget = QTableWidgetItem(str(particula.destino_y))
                velocidad_widget = QTableWidgetItem(str(particula.velocidad))
                red_widget = QTableWidgetItem(str(particula.red))
                green_widget = QTableWidgetItem(str(particula.green))
                blue_widget = QTableWidgetItem(str(particula.blue))
                distancia_widget = QTableWidgetItem(str(particula.distancia))

                self.ui.tabla.setItem(0, 0, id_widget)
                self.ui.tabla.setItem(0, 1, origen_x_widget)
                self.ui.tabla.setItem(0, 2, origen_y_widget)
                self.ui.tabla.setItem(0, 3, destino_x_widget)
                self.ui.tabla.setItem(0, 4, destino_y_widget)
                self.ui.tabla.setItem(0, 5, velocidad_widget)
                self.ui.tabla.setItem(0, 6, red_widget)
                self.ui.tabla.setItem(0, 7, green_widget)
                self.ui.tabla.setItem(0, 8, blue_widget)
                self.ui.tabla.setItem(0, 9, distancia_widget)

                encontrado = True
                return
        if not encontrado:
            QMessageBox.warning(
                self,
                "Atencion",
                f'La particula con id "{id}" no fue encontrado'
            )

    @Slot()
    def mostrar_tabla(self):
        self.ui.tabla.setColumnCount(10)
        headers = ["Id", "Origen X", "Origen Y", "Destino X", "Destino Y", "Velocidad", "Red", "Green", "Blue", "Distancia"]
        self.ui.tabla.setHorizontalHeaderLabels(headers)

        self.ui.tabla.setRowCount(len(self.particulas))

        row = 0
        for particula in self.particulas:
            id_widget = QTableWidgetItem(str(particula.id))
            origen_x_widget = QTableWidgetItem(str(particula.origen_x))
            origen_y_widget = QTableWidgetItem(str(particula.origen_y))
            destino_x_widget = QTableWidgetItem(str(particula.destino_x))
            destino_y_widget = QTableWidgetItem(str(particula.destino_y))
            velocidad_widget = QTableWidgetItem(str(particula.velocidad))
            red_widget = QTableWidgetItem(str(particula.red))
            green_widget = QTableWidgetItem(str(particula.green))
            blue_widget = QTableWidgetItem(str(particula.blue))
            distancia_widget = QTableWidgetItem(str(particula.distancia))

            self.ui.tabla.setItem(row, 0, id_widget)
            self.ui.tabla.setItem(row, 1, origen_x_widget)
            self.ui.tabla.setItem(row, 2, origen_y_widget)
            self.ui.tabla.setItem(row, 3, destino_x_widget)
            self.ui.tabla.setItem(row, 4, destino_y_widget)
            self.ui.tabla.setItem(row, 5, velocidad_widget)
            self.ui.tabla.setItem(row, 6, red_widget)
            self.ui.tabla.setItem(row, 7, green_widget)
            self.ui.tabla.setItem(row, 8, blue_widget)
            self.ui.tabla.setItem(row, 9, distancia_widget)

            row += 1

    @Slot()
    def action_abrir_archivo(self):
        # print('abrir_archivo')
        ubicacion = QFileDialog.getOpenFileName(
            self,
            'Abrir Archivo',
            '.',
            'JSON (*.json)'
        )[0]
        if self.particulas.abrir(ubicacion):
            QMessageBox.information(
                self,
                "Exito",
                "Se abrio el archivo " + ubicacion
            )
        else:
            QMessageBox.critical(
                self,
                "Error",
                "Error al abrir el archivo " + ubicacion
            )

    @Slot()
    def action_guardar_archivo(self):
        # print('guardar_archivo')
        ubicacion = QFileDialog.getSaveFileName(
            self,
            'Guardar Archivo',
            '.',
            'JSON (*.json)'
        )[0]
        print(ubicacion)
        if self.particulas.guardar(ubicacion):
            QMessageBox.information(
                self,
                "Exito",
                "Se pudo crear el archivo " + ubicacion
            )
        else:
            QMessageBox.critical(
                self,
                "Error",
                "No se pudo crear el archivo " + ubicacion
            )

    @Slot()
    def click_mostrar(self):
        # self.particulas.mostrar()
        self.ui.salida.clear()
        self.ui.salida.insertPlainText(str(self.particulas))


    @Slot()
    def click_agregar_final(self):
        id = self.ui.id_spinBox.value()
        origen_x = self.ui.origen_x_spinBox.value()
        origen_y = self.ui.origne_y_spinBox.value()
        destino_x = self.ui.destino_x_spinBox.value()
        destino_y = self.ui.destino_y_spinBox.value()
        velocidad = self.ui.velocidad_spinBox.value()
        red = self.ui.red_spinBox.value()
        green = self.ui.green_spinBox.value()
        blue = self.ui.blue_spinBox.value()

        particula = Particula(id, origen_x, origen_y, destino_x, destino_y, velocidad, red, green, blue, distancia = distancia_euclidiana)
        self.particulas.agregar_final(particula)

        # print(id, origen_x, origen_y, destino_x, destino_y, velocidad, red, green, blue)
        # self.ui.salida.insertPlainText(str(id) + str(origen_x) + str(origen_y) + str(destino_x) + str(destino_y) + str(velocidad) + str(red) + str(green) + str(blue) )
    @Slot()
    def click_agregar_inicio(self):
        id = self.ui.id_spinBox.value()
        origen_x = self.ui.origen_x_spinBox.value()
        origen_y = self.ui.origne_y_spinBox.value()
        destino_x = self.ui.destino_x_spinBox.value()
        destino_y = self.ui.destino_y_spinBox.value()
        velocidad = self.ui.velocidad_spinBox.value()
        red = self.ui.red_spinBox.value()
        green = self.ui.green_spinBox.value()
        blue = self.ui.blue_spinBox.value()

        particula = Particula(id, origen_x, origen_y, destino_x, destino_y, velocidad, red, green, blue, distancia = distancia_euclidiana)
        self.particulas.agregar_inicio(particula)

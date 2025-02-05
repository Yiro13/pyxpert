import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QGraphicsScene,
    QGraphicsView,
    QLineEdit,
    QLabel,
)
from PyQt5.QtCore import Qt, QEventLoop
from PyQt5.QtGui import QBrush, QColor, QPen, QFont, QPainter

from rulesbased.knowledgeBase.rule import Rule
from rulesbased.knowledgeBase.knowledgeBase import KnowledgeBase
from rulesbased.inferenceEngine.inferenceEngine import InferenceEngine


class GraphView(QGraphicsView):
    def __init__(self, parent=None):
        super(GraphView, self).__init__(parent)
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.setRenderHint(QPainter.Antialiasing)
        self.setMinimumSize(620, 480)

    def update_scene(self, nodes, layout_positions):
        self.scene.clear()

        pen_line = QPen(Qt.black)
        pen_line.setWidth(2)
        for node in nodes:
            origen = layout_positions.get(node.fact, (0, 0))
            for nodo_dest in node.next:
                destino = layout_positions.get(nodo_dest.fact, (0, 0))
                self.scene.addLine(
                    origen[0], origen[1], destino[0], destino[1], pen_line
                )

        radio = 20
        font = QFont("Arial", 10)
        for node in nodes:
            x, y = layout_positions.get(node.fact, (0, 0))
            if node.status is None:
                color = QColor("lightgreen")
            elif node.status:
                color = QColor("lightblue")
            else:
                color = QColor("salmon")
            brush = QBrush(color)
            pen = QPen(Qt.black)
            self.scene.addEllipse(
                x - radio, y - radio, radio * 2, radio * 2, pen, brush
            )
            text = self.scene.addText(node.fact, font)
            text_rect = text.boundingRect()
            text.setPos(x - text_rect.width() / 2, y - text_rect.height() / 2)
        self.scene.setSceneRect(0, 0, 620, 480)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Sistema de Inferencia Basado en Reglas")
        self.resize(800, 650)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        control_widget = QWidget()
        control_layout = QHBoxLayout(control_widget)
        main_layout.addWidget(control_widget)

        self.btn_backward = QPushButton("Backward Chaining")
        self.btn_forward = QPushButton("Forward Chaining")
        self.btn_reset = QPushButton("Reset Tree")
        control_layout.addWidget(self.btn_backward)
        control_layout.addWidget(self.btn_forward)
        control_layout.addWidget(self.btn_reset)

        self.input_container = QWidget()
        input_layout = QHBoxLayout(self.input_container)
        self.input_label = QLabel("")
        self.node_input = QLineEdit()
        self.submit_button = QPushButton("Submit")
        input_layout.addWidget(self.input_label)
        input_layout.addWidget(self.node_input)
        input_layout.addWidget(self.submit_button)
        self.input_container.hide()  # Se oculta hasta que se necesite.
        main_layout.addWidget(self.input_container)

        self.graph_view = GraphView()
        main_layout.addWidget(self.graph_view)

        self.kb = KnowledgeBase()
        self.kb.addRule(Rule(fact={"A": True, "B": True}, conclusion="C"))
        self.kb.addRule(Rule(fact={"D": True, "E": True, "F": True}, conclusion="G"))
        self.kb.addRule(Rule(fact={"H": True, "I": True}, conclusion="J"))
        self.kb.addRule(Rule(fact={"C": True, "G": True}, conclusion="K"))
        self.kb.addRule(Rule(fact={"J": True, "G": True}, conclusion="L"))
        self.kb.addRule(Rule(fact={"K": True, "L": True}, conclusion="M"))

        self.engine = InferenceEngine(self.kb, self.graph_view, self)

        self.btn_backward.clicked.connect(self.run_backward)
        self.btn_forward.clicked.connect(self.run_forward)
        self.btn_reset.clicked.connect(self.reset_tree)

        self.input_loop = None

    def run_backward(self):
        hecho, ok = self.get_simple_input(
            "Backward Chaining", "Ingrese el hecho a evaluar (ej.: 'M'):"
        )
        if ok and hecho:
            self.engine.backwardChain(hecho.strip())

    def run_forward(self):
        self.engine.forwardChain()

    def reset_tree(self):
        self.engine.reset_tree()

    def get_simple_input(self, title: str, prompt: str):
        self.input_label.setText(prompt)
        self.input_container.show()
        self.node_input.clear()
        loop = QEventLoop()
        self.submit_button.clicked.connect(loop.quit)
        loop.exec_()
        value = self.node_input.text()
        self.input_container.hide()
        return value, True

    def get_node_input(self, fact: str) -> str:
        self.input_label.setText(f"Ingrese el valor para '{fact}' (True/False):")
        self.node_input.clear()
        self.input_container.show()
        loop = QEventLoop()
        self.submit_button.clicked.connect(loop.quit)
        loop.exec_()
        value = self.node_input.text()
        self.input_container.hide()
        return value


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

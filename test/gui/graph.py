# create a chart

from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtChart import QChart, QChartView, QLineSeries, QValueAxis
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import QPoint, QTimer


class Graph(QChart):
    """Creates a chart with a list of values.
    The chart is updated with new values using the update() method
    MUST BE USED WITH QChartView"""

    def __init__(self, title, values: list):
        super().__init__()
        self.setTitle(title)

        # set up the series from values
        self.count = 0
        self.lineSeries = QLineSeries()
        self.valuesLen = len(values)
        for i in range(self.valuesLen):
            self.lineSeries.append(QPoint(i, values[i]))
            self.count += 1

        self.addSeries(self.lineSeries)
        self.xAxis = QValueAxis()
        self.xAxis.setRange(0, self.count)
        self.yAxis = QValueAxis()
        self.yAxis.setRange(0, 100)
        self.setAxisX(self.xAxis, self.lineSeries)
        self.setAxisY(self.yAxis, self.lineSeries)

    def update(self, value):
        """Update the chart with a new value"""
        self.lineSeries.append(QPoint(self.count, value))
        self.count += 1
        self.xAxis.setRange(0, self.count)


if __name__ == "__main__":
    app = QApplication([])

    # Example data
    data = [1, 3, 2, 4, 6, 5, 7]

    # Create the chart
    chart = Graph("Example Chart", data)

    # Create the chart view
    chartView = QChartView(chart)
    chartView.setRenderHint(QPainter.Antialiasing)

    # Create the main window
    window = QMainWindow()
    window.setCentralWidget(chartView)
    window.resize(800, 600)
    window.show()

    # Update the chart
    chart.update(50)

    app.exec_()

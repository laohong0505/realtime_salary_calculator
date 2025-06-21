
import sys
import time
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QLineEdit, QVBoxLayout, QHBoxLayout, QGridLayout, QMessageBox
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont

class SalaryCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("实时工资计算器")
        self.setStyleSheet("background-color: black; color: gold;")
        self.setGeometry(300, 200, 400, 300)
        self.init_ui()

        self.total_seconds = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)

    def init_ui(self):
        self.font = QFont("Microsoft YaHei", 12)

        self.salary_input = QLineEdit("5000")
        self.salary_input.setFont(self.font)
        self.hours_input = QLineEdit("8")
        self.hours_input.setFont(self.font)
        self.days_input = QLineEdit("22")
        self.days_input.setFont(self.font)

        self.start_button = QPushButton("上班")
        self.start_button.setFont(self.font)
        self.start_button.clicked.connect(self.start_work)

        grid = QGridLayout()
        grid.addWidget(QLabel("月薪 (人民币)："), 0, 0)
        grid.addWidget(self.salary_input, 0, 1)
        grid.addWidget(QLabel("每天工作小时数："), 1, 0)
        grid.addWidget(self.hours_input, 1, 1)
        grid.addWidget(QLabel("当月上班天数："), 2, 0)
        grid.addWidget(self.days_input, 2, 1)
        grid.addWidget(self.start_button, 3, 0, 1, 2)

        self.setLayout(grid)

    def start_work(self):
        try:
            self.salary = float(self.salary_input.text())
            self.hours_per_day = float(self.hours_input.text())
            self.days_per_month = float(self.days_input.text())
        except ValueError:
            QMessageBox.critical(self, "错误", "请输入合法的数字！")
            return

        self.per_second_salary = self.salary / (self.hours_per_day * 3600 * self.days_per_month)
        self.timer.start(1000)
        self.switch_to_work_ui()

    def switch_to_work_ui(self):
        for i in reversed(range(self.layout().count())):
            self.layout().itemAt(i).widget().setParent(None)

        self.timer_label = QLabel("正在上班中")
        self.timer_label.setAlignment(Qt.AlignCenter)
        self.timer_label.setFont(QFont("Microsoft YaHei", 14))

        self.time_display = QLabel("00:00:00")
        self.time_display.setAlignment(Qt.AlignCenter)
        self.time_display.setFont(QFont("Consolas", 18))

        self.earned_label = QLabel("已赚: ¥0.00")
        self.earned_label.setAlignment(Qt.AlignCenter)
        self.earned_label.setFont(QFont("Microsoft YaHei", 14))

        self.stop_button = QPushButton("下班")
        self.stop_button.setFont(self.font)
        self.stop_button.clicked.connect(self.stop_work)

        layout = QVBoxLayout()
        layout.addWidget(self.timer_label)
        layout.addWidget(self.time_display)
        layout.addWidget(self.earned_label)
        layout.addWidget(self.stop_button)
        self.setLayout(layout)

    def update_timer(self):
        self.total_seconds += 1
        hours = self.total_seconds // 3600
        minutes = (self.total_seconds % 3600) // 60
        seconds = self.total_seconds % 60
        self.time_display.setText(f"{hours:02}:{minutes:02}:{seconds:02}")

        earned = self.total_seconds * self.per_second_salary
        self.earned_label.setText(f"已赚: ¥{earned:.2f}")

    def stop_work(self):
        self.timer.stop()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SalaryCalculator()
    window.show()
    sys.exit(app.exec_())

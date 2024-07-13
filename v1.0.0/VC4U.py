import sys
import threading
import time
from datetime import datetime

from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QApplication,
    QFileDialog,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
)


class VideoCutterApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Video Cutter v1.0")
        self.setGeometry(100, 100, 480, 420)

        self.initUI()

    def initUI(self):
        # Heading title at top
        heading_label = QLabel(self)
        heading_label.setText("Video Cutter")
        font = QFont()
        font.setBold(True)
        heading_label.setFont(font)
        heading_label.setStyleSheet("color: #FFF01F; background-color: #2A292B")
        heading_label.setGeometry(10, 10, 460, 50)

        # Input file selection
        self.input_button = QPushButton(self)
        self.input_button.setText("Select Input File")
        self.input_button.setGeometry(10, 70, 200, 30)
        self.input_button.clicked.connect(self.select_input_file)

        self.input_entry = QLineEdit(self)
        self.input_entry.setGeometry(10, 110, 460, 30)

        # Output file selection
        self.output_button = QPushButton(self)
        self.output_button.setText("Select Output File")
        self.output_button.setGeometry(10, 150, 200, 30)
        self.output_button.clicked.connect(self.select_output_file)

        self.output_entry = QLineEdit(self)
        self.output_entry.setGeometry(10, 190, 460, 30)

        # Start time input
        self.label_start = QLabel(self)
        self.label_start.setText("Start Time (hh:mm:ss.mmm)")
        self.label_start.setGeometry(10, 230, 200, 30)

        self.entry_start = QLineEdit(self)
        self.entry_start.setText("00:00:00.000")
        self.entry_start.setGeometry(10, 270, 200, 30)

        # End time input
        self.label_end = QLabel(self)
        self.label_end.setText("End Time (hh:mm:ss.mmm)")
        self.label_end.setGeometry(10, 310, 200, 30)

        self.entry_end = QLineEdit(self)
        self.entry_end.setText("00:00:00.000")
        self.entry_end.setGeometry(10, 350, 200, 30)

        # Cut button
        self.cut_button = QPushButton(self)
        self.cut_button.setText("Cut Video")
        self.cut_button.setGeometry(10, 390, 200, 30)
        self.cut_button.clicked.connect(self.cut_video)

        # Status label
        self.status_label = QLabel(self)
        self.status_label.setGeometry(10, 430, 460, 30)

    def select_input_file(self):
        input_file, _ = QFileDialog.getOpenFileName(
            self,
            "Select Video File",
            "",
            "Video Files (*.mp4 *.avi *.mkv);;All Files (*)",
        )
        if input_file:
            self.input_entry.setText(input_file)

    def select_output_file(self):
        output_file, _ = QFileDialog.getSaveFileName(
            self,
            "Save Cut Video As",
            "",
            "Video Files (*.mp4 *.avi *.mkv);;All Files (*)",
            options=QFileDialog.DontConfirmOverwrite,
        )
        if output_file:
            self.output_entry.setText(output_file)

    def time_to_seconds(self, time_str):
        time_obj = datetime.strptime(time_str, "%H:%M:%S.%f")
        seconds = (time_obj - datetime(1900, 1, 1)).total_seconds()
        return seconds

    def update_status_label(self):
        for _ in range(10):  # Number of times to blink
            self.status_label.setText("Cutting video in progress")
            self.status_label.setStyleSheet("color: #CC1512; background-color: #FFFFFF")
            QApplication.processEvents()
            time.sleep(0.5)
            self.status_label.setText("Cutting video in progress")
            self.status_label.setStyleSheet("color: #FBFFFF; background-color: #CC1512")
            QApplication.processEvents()
            time.sleep(0.5)

    def cut_video(self):
        def perform_cut():
            input_file = self.input_entry.text()
            start_time = self.entry_start.text()
            end_time = self.entry_end.text()
            output_file = self.output_entry.text()

            try:
                start_seconds = self.time_to_seconds(start_time)
                end_seconds = self.time_to_seconds(end_time)

                threading.Thread(target=self.update_status_label).start()

                ffmpeg_extract_subclip(
                    input_file, start_seconds, end_seconds, targetname=output_file
                )

                # Update the status label after the cutting is completed
                # Blink the status label text
                for _ in range(10):  # Number of times to blink
                    self.status_label.setText("Video cut successfully!")
                    self.status_label.setStyleSheet("color: #000000; background-color: #FFFFFF")
                    QApplication.processEvents()
                    time.sleep(0.5)
                    self.status_label.setText("Video cut successfully!")
                    self.status_label.setStyleSheet("color: #FBFFFF; background-color: #000000")
                    QApplication.processEvents()
                    time.sleep(0.5)
            except Exception as e:
                self.status_label.setText(f"Error: {str(e)}")

        threading.Thread(target=perform_cut).start()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VideoCutterApp()
    window.show()
    sys.exit(app.exec_())

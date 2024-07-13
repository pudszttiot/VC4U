import os
import sys
import threading
from datetime import datetime

from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import (
    QApplication,
    QFileDialog,
    QLabel,
    QLineEdit,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QTimeEdit,
)


class VideoCutterApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Video Cutter v1.0")
        self.setGeometry(100, 100, 480, 520)

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
        self.input_button.setGeometry(10, 70, 150, 30)
        self.input_button.clicked.connect(self.select_input_file)

        self.input_entry = QLineEdit(self)
        self.input_entry.setGeometry(170, 70, 300, 30)

        # Output file selection
        self.output_button = QPushButton(self)
        self.output_button.setText("Select Output File")
        self.output_button.setGeometry(10, 110, 150, 30)
        self.output_button.clicked.connect(self.select_output_file)

        self.output_entry = QLineEdit(self)
        self.output_entry.setGeometry(170, 110, 300, 30)

        # Start time input
        self.label_start = QLabel(self)
        self.label_start.setText("Start Time (hh:mm:ss.mmm)")
        self.label_start.setGeometry(10, 150, 200, 30)

        self.time_edit_start = QTimeEdit(self)
        self.time_edit_start.setDisplayFormat("HH:mm:ss.zzz")
        self.time_edit_start.setGeometry(220, 150, 150, 30)

        # End time input
        self.label_end = QLabel(self)
        self.label_end.setText("End Time (hh:mm:ss.mmm)")
        self.label_end.setGeometry(10, 190, 200, 30)

        self.time_edit_end = QTimeEdit(self)
        self.time_edit_end.setDisplayFormat("HH:mm:ss.zzz")
        self.time_edit_end.setGeometry(220, 190, 150, 30)

        # Cut button
        self.cut_button = QPushButton(self)
        self.cut_button.setText("Cut Video")
        self.cut_button.setGeometry(10, 230, 150, 30)
        self.cut_button.clicked.connect(self.cut_video)

        # Progress bar
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setGeometry(170, 230, 300, 30)

        # Status label
        self.status_label = QLabel(self)
        self.status_label.setGeometry(10, 270, 460, 30)
        self.status_label.setAlignment(Qt.AlignCenter)

        # Original and Cut size labels
        self.original_size_label = QLabel(self)
        self.original_size_label.setGeometry(10, 310, 460, 20)

        self.cut_size_label = QLabel(self)
        self.cut_size_label.setGeometry(10, 340, 460, 20)

        # Clear button
        self.clear_button = QPushButton(self)
        self.clear_button.setText("Clear")
        self.clear_button.setGeometry(10, 380, 100, 30)
        self.clear_button.clicked.connect(self.clear_fields)

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

    def cut_video(self):
        def perform_cut():
            input_file = self.input_entry.text()
            start_time = self.time_edit_start.time().toString("hh:mm:ss.zzz")
            end_time = self.time_edit_end.time().toString("hh:mm:ss.zzz")
            output_file = self.output_entry.text()

            try:
                start_seconds = self.time_to_seconds(start_time)
                end_seconds = self.time_to_seconds(end_time)

                self.update_status_label("Cutting video in progress")

                ffmpeg_extract_subclip(
                    input_file, start_seconds, end_seconds, targetname=output_file
                )

                # Get file sizes
                original_size = os.path.getsize(input_file)
                cut_size = os.path.getsize(output_file)

                # Update status label after cutting is completed
                self.update_status_label("Video cut successfully!")

                # Display file sizes
                self.original_size_label.setText(
                    f"Original Size: {self.format_size(original_size)}"
                )
                self.cut_size_label.setText(f"Cut Size: {self.format_size(cut_size)}")
            except Exception as e:
                self.update_status_label(f"Error: {str(e)}")

        threading.Thread(target=perform_cut).start()

    def update_status_label(self, message):
        self.status_label.setText(message)

    def time_to_seconds(self, time_str):
        time_obj = datetime.strptime(time_str, "%H:%M:%S.%f")
        seconds = (time_obj - datetime(1900, 1, 1)).total_seconds()
        return seconds

    def format_size(self, size):
        # Convert size to human-readable format
        for unit in ["B", "KB", "MB", "GB"]:
            if size < 1024.0:
                return f"{size:.2f} {unit}"
            size /= 1024.0

    def clear_fields(self):
        self.input_entry.clear()
        self.output_entry.clear()
        self.time_edit_start.setTime(QTime(0, 0))
        self.time_edit_end.setTime(QTime(0, 0))
        self.progress_bar.setValue(0)
        self.update_status_label("")
        self.original_size_label.setText("")
        self.cut_size_label.setText("")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VideoCutterApp()
    window.setWindowIcon(QIcon(r"../Images/window_icon1.png"))  # Set window icon
    window.show()
    sys.exit(app.exec_())

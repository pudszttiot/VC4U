import logging
import os
import sys
import threading
from datetime import datetime

from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from PyQt5.QtCore import QFile, Qt, QTextStream, QTime
from PyQt5.QtGui import QIcon, QMovie, QPixmap
from PyQt5.QtWidgets import (
    QApplication,
    QFileDialog,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTimeEdit,
    QVBoxLayout,
    QWidget,
)


class VideoCutterApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("VC4U")
        self.setGeometry(100, 100, 480, 520)
        self.setWindowIcon(QIcon(r"../Images/window_icon4.png"))  # Provide the path to your icon

        self.initUI()

        self.cut_thread = None
        self.terminate_cut = threading.Event()

    def initUI(self):
        # Heading image at top
        heading_image_label = QLabel(self)
        pixmap = QPixmap("../Images/VC4U_Heading3.png")  # Provide path to your image file
        scaled_pixmap = pixmap.scaledToWidth(self.width(), Qt.SmoothTransformation)
        heading_image_label.setPixmap(scaled_pixmap)
        heading_image_label.setGeometry(10, 10, self.width(), scaled_pixmap.height())

        # Load the stylesheet from the file
        style_file = QFile("style.qss")
        if style_file.open(QFile.ReadOnly | QFile.Text):
            stream = QTextStream(style_file)
            app.setStyleSheet(stream.readAll())
            style_file.close()

        # Create a central widget and set a layout
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        layout.addWidget(heading_image_label)

        # Input file selection
        self.input_button = QPushButton(self)
        self.input_button.setText("Select Input File")
        layout.addWidget(self.input_button)
        self.input_button.clicked.connect(self.select_input_file)
        self.input_button.setToolTip("Click to select the input video file")

        self.input_entry = QLineEdit(self)
        layout.addWidget(self.input_entry)

        # Output file selection
        self.output_button = QPushButton(self)
        self.output_button.setText("Select Output File")
        layout.addWidget(self.output_button)
        self.output_button.clicked.connect(self.select_output_file)
        self.output_button.setToolTip("Click to select the output video file")

        self.output_entry = QLineEdit(self)
        layout.addWidget(self.output_entry)

        # Start time input
        self.label_start = QLabel(self)
        self.label_start.setText("Start Time (hh:mm:ss.mmm)")
        layout.addWidget(self.label_start)

        self.time_edit_start = QTimeEdit(self)
        self.time_edit_start.setDisplayFormat("HH:mm:ss.zzz")
        layout.addWidget(self.time_edit_start)

        # End time input
        self.label_end = QLabel(self)
        self.label_end.setText("End Time (hh:mm:ss.mmm)")
        layout.addWidget(self.label_end)

        self.time_edit_end = QTimeEdit(self)
        self.time_edit_end.setDisplayFormat("HH:mm:ss.zzz")
        layout.addWidget(self.time_edit_end)

        # Cut button
        self.cut_button = QPushButton(self)
        self.cut_button.setText("Cut Video")
        layout.addWidget(self.cut_button)
        self.cut_button.clicked.connect(self.cut_video)
        self.cut_button.setToolTip("Click to cut the video")

        # Animation label
        self.animation_label = QLabel(self)
        self.movie = QMovie(
            "../Images/spinner3.gif"
        )  # Replace "animation.gif" with the path to your GIF file
        self.animation_label.setMovie(self.movie)
        layout.addWidget(self.animation_label)
        layout.addWidget(self.animation_label, alignment=Qt.AlignCenter)
        self.animation_label.hide()

        # Status label
        self.status_label = QLabel(self)
        layout.addWidget(self.status_label)
        self.status_label.setAlignment(Qt.AlignCenter)

        # Original and Cut size labels
        self.original_size_label = QLabel(self)
        layout.addWidget(self.original_size_label)

        self.cut_size_label = QLabel(self)
        layout.addWidget(self.cut_size_label)

        # Clear button
        self.clear_button = QPushButton(self)
        self.clear_button.setText("Clear")
        layout.addWidget(self.clear_button)
        self.clear_button.clicked.connect(self.clear_fields)
        self.clear_button.setToolTip("Clear all fields and reset")

        self.setCentralWidget(central_widget)

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
        if self.cut_thread and self.cut_thread.is_alive():
            QMessageBox.warning(
                self, "Warning", "A video cutting operation is already in progress."
            )
            return

        input_file = self.input_entry.text()
        output_file = self.output_entry.text()

        if not input_file:
            QMessageBox.warning(self, "Error", "Please select an input video file.")
            return

        if not output_file:
            QMessageBox.warning(self, "Error", "Please select an output video file.")
            return

        def perform_cut():
            try:
                start_time = self.time_edit_start.time().toString("HH:mm:ss.zzz")
                end_time = self.time_edit_end.time().toString("HH:mm:ss.zzz")

                start_seconds = self.time_to_seconds(start_time)
                end_seconds = self.time_to_seconds(end_time)

                self.update_status_label("Cutting video in progress...")
                self.disable_ui()

                ffmpeg_extract_subclip(
                    input_file, start_seconds, end_seconds, targetname=output_file
                )

                original_size = os.path.getsize(input_file)
                cut_size = os.path.getsize(output_file)

                self.update_status_label("Video cut successfully!")

                self.original_size_label.setText(
                    f"Original Size: {self.format_size(original_size)}"
                )
                self.cut_size_label.setText(f"Cut Size: {self.format_size(cut_size)}")
            except Exception as e:
                self.update_status_label(f"Error: {str(e)}")
            finally:
                self.enable_ui()
                self.animation_label.hide()  # Hide the animation after completion

        self.cut_thread = threading.Thread(target=perform_cut)
        self.cut_thread.start()
        self.animation_label.show()  # Show the animation while processing
        self.movie.start()  # Start the animation

    def disable_ui(self):
        self.input_button.setEnabled(False)
        self.output_button.setEnabled(False)
        self.time_edit_start.setEnabled(False)
        self.time_edit_end.setEnabled(False)
        self.cut_button.setEnabled(False)
        self.clear_button.setEnabled(False)

    def enable_ui(self):
        self.input_button.setEnabled(True)
        self.output_button.setEnabled(True)
        self.time_edit_start.setEnabled(True)
        self.time_edit_end.setEnabled(True)
        self.cut_button.setEnabled(True)
        self.clear_button.setEnabled(True)

    def update_status_label(self, message):
        self.status_label.setText(message)

    def time_to_seconds(self, time_str):
        try:
            time_obj = datetime.strptime(time_str, "%H:%M:%S.%f")
            seconds = (time_obj - datetime(1900, 1, 1)).total_seconds()
            return seconds
        except ValueError:
            raise ValueError("Invalid time format. Use hh:mm:ss.mmm")

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
        self.update_status_label("")
        self.original_size_label.setText("")
        self.cut_size_label.setText("")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app = QApplication(sys.argv)

    window = VideoCutterApp()
    window.show()
    sys.exit(app.exec_())

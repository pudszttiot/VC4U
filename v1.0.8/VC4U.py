import logging
import os
import sys
import threading
from datetime import datetime

from menu_bar import MenuBar
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from pydub import AudioSegment
from PyQt5.QtCore import QFile, Qt, QTextStream, QTime
from PyQt5.QtGui import QIcon, QMovie
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
    QHBoxLayout,
    QWidget,
)

# Constants for supported file types
VIDEO_EXTENSIONS = ['.mp4', '.avi', '.mkv']
AUDIO_EXTENSIONS = ['.mp3', '.wav', '.flac']
ALL_EXTENSIONS = VIDEO_EXTENSIONS + AUDIO_EXTENSIONS

class VideoCutterApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VC4U")
        self.setGeometry(400, 50, 480, 520)
        self.setWindowIcon(QIcon(r"../Images/window_icon4.png"))  # Provide the path to your icon
        self.initUI()
        self.cut_thread = None
        self.terminate_cut = threading.Event()

    def initUI(self):
        # Heading image at top
        heading_image_label = QLabel(self)
        self.movie = QMovie("../Images/Header1.gif")  # Provide path to your GIF file
        heading_image_label.setMovie(self.movie)
        self.movie.start()

        # Load the stylesheet from the file
        self.load_stylesheet("style.qss")

        # Create a central widget and set a layout
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)

        # Center the heading image
        heading_layout = QHBoxLayout()
        heading_layout.addStretch()
        heading_layout.addWidget(heading_image_label)
        heading_layout.addStretch()
        main_layout.addLayout(heading_layout)

        # Add menu bar
        self.menu_bar = MenuBar(self)
        self.setMenuBar(self.menu_bar)

        self.input_button, self.input_entry = self.create_file_selection(main_layout, "Select Input File", self.select_input_file)
        self.output_button, self.output_entry = self.create_file_selection(main_layout, "Select Output File", self.select_output_file)

        self.label_start, self.time_edit_start = self.create_time_edit(main_layout, "Start Time (hh:mm:ss.mmm)")
        self.label_end, self.time_edit_end = self.create_time_edit(main_layout, "End Time (hh:mm:ss.mmm)")

        self.cut_button = self.create_button(main_layout, "Cut File", self.cut_file, "Click to cut the video or audio file")

        self.animation_label = QLabel(self)
        self.spinner_movie = QMovie("../Images/spinner3.gif")  # Replace "spinner3.gif" with the path to your GIF file
        self.animation_label.setMovie(self.spinner_movie)
        main_layout.addWidget(self.animation_label, alignment=Qt.AlignCenter)
        self.animation_label.hide()

        self.status_label = QLabel(self)
        main_layout.addWidget(self.status_label)
        self.status_label.setAlignment(Qt.AlignCenter)

        self.original_size_label = QLabel(self)
        main_layout.addWidget(self.original_size_label)

        self.cut_size_label = QLabel(self)
        main_layout.addWidget(self.cut_size_label)

        self.clear_button = self.create_button(main_layout, "Clear", self.clear_fields, "Clear all fields and reset")

        self.setCentralWidget(central_widget)

    def load_stylesheet(self, stylesheet_path):
        style_file = QFile(stylesheet_path)
        if style_file.open(QFile.ReadOnly | QFile.Text):
            stream = QTextStream(style_file)
            app.setStyleSheet(stream.readAll())
            style_file.close()

    def create_file_selection(self, layout, button_text, button_callback):
        button = QPushButton(self)
        button.setText(button_text)
        layout.addWidget(button)
        button.clicked.connect(button_callback)
        button.setToolTip(f"Click to {button_text.lower()}")

        line_edit = QLineEdit(self)
        layout.addWidget(line_edit)
        return button, line_edit

    def create_time_edit(self, layout, label_text):
        label = QLabel(self)
        label.setText(label_text)
        layout.addWidget(label)

        time_edit = QTimeEdit(self)
        time_edit.setDisplayFormat("HH:mm:ss.zzz")
        layout.addWidget(time_edit)
        return label, time_edit

    def create_button(self, layout, text, callback, tooltip):
        button = QPushButton(self)
        button.setText(text)
        layout.addWidget(button)
        button.clicked.connect(callback)
        button.setToolTip(tooltip)
        return button

    def select_input_file(self):
        input_file, _ = QFileDialog.getOpenFileName(
            self,
            "Select Video or Audio File",
            "",
            "Video Files (*.mp4 *.avi *.mkv);;Audio Files (*.mp3 *.wav *.flac);;All Files (*)",
        )
        if input_file:
            self.input_entry.setText(input_file)

    def select_output_file(self):
        output_file, _ = QFileDialog.getSaveFileName(
            self,
            "Save Cut File As",
            "",
            "Video Files (*.mp4 *.avi *.mkv);;Audio Files (*.mp3 *.wav *.flac);;All Files (*)",
            options=QFileDialog.DontConfirmOverwrite,
        )
        if output_file:
            self.output_entry.setText(output_file)

    def cut_file(self):
        if self.cut_thread and self.cut_thread.is_alive():
            QMessageBox.warning(self, "Warning", "A cutting operation is already in progress.")
            return

        input_file = self.input_entry.text()
        output_file = self.output_entry.text()

        if not input_file or not output_file:
            QMessageBox.warning(self, "Error", "Please select both input and output files.")
            return

        self.cut_thread = threading.Thread(target=self.perform_cut, args=(input_file, output_file))
        self.cut_thread.start()
        self.animation_label.show()  # Show the animation while processing
        self.spinner_movie.start()  # Start the animation

    def perform_cut(self, input_file, output_file):
        try:
            start_seconds = self.time_to_seconds(self.time_edit_start.time().toString("HH:mm:ss.zzz"))
            end_seconds = self.time_to_seconds(self.time_edit_end.time().toString("HH:mm:ss.zzz"))

            self.update_status_label("Cutting in progress...")
            self.disable_ui()

            file_extension = os.path.splitext(input_file)[1].lower()

            if file_extension in VIDEO_EXTENSIONS:
                ffmpeg_extract_subclip(input_file, start_seconds, end_seconds, targetname=output_file)
            elif file_extension in AUDIO_EXTENSIONS:
                audio = AudioSegment.from_file(input_file)
                cut_audio = audio[start_seconds * 1000:end_seconds * 1000]
                cut_audio.export(output_file, format=file_extension[1:])
            else:
                raise ValueError("Unsupported file type")

            self.show_file_sizes(input_file, output_file)
            self.update_status_label("File cut successfully!")
        except Exception as e:
            logging.exception("Error cutting file")
            self.update_status_label(f"Error: {str(e)}")
        finally:
            self.enable_ui()
            self.animation_label.hide()  # Hide the animation after completion

    def show_file_sizes(self, input_file, output_file):
        original_size = os.path.getsize(input_file)
        cut_size = os.path.getsize(output_file)
        self.original_size_label.setText(f"Original Size: {self.format_size(original_size)}")
        self.cut_size_label.setText(f"Cut Size: {self.format_size(cut_size)}")

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
            return (time_obj - datetime(1900, 1, 1)).total_seconds()
        except ValueError:
            raise ValueError("Invalid time format. Use hh:mm:ss.mmm")

    def format_size(self, size):
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

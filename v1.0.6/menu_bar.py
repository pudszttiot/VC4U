from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QAction,
    QApplication,
    QDialog,
    QLabel,
    QMainWindow,
    QMenuBar,
    QScrollArea,
    QVBoxLayout,
)


class HelpDialog(QDialog):
    def __init__(self):
        super(HelpDialog, self).__init__()
        self.setWindowTitle("How to Use...")
        self.setGeometry(550, 350, 800, 600)
        self.setWindowIcon(QIcon("../Images/window_icon4.png"))  # Corrected path

        help_text = r"""
            <p style="text-align: center;">
            <h2><span style="color: #00FF00;">===================================</span></h2>
            <h1><span style="color: #F5F5F5;">🛠 VC4U 🛠</span></h1>
            <h2><span style="color: #FFFFFF;">📝 Version: 1.0.6</span></h2>
            <h2><span style="color: #FFFFFF;">📅 Release Date: April 30, 2024</span></h2>
            <h2><span style="color: #00FF00;">===================================</span></h2></p>
        
            <p style="text-align: center;">
            <span style="color: #282c34; background-color: yellow;">
            <strong><span style="color: #000000; background-color: yellow;">VC4U</span></strong>
            simplifies video cutting! Just choose your files, set start and end times,<br>and VC4U handles the rest.
            It supports popular formats like MP4, AVI, and MKV, <br>giving real-time feedback and displaying file sizes after.
            Easy video cutting with VC4U!
            </span></p>

            <p><h3><span style="color: #FF0080;">Here's how to use it:</span></h3></p>
            <ol>
                <li>Select the input video file by clicking on the <strong><span style="color: #FF6600;">"Select Input File"</span></strong> button.</li>
                <li>Select the output file location by clicking on the <strong><span style="color: #FF6600;">"Select Output File"</span></strong> button.</li>
                <li>Set the start and end times for the segment you want to cut.</li>
                <li>Click on the <strong><span style="color: #FF6600;">"Cut Video"</span></strong> to start the cutting process.</li>
                <li>The original and cut file sizes will be displayed after the process completes.</li>
            </ol>

            <p style="font-size: 20px; font-family: doergon, sans-serif; text-align: center;"><span style="color: #030303; background-color:#f5f5f5;">That's it!... Thank you for using <strong><span style="color: #94c7f7;">VC4U!</span></strong></span></p>

    
            <!-- Add an image here -->
            <p style="text-align: center;"><img src="..\Images\VC4U_heading2.png" alt="VC4U.png" width="200" height="150" border="1">

            <h6 style="color: #e8eaea;">▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃</h6>
        

        
        <h3><span style="color: #39ff14; background-color: #000000;">╬╬══▲▲▲👽👽 <u>MY CHANNELS</u> 👽👽▲▲▲══╬╬</span></h3></p>
            <br>
            <br>

            <span>
            <img src="../Socials/Github.png" alt="Github.png" width="20" height="20" border="2">
            <a href="https://github.com/pudszttiot" style="display:inline-block; text-decoration:none; color:#e8eaea; margin-right:20px;" onclick="openLink('https://github.com/pudszttiot')">Github Page</a>
            </span> 

            <span>
            <img src="../Socials/Youtube.png" alt="Youtube.png" width="20" height="20" border="2">
            <a href="https://youtube.com/@pudszTTIOT" style="display:inline-block; text-decoration:none; color:#ff0000;" onclick="openLink('https://youtube.com/@pudszTTIOT')">YouTube Page</a>
            </span>

            <span>
            <img src="../Socials/SourceForge.png" alt="SourceForge.png" width="20" height="20" border="2">
            <a href="https://sourceforge.net/u/pudszttiot" style="display:inline-block; text-decoration:none; color:#ee730a;" onclick="openLink('https://sourceforge.net/u/pudszttiot')">SourceForge Page</a>
            </span>
        
            <span>
            <img src="../Socials/Dailymotion.png" alt="Dailymotion.png" width="20" height="20" border="2">
            <a href="https://dailymotion.com/pudszttiot" style="display:inline-block; text-decoration:none; color:#0062ff;" onclick="openLink('https://dailymotion.com/pudszttiot')">Dailymotion Page</a>
            </span>

            <span>
            <img src="../Socials/Blogger.png" alt="Blogger.png" width="20" height="20" border="2">
            <a href="https://pudszttiot.blogspot.com" style="display:inline-block; text-decoration:none; color:#ff5722;" onclick="openLink('https://pudszttiot.blogspot.com')">Blogger Page</a>
            </span>

            <script>
            function openLink(url) {
                QDesktopServices.openUrl(QUrl(url));
            }
            </script>

        """

        help_label = QLabel()
        help_label.setAlignment(Qt.AlignLeft)
        help_label.setText(help_text)
        help_label.setOpenExternalLinks(True)  # Allow QLabel to open external links

        # Add a CSS background color
        help_label.setStyleSheet(
            "color: #1E90FF; background-color: #333333; padding: 10px;"
            "border: 2px solid #1E90FF; border-radius: 10px;"
        )

        # Create a scroll area for the help text
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        scroll_area.setWidget(help_label)

        layout = QVBoxLayout()
        layout.addWidget(scroll_area)
        self.setLayout(layout)


class MenuBar(QMenuBar):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Add styles to the menu bar
        self.setStyleSheet(
            "QMenuBar { background-color: #333333; color: #ffffff; }"
            "QMenuBar::item:selected { background-color: #555555; color: #ffffff; }"
            "QMenu { background-color: #ffffff; /* Change the background color of the submenu */ }"
            "QMenu::item:selected { background-color: #dbdbdb /* Change the background color of the selected submenu item */ }"
        )

        file_menu = self.addMenu("&File")
        exit_action = QAction("&Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.exit_application)  # Quit the application
        file_menu.addAction(exit_action)

        # Add Help menu
        help_menu = self.addMenu("&Help")
        how_to_use_action = QAction("&How to Use...", self)
        how_to_use_action.triggered.connect(self.how_to_use)
        help_menu.addAction(how_to_use_action)

    def how_to_use(self):
        dialog = HelpDialog()
        dialog.exec_()

    def exit_application(self):
        QApplication.instance().quit()
        # Close the main window
        self.parent().close()


# Example usage
if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    mainWindow = QMainWindow()
    menuBar = MenuBar(mainWindow)
    mainWindow.setMenuBar(menuBar)
    mainWindow.show()
    sys.exit(app.exec_())

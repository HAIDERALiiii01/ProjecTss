import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtCore import QUrl
from pathlib import Path
import random
import shutil



class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MERCY")
        self.used_rects = []
        self.random_labels = []
        self.active_animations = []

        # ------------------ Background ------------------
        self.bg_label = QtWidgets.QLabel(self)
        pixmap = QtGui.QPixmap('stuff/bg.png')
        self.bg_label.setPixmap(pixmap)
        self.bg_label.setScaledContents(True)
        self.bg_label.setGeometry(0, 0, 5376, 3542)

        # ------------------ Label ------------------
        self.label = QtWidgets.QLabel("No folder selected", alignment=QtCore.Qt.AlignCenter, parent=self)

        # ------------------ Buttons ------------------
        font_id = QtGui.QFontDatabase.addApplicationFont("stuff/font/font/font.ttf")
        font_family = QtGui.QFontDatabase.applicationFontFamilies(font_id)[0]

        self.button1 = QtWidgets.QPushButton("SNAP!", parent=self)
        self.button1.setFont(QtGui.QFont(font_family, 50))
        self.button1.setFixedSize(270, 70)
        self.button1.setStyleSheet("""
            QPushButton {
                background-color: purple;
                color: yellow;
                border: 3px solid white;
                font-weight: 400;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: yellow;
                color: purple;
                border: 3px solid black;
            }
            QPushButton:pressed {
                background-color: red;
            }
        """)

        self.button2 = QtWidgets.QPushButton("SELECT UNIVERSE", parent=self)
        self.button2.setFont(QtGui.QFont(font_family, 20))
        self.button2.setFixedSize(270, 50)
        self.button2.setStyleSheet("""
            QPushButton {
                background-color: purple;
                color: yellow;
                border: 3px solid white;
                font-weight: 400;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: yellow;
                color: purple;
                border: 3px solid black;
            }
            QPushButton:pressed {
                background-color: red;
            }
        """)

        # ------------------ GIF/Image ------------------
        self.pic = QtWidgets.QLabel(parent=self)
        self.pic.setFixedSize(350, 350)
        self.pic.setStyleSheet("border: none; background: transparent;")
        pixmap = QtGui.QPixmap("stuff/picture.png")
        self.scaled_pixmap = pixmap.scaled(
            400, 400,
            QtCore.Qt.AspectRatioMode.KeepAspectRatio,
            QtCore.Qt.TransformationMode.SmoothTransformation
        )
        self.pic.setPixmap(self.scaled_pixmap)
        self.pic.setAlignment(QtCore.Qt.AlignCenter)

        # ------------------ Audio ------------------
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)

        # ------------------ Layout ------------------
        self.foreground = QtWidgets.QWidget(self)
        v_layout = QtWidgets.QVBoxLayout(self.foreground)
        h_layout = QtWidgets.QHBoxLayout()
        h_layout.addStretch()
        h_layout.addWidget(self.button1)
        h_layout.addWidget(self.button2)
        h_layout.addStretch()
        h_layout.setSpacing(5)
        v_layout.addStretch()
        v_layout.addWidget(self.pic, alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)
        v_layout.addStretch()
        v_layout.addWidget(self.label, alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)
        v_layout.addLayout(h_layout)
        v_layout.setSpacing(20)
        v_layout.setContentsMargins(0, 0, 0, 50)

        # ------------------ Signals ------------------
        self.button1.clicked.connect(self.on_snap)
        self.button2.clicked.connect(self.open_folder)

        # ------------------ Random Images ------------------
        self.random_images = ["stuff/1.png", "stuff/2.png", "stuff/3.png", "stuff/4.png"]  # add your images here
  
    def delete(self):
                
        main_folder = Path(self.label.text())

        # Get all items (files + folders)
        items = list(main_folder.iterdir())

        half_count = len(items) // 2

        items_to_delete = random.sample(items, half_count)

        for item in items_to_delete:
            if item.is_dir():
                shutil.rmtree(item)   # delete folder
            else:
                item.unlink()         # delete file

        print(f"Deleted {len(items_to_delete)} items.")
    
    # ------------------ Snap Button ------------------
    def on_snap(self):
        if self.label.text() != "No folder selected":
            self.play_audio()
            self.show_gif()
            self.snap_effect()
            self.delete()
            
        else:
            self.label.setText("Please select folder")

    # ------------------ Audio ------------------
    def play_audio(self):
        self.player.setSource(QUrl.fromLocalFile("stuff/sound.mp3"))
        self.audio_output.setVolume(50)
        self.player.play()

    # ------------------ GIF ------------------
    def show_gif(self):
        self.original_pixmap = self.scaled_pixmap
        self.movie = QtGui.QMovie("stuff/snap.gif")
        self.movie.setScaledSize(QtCore.QSize(400, 400))
        self.movie.setSpeed(70)
        self.pic.setMovie(self.movie)
        self.movie.frameChanged.connect(self.check_last_frame)
        self.movie.start()

    def check_last_frame(self, frame_number):
        if frame_number == self.movie.frameCount() - 1:
            self.movie.stop()
            self.pic.setPixmap(self.original_pixmap)

    # ------------------ Random Image Logic ------------------
    def get_random_position(self, img_width, img_height):
        max_x = self.width() - img_width
        max_y = self.height() - img_height
        while True:
            x = random.randint(0, max_x)
            y = random.randint(0, max_y)
            candidate_rect = QtCore.QRect(x, y, img_width, img_height)
            # Avoid buttons, labels, and GIF
            forbidden = [
                self.button1.geometry(),
                self.button2.geometry(),
                self.label.geometry(),
                self.pic.geometry(),
            ] + self.used_rects
            if not any(candidate_rect.intersects(area) for area in forbidden):
                return x, y

    def show_random_image(self, image_path):
        original = QtGui.QPixmap(image_path)
        pixmap = original.scaled(
            100, 100,
            QtCore.Qt.KeepAspectRatio,
            QtCore.Qt.SmoothTransformation
        )
        img_label = QtWidgets.QLabel(self)
        img_label.setPixmap(pixmap)
        # img_label.setScaledContents(True)
        img_label.setFixedSize(100, 100)

        x, y = self.get_random_position(100, 100)
        img_label.move(x, y)
        img_label.show()

        # 🔥 Save this rectangle so next images avoid it
        rect = QtCore.QRect(x, y, 100, 100)
        self.used_rects.append(rect)
        self.random_labels.append(img_label)

    def snap_effect(self):
        # pick half of the images randomly
        labels_to_snap = random.sample(
            self.random_labels,
            len(self.random_labels) // 2
        )
        
        for label in labels_to_snap:

            pixmap = label.pixmap()
            if not pixmap:
                continue

            piece_size = 20  # smaller = more particles (5–15 recommended)
            width = pixmap.width()
            height = pixmap.height()

            for x in range(0, width, piece_size):
                for y in range(0, height, piece_size):

                    piece = pixmap.copy(x, y, piece_size, piece_size)

                    particle = QtWidgets.QLabel(self)
                    particle.setPixmap(piece)
                    particle.setFixedSize(piece_size, piece_size)

                    global_pos = label.pos()
                    particle.move(global_pos.x() + x, global_pos.y() + y)
                    particle.show()

                    # Opacity
                    opacity = QtWidgets.QGraphicsOpacityEffect(particle)
                    particle.setGraphicsEffect(opacity)

                    fade = QtCore.QPropertyAnimation(opacity, b"opacity")
                    fade.setDuration(random.randint(800, 1600))
                    fade.setStartValue(1)
                    fade.setEndValue(0)

                    # Random dust drift
                    dx = random.randint(-80, 80)
                    dy = random.randint(-120, -40)

                    move = QtCore.QPropertyAnimation(particle, b"pos")
                    move.setDuration(random.randint(800, 1600))
                    move.setStartValue(particle.pos())
                    move.setEndValue(particle.pos() + QtCore.QPoint(dx, dy))

                    group = QtCore.QParallelAnimationGroup()
                    group.addAnimation(fade)
                    group.addAnimation(move)

                    group.finished.connect(particle.deleteLater)
                    self.active_animations.append(group)
                    group.finished.connect(lambda g=group: self.active_animations.remove(g))
                    group.start()

            label.deleteLater()

        # Keep images that were not snapped
        self.random_labels = [
            label for label in self.random_labels
            if label not in labels_to_snap
        ]
        self.used_rects = []  
          
    def show_random_image_from_list(self):
        img = random.choice(self.random_images)
        self.show_random_image(img)

    # ------------------ Window Events ------------------
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()

    def showEvent(self, event):
        super().showEvent(event)
        self.foreground.setGeometry(0, 0, self.width(), self.height())
        self.bg_label.setGeometry(0, 0, self.width(), self.height())

    def show_multiple_random_images(self, count=10, interval=500):
        self.images_shown = 0  # counter
        self.used_rects = []
        self.timer = QtCore.QTimer()
        
        def add_image():
            self.show_random_image_from_list()
            self.images_shown += 1
            if self.images_shown >= count:
                self.timer.stop()  # stop after reaching the count

        self.timer.timeout.connect(add_image)
        self.timer.start(interval)  # interval in milliseconds

    # ------------------ Folder Selection ------------------
    def open_folder(self):
        folder = QtWidgets.QFileDialog.getExistingDirectory(self, "Select a Folder")
        if folder:
            self.label.setText(folder)
            self.show_multiple_random_images()


# ------------------ Run App ------------------
app = QtWidgets.QApplication(sys.argv)
window = MyWidget()
window.showFullScreen()
sys.exit(app.exec())
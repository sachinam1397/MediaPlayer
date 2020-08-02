from PyQt5.QtWidgets import QFileDialog, QSizePolicy, QStyle, QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QSlider
from PyQt5.QtGui import QIcon, QPalette
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import Qt, QUrl
import sys



class Window(QWidget):
	def __init__(self):
		super().__init__()

		self.setWindowTitle("PyQt5 Player")
		self.setGeometry(350,100,700,500)

		p = self.palette()
		p.setColor(QPalette.Window, Qt.black)
		self.setPalette(p)

		self.init_ui()

		self.show()

	def init_ui(self):
		self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

		# create video widget object
		videoWidget = QVideoWidget()

		# create open object
		openButton = QPushButton('Open Video')
		openButton.clicked.connect(self.open_file)

		self.playButton = QPushButton()
		self.playButton.setEnabled(False)
		self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
		self.playButton.clicked.connect(self.play_video)


		self.slider = QSlider(Qt.Horizontal)
		self.slider.setRange(0,0)
		self.slider.sliderMoved.connect(self.set_position)

		# create label
		self.label = QLabel()
		self.label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

		# create HBoxLayout
		hBoxLayout = QHBoxLayout()
		hBoxLayout.setContentsMargins(0,0,0,0)

		hBoxLayout.addWidget(openButton)
		hBoxLayout.addWidget(self.playButton)
		hBoxLayout.addWidget(self.slider)


		vBoxLayout = QVBoxLayout()
		vBoxLayout.addWidget(videoWidget)
		vBoxLayout.addLayout(hBoxLayout)
		vBoxLayout.addWidget(self.label)

		self.setLayout(vBoxLayout)
		self.mediaPlayer.setVideoOutput(videoWidget)

		# media player signals
		self.mediaPlayer.stateChanged.connect(self.mediaState_change)
		self.mediaPlayer.positionChanged.connect(self.position_changed)
		self.mediaPlayer.durationChanged.connect(self.duration_changed) 



	def open_file(self):
		filename, _  =QFileDialog.getOpenFileName(self,"Open Video")
		if filename != '':
			self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(filename)))
			self.playButton.setEnabled(True)


	def play_video(self):
		if(self.mediaPlayer.state() == QMediaPlayer.PlayingState):
			self.mediaPlayer.pause()
		else:
			self.mediaPlayer.play()


	def mediaState_change(self,state):
		if(self.mediaPlayer.state() == QMediaPlayer.PlayingState):
			self.playButton.setIcon(
				self.style().standardIcon(QStyle.SP_MediaPause)
				)
		else:
			self.playButton.setIcon(
				self.style().standardIcon(QStyle.SP_MediaPlay)
				)

	def position_changed(self,position):
		self.slider.setValue(position)

	def duration_changed(self,duration):
		self.slider.setRange(0,duration)

	def set_position(self,position):
		self.mediaPlayer.setPosition(position)

	def handle_errors(self):
		self.playButton.setEnabled(False)
		self.label.setText("Error: " + self.mediaPlayer.errorString())







if __name__ == "__main__":
	app = QApplication(sys.argv)
	window = Window()
	sys.exit(app.exec_())

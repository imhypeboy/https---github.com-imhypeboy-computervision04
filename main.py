import sys
import cv2 as cv
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QComboBox, QVBoxLayout, QWidget, QFileDialog
from PyQt5.QtCore import Qt

class VideoSpecialEffect(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("비디오 특수 효과")
        self.setGeometry(200, 200, 800, 600)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # 레이아웃 설정
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # 스타일시트 설정
        self.setStyleSheet("""
            QPushButton {
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton#videoButton {
                background-color: #4CAF50;
            }
            QPushButton#videoCaptureButton {
                background-color: #2196F3;
            }
            QPushButton#captureButton {
                background-color: #FFC107;
                color: black;
            }
            QPushButton#quitButton {
                background-color: #f44336;
            }
            QComboBox {
                font-size: 18px;
                padding: 5px;
            }
        """)

        # 버튼 및 콤보박스 추가
        self.videoButton = QPushButton("시작", self)
        self.videoButton.setObjectName("videoButton")
        self.layout.addWidget(self.videoButton, alignment=Qt.AlignCenter)

        self.videoCaptureButton = QPushButton("비디오 캡처 시작/종료", self)
        self.videoCaptureButton.setObjectName("videoCaptureButton")
        self.layout.addWidget(self.videoCaptureButton, alignment=Qt.AlignCenter)

        self.captureButton = QPushButton("이미지 캡처", self)
        self.captureButton.setObjectName("captureButton")
        self.layout.addWidget(self.captureButton, alignment=Qt.AlignCenter)

        self.quitButton = QPushButton("나가기", self)
        self.quitButton.setObjectName("quitButton")
        self.layout.addWidget(self.quitButton, alignment=Qt.AlignCenter)

        self.pickCombo = QComboBox(self)
        self.pickCombo.addItems(["엠보싱", "카툰", "연필 스케치(명암)", "연필 스케치(컬러)", "유화"])
        self.layout.addWidget(self.pickCombo, alignment=Qt.AlignCenter)

        # 버튼 클릭 연결
        self.videoButton.clicked.connect(self.videoSpecialEffectFunction)
        self.videoCaptureButton.clicked.connect(self.toggleVideoCapture)
        self.captureButton.clicked.connect(self.captureImage)
        self.quitButton.clicked.connect(self.quitFunction)

        self.is_recording = False
        self.out = None
        self.special_img = None

    def videoSpecialEffectFunction(self):
        try:
            self.cap = cv.VideoCapture(0, cv.CAP_DSHOW)
            if not self.cap.isOpened():
                raise RuntimeError("카메라 연결 실패")

            fps = self.cap.get(cv.CAP_PROP_FPS)
            if fps == 0:
                fps = 30.0  # 기본값

            while True:
                ret, frame = self.cap.read()
                if not ret:
                    break

                pick_effect = self.pickCombo.currentIndex()
                try:
                    if pick_effect == 0:  # 엠보싱
                        femboss = np.array([[-1.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 1.0]])
                        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
                        gray16 = np.int16(gray)
                        self.special_img = np.uint8(np.clip(cv.filter2D(gray16, -1, femboss) + 128, 0, 255))
                    elif pick_effect == 1:  # 카툰
                        self.special_img = cv.stylization(frame, sigma_s=60, sigma_r=0.45)
                    elif pick_effect == 2:  # 연필 스케치(명암)
                        gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
                        self.special_img = cv.GaussianBlur(gray_frame, (21, 21), sigmaX=0, sigmaY=0)
                    elif pick_effect == 3:  # 연필 스케치(컬러)
                        _, self.special_img = cv.pencilSketch(frame, sigma_s=60, sigma_r=0.07, shade_factor=0.02)
                    elif pick_effect == 4:  # 유화
                        try:
                            self.special_img = cv.xphoto.oilPainting(frame, 7, 1)
                        except AttributeError:
                            print("유화 효과를 적용하려면 'opencv-contrib-python'이 필요합니다.")
                            self.special_img = frame
                    else:
                        self.special_img = frame
                except Exception as e:
                    print(f"효과 적용 중 오류 발생: {e}")
                    self.special_img = frame

                if self.is_recording and self.out is not None:
                    self.out.write(self.special_img)

                cv.imshow("Special effect", self.special_img)
                key = cv.waitKey(int(1000 / fps))
                if key & 0xFF == ord('q') or key == 27:
                    break

        finally:
            self.quitFunction()

    def toggleVideoCapture(self):
        if not self.is_recording:
            fname, _ = QFileDialog.getSaveFileName(self, '비디오 파일 저장', './', 'MP4 Files (*.mp4);;AVI Files (*.avi)')
            if fname:
                fourcc = cv.VideoWriter_fourcc(*'avc1') if fname.endswith('.mp4') else cv.VideoWriter_fourcc(*'XVID')
                fps = self.cap.get(cv.CAP_PROP_FPS)
                if fps == 0:
                    fps = 30.0
                frame_size = (self.special_img.shape[1], self.special_img.shape[0]) if self.special_img is not None else (640, 480)
                self.out = cv.VideoWriter(fname, fourcc, fps, frame_size)
                self.is_recording = True
                print(f"비디오 캡처 시작: {fname}")
        else:
            self.is_recording = False
            if self.out is not None:
                self.out.release()
                self.out = None
            print("비디오 캡처 종료")

    def captureImage(self):
        if self.special_img is not None:
            fname, _ = QFileDialog.getSaveFileName(self, '이미지 저장', './', 'PNG Files (*.png);;JPEG Files (*.jpg)')
            if fname:
                cv.imwrite(fname, self.special_img)
                print(f"이미지가 저장되었습니다: {fname}")

    def quitFunction(self):
        if hasattr(self, 'cap') and self.cap.isOpened():
            self.cap.release()
        if self.out is not None:
            self.out.release()
        cv.destroyAllWindows()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = VideoSpecialEffect()
    win.show()
    sys.exit(app.exec_())

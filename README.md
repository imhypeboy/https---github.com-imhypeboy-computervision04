# 실행 파일 다운로드 후
1. dist 폴더 클릭후,`main.exe` 파일을 더블 클릭하여 실행합니다.
2. '시작'버튼을 눌러 비디오 캡처, 이미지 캡처 가능합니다.
3. 'q' 키 또는 'esc' 키로 종료할 수 있습니다.

📝 프로젝트 개요
"비디오 특수 효과" 애플리케이션은 웹캠 영상을 실시간으로 캡처하고 다양한 특수 효과를 적용하여 화면에 출력하는 프로그램입니다. 
버튼과 콤보박스를 통해 쉽게 영상을 시작하고 원하는 효과를 선택하며, 프로그램을 종료할 수 있습니다.

🚀 주요 기능
🔴 실시간 비디오 캡처: 웹캠을 통해 실시간으로 영상을 캡처합니다.
🎨 특수 효과 적용: 엠보싱, 카툰, 연필 스케치(명암 및 컬러), 유화 효과를 지원합니다.
💻 UI 구성: 최신 스타일을 반영하여 버튼과 콤보박스를 시각적으로 개선했습니다.
📐 창 크기 조절: 창 크기에 맞춰 버튼과 콤보박스의 크기가 자동으로 조절됩니다.
⏹️ 종료 기능: 'q' 또는 'esc' 키를 눌러 비디오 창을 종료할 수 있습니다.

💻 개발 환경

Python 버전: 3.9
PyQt5: 5.15.10
OpenCV: 4.5.x
IDE: Visual Studio Code
가상환경: Conda (vision_agent_project6_env)
🛠️ 설치 및 실행

# 가상환경 활성화
conda activate vision_agent_project6_env

# 필수 패키지 설치
pip install PyQt5 opencv-python numpy

# 프로그램 실행
python main.py
📦 실행 파일 생성 (PyInstaller)
PyInstaller를 이용하여 실행 파일(.exe)로 패키징할 수 있습니다.


코드 복사
# 실행 파일 생성 (콘솔 창 없이)
pyinstaller --onefile --windowed main.py
📋 종속성

PyQt5
OpenCV (opencv-python)
Numpy
ℹ️ 기타

비디오 창을 종료할 때 'q' 키 또는 'esc' 키를 사용할 수 있으며, "나가기" 버튼을 클릭해도 종료됩니다.

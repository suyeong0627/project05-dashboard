# 📊 Project 05. GUI 기반 가상 센서 데이터 통합 대시보드

> 🤖 **아두이노 없이** Python으로 가상 센서 데이터를 생성하여  
> **Streamlit + Plotly**로 실시간 시뮬레이션하는 교육용 대시보드

---

## 🌐 배포 링크

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://suyeong0627-project05-dashboard.streamlit.app/)

👉 **[앱 바로가기](https://suyeong0627-project05-dashboard.streamlit.app/)**


---

## 💡 프로젝트 개요

### 🎯 목표
- 아두이노 없이 **순수 Python**으로 가상 센서 데이터 생성
- 실시간 **3채널 센서 모니터링** 대시보드
- 데이터 기록 및 **CSV 다운로드** 기능
- **이상치 자동 감지** 및 경고

### 📌 활용 분야
- 기초 물리 실험 교육
- 데이터 수집 및 시각화 학습
- 실시간 센서 대시보드 프로토타입

---

## 🛠 사용 기술 스택

| 분류 | 기술 | 용도 |
|------|------|------|
| 🖥️ **Frontend** | `Streamlit` | 웹 인터페이스 구성 |
| 📊 **시각화** | `Plotly` | 실시간 3채널 차트 렌더링 |
| 🔢 **데이터 처리** | `NumPy`, `Pandas` | 가상 센서 신호 생성 및 통계 |
| 📥 **저장** | `CSV` | 측정 데이터 다운로드 |
| ☁️ **배포** | `Streamlit Cloud` | 무료 클라우드 호스팅 |
| 🐍 **언어** | `Python 3.10+` | 전체 로직 |

---

## 📂 프로젝트 구조

project05-dashboard/
├── app.py # 메인 Streamlit 대시보드
├── requirements.txt # 패키지 의존성 목록
├── README.md # 프로젝트 설명 (이 파일)
└── .gitignore # Git 무시 파일 (선택사항)


### 🔧 requirements.txt
streamlit>=1.28.0
pandas>=2.0.0
numpy>=1.24.0
plotly>=5.17.0

---

## ⚙️ 주요 기능

### 📡 실시간 시뮬레이션 제어

| 기능 | 설명 | 단축키 |
|------|------|--------|
| ▶️ **시작** | 가상 센서 시뮬레이션 ON | - |
| ⏸️ **정지** | 가상 센서 시뮬레이션 OFF | - |
| 🔴 **기록 시작** | 데이터 기록 ON | - |
| ⏹️ **기록 정지** | 데이터 기록 OFF | - |
| 🗑️ **데이터 초기화** | 전체 기록 데이터 리셋 | - |
| 📥 **CSV 다운로드** | 기록된 센서 데이터 즉시 내보내기 | - |

### ⚙️ 사이드바 제어 패널

| 설정 | 범위 | 기본값 | 설명 |
|------|------|--------|------|
| 🔊 **노이즈 레벨** | 0.0 ~ 3.0 | 0.5 | 센서 신호 노이즈 강도 조절 |
| ⚡ **업데이트 속도** | 0.1 ~ 1.0초 | 0.3초 | 차트 갱신 주기 조절 |
| 📈 **최대 표시 포인트** | 50 ~ 300 | 150 | 차트에 표시할 최대 데이터 수 |
| ⚖️ **온도 Gain** | 실수 입력 | 1.0 | 온도 신호 배율 캘리브레이션 |
| ⚖️ **온도 Offset** | 실수 입력 | 0.0 | 온도 신호 오프셋 캘리브레이션 |

### 🚨 이상치 자동 감지

| 채널 | 정상 범위 | 이상치 경고 |
|------|-----------|-------------|
| 🌡️ **온도** | 20 ~ 28°C | 범위 초과 시 실시간 경고 |
| 💡 **조도** | 150 ~ 850 lux | 범위 초과 시 실시간 경고 |
| 🌪️ **기압** | 1009 ~ 1017 hPa | 범위 초과 시 실시간 경고 |

---

## 📊 가상 센서 신호 상세 설명

### 🌡️ 온도 (Temperature)

\[
T(t) = 24 + 2\sin(0.01t) + \varepsilon_T
\]

- **기본값**: 22 ~ 26°C
- **변화 속도**: 매우 느림 (큰 시스템의 열응답 모방)
- **노이즈**: 매우 작음 (안정적인 센서)
- **물리적 의미**: 실내 온도의 천천한 변화

### 💡 조도 (Light Intensity)

\[
L(t) = 500 + 150\sin(0.03t) + 50\sin(0.1t) + \varepsilon_L
\]

- **기본값**: 300 ~ 700 lux (실내 조명 수준)
- **변화 속도**: 빠름 (여러 주기 신호 혼합)
- **노이즈**: 중간 크기
- **물리적 의미**: 창문 빛 + 실내 조명의 복합 영향

### 🌪️ 기압 (Atmospheric Pressure)

\[
P(t) = 1013 + 3\sin(0.005t) + \varepsilon_P
\]

- **기본값**: 1010 ~ 1016 hPa (표준 대기압 근처)
- **변화 속도**: 매우 느림 (기후 시스템의 시간 규모)
- **노이즈**: 매우 작음
- **물리적 의미**: 일일 기압 변화

---

## 🚀 로컬 실행 방법

### 필수 요구사항
- Python 3.10 이상
- pip (Python 패키지 관리자)

### 1단계: 저장소 클론

```bash
git clone https://github.com/your-username/project05-dashboard.git
cd project05-dashboard
2단계: 가상 환경 생성 (선택사항이지만 권장)
Windows:
python -m venv venv
venv\Scripts\activate
macOS / Linux:
python3 -m venv venv
source venv/bin/activate
3단계: 패키지 설치
pip install -r requirements.txt
4단계: 앱 실행
streamlit run app.py
출력 예시:
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.1.xxx:8501

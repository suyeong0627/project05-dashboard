import streamlit as st
import pandas as pd
import numpy as np
import time
import datetime
import plotly.graph_objs as go
from plotly.subplots import make_subplots

# ─────────────────────────────────────
# 페이지 설정
# ─────────────────────────────────────
st.set_page_config(
    page_title="Project 05 - 가상 센서 대시보드",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Project 05. GUI 기반 가상 센서 데이터 대시보드")
st.markdown("""
> 🤖 **아두이노 없이** Python으로 가상 센서 데이터를 생성하여
> 실시간 시뮬레이션하는 대시보드입니다.
""")

# ─────────────────────────────────────
# Session State 초기화
# ─────────────────────────────────────
if 'running'       not in st.session_state: st.session_state.running       = False
if 'recording'     not in st.session_state: st.session_state.recording     = False
if 'data'          not in st.session_state: st.session_state.data          = []
if 't'             not in st.session_state: st.session_state.t             = 0
if 'prev_temp'     not in st.session_state: st.session_state.prev_temp     = 23.0
if 'prev_light'    not in st.session_state: st.session_state.prev_light    = 500.0
if 'prev_pressure' not in st.session_state: st.session_state.prev_pressure = 1013.0

# ─────────────────────────────────────
# 사이드바 - 제어 패널
# ─────────────────────────────────────
st.sidebar.header("⚙️ 제어 패널")

noise_level  = st.sidebar.slider("🔊 노이즈 레벨",         0.0, 3.0, 0.5, 0.1)
update_speed = st.sidebar.slider("⚡ 업데이트 속도(초)",    0.1, 1.0, 0.3, 0.1)
max_points   = st.sidebar.slider("📈 최대 표시 포인트",      50, 300, 150,  10)

st.sidebar.markdown("---")
st.sidebar.header("🔧 채널별 캘리브레이션")
temp_gain   = st.sidebar.number_input("온도 Gain",   value=1.0, step=0.1)
temp_offset = st.sidebar.number_input("온도 Offset", value=0.0, step=0.5)

# ─────────────────────────────────────
# 버튼 행
# ─────────────────────────────────────
col1, col2, col3 = st.columns(3)

with col1:
    if st.button(
        "⏸️ 시뮬레이션 정지" if st.session_state.running
        else "▶️ 시뮬레이션 시작",
        use_container_width=True
    ):
        st.session_state.running = not st.session_state.running

with col2:
    if st.button(
        "⏹️ 기록 정지" if st.session_state.recording
        else "🔴 기록 시작",
        use_container_width=True
    ):
        st.session_state.recording = not st.session_state.recording

with col3:
    if st.button("🗑️ 데이터 초기화", use_container_width=True):
        st.session_state.data          = []
        st.session_state.t             = 0
        st.session_state.prev_temp     = 23.0
        st.session_state.prev_light    = 500.0
        st.session_state.prev_pressure = 1013.0

# ─────────────────────────────────────
# CSV 다운로드 버튼
# ─────────────────────────────────────
if st.session_state.data:
    df = pd.DataFrame(st.session_state.data)
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "📥 CSV 다운로드",
        csv,
        file_name="sensor_log.csv",
        mime="text/csv",
        use_container_width=True
    )

st.markdown("---")

# ─────────────────────────────────────
# 플레이스홀더 (실시간 업데이트용)
# ─────────────────────────────────────
metric_ph  = st.empty()
chart_ph   = st.empty()
anomaly_ph = st.empty()
stats_ph   = st.empty()

# ─────────────────────────────────────
# 가상 센서 데이터 생성 함수 (현실적 버전)
# ─────────────────────────────────────
def generate_sensor(t, noise):
    """
    현실적인 가상 센서 신호 생성
    - 온도  : 천천히 변하는 실내 온도 (22~26°C) → 순간 점프 없음
    - 조도  : 조금 더 빠르게 변하는 조명 (300~700 lux)
    - 기압  : 매우 천천히 변하는 기압 (1010~1016 hPa)
    """

    # ── 온도 ────────────────────────────────
    # 긴 주기 사인파로 목표값 설정 → 이전 값에서 조금씩만 이동
    target_temp = 24 + 2 * np.sin(0.01 * t)
    diff = np.clip(target_temp - st.session_state.prev_temp, -0.1, 0.1)
    temp = st.session_state.prev_temp + diff
    temp += np.random.normal(0, noise * 0.05)   # 노이즈 최소화
    temp = temp * temp_gain + temp_offset
    temp = round(np.clip(temp, 20.0, 28.0), 2)  # 20~28°C 범위 고정
    st.session_state.prev_temp = temp

    # ── 조도 ────────────────────────────────
    target_light = 500 + 150 * np.sin(0.03 * t) + 50 * np.sin(0.1 * t)
    diff_l = np.clip(target_light - st.session_state.prev_light, -5, 5)
    light  = st.session_state.prev_light + diff_l
    light += np.random.normal(0, noise * 2)
    light  = round(np.clip(light, 100.0, 900.0), 2)
    st.session_state.prev_light = light

    # ── 기압 ────────────────────────────────
    target_pres = 1013 + 3 * np.sin(0.005 * t)
    diff_p = np.clip(target_pres - st.session_state.prev_pressure, -0.2, 0.2)
    pressure  = st.session_state.prev_pressure + diff_p
    pressure += np.random.normal(0, noise * 0.1)
    pressure  = round(np.clip(pressure, 1008.0, 1018.0), 2)
    st.session_state.prev_pressure = pressure

    return temp, light, pressure

# ─────────────────────────────────────
# 이상치 감지 함수
# ─────────────────────────────────────
def detect_anomaly(temp, light, pressure):
    anomalies = []
    if abs(temp - 24) > 4:
        anomalies.append(f"⚠️ 온도 이상치: **{temp:.1f}°C** (정상범위: 20~28°C)")
    if light < 150 or light > 850:
        anomalies.append(f"⚠️ 조도 이상치: **{light:.1f} lux** (정상범위: 150~850)")
    if abs(pressure - 1013) > 4:
        anomalies.append(f"⚠️ 기압 이상치: **{pressure:.1f} hPa** (정상범위: 1009~1017)")
    return anomalies

# ─────────────────────────────────────
# 차트 렌더링 함수
# ─────────────────────────────────────
def render_chart(df):
    fig = make_subplots(
        rows=3, cols=1,
        subplot_titles=("🌡️ 온도 (°C)", "💡 조도 (lux)", "🌪️ 기압 (hPa)"),
        shared_xaxes=True,
        vertical_spacing=0.08
    )

    fig.add_trace(go.Scatter(
        x=df["time"], y=df["temperature"],
        mode="lines", name="온도",
        line=dict(color="#FF6B6B", width=2)
    ), row=1, col=1)

    fig.add_trace(go.Scatter(
        x=df["time"], y=df["light"],
        mode="lines", name="조도",
        line=dict(color="#FFD93D", width=2)
    ), row=2, col=1)

    fig.add_trace(go.Scatter(
        x=df["time"], y=df["pressure"],
        mode="lines", name="기압",
        line=dict(color="#6BCB77", width=2)
    ), row=3, col=1)

    fig.update_layout(
        height=550,
        template="plotly_dark",
        showlegend=True,
        title_text="📊 실시간 가상 센서 모니터링",
        margin=dict(t=60, b=20)
    )
    return fig

# ─────────────────────────────────────
# 메인 시뮬레이션 루프
# ─────────────────────────────────────
if st.session_state.running:
    for _ in range(500):
        if not st.session_state.running:
            break

        st.session_state.t += 1
        t = st.session_state.t

        temp, light, pressure = generate_sensor(t, noise_level)
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")

        # 기록 중이면 저장
        if st.session_state.recording:
            st.session_state.data.append({
                "timestamp":   timestamp,
                "time":        t,
                "temperature": temp,
                "light":       light,
                "pressure":    pressure
            })

        display = (st.session_state.data[-max_points:]
                   if st.session_state.data else [])

        # ── 현재값 메트릭 카드 ──────────────
        with metric_ph.container():
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("🌡️ 온도",    f"{temp:.1f} °C",
                      f"{temp - 24:.2f}")
            m2.metric("💡 조도",    f"{light:.1f} lux",
                      f"{light - 500:.1f}")
            m3.metric("🌪️ 기압",    f"{pressure:.1f} hPa",
                      f"{pressure - 1013:.2f}")
            m4.metric("📝 기록 수", f"{len(st.session_state.data)} 개",
                      "● 기록중" if st.session_state.recording else "○ 정지")

        # ── 차트 ───────────────────────────
        if len(display) > 2:
            df_disp = pd.DataFrame(display)
            chart_ph.plotly_chart(
                render_chart(df_disp),
                use_container_width=True
            )

        # ── 이상치 알림 ────────────────────
        anomalies = detect_anomaly(temp, light, pressure)
        if anomalies:
            anomaly_ph.error("**🚨 이상치 감지!**\n\n" + "\n\n".join(anomalies))
        else:
            anomaly_ph.success("✅ 모든 센서 정상 범위")

        # ── 통계 카드 ──────────────────────
        if len(display) > 2:
            df_disp = pd.DataFrame(display)
            with stats_ph.container():
                st.markdown("### 📐 실시간 통계")
                st.dataframe(
                    df_disp[["temperature", "light", "pressure"]]
                    .describe().round(2),
                    use_container_width=True
                )

        time.sleep(update_speed)

else:
    st.info("▶️ **시뮬레이션 시작** 버튼을 눌러주세요!")

    if st.session_state.data:
        df_all = pd.DataFrame(st.session_state.data)
        chart_ph.plotly_chart(
            render_chart(df_all[-max_points:]),
            use_container_width=True
        )
        with stats_ph.container():
            st.markdown("### 📐 최종 통계")
            st.dataframe(
                df_all[["temperature", "light", "pressure"]]
                .describe().round(2),
                use_container_width=True
            )

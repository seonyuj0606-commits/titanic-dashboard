
# ==========================================
# 1. 라이브러리 불러오기
# ==========================================
import streamlit as st
import pandas as pd
import plotly.express as px

# ==========================================
# 2. 페이지 설정
# ==========================================
st.set_page_config(
    page_title="타이타닉 생존율 대시보드",
    layout="wide"
)

# ==========================================
# 3. 데이터 불러오기
# ==========================================
@st.cache_data
def load_data():
    return pd.read_csv("titanic.csv")

# ==========================================
# 4. 데이터 필터 함수
# ==========================================
def filter_data(df, sexes, classes, age_range):

    f = df[
        df["sex"].isin(sexes) &
        df["pclass"].isin(classes)
    ]

    # 전체 나이 범위가 아닐 때만 나이 필터 적용
    if age_range != (0, 80):
        f = f[f["age"].between(*age_range)]

    return f

# ==========================================
# 5. KPI 계산 함수
# ==========================================
def kpi(df):

    count = len(df)

    survival = df["survived"].mean() * 100
    average_age = df["age"].mean()

    return count, survival, average_age

# ==========================================
# 6. 객실 등급별 생존율 차트
# ==========================================
def class_rate_bar(df):

    r = (
        df.groupby("pclass")["survived"]
        .mean()
        .mul(100)
        .round(1)
        .reset_index()
    )

    fig = px.bar(
        r,
        x="pclass",
        y="survived",
        text="survived",
        title="객실 등급별 생존율(%)",
        labels={
            "pclass": "객실 등급",
            "survived": "생존율(%)"
        },
        color_discrete_sequence=["#207A99"]
    )

    fig.update_traces(texttemplate="%{text}%", textposition="outside")
    fig.update_layout(yaxis_range=[0, 100])

    return fig

# ==========================================
# 7. 생존 여부별 나이 분포 차트
# ==========================================
def age_hist(df):

    fig = px.histogram(
        df,
        x="age",
        color="survived",
        barmode="overlay",
        opacity=0.6,
        title="생존 여부별 나이 분포",
        labels={
            "age": "나이",
            "survived": "생존 여부"
        },
        color_discrete_map={
            0: "#A8B4BC",
            1: "#207A99"
        }
    )

    return fig

# ==========================================
# 8. 데이터 불러오기
# ==========================================
df = load_data()

# ==========================================
# 9. 대시보드 제목
# ==========================================
st.title("타이타닉, 누가 살아남았나?")
st.caption("성별 · 객실 등급 · 나이에 따른 생존율 분석")

# ==========================================
# 10. 사이드바 필터
# ==========================================
st.sidebar.header("데이터 필터")

sexes = st.sidebar.multiselect(
    "성별",
    ["male", "female"],
    ["male", "female"]
)

classes = st.sidebar.multiselect(
    "객실 등급",
    [1, 2, 3],
    [1, 2, 3]
)

ages = st.sidebar.slider(
    "나이 범위",
    0,
    80,
    (0, 80)
)

# ==========================================
# 11. 필터 적용
# ==========================================
f = filter_data(df, sexes, classes, ages)

# ==========================================
# 12. KPI 숫자 표시
# ==========================================
count, survival, average_age = kpi(f)

st.subheader("핵심 분석 지표")

c1, c2, c3 = st.columns(3)

c1.metric("승객 수", f"{count:,}명")

c2.metric(
    "생존율",
    f"{survival:.1f}%" if pd.notna(survival) else "데이터 없음"
)

c3.metric(
    "평균 나이",
    f"{average_age:.1f}세" if pd.notna(average_age) else "데이터 없음"
)

st.divider()

# ==========================================
# 13. 차트 2개 나란히 표시
# ==========================================
st.subheader("생존율과 나이 분석")

if f.empty:
    st.warning("선택한 조건에 해당하는 승객이 없습니다.")
else:
    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(
            class_rate_bar(f),
            use_container_width=True
        )

    with col2:
        st.plotly_chart(
            age_hist(f),
            use_container_width=True
        )

# ==========================================
# 14. 상세 데이터 표
# ==========================================
with st.expander("데이터 보기"):
    st.dataframe(f, use_container_width=True)

# ==========================================
# 15. 분석 결과 안내
# ==========================================
st.info(
    "왼쪽 필터를 변경하면 승객 수, 생존율, 평균 나이와 "
    "차트가 자동으로 변경됩니다."
)

st.caption("AI 기반 데이터 전처리 및 시각화 | 12주차")

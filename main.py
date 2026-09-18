import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 영화 데이터 그래프 도감 2 - 분포와 관계")

st.write(
    "1년간 박스오피스 10위권에 든 영화 가운데 "
    "해당 기간에 개봉한 영화들의 데이터를 다양한 그래프로 살펴봅니다."
)

DATA_URL = (
    "https://raw.githubusercontent.com/greatsong/"
    "modudata/main/data/kobis_movies.csv"
)


@st.cache_data
def load_data():
    return pd.read_csv(DATA_URL)


df = load_data()


# ================================
# 데이터 전처리
# ================================

df["genre_main"] = (
    df["genre"]
    .fillna("장르 미상")
    .astype(str)
    .str.split(r"[|/]")
    .str[0]
    .str.strip()
)

df["genre_main"] = df["genre_main"].replace("", "장르 미상")


numeric_columns = [
    "first_scrn",
    "first_show",
    "first_week_audi",
    "total_audi",
    "days_in_top10"
]

for column in numeric_columns:
    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    )


# ================================
# 그래프 1
# 장르별 영화 편수
# ================================

st.header("1. 장르별 영화 편수")

genre_count = (
    df["genre_main"]
    .value_counts()
    .reset_index()
)

genre_count.columns = [
    "장르",
    "영화 편수"
]

fig_genre = px.pie(
    genre_count,
    names="장르",
    values="영화 편수",
    hole=0.45,
    title="장르별 영화 편수"
)

fig_genre.update_traces(
    hovertemplate=(
        "<b>%{label}</b><br>"
        "영화 편수: %{value}편<br>"
        "비율: %{percent}"
        "<extra></extra>"
    )
)

fig_genre.update_layout(
    legend_title_text="장르",
    margin=dict(
        t=60,
        b=20,
        l=20,
        r=20
    )
)

st.plotly_chart(
    fig_genre,
    use_container_width=True
)

st.markdown("---")

st.subheader("💡 이 그래프로 알 수 있는 것")

st.write(
    "장르별로 박스오피스 10위권에 든 영화가 "
    "몇 편씩 분포되어 있는지 비교할 수 있습니다."
)

st.markdown("---")


# ================================
# 그래프 2
# 장르별 영화와 총 관객 수
# ================================

st.header("2. 장르별 영화와 총 관객 수")

treemap_data = df.dropna(
    subset=[
        "total_audi",
        "movieNm",
        "genre_main"
    ]
).copy()

treemap_data = treemap_data[
    treemap_data["total_audi"] >= 0
]

fig_treemap = px.treemap(
    treemap_data,
    path=[
        "genre_main",
        "movieNm"
    ],
    values="total_audi",
    title="장르 안의 영화와 총 관객 수"
)

fig_treemap.update_traces(
    hovertemplate=(
        "<b>%{label}</b><br>"
        "총 관객: %{value:,.0f}명"
        "<extra></extra>"
    )
)

fig_treemap.update_layout(
    margin=dict(
        t=60,
        b=20,
        l=20,
        r=20
    )
)

st.plotly_chart(
    fig_treemap,
    use_container_width=True
)

st.markdown("---")

st.subheader("💡 이 그래프로 알 수 있는 것")

st.write(
    "장르별로 어떤 영화가 포함되어 있으며 "
    "영화마다 총 관객 수가 얼마나 다른지 비교할 수 있습니다."
)

st.markdown("---")


# ================================
# 그래프 3
# 총 관객 수의 분포
# ================================

st.header("3. 총 관객 수의 분포")

hist_data = df.dropna(
    subset=[
        "total_audi",
        "movieNm"
    ]
).copy()

hist_data = hist_data[
    hist_data["total_audi"] > 0
]

fig_hist = px.histogram(
    hist_data,
    x="total_audi",
    nbins=15,
    title="영화별 총 관객 수 분포",
    labels={
        "total_audi": "총 관객 수(명)",
        "count": "영화 편수"
    }
)

fig_hist.update_layout(
    margin=dict(
        t=60,
        b=20,
        l=20,
        r=20
    )
)

st.plotly_chart(
    fig_hist,
    use_container_width=True
)


hist_bins = pd.cut(
    hist_data["total_audi"],
    bins=15
)

bin_counts = (
    hist_bins
    .value_counts()
    .sort_index()
)

most_common_bin = bin_counts.idxmax()

lower = most_common_bin.left
upper = most_common_bin.right


max_movie = hist_data.loc[
    hist_data["total_audi"].idxmax()
]

max_movie_name = max_movie["movieNm"]
max_movie_audience = max_movie["total_audi"]


st.markdown("---")

st.subheader("💡 이 그래프로 알 수 있는 것")

st.write(
    f"대부분의 영화는 총 관객 수가 약 "
    f"{lower:,.0f}명 ~ {upper:,.0f}명 구간에 몰려 있습니다."
)

st.write(
    f"총 관객이 가장 많은 영화는 "
    f"**{max_movie_name}**으로, "
    f"총 관객 수는 **{max_movie_audience:,.0f}명**입니다."
)

st.markdown("---")


# ================================
# 그래프 4
# 개봉일 스크린 수와 총 관객의 관계
# ================================

st.header("4. 개봉일 스크린 수와 총 관객의 관계")

scatter_data = df.dropna(
    subset=[
        "first_scrn",
        "total_audi",
        "movieNm",
        "genre_main"
    ]
).copy()

scatter_data = scatter_data[
    (scatter_data["first_scrn"] >= 0) &
    (scatter_data["total_audi"] >= 0)
]

fig_scatter = px.scatter(
    scatter_data,
    x="first_scrn",
    y="total_audi",
    color="genre_main",
    hover_name="movieNm",
    title="개봉일 스크린 수와 총 관객의 관계",
    labels={
        "first_scrn": "개봉일 스크린 수",
        "total_audi": "총 관객 수(명)",
        "genre_main": "장르"
    }
)

fig_scatter.update_traces(
    marker=dict(size=9),
    hovertemplate=(
        "<b>%{hovertext}</b><br>"
        "개봉일 스크린 수: %{x:,.0f}개<br>"
        "총 관객: %{y:,.0f}명"
        "<extra></extra>"
    )
)

fig_scatter.update_layout(
    margin=dict(
        t=60,
        b=20,
        l=20,
        r=20
    )
)

st.plotly_chart(
    fig_scatter,
    use_container_width=True
)

st.markdown("---")

st.subheader("💡 이 그래프로 알 수 있는 것")

st.write(
    "개봉일 스크린 수와 총 관객 수의 관계를 살펴보고 "
    "장르별 영화의 분포를 비교할 수 있습니다."
)

st.markdown("---")


# ================================
# 그래프 5
# 장르별 총 관객 수 분포
# ================================

st.header("5. 장르별 총 관객 수 분포")

box_data = df.dropna(
    subset=[
        "genre_main",
        "total_audi",
        "movieNm"
    ]
).copy()

box_data = box_data[
    box_data["total_audi"] >= 0
]

genre_movie_counts = (
    box_data["genre_main"]
    .value_counts()
)

selected_genres = genre_movie_counts[
    genre_movie_counts >= 10
].index

box_data = box_data[
    box_data["genre_main"].isin(
        selected_genres
    )
]

fig_box = px.box(
    box_data,
    x="genre_main",
    y="total_audi",
    color="genre_main",
    points="outliers",
    hover_name="movieNm",
    title="영화가 10편 이상인 장르별 총 관객 수",
    labels={
        "genre_main": "장르",
        "total_audi": "총 관객 수(명)"
    }
)

fig_box.update_traces(
    hovertemplate=(
        "<b>%{hovertext}</b><br>"
        "총 관객: %{y:,.0f}명"
        "<extra></extra>"
    )
)

fig_box.update_layout(
    showlegend=False,
    margin=dict(
        t=60,
        b=20,
        l=20,
        r=20
    )
)

st.plotly_chart(
    fig_box,
    use_container_width=True
)

st.markdown("---")

st.subheader("💡 이 그래프로 알 수 있는 것")

st.write(
    "영화가 10편 이상인 장르를 대상으로 "
    "총 관객 수의 중앙값과 분포를 비교하고, "
    "상자 밖의 점을 통해 다른 영화보다 관객 수가 "
    "특히 많은 영화를 확인할 수 있습니다."
)

st.markdown("---")


# ================================
# 그래프 6
# 첫 주 관객 버블 그래프
# ================================

st.header("6. 첫 주 관객을 크기로 나타낸 버블 그래프")

bubble_data = df.dropna(
    subset=[
        "first_scrn",
        "total_audi",
        "first_week_audi",
        "movieNm",
        "genre_main"
    ]
).copy()

bubble_data = bubble_data[
    (bubble_data["first_scrn"] >= 0) &
    (bubble_data["total_audi"] >= 0) &
    (bubble_data["first_week_audi"] >= 0)
]

fig_bubble = px.scatter(
    bubble_data,
    x="first_scrn",
    y="total_audi",
    size="first_week_audi",
    color="genre_main",
    hover_name="movieNm",
    size_max=45,
    title="개봉일 스크린 수와 총 관객 수 - 첫 주 관객 버블 그래프",
    labels={
        "first_scrn": "개봉일 스크린 수",
        "total_audi": "총 관객 수(명)",
        "first_week_audi": "첫 주 관객(명)",
        "genre_main": "장르"
    }
)

fig_bubble.update_traces(
    hovertemplate=(
        "<b>%{hovertext}</b><br>"
        "개봉일 스크린 수: %{x:,.0f}개<br>"
        "총 관객: %{y:,.0f}명"
        "<extra></extra>"
    )
)

fig_bubble.update_layout(
    margin=dict(
        t=60,
        b=20,
        l=20,
        r=20
    )
)

st.plotly_chart(
    fig_bubble,
    use_container_width=True
)

st.markdown("---")

st.subheader("💡 이 그래프로 알 수 있는 것")

st.write(
    "개봉일 스크린 수와 총 관객 수의 관계를 살펴보면서 "
    "버블 크기를 통해 첫 주 관객이 많은 영화를 "
    "함께 비교할 수 있습니다."
)

st.markdown("---")


# ================================
# 그래프 7
# 제작 국가 → 장르 선버스트
# ================================

st.header("7. 제작 국가와 장르별 영화 편수")

sunburst_data = df.dropna(
    subset=[
        "nation",
        "genre_main",
        "movieNm"
    ]
).copy()

sunburst_data["nation"] = (
    sunburst_data["nation"]
    .astype(str)
    .str.strip()
)

sunburst_data["genre_main"] = (
    sunburst_data["genre_main"]
    .astype(str)
    .str.strip()
)

sunburst_data["nation"] = (
    sunburst_data["nation"]
    .replace("", "국가 미상")
)

sunburst_data["genre_main"] = (
    sunburst_data["genre_main"]
    .replace("", "장르 미상")
)

sunburst_data["영화 편수"] = 1

fig_sunburst = px.sunburst(
    sunburst_data,
    path=[
        "nation",
        "genre_main"
    ],
    values="영화 편수",
    title="제작 국가 → 장르별 영화 편수"
)

fig_sunburst.update_traces(
    hovertemplate=(
        "<b>%{label}</b><br>"
        "영화 편수: %{value}편"
        "<extra></extra>"
    )
)

fig_sunburst.update_layout(
    margin=dict(
        t=60,
        b=20,
        l=20,
        r=20
    )
)

st.plotly_chart(
    fig_sunburst,
    use_container_width=True
)

st.markdown("---")

st.subheader("💡 이 그래프로 알 수 있는 것")

st.write(
    "제작 국가별로 어떤 장르의 영화가 많이 만들어졌는지 "
    "영화 편수를 기준으로 한눈에 비교할 수 있습니다."
)

st.markdown("---")


# ================================
# 그래프 8
# 장르별 총 관객 산점도
# ================================

st.header("8. 장르 중에 총 관객수가 많은 장르는 무엇인가?")

genre_audience_data = df.dropna(
    subset=[
        "genre_main",
        "total_audi",
        "movieNm"
    ]
).copy()

genre_audience_data = genre_audience_data[
    genre_audience_data["total_audi"] >= 0
]

fig_genre_audience = px.scatter(
    genre_audience_data,
    x="genre_main",
    y="total_audi",
    hover_name="movieNm",
    title="장르 중에 총 관객수가 많은 장르는 무엇인가?",
    labels={
        "genre_main": "장르",
        "total_audi": "총 관객 수(명)"
    }
)

fig_genre_audience.update_traces(
    marker=dict(size=9),
    hovertemplate=(
        "<b>%{hovertext}</b><br>"
        "장르: %{x}<br>"
        "총 관객: %{y:,.0f}명"
        "<extra></extra>"
    )
)

fig_genre_audience.update_layout(
    margin=dict(
        t=60,
        b=20,
        l=20,
        r=20
    )
)

st.plotly_chart(
    fig_genre_audience,
    use_container_width=True
)

st.markdown("---")

st.subheader("💡 이 그래프로 알 수 있는 것")

st.write(
    "장르별 영화의 총 관객 수를 비교하여 "
    "어떤 장르에 관객 수가 많은 영화가 많이 분포하는지 "
    "살펴볼 수 있습니다."
)

st.markdown("---")

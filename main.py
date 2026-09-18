# =================================
# 그래프 8
# 장르별 총 관객 산점도
# =================================
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

# ---------------------------------
# 그래프 설명 구역
# ---------------------------------
st.markdown("---")

st.subheader("💡 이 그래프로 알 수 있는 것")

st.write(
    "장르별 영화의 총 관객 수를 비교하여 "
    "어떤 장르에 관객 수가 많은 영화가 많이 분포하는지 살펴볼 수 있습니다."
)

st.markdown("---")

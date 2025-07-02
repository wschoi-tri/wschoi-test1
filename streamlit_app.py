import streamlit as st
import requests
import urllib3

http = urllib3.PoolManager()
# 기본 API URL 설정
API_URL = st.text_input("API Base URL", value="http://10.254.103.39:8080/")
recomm_typ = st.selectbox("추천선택",
    options=[
        "buytogether",
        "viewtogether"
    ]
)

# 사용자 입력 폼
with st.form(key="view_form"):
    st.subheader("조회 파라미터")
    prd_no = st.text_input("상품번호", value="388856560")
    k = st.slider(
        "추천 개수 (k)", min_value=1, max_value=500, value=20
    )
    submit_button = st.form_submit_button(label="조회")

def show_image_grid(items, columns_per_row=5, title=None):
    if title:
        st.subheader(title)
    try:
        rows = [items[i: i + columns_per_row] for i in range(0, len(items), columns_per_row)]
        for row in rows:
            cols = st.columns(len(row), gap="small")
            for col, rec in zip(cols, row):
                img_url = rec.get("prd_img")
                url = rec.get("prd_url")
                prd_no = rec.get("prd_no")
                prd_nm = rec.get("prd_nm")
                score = rec.get("score")
                with col:
                    if img_url:
                        st.image(img_url, width=140)
                    if score == 0.0:
                        st.markdown(
                            f"<a href='{url}'>**{prd_no}**</a>", unsafe_allow_html=True
                        )
                    else:
                        st.markdown(
                            f"<a href='{url}'>**{prd_no}**</a><br>**Score:** {score:.6f}<br>{prd_nm}", unsafe_allow_html=True
                        )
    except Exception as e:
        st.error(f"이미지 표시 오류: {e}")

# 폼 제출 시 API 호출 및 이미지 표시
if submit_button:
    try:
        # 추천 API 호출
        params = dict(
            prd_no=int(prd_no),
            size=int(k)
        )
        response = requests.get(f"{API_URL}/{recomm_typ}", params=params)
        response.raise_for_status()
        data = response.json()

        # 원상품 이미지
        try:
            ori_img_resp = http.request(
                "GET",
                f"http://hapix.halfclub.com/searches/prdList/?keyword={prd_no}&siteCd=1&device=mc",
            )
            ori_list = []
            if ori_img_resp.status == 200:
                j = ori_img_resp.json()
                url = j["data"]["result"]["hits"]["hits"][0]["_source"]["appPrdImgUrl"]
                ori_list.append({"prd_no": prd_no, "score": 0.0, "prd_nm": "", "prd_url": "https://www.halfclub.com/product/" + str(prd_no), "prd_img": url})
            show_image_grid(ori_list, columns_per_row=1, title="원상품 이미지")
        except Exception as e:
            st.error(f"원상품 이미지 로드 오류: {e}")

        # 추천 상품 이미지 및 점수
        recs = []
        for rec in data.get("result", []):
            prd_no = rec.get("prd_no")
            score = rec.get("score", 0.0)
            prd_nm = rec.get("prd_nm")
            prd_img = rec.get("prd_img")
            prd_url = rec.get("prd_url")
            recs.append({"prd_no": prd_no, "score": score, "prd_nm": prd_nm, "prd_url": "https://www.halfclub.com/product/" + str(prd_no), "prd_img": prd_img})
        show_image_grid(recs, columns_per_row=5, title="추천 상품 이미지 및 점수")

    except requests.exceptions.HTTPError as http_err:
        st.error(f"HTTP 에러: {http_err}")
    except Exception as err:
        st.error(f"오류 발생: {err}")

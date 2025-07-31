import streamlit as st
import requests
import urllib3

st.set_page_config(layout="wide")

http = urllib3.PoolManager()
# 기본 API URL 설정
API_URL = st.text_input("API Base URL", value="https://cf-hapi.halfclub.com/recommend")
recomm_typ = st.selectbox("추천선택",
    options=[
        "buytogether",
        "buyuser",
        "viewtogether",
        "viewuser",
        # "category",
        "similaritem",
        "similar-image",
        "recommendforyou",
        "keyword-search"
    ]
)

self_yn = False
# 사용자 입력 폼
with st.form(key="view_form"):
    st.subheader("조회 파라미터")
    input_text = "상품번호"
    input_value = "388857758"
    if recomm_typ in ["similar-image"]:
        input_value = "381894156"
    if recomm_typ in ["similaritem"]:
        input_value = "391287472"
    if recomm_typ in ["keyword-search"]:
        input_text = "검색어"
        input_value = "뉴발란스 운동화"
    if recomm_typ in ["recommendforyou"]:
        input_text = "상품번호 리스트 (',' 로 구분)"
        input_value = "391834089,388857758,391287472"
    prd_no = st.text_input(input_text, value=input_value)
    
    age = ""
    gender = ""
    if recomm_typ in ["buytogetherage", "buyuser", "viewuser"]:
        # age = st.selectbox("연령대", options=["10대", "20대", "30대", "40대", "50대", "60대"], index=0)
        age = st.selectbox("연령", options=["01:40 미만", "02:40 이상"], index=0)
    if recomm_typ in ["buytogethergender", "buyuser", "viewuser"]:
        gender = st.selectbox("성별", options=["남성01", "여성02"], index=0)
    if recomm_typ in ["buytogether", "viewtogether", "buyuser", "viewuser"]:
        self_yn = st.selectbox("대체 로직", options=[False, True], index=0)
        
    k = st.slider(
        "추천 개수 (k)", min_value=1, max_value=500, value=50
    )
    k = st.number_input("추천 개수 (k)", value=k, min_value=1, max_value=500, key="k_input")
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
                        st.image(img_url, width=350)
                    if (not score) or score == 0.0:
                        st.markdown(
                            f"<a href='{url}'>**{prd_no}**</a><br/><p style='font-size:11pt;'>{prd_nm}</p>", unsafe_allow_html=True
                        )
                    else:
                        st.markdown(
                            f"<a href='{url}'>**{prd_no}**</a><br/>**Score:** {score:.3f}<br/><p style='font-size:11pt;'>{prd_nm}</p>", unsafe_allow_html=True
                        )
    except Exception as e:
        st.error(f"이미지 표시 오류: {e}")

# 폼 제출 시 API 호출 및 이미지 표시
if submit_button:
    try:
        # 추천 API 호출
        if recomm_typ in ["buytogetherage"]:
            params = dict(
                prd_no=int(prd_no+age[:2]),
                size=int(k)
            )
        elif recomm_typ in ["buytogethergender"]:
            params = dict(
                prd_no=int(prd_no+gender[-2:]),
                size=int(k)
            )
        elif recomm_typ in ["buyuser", "viewuser"]:
            params = dict(
                prd_no=int(prd_no),
                age=age[:2],
                gender=gender[-2:],
                self_yn=bool(self_yn),
                size=int(k)
            )
        elif recomm_typ in ["buytogether", "viewtogether"]:
            params = dict(
                prd_no=int(prd_no),
                self_yn=bool(self_yn),
                size=int(k)
            )
        elif recomm_typ in ["recommendforyou"]:
            params = dict(
                prd_no_list=[int(x) for x in prd_no.split(",")],
                # mem_no=int(prd_no),
                size=int(k)
            )
        elif recomm_typ not in ["keyword-search"]:
            params = dict(
                prd_no=int(prd_no),
                mem_no=int(prd_no),
                size=int(k)
            )
        else:
            params = dict(
                keyword=str(prd_no),
                limit=int(k)
            )
        response = requests.get(f"{API_URL}/{recomm_typ}", params=params)
        response.raise_for_status()
        data = response.json()

        if recomm_typ in ["similar-image"]:
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
                    prdNm = j["data"]["result"]["hits"]["hits"][0]["_source"]["prdNm"]
                    ori_list.append({"prd_no": prd_no, "score": 0.0, "prd_nm": prdNm, "prd_url": "https://www.halfclub.com/product/" + str(prd_no), "prd_img": url})
                show_image_grid(ori_list, columns_per_row=1, title="원상품 이미지")
            except Exception as e:
                st.error(f"원상품 이미지 로드 오류: {e}")
        elif recomm_typ in ["buytogether", "viewtogether", "similaritem", "buytogetherage", "buytogethergender", "buyuser", "viewuser"]:
            resp_prd_no = data.get("prd_no", prd_no)
            if resp_prd_no == 0:
                st.error("결과 없음")
            else:
                try:
                    ori_img_resp = http.request(
                        "GET",
                        f"http://hapix.halfclub.com/searches/prdList/?keyword={resp_prd_no}&siteCd=1&device=mc",
                    )
                    ori_list = []
                    if ori_img_resp.status == 200:
                        j = ori_img_resp.json()
                        url = j["data"]["result"]["hits"]["hits"][0]["_source"]["appPrdImgUrl"]
                        prdNm = j["data"]["result"]["hits"]["hits"][0]["_source"]["prdNm"]
                        if recomm_typ in ["buytogetherage"]:
                            prdNm = f"연령대: {age}<br/>" + prdNm
                        elif recomm_typ in ["buytogethergender"]:
                            prdNm = f"성별: {'남성' if gender[-2:] == '01' else ('여성' if gender[-2:] == '02' else '선택없음')}<br/>" + prdNm
                        elif recomm_typ in ["recommendforyou"]:
                            prdNm = "마지막확인 상품<br/>" + prdNm

                        ori_list.append({"prd_no": resp_prd_no, "score": 1.0, "prd_nm": prdNm, "prd_url": "https://www.halfclub.com/product/" + str(resp_prd_no), "prd_img": url})
                    show_image_grid(ori_list, columns_per_row=1, title="원상품 이미지")
                except Exception as e:
                    st.error(f"원상품 이미지 로드 오류: {e}")
        elif recomm_typ in ["recommendforyou"]:
            resp_prd_no = data.get("prd_no_list", [])
            if not resp_prd_no:
                st.error("결과 없음")
            else:
                ori_list = []
                for prd_no in resp_prd_no:
                    try:
                        ori_img_resp = http.request(
                            "GET",
                            f"http://hapix.halfclub.com/searches/prdList/?keyword={prd_no}&siteCd=1&device=mc",
                        )
                        if ori_img_resp.status == 200:
                            j = ori_img_resp.json()
                            url = j["data"]["result"]["hits"]["hits"][0]["_source"]["appPrdImgUrl"]
                            prdNm = j["data"]["result"]["hits"]["hits"][0]["_source"]["prdNm"]
                            if recomm_typ in ["buytogetherage"]:
                                prdNm = f"연령대: {age}<br/>" + prdNm
                            elif recomm_typ in ["buytogethergender"]:
                                prdNm = f"성별: {'남성' if gender[-2:] == '01' else ('여성' if gender[-2:] == '02' else '선택없음')}<br/>" + prdNm
                            # elif recomm_typ in ["recommendforyou"]:
                            #     prdNm = "마지막확인 상품<br/>" + prdNm

                            ori_list.append({"prd_no": prd_no, "score": 1.0, "prd_nm": prdNm, "prd_url": "https://www.halfclub.com/product/" + str(prd_no), "prd_img": url})
                    except Exception as e:
                        st.error(f"원상품 이미지 로드 오류: {e}")
                    
                if ori_list:
                    show_image_grid(ori_list, columns_per_row=5, title="원상품 이미지")

        # 추천 상품 이미지 및 점수
        recs = []
        if recomm_typ not in ["keyword-search", "similar-image"]:
            if data.get("ml_type", []):
                if data.get("ml_type") == "ml":
                    st.text_input("", "ML 추천 결과")
                    self_yn = False
                else:
                    st.text_input("", "대체 조회 결과")
                    self_yn = True
            
            for rec in data.get("result", []):
                prd_no = rec.get("prdNo")
                score = rec.get("score", 0.0)
                prd_nm = rec.get("prdNm")
                prd_img = rec.get("appPrdImgUrl")
                
                if rec.get("gender", ""):
                    prd_nm = f"성별: {'남성' if rec.get("gender") == '01' else ('여성' if rec.get("gender") == '02' else '')}<br/>" + prd_nm
                if rec.get("age", ""):
                    prd_nm = f"연령: {'40 미만' if rec.get("age") == '01' else ('40 이상' if rec.get("age") == '02' else '')}<br/>" + prd_nm
                if rec.get("rcm_prd_no", ""):
                    prd_nm = prd_nm + f"<br/>원상품:<a href='https://www.halfclub.com/product/{rec.get("rcm_prd_no", "")}'>{rec.get("rcm_prd_no", "")}</a>"

                recs.append({"prd_no": prd_no, "score": score, "prd_nm": prd_nm, "prd_url": "https://www.halfclub.com/product/" + str(prd_no), "prd_img": prd_img})
        elif recomm_typ in ["similar-image"]:
            for rec in data.get("result", []):
                prd_no = rec.get("prd_no")
                score = rec.get("score", 0.0)
                prd_nm = rec.get("prd_nm")
                prd_img = rec.get("prd_img")

                recs.append({"prd_no": prd_no, "score": score, "prd_nm": prd_nm, "prd_url": "https://www.halfclub.com/product/" + str(prd_no), "prd_img": prd_img})
        else:
            for rec in data:
                prd_no = rec.get("prd_no")
                score = rec.get("score", 0.0)
                prd_nm = rec.get("prd_nm")
                prd_img = rec.get("prd_img")
                prd_url = rec.get("prd_url")
                recs.append({"prd_no": prd_no, "score": score, "prd_nm": prd_nm, "prd_url": "https://www.halfclub.com/product/" + str(prd_no), "prd_img": prd_img})
                
        if not recs:
            st.error("리스트 결과 없음")
        else:
            show_image_grid(recs, columns_per_row=5, title="추천 상품 이미지 및 점수")

    except requests.exceptions.HTTPError as http_err:
        st.error(f"HTTP 에러: {http_err}")
    except Exception as err:
        st.error(f"오류 발생: {err}")

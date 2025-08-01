import streamlit as st
import requests
import urllib3

http = urllib3.PoolManager()

# st.set_page_config(
#     page_title="추천 서비스 (ML)",
#     layout="wide",
# )
st.header("추천 서비스 (ML)")
# st.set_page_config(layout="wide")


API_URL = "https://cf-hapi.halfclub.com/recommend"
self_yn = False
k = 50

select_prd_no = ""
select_prd_nm = ""
recomm_typ = ""
age = ""
gender = ""



st.subheader("추천 서비스 조회")

# 추천 서비스 유형
ml_types = [
    {"함께 본 상품": "viewtogether"},
    {"함께 본 상품 (연령/성별)": "viewuser"},
    {"함께 구매한 상품": "buytogether"},
    {"함께 구매한 상품 (연령/성별)": "buyuser"},
    {"유사 상품": "similaritem"},
    {"유사 이미지 상품": "similar-image"},
    {"개인화 추천": "recommendforyou"},
    {"검색 개인화": "keyword-search"}
]
select_type = st.selectbox("추천 서비스 유형",
    options=[
        list(ml_types[0].keys())[0],
        # list(ml_types[1].keys())[0],
        list(ml_types[2].keys())[0],
        # list(ml_types[3].keys())[0],
        list(ml_types[4].keys())[0],
        list(ml_types[5].keys())[0],
        list(ml_types[6].keys())[0],
        list(ml_types[7].keys())[0]
    ]
)

view_options = [
    {"prd_nm": "스커트", "prd_no": 379859455, "prd_img": "https://cdn2.halfclub.com/rimg/500x667/contain/cdn/product/SA000697/P379859455/1_P379859455_basic_1753948523039.jpg?format=webp"},
    {"prd_nm": "여성자켓", "prd_no": 386363240, "prd_img": "https://cdn2.halfclub.com/rimg/500x667/contain/cdn/product/A7939/P386363240/1_P386363240_basic_1748582603573.jpg?format=webp"},
    {"prd_nm": "여성코트", "prd_no": 384872711, "prd_img": "https://cdn2.halfclub.com/rimg/500x667/contain/cdn/product/A1394/P384872711/1_P384872711_basic_1741942329851.jpg?format=webp"},
    {"prd_nm": "여성데님", "prd_no": 354854282, "prd_img": "https://cdn2.halfclub.com/rimg/500x667/contain/cdn/product/SA004354/P354854282/1_P354854282_basic_1751338090084.jpg?format=webp"},
    {"prd_nm": "여성코트", "prd_no": 348548747, "prd_img": "https://cdn2.halfclub.com/rimg/500x667/contain/cdn/product/A1863/P348548747/1_P348548747_basic_1697433371437.jpg?format=webp"},
    {"prd_nm": "여성가방", "prd_no": 352872450, "prd_img": "https://cdn2.halfclub.com/rimg/500x667/contain/cdn/product/SA003626/P352872450/1_P352872450_basic_1754027266655.jpg?format=webp"},
    # {"prd_nm": "티셔츠", "prd_no": 395848372, "prd_img": "https://cdn2.halfclub.com/rimg/500x667/contain/cdn/product/SA004785/P395848372/1_P395848372_basic_1750035972338.jpg?format=webp"},
    # {"prd_nm": "원피스", "prd_no": 402544118, "prd_img": "https://cdn2.halfclub.com/rimg/500x667/contain/cdn/product/A1863/P402544118/1_P402544118_basic_1753455065108.jpg?format=webp"},
    # {"prd_nm": "골프웨어", "prd_no": 398183077, "prd_img": "https://cdn2.halfclub.com/rimg/500x667/contain/cdn/product/SA003881/P398183077/1_P398183077_basic_1750813492910.jpg?format=webp"},
    # {"prd_nm": "롱코트", "prd_no": 353797397, "prd_img": "https://cdn2.halfclub.com/rimg/500x667/contain/cdn/product/A2703/P353797397/1_P353797397_basic_1705311770902.jpg?format=webp"}
]
buy_options = [
    {"prd_nm": "스커트", "prd_no": 379859455, "prd_img": "https://cdn2.halfclub.com/rimg/500x667/contain/cdn/product/SA000697/P379859455/1_P379859455_basic_1753948523039.jpg?format=webp"},
    {"prd_nm": "여성자켓", "prd_no": 386363240, "prd_img": "https://cdn2.halfclub.com/rimg/500x667/contain/cdn/product/A7939/P386363240/1_P386363240_basic_1748582603573.jpg?format=webp"},
    {"prd_nm": "여성코트", "prd_no": 384872711, "prd_img": "https://cdn2.halfclub.com/rimg/500x667/contain/cdn/product/A1394/P384872711/1_P384872711_basic_1741942329851.jpg?format=webp"},
    {"prd_nm": "여성데님", "prd_no": 354854282, "prd_img": "https://cdn2.halfclub.com/rimg/500x667/contain/cdn/product/SA004354/P354854282/1_P354854282_basic_1751338090084.jpg?format=webp"},
    {"prd_nm": "여성코트", "prd_no": 348548747, "prd_img": "https://cdn2.halfclub.com/rimg/500x667/contain/cdn/product/A1863/P348548747/1_P348548747_basic_1697433371437.jpg?format=webp"},
    {"prd_nm": "여성가방", "prd_no": 352872450, "prd_img": "https://cdn2.halfclub.com/rimg/500x667/contain/cdn/product/SA003626/P352872450/1_P352872450_basic_1754027266655.jpg?format=webp"},
    {"prd_nm": "티셔츠", "prd_no": 395848372, "prd_img": "https://cdn2.halfclub.com/rimg/500x667/contain/cdn/product/SA004785/P395848372/1_P395848372_basic_1750035972338.jpg?format=webp"},
    {"prd_nm": "원피스", "prd_no": 402544118, "prd_img": "https://cdn2.halfclub.com/rimg/500x667/contain/cdn/product/A1863/P402544118/1_P402544118_basic_1753455065108.jpg?format=webp"},
    {"prd_nm": "골프웨어", "prd_no": 398183077, "prd_img": "https://cdn2.halfclub.com/rimg/500x667/contain/cdn/product/SA003881/P398183077/1_P398183077_basic_1750813492910.jpg?format=webp"},
    {"prd_nm": "롱코트", "prd_no": 353797397, "prd_img": "https://cdn2.halfclub.com/rimg/500x667/contain/cdn/product/A2703/P353797397/1_P353797397_basic_1705311770902.jpg?format=webp"}
]
similaritem_options = [
    {"prd_nm": "스커트", "prd_no": 379859455, "prd_img": "https://cdn2.halfclub.com/rimg/500x667/contain/cdn/product/SA000697/P379859455/1_P379859455_basic_1753948523039.jpg?format=webp"},
    {"prd_nm": "여성자켓", "prd_no": 386363240, "prd_img": "https://cdn2.halfclub.com/rimg/500x667/contain/cdn/product/A7939/P386363240/1_P386363240_basic_1748582603573.jpg?format=webp"},
    {"prd_nm": "여성코트", "prd_no": 384872711, "prd_img": "https://cdn2.halfclub.com/rimg/500x667/contain/cdn/product/A1394/P384872711/1_P384872711_basic_1741942329851.jpg?format=webp"},
    {"prd_nm": "여성데님", "prd_no": 354854282, "prd_img": "https://cdn2.halfclub.com/rimg/500x667/contain/cdn/product/SA004354/P354854282/1_P354854282_basic_1751338090084.jpg?format=webp"},
    {"prd_nm": "여성코트", "prd_no": 348548747, "prd_img": "https://cdn2.halfclub.com/rimg/500x667/contain/cdn/product/A1863/P348548747/1_P348548747_basic_1697433371437.jpg?format=webp"},
    {"prd_nm": "여성가방", "prd_no": 352872450, "prd_img": "https://cdn2.halfclub.com/rimg/500x667/contain/cdn/product/SA003626/P352872450/1_P352872450_basic_1754027266655.jpg?format=webp"},
    {"prd_nm": "티셔츠", "prd_no": 395848372, "prd_img": "https://cdn2.halfclub.com/rimg/500x667/contain/cdn/product/SA004785/P395848372/1_P395848372_basic_1750035972338.jpg?format=webp"},
    {"prd_nm": "원피스", "prd_no": 402544118, "prd_img": "https://cdn2.halfclub.com/rimg/500x667/contain/cdn/product/A1863/P402544118/1_P402544118_basic_1753455065108.jpg?format=webp"},
    {"prd_nm": "골프웨어", "prd_no": 398183077, "prd_img": "https://cdn2.halfclub.com/rimg/500x667/contain/cdn/product/SA003881/P398183077/1_P398183077_basic_1750813492910.jpg?format=webp"},
    {"prd_nm": "롱코트", "prd_no": 353797397, "prd_img": "https://cdn2.halfclub.com/rimg/500x667/contain/cdn/product/A2703/P353797397/1_P353797397_basic_1705311770902.jpg?format=webp"}
]
similarimage_options = [
    {"prd_nm": "티셔츠", "prd_no": 395848372, "prd_img": "https://cdn2.halfclub.com/rimg/500x667/contain/cdn/product/SA004785/P395848372/1_P395848372_basic_1750035972338.jpg?format=webp"},
    {"prd_nm": "원피스", "prd_no": 402544118, "prd_img": "https://cdn2.halfclub.com/rimg/500x667/contain/cdn/product/A1863/P402544118/1_P402544118_basic_1753455065108.jpg?format=webp"},
    {"prd_nm": "골프웨어", "prd_no": 398183077, "prd_img": "https://cdn2.halfclub.com/rimg/500x667/contain/cdn/product/SA003881/P398183077/1_P398183077_basic_1750813492910.jpg?format=webp"},
    {"prd_nm": "롱코트", "prd_no": 353797397, "prd_img": "https://cdn2.halfclub.com/rimg/500x667/contain/cdn/product/A2703/P353797397/1_P353797397_basic_1705311770902.jpg?format=webp"}
] 
search_options = [
    {"prd_nm": "티셔츠", "prd_no": 0, "prd_img": ""},
    {"prd_nm": "운동화", "prd_no": 1, "prd_img": ""},
    {"prd_nm": "닥스", "prd_no": 2, "prd_img": ""},
    {"prd_nm": "헤지스", "prd_no": 3, "prd_img": ""},
    {"prd_nm": "자켓", "prd_no": 4, "prd_img": ""},
    {"prd_nm": "골프화", "prd_no": 5, "prd_img": ""},
    {"prd_nm": "팬츠", "prd_no": 6, "prd_img": ""},
    {"prd_nm": "니트", "prd_no": 7, "prd_img": ""},
    {"prd_nm": "지갑", "prd_no": 8, "prd_img": ""},
    {"prd_nm": "CNN APPAREL", "prd_no": 9, "prd_img": ""},
    {"prd_nm": "팬암", "prd_no": 10, "prd_img": ""},
    {"prd_nm": "폴로랄프로렌", "prd_no": 11, "prd_img": ""}
]
search_gender_options = {
    "남성": "male",
    "여성": "female"
}
gender_options = {
    "남성": "01",
    "여성": "02"
}
age_options = {
    "40대 미만": "01",
    "40대 이상": "02"
}

recommend_type = ""
recommend_type_nm = ""
for item in ml_types:
    if list(item.keys())[0] == select_type:
        recommend_type = list(item.values())[0]
        recommend_type_nm = list(item.keys())[0]
        break
    
recommend_sample = view_options
gender_params = gender_options
age_params = age_options

if recommend_type in ["keyword-search"]:
    recommend_sample = search_options
    gender_params = search_gender_options

if "recommendforyou" not in st.session_state or recommend_type not in ["recommendforyou"]:
    st.session_state.recommendforyou = set()

# 선택 토글 함수
# def toggle_selection(name):
#     st.session_state.selected = name

submit_button = None
input_yn = st.checkbox("직접입력", value=False, key="direct_input")

# 추천 대상 이미지 선택
if not input_yn:
    # 추천 대상 이미지 버튼 CSS 설정
    st.markdown("""
        <style>
        .full-btn > button {
            width: 100% !important;
            height: auto !important;
            padding: 0 !important;
            border: 3px solid transparent;
            border-radius: 10px;
            overflow: hidden;
        }
        .full-btn > button:hover {
            border-color: #aaa;
        }
        .full-btn {
            margin-bottom: 10px;
        }
        .selected-btn > button {
            border-color: #ff4b4b !important;
        }
        .btn-content {
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        .btn-content img {
            width: 100%;
            height: auto;
            border-bottom: 1px solid #ddd;
        }
        .btn-text {
            font-weight: bold;
            font-size: 16px;
            padding: 8px;
            text-align: center;
            width: 100%;
        }
        </style>
    """, unsafe_allow_html=True)
    
    col_count = 6
    if recommend_type in ["keyword-search"]:
        gender = st.selectbox("성별", options=["", "남성", "여성"], index=0)
        st.markdown("키워드")
        col_count = 4
        
    # 이미지 버튼 표시
    cols = st.columns(col_count)
    for i, value in enumerate(recommend_sample):
        prd_nm = value.get("prd_nm", "")
        prd_img = value.get("prd_img", "")
        prd_no = value.get("prd_no", "")
        
        selected_class = ""
        with cols[i % col_count]:
            btn = st.container()
            with btn:
                if st.button(
                    label=prd_nm,
                    key=f"btn_{prd_no}",
                    # help=prd_nm,
                    use_container_width=True
                ):
                    selected_class = "selected-btn"
                    select_prd_no = str(prd_no)
                    if recommend_type in ["keyword-search"]:
                        select_prd_no = str(prd_nm)
                        prd_no  = str(prd_nm)
                    st.session_state.selected = prd_nm
                    
                    if recommend_type in ["recommendforyou"]:
                        if prd_no not in st.session_state.recommendforyou:
                            st.session_state.recommendforyou.add(prd_no)
                        else:
                            st.session_state.recommendforyou.remove(prd_no)
                            selected_class = ""

                if prd_img:
                    if prd_no in st.session_state.recommendforyou:
                        selected_class = "selected-btn"
                    st.markdown(
                        f"""
                        <div class="full-btn {selected_class}">
                            <button>
                                <div class="btn-content">
                                    <img src="{prd_img}" />
                                    <a href="https://www.halfclub.com/product/{prd_no}">{prd_no}</a>
                                </div>
                            </button>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
# 추천 대상 직접 입력
else:
    with st.form(key="view_form"):
        input_text = "상품번호"
        input_value = ""
        if recommend_type in ["keyword-search"]:
            input_text = "검색어"
        elif recommend_type in ["recommendforyou"]:
            input_text = "상품번호 리스트 (ex. 상품번호1,상품번호2,상품번호3)"
        prd_no = st.text_input(input_text, value=input_value)
        
        
        age = ""
        gender = ""
        if recommend_type in ["buytogetherage", "buyuser", "viewuser"]:
            age = st.selectbox("연령", options=["40대 미만", "40대 이상"], index=0)
        
        if recommend_type in ["keyword-search", "buyuser", "viewuser"]:
            gender = st.selectbox("성별", options=["", "남성", "여성"], index=0)
        
        submit_button = st.form_submit_button(label="조회")

# 가로선
st.markdown("---")

#  추천 대상 상품 표시
def show_target(items, columns_per_row=5, title=None):    
    if title:
        if input_yn:
            title = title + ": 직접 입력"
        else:
            if st.session_state.selected:
                title = title + f": {st.session_state.selected}"
        st.subheader(title)
    try:
        rows = [items[i: i + columns_per_row] for i in range(0, len(items), columns_per_row)]
        for row in rows:
            cols = st.columns(len(row), gap="small")
            for col, rec in zip(cols, row):
                prd_no = rec.get("prd_no")
                prd_nm = rec.get("prd_nm")
                st.markdown(f"상품번호: <a href='https://www.halfclub.com/product/{prd_no}'>{prd_no}</a><br/>상품명: {prd_nm}", unsafe_allow_html=True)

        # 가로선
        st.markdown("---")
    except Exception as e:
        st.error(f"이미지 표시 오류: {e}")

# 추천 결과 상품 리스트 표시
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
                        if not columns_per_row == 1:
                            # st.image(img_url, width=150)
                        # else:
                            st.image(img_url, width=130)
                    if (not score) or score == 0.0:
                        st.markdown(
                            f"<a href='{url}'>**{prd_no}**</a><br/><p style='font-size:11pt;'>{prd_nm}</p>", unsafe_allow_html=True
                        )
                    else:
                        st.markdown(
                            f"상품: <a href='{url}'>{prd_no}</a><br/>추천 스코어: {score:.3f}<br/>"
                            + f"{prd_nm}", unsafe_allow_html=True
                        )
    except Exception as e:
        st.error(f"이미지 표시 오류: {e}")


# 추천 조회
def submit():
    # 추천 서비스 유형 선택
    if not select_type:
        return
    # 상품 번호 입력
    if not select_prd_no:
        return
    
    try:
        if recommend_type in ["viewtogether", "buytogether", "similaritem", "similar-image"]:
            params = dict(
                prd_no=int(select_prd_no),
                size=int(k)
            )
        elif recommend_type in ["buyuser", "viewuser"]:
            params = dict(
                prd_no=int(select_prd_no),
                age=age[:2],
                gender=gender[-2:],
                self_yn=bool(self_yn),
                size=int(k)
            )
        elif recommend_type in ["keyword-search"]:
            selected_gender = ""
            if gender:
                for item in search_gender_options:
                    if item == gender:
                        selected_gender = search_gender_options[item]
                        break
            params = dict(
                keyword=select_prd_no,
                gender=selected_gender,
                limit=int(k)
            )
        elif recommend_type in ["recommendforyou"]:
            params = dict(
                prd_no_list=list(st.session_state.recommendforyou),
                size=int(k)
            )
        response = requests.get(f"{API_URL}/{recommend_type}", params=params)
        response.raise_for_status()
        data = response.json()

        if recommend_type in ["similar-image"]:
            # 원상품 이미지
            try:
                ori_img_resp = http.request(
                    "GET",
                    f"http://hapix.halfclub.com/searches/prdList/?keyword={select_prd_no}&siteCd=1&device=mc",
                )
                ori_list = []
                if ori_img_resp.status == 200:
                    j = ori_img_resp.json()
                    prd_no = j["data"]["result"]["hits"]["hits"][0]["_source"]["prdNo"]
                    url = j["data"]["result"]["hits"]["hits"][0]["_source"]["appPrdImgUrl"]
                    prdNm = j["data"]["result"]["hits"]["hits"][0]["_source"]["prdNm"]
                    ori_list.append({"prd_no": prd_no, "score": 0.0, "prd_nm": prdNm, "prd_url": "https://www.halfclub.com/product/" + str(prd_no), "prd_img": url})
                show_image_grid(ori_list, columns_per_row=10, title="추천 대상 상품")
            except Exception as e:
                st.error(f"원상품 이미지 로드 오류: {e}")
        elif recommend_type in ["buytogether", "viewtogether", "similaritem", "buytogetherage", "buytogethergender", "buyuser", "viewuser"]:
            resp_prd_no = data.get("prd_no", select_prd_no)
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
                        if recommend_type in ["buytogetherage"]:
                            prdNm = f"연령대: {age}<br/>" + prdNm
                        elif recommend_type in ["buytogethergender"]:
                            prdNm = f"성별: {'남성' if gender[-2:] == '01' else ('여성' if gender[-2:] == '02' else '선택없음')}<br/>" + prdNm
                        elif recommend_type in ["recommendforyou"]:
                            prdNm = "마지막확인 상품<br/>" + prdNm

                        ori_list.append({"prd_no": resp_prd_no, "score": 1.0, "prd_nm": prdNm, "prd_url": "https://www.halfclub.com/product/" + str(resp_prd_no), "prd_img": url})
                    show_target(ori_list, columns_per_row=1, title="추천 대상 상품")
                except Exception as e:
                    st.error(f"원상품 이미지 로드 오류: {e}")
        elif recommend_type in ["recommendforyou"]:
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
                            if recommend_type in ["buytogetherage"]:
                                prdNm = f"연령대: {age}<br/>" + prdNm
                            elif recommend_type in ["buytogethergender"]:
                                prdNm = f"성별: {'남성' if gender[-2:] == '01' else ('여성' if gender[-2:] == '02' else '선택없음')}<br/>" + prdNm
                            # elif recomm_typ in ["recommendforyou"]:
                            #     prdNm = "마지막확인 상품<br/>" + prdNm

                            ori_list.append({"prd_no": prd_no, "score": 1.0, "prd_nm": prdNm, "prd_url": "https://www.halfclub.com/product/" + str(prd_no), "prd_img": url})
                    except Exception as e:
                        st.error(f"원상품 이미지 로드 오류: {e}")
                    
                if ori_list:
                    show_image_grid(ori_list, columns_per_row=6, title="추천 대상 상품")

        # 추천 상품 이미지 및 점수
        recs = []
        recs_title = "추천 결과 상품 리스트"
        ml_type = ""
                
        if recommend_type not in ["keyword-search"]:
            ml_type = data.get("ml_type", [])
            if ml_type:
                if ml_type == "ml":
                    recs_title = recs_title + f": {recommend_type_nm} ML"
            
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
        elif recommend_type in ["similar-image"]:
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
            show_image_grid(recs, columns_per_row=5, title=recs_title)

    except requests.exceptions.HTTPError as http_err:
        st.error(f"HTTP 에러: {http_err}")
    except Exception as err:
        st.error(f"오류 발생: {err}")


# # 폼 제출 시 API 호출 및 이미지 표시
if submit_button:
    select_prd_no = prd_no
    submit()
elif submit:
    # select_prd_no = prd_no
    submit()

import streamlit as st
import requests
import urllib3

http = urllib3.PoolManager()

# st.set_page_config(
#     page_title="추천 서비스 (ML)",
#     layout="wide",
# )
st.header("추천 서비스 (ML)")


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
    {"prd_nm": "스커트1", "prd_no": 379859455, "prd_img": "https://cdn2.halfclub.com/rimg/500x667/contain/cdn/product/SA000697/P379859455/1_P379859455_basic_1753948523039.jpg?format=webp"},
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
viewuser_options = [
    {"prd_nm": "스커트11", "prd_no": 379859455, "prd_img": "https://cdn2.halfclub.com/rimg/500x667/contain/cdn/product/SA000697/P379859455/1_P379859455_basic_1753948523039.jpg?format=webp"},
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
    {"prd_nm": "스커트2", "prd_no": 379859455, "prd_img": "https://cdn2.halfclub.com/rimg/500x667/contain/cdn/product/SA000697/P379859455/1_P379859455_basic_1753948523039.jpg?format=webp"},
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
buyuser_options = [
    {"prd_nm": "스커트22", "prd_no": 379859455, "prd_img": "https://cdn2.halfclub.com/rimg/500x667/contain/cdn/product/SA000697/P379859455/1_P379859455_basic_1753948523039.jpg?format=webp"},
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
    {"prd_nm": "스커트3", "prd_no": 379859455, "prd_img": "https://cdn2.halfclub.com/rimg/500x667/contain/cdn/product/SA000697/P379859455/1_P379859455_basic_1753948523039.jpg?format=webp"},
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
recommendforyou_options = [
    {"prd_nm": "스커트4", "prd_no": 379859455, "prd_img": "https://cdn2.halfclub.com/rimg/500x667/contain/cdn/product/SA000697/P379859455/1_P379859455_basic_1753948523039.jpg?format=webp"},
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
    {"prd_nm": "티셔츠4", "prd_no": 395848372, "prd_img": "https://cdn2.halfclub.com/rimg/500x667/contain/cdn/product/SA004785/P395848372/1_P395848372_basic_1750035972338.jpg?format=webp"},
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

input_yn = st.checkbox("직접입력", value=False, key="direct_input")

if recommend_type in ["keyword-search"]:
    gender = st.selectbox("성별", options=["", "남성", "여성"], index=0)
elif recommend_type in ["buytogether", "viewtogether"]:
    user_yn = st.checkbox("회원 유형 선택", value=False, key="user_chk_input")
    if user_yn:
        age = st.selectbox("나이 (40대 미만, 이상)", options=["", "40대 미만", "40대 이상"], index=0)
        if age:
            gender = st.selectbox("성별", options=["남성", "여성"], index=0)
        else:
            gender = st.selectbox("성별", options=["", "남성", "여성"], index=0)
            
recommend_sample = view_options
gender_params = gender_options
age_params = age_options

# 추천에 따른 대상 리스트 설정
if recommend_type in ["keyword-search"]:
    recommend_sample = search_options
    gender_params = search_gender_options
elif recommend_type in ["viewtogether", "viewuser"]:
    if user_yn:
        recommend_sample = viewuser_options
    else:
        recommend_sample = view_options
elif recommend_type in ["buytogether", "buyuser"]:
    if user_yn:
        recommend_sample = buyuser_options
    else:
        recommend_sample = buy_options
elif recommend_type in ["similaritem"]:
    recommend_sample = similaritem_options
elif recommend_type in ["similar-image"]:
    recommend_sample = similarimage_options
elif recommend_type in ["recommendforyou"]:
    recommend_sample = recommendforyou_options


if "recommendforyou" not in st.session_state or recommend_type not in ["recommendforyou"]:
    st.session_state.recommendforyou = set()
    
if "gender" not in st.session_state or recommend_type not in ["buyuser", "viewuser"]:
    st.session_state.gender = ""
    
if "age" not in st.session_state or recommend_type not in ["buyuser", "viewuser"]:
    st.session_state.age = ""


submit_button = None

            
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
            width: 55%;
            height: auto;
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
        st.markdown("검색 키워드 선택")
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
                            <div class="btn-content">
                                <img src="{prd_img}" />
                                <a href="https://www.halfclub.com/product/{prd_no}">{prd_no}</a>
                            </div>
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
        cols = st.columns([1.5, 8.5])
        for row in rows:
            rec = row[0]
            img_url = rec.get("prd_img", "")
            prd_nm = rec.get("prd_nm", "")
            with cols[0]:
                st.image(img_url, width=100)
            with cols[1]:
                st.markdown(prd_nm, unsafe_allow_html=True)
        # 가로선
        st.markdown("---")
    except Exception as e:
        st.error(f"이미지 표시 오류: {e}")

# 추천 결과 상품 리스트 표시
def show_grid(items, columns_per_row=5, title=None, img_width=220):
    if title:
        st.subheader(title)
    try:
        rows = [items[i: i + columns_per_row] for i in range(0, len(items), columns_per_row)]
        for row in rows:
            cols = st.columns(len(row), gap="small")
            for col, rec in zip(cols, row):
                # prd_no = rec.get("prd_no")
                # url = rec.get("prd_url")
                # score = rec.get("score")
                img_url = rec.get("prd_img")
                prd_nm = rec.get("prd_nm")
                with col:
                    if img_url:
                        # if score:
                        #     st.markdown(f"<p style='font-size:11pt;margin:0;padding:0;'>상품: <a href='{url}'>{prd_no}</a><br/>추천 스코어: {score:.3f}</p>", unsafe_allow_html=True)
                        # else:
                        #     st.markdown(f"<p style='font-size:11pt;margin:0;padding:0;'>상품: <a href='{url}'>{prd_no}</a></p>", unsafe_allow_html=True)
                        st.image(img_url, width=img_width)
                        st.markdown(prd_nm, unsafe_allow_html=True)
                    else:
                        continue
        # 가로선
        st.markdown("---")
    except Exception as e:
        return

# 추천 조회
def submit():
    # 추천 서비스 유형 선택
    if not select_type:
        return
    # 상품 번호 입력
    if not select_prd_no:
        return
    
    try:
        global recommend_type, gender, age
        selected_gender = ""
        selected_age = ""
        if recommend_type in ["viewtogether", "buytogether"]:
            if not gender and st.session_state.gender:
                gender = st.session_state.gender
            if gender:
                for item in gender_options:
                    if item == gender:
                        selected_gender = gender_options[item]
                        break
            if not age and st.session_state.age:
                age = st.session_state.age
            if age:
                for item in age_options:
                    if item == age:
                        selected_age = age_options[item]
                        break
            if gender and age:
                if recommend_type in ["viewtogether"]:
                    recommend_type = "viewuser"
                elif recommend_type in ["buytogether"]:
                    recommend_type = "buyuser"
                params = dict(
                    prd_no=int(select_prd_no),
                    age=selected_age,
                    gender=selected_gender,
                    # self_yn=bool(self_yn),
                    size=int(k)
                )
            else:
                params = dict(
                    prd_no=int(select_prd_no),
                    size=int(k)
                )
        elif recommend_type in ["keyword-search"]:
            if st.session_state.gender:
                gender = st.session_state.gender
            else:
                gender = ""
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
        else:
            params = dict(
                prd_no=int(select_prd_no),
                size=int(k)
            )
        response = requests.get(f"{API_URL}/{recommend_type}", params=params)
        response.raise_for_status()
        data = response.json()
        
        # 추천 대상 상품 표시
        if recommend_type in ["keyword-search"]:
            if gender:
                st.subheader(f"검색 키워드: {select_prd_no} ({gender})")
            else:
                st.subheader(f"검색 키워드: {select_prd_no}")
            # 가로선
            st.markdown("---")
        else:
            prd_no_list = []
            if "prd_no_list" in data:
                prd_no_list = data.get("prd_no_list", [])
            elif "prd_no" in data:
                prd_no_list.append(data.get("prd_no"))
            if not prd_no_list:
                st.error("결과 없음")
            else:
                ori_prd_list = []
                for resp_prd_no in prd_no_list:
                    ori_img_resp = http.request(
                        "GET",
                        f"http://hapix.halfclub.com/searches/prdList/?keyword={resp_prd_no}&siteCd=1&device=mc",
                    )
                    if ori_img_resp.status == 200:
                        try:
                            j = ori_img_resp.json()
                            resp_data = j["data"]["result"]["hits"]["hits"][0]["_source"]
                            prdNo = resp_data.get("prdNo", "")
                            prdNm = resp_data.get("prdNm", "")
                            dcPrc = resp_data.get("dcPrcMc", 0)
                            imgUrl = resp_data.get("appPrdImgUrl", "")
                            brandNm = resp_data.get("brandNm", "")
                            prdUrl = f"https://www.halfclub.com/product/{prdNo}"
                            
                            text = ""
                            if len(prd_no_list) > 1:
                                text = text + "<p style='font-size:10pt;margin:0;padding:0;'>"
                            text = text + f"브랜드 : {brandNm}<br/>"
                            text = text + f"상 품 : <a href='https://www.halfclub.com/product/{prdNo}'>{prdNo}</a><br/>"
                            text = text + f"가 격 : {dcPrc:,}<br/>"
                            if len(prd_no_list) > 1:
                                text = text + f"상품명 :<br/>{prdNm}<br/>"
                            else:
                                text = text + f"상품명 : {prdNm}<br/>"
                                
                            if age or gender:
                                text = text + f"<br/>"
                                if age:
                                    text = text + f" ■ 선택 나이 : {age}<br/>"
                                if gender:
                                    text = text + f" ■ 선택 성별 : {gender}<br/>"
                            if len(prd_no_list) > 1:
                                text = text + f"</p><br/>"
                            
                            ori_prd_list.append({
                                "prd_no": prdNo
                                , "score": 0
                                , "prd_nm": text
                                , "prd_url": prdUrl
                                , "prd_img": imgUrl
                            })
                        except Exception as ex:
                            continue
                if ori_prd_list:
                    if len(ori_prd_list) == 1:
                        show_target(ori_prd_list, columns_per_row=1, title="추천 대상 상품")
                    else:
                        show_grid(ori_prd_list, columns_per_row=5, title="추천 대상 상품", img_width=130)
                
        # 추천 상품 이미지 및 점수
        recs = []
        recs_title = "추천 결과 상품 리스트"
        ml_type = ""
                
        ml_data = []
        if recommend_type in ["keyword-search"]:
            ml_data = data
        else:
            ml_data = data.get("result", [])
            ml_type = data.get("ml_type", [])
            if ml_type:
                if ml_type == "ml":
                    recs_title = recs_title + f": {recommend_type_nm} ML"
                            
        for rec in ml_data:
            if recommend_type in ["keyword-search"]:
                prd_no = rec.get("prd_no")
                score = rec.get("score", 0.0)
                prd_nm = rec.get("prd_nm")
                prd_img = rec.get("prd_img")
                prc = rec.get("price")
                brandNm = rec.get("brandNm", "")
            else:
                prd_no = rec.get("prdNo")
                score = rec.get("score", 0.0)
                prd_nm = rec.get("prdNm")
                prd_img = rec.get("appPrdImgUrl")
                prc = rec.get("dcPrcMc")
                brandNm = rec.get("brandNm", "")
                
                        
            text = ""
            
            # 추천 정보 표시
            if rec.get("rcm_prd_no", ""):
                text = text + f"<p style='font-size:9pt;margin:0;padding:0;'>"
                text = text + f"추천 대상: {rec.get("rcm_prd_no", "")}<br/>"
                text = text + f"</p>"
            if rec.get("age", ""):
                for item in age_options:
                    if age_options[item] == rec.get("age", ""):
                        text = text + f"<p style='font-size:9pt;margin:0;padding:0;'>"
                        text = text + f"■ 나이: {item}<br/>"
                        text = text + f"</p>"
                        break
            if rec.get("gender", ""):
                for item in gender_options:
                    if gender_options[item] == rec.get("gender", ""):
                        text = text + f"<p style='font-size:9pt;margin:0;padding:0;'>"
                        text = text + f"■ 성별: {item}<br/>"
                        text = text + f"</p>"
                        break
            
            # 상품 정보 표시
            text = text + f"<p style='font-size:10pt;margin:0;padding:0;'>"
            if score:
                text = text + f"추천 스코어 : {score:.4f}<br/>"
            text = text + f"브랜드 : {brandNm}<br/>"
            text = text + f"상 품 : <a href='https://www.halfclub.com/product/{prd_no}'>{prd_no}</a><br/>"
            text = text + f"가 격 : {prc:,} 원<br/>"
            text = text + f"상품명 :<br/>{prd_nm}<br/>"
            text = text + f"</p><br/>"
            
            recs.append({"prd_no": prd_no, "score": score, "prd_nm": text, "prd_url": "https://www.halfclub.com/product/" + str(prd_no), "prd_img": prd_img})

        if not recs:
            st.error("리스트 결과 없음")
        else:
            show_grid(recs, columns_per_row=4, title=recs_title)

    except requests.exceptions.HTTPError as http_err:
        st.error(f"HTTP 에러: {http_err}")
    except Exception as err:
        st.error(f"오류 발생: {err}")

# 폼 제출 시 API 호출 및 이미지 표시
if submit_button:
    select_prd_no = prd_no
    if recommend_type in ["buytogether","viewtogether","keyword-search"]:
        if gender:
            st.session_state.gender = gender
    if recommend_type in ["buytogether","viewtogether"]:
        if age:
            st.session_state.age = age
    if recommend_type in ["recommendforyou"]:
        if prd_no:
            st.session_state.recommendforyou = set()
            for prd in prd_no.split(","):
                st.session_state.recommendforyou.add(prd)
    submit()
elif submit:
    if recommend_type in ["keyword-search"]:
        if gender:
            st.session_state.gender = gender
    submit()


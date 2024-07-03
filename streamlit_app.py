import streamlit as st
import urllib3
import json

# test url : https://omnicommerce-ktweaetjdkpsnzchqx2dr8.streamlit.app
# https://wschoi-test1-s9z9dkk1uh.streamlit.app/
# 실행 : streamlit run ./api/recommendation.py
# 심각 : 356049403

comtype = st.radio(
    "조회 구분",
    ["소량재고","유사상품 추천","개인화 추천"]
)

if comtype == "유사상품 추천":
    placetext = "상품"
elif comtype == "개인화 추천":
    placetext = "회원"
else:
    placetext = "소량재고"

prd_no = ""
if comtype != "소량재고":
    prd_no = st.text_input("상품 추천 TEST", placeholder=placetext + "번호를 입력하세요").strip()
    st.write("입력된 " +placetext+ "번호 : ", prd_no)

try:
    http = urllib3.PoolManager()

    oriImage = ""
    url = ""
    data = {}

    if prd_no != "":
        if comtype == "유사상품 추천":
            oridata = http.request("GET", "http://apix.halfclub.com/searches/prdList/?keyword=" + prd_no + "&siteCd=1&device=mc").json()
            oriImage = oridata["data"]["result"]["hits"]["hits"][0]["_source"]["appPrdImgUrl"]
            st.image(oriImage)
            # st.markdown("""---""")

        if comtype == "유사상품 추천":
            url = "http://develop-api.halfclub.com/searches/recommProducts/?prdNo=" + prd_no
        else:
            url = "http://develop-api.halfclub.com/searches/personalProducts/?deviceID=" + prd_no
    elif comtype == "소량재고":
        url = "https://develop-api.halfclub.com/searches/lowStockProductList/"

    data = http.request("GET", url).json()
    st.markdown("""---""")
    st.text_input("Request API URL", url)
    st.markdown("""---""")

    if len(data["data"]) > 0:
        recommend_list = data["data"]
        result_container = st.container()
        link_container = st.container()
        recognition_result_container = result_container.columns(4)
        i=0
        for recommend in recommend_list:
            try:
                with recognition_result_container[i%4]:
                    st.write("상품 이동 : [" + str(recommend["prdNo"]) + "](" + str(recommend["appPrdDtlUrl"]) + ")")
                    st.image(recommend["appPrdImgUrl"], caption= str(recommend["prdNo"]) + " | "+ str(format(recommend["dcPrcApp"], ',')) + "원")
                i=i+1
            except Exception as ex:
                st.text(ex)                
        st.markdown("""---""")
        # st.json(recommend_list)
     

        
        url2 = f"https://api.kr.omnicommerce.ai/2023-02/similar-items/recommend/{prd_no}?limit=30"
        reqHeader = urllib3.HTTPHeaderDict()
        reqHeader.add("x-api-key", "FjrRJypJ7dQu2vVKJ9Z4WrcJDX4F6SFdQ8BHwjJE")
        reqHeader.add("Content-Type", "application/json")
        resp = urllib3.request(
            "GET",
            url2,
            headers=reqHeader,
        )
        st.text_input("Request API URL2", url2)
        st.json(resp)

        # respData = resp.data.decode("utf-8")
        # dataom = json.load(respData)
        # st.json(dataom.get("recommendation"))
except Exception as ex:
    st.text(ex)



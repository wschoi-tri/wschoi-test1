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
mem_no = ""
dispCtgrNo = ""
strategy = ""
strategys = ["similar-items","often-viewed-together","recommended-for-you", "popular-items", "frequently-bought-together"]
strategys_noproduct = ["often-viewed-together","recommended-for-you", "popular-items", "frequently-bought-together"]
if comtype != "소량재고":
    st.markdown("""---""")
    if comtype == "유사상품 추천":
        prd_no = st.text_input("상품번호", "354783472", placeholder=placetext + "번호를 입력하세요").strip()
        st.write("입력된 " +placetext+ "번호 : ", prd_no)
        dispCtgrNo = st.text_input("전시번호", "110", placeholder=placetext + "번호를 입력하세요").strip()
        st.write("입력된 전시번호 : ", dispCtgrNo)
    elif comtype == "개인화 추천":
        prd_no = st.text_input("상품번호", "354783472", placeholder=placetext + "번호를 입력하세요").strip()
        st.write("입력된 상품번호 : ", prd_no)
        mem_no = st.text_input("회원번호", "7614d21f100cbb15f6cad643077160c5b339b9a3c3a9eb3952782c74d8bd650f", placeholder=placetext + "번호를 입력하세요").strip()
        st.write("입력된 회원번호 : ", mem_no)
        st.markdown("""---""")
        if prd_no != "" :
            strategy = st.radio(
                "추천방법",
                strategys
            )
        else :
            strategy = st.radio(
                "추천방법",
                strategys_noproduct
            )
        st.write("선택된 추천방법 : ", strategy)

try:
    http = urllib3.PoolManager()

    oriImage = ""
    url = ""
    data = {}

    if prd_no != "":
        st.markdown("""---""")
        oridata = http.request("GET", "http://apix.halfclub.com/searches/prdList/?keyword=" + prd_no + "&siteCd=1&device=mc").json()
        oriImage = oridata["data"]["result"]["hits"]["hits"][0]["_source"]["appPrdImgUrl"]
        st.image(oriImage)
    
    if comtype == "유사상품 추천":
        if prd_no != "":
            url = f"http://develop-api.halfclub.com/searches/recommProducts/?prdNo={prd_no}&dispCtgrNo={dispCtgrNo}"
        else:
            url = f"http://develop-api.halfclub.com/searches/recommProducts/?prdNo=0&dispCtgrNo={dispCtgrNo}"
        
    if comtype == "개인화 추천":
        url = f"http://develop-api.halfclub.com/searches/recommend/?deviceID={mem_no}&prdNo={prd_no}&strategy={strategy}"

    if comtype == "소량재고":
        url = "https://develop-api.halfclub.com/searches/lowStockProductList/"

    omni_recomm_url = f"https://api.kr.omnicommerce.ai/2023-02/similar-items/recommend/{prd_no}?limit=60"

    st.markdown("""---""")
    st.text_input("Request Search API URL", url)
    st.markdown("""---""")

    data = http.request("GET", url)
    dataJson = data.json()
    if data.status >= 300:
        st.json(dataJson)

    if data.status < 300 and len(dataJson["data"]) > 0:
        recommend_list = dataJson["data"]
        result_container = st.container(border=True)
        link_container = st.container(border=True)
        recognition_result_container = result_container.columns(4)

        if prd_no != "" and comtype == "유사상품 추천":
            omni_resp = http.request(
                "GET",
                omni_recomm_url,
                headers={"x-api-key":"FjrRJypJ7dQu2vVKJ9Z4WrcJDX4F6SFdQ8BHwjJE"},
            )
            st.text(1)
            omni_respData = omni_resp.data.decode("utf-8")
            omni_data = json.loads(omni_respData)
            st.json(omni_data)
        i=0
        for recommend in recommend_list:
            try:
                with recognition_result_container[i%4]:
                    st.write("상품 이동 : [" + str(recommend["prdNo"]) + "](" + str(recommend["appPrdDtlUrl"]) + ")")
                    sScore = ""
                    if prd_no != "" and comtype == "유사상품 추천":
                        for omni_data1 in omni_data["recommendation"]:
                            if omni_data1["id"] == str(recommend["prdNo"]) :
                                sScore = " | 유사점수 : " + str(omni_data1["similarityScore"])
                    st.image(recommend["appPrdImgUrl"], caption= str(recommend["prdNo"]) + " | "+ str(format(recommend["dcPrcApp"], ',')) + "원" + sScore)
                i=i+1
            except Exception as ex:
                st.text(ex)
    
    st.markdown("""---""")
    if comtype == "개인화 추천":
        for strategy in strategys:
            url = f"https://api.kr.omnicommerce.ai/2023-06/personalization/interest/{prd_no}?deviceId={mem_no}&limit=30&strategy={strategy}&showInfo=IMAGE_INFO&showInfo=METADATA&showInfo=CONTEXT_INFO"
            st.text_input(f"개인화 추천 ({strategy})", url)
            resp = http.request(
                "GET",
                url,
                headers={"x-api-key":"gwQVGPN8hZUuUi7M7hAJYZWwy7wEPPd4Bk6GipDu"},
            )            
            respData = resp.data.decode("utf-8")
            respJson = json.loads(respData)

            if resp.status >= 300:
                st.json(respJson)
                continue

            i=0
            container = st.container(border=True)
            col_container = container.columns(4)
            for row in respJson["recommendation"]:
                try:
                    if http.request("GET", row["imageInfo"]["url"]).status == 200:
                        with col_container[i%4]:
                            st.image(row["imageInfo"]["url"], caption= str(row["id"]) + " | "+ str(format(row["metadata"]["discountPrice"], ',')) + "원")
                        i=i+1
                except Exception as ex:
                    st.text(ex)


except Exception as ex:
    st.json(ex)

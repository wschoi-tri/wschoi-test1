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
strategy = ""
if comtype != "소량재고":
    st.markdown("""---""")
    if comtype == "유사상품 추천":
        prd_no = st.text_input("상품번호", "354783472", placeholder=placetext + "번호를 입력하세요").strip()
        st.write("입력된 " +placetext+ "번호 : ", prd_no)
    elif comtype == "개인화 추천":
        prd_no = st.text_input("상품번호", "354783472", placeholder=placetext + "번호를 입력하세요").strip()
        st.write("입력된 상품번호 : ", prd_no)
        mem_no = st.text_input("회원번호", "7614d21f100cbb15f6cad643077160c5b339b9a3c3a9eb3952782c74d8bd650f", placeholder=placetext + "번호를 입력하세요").strip()
        st.write("입력된 회원번호 : ", mem_no)
        strategy = st.radio(
            "추천방법",
            ["similar-items","often-viewed-together","recommended-for-you"]
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
            url = f"http://develop-api.halfclub.com/searches/recommProducts/?prdNo={prd_no}"
        else:
            url = f"http://develop-api.halfclub.com/searches/recommend/?deviceID={mem_no}&prdNo={prd_no}&strategy={strategy}"
    elif comtype == "소량재고":
        url = "https://develop-api.halfclub.com/searches/lowStockProductList/"

    omni_recomm_url = f"https://api.kr.omnicommerce.ai/2023-02/similar-items/recommend/{prd_no}?limit=60"
        
    data = http.request("GET", url).json()
    st.markdown("""---""")
    st.text_input("Request Search API URL", url)
    if prd_no != "" and comtype == "유사상품 추천":
        st.text_input("Request Omni API URL", omni_recomm_url)
    st.markdown("""---""")

    if len(data["data"]) > 0:
        recommend_list = data["data"]
        result_container = st.container(border=True)
        link_container = st.container(border=True)
        recognition_result_container = result_container.columns(4)

        if prd_no != "" and comtype == "유사상품 추천":
            omni_resp = http.request(
                "GET",
                omni_recomm_url,
                headers={"x-api-key":"FjrRJypJ7dQu2vVKJ9Z4WrcJDX4F6SFdQ8BHwjJE"},
            )
            omni_respData = omni_resp.data.decode("utf-8")
            omni_data = json.loads(omni_respData)
            # st.json(omni_data["recommendation"])
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
        omni_pers_url = f"https://api.kr.omnicommerce.ai/2023-06/personalization/interest/{prd_no}?deviceId={mem_no}&limit=30&strategy=similar-items&showInfo=IMAGE_INFO&showInfo=METADATA&showInfo=CONTEXT_INFO"
        omni_pers_url = f"https://api.kr.omnicommerce.ai/2023-06/personalization/interest/{prd_no}?deviceId={mem_no}&limit=30&strategy=similar-items&showInfo=IMAGE_INFO&showInfo=METADATA&showInfo=CONTEXT_INFO"
        st.text_input("개인화 추천 (similar-items)", omni_pers_url)
        omni_pers_resp = http.request(
            "GET",
            omni_pers_url,
            headers={"x-api-key":"gwQVGPN8hZUuUi7M7hAJYZWwy7wEPPd4Bk6GipDu"},
        )
        omni_pers_respData = omni_pers_resp.data.decode("utf-8")
        omni_pers_data = json.loads(omni_pers_respData)

        i=0
        result_container2 = st.container(border=True)
        recognition_result_container2 = result_container2.columns(4)
        for recommend in omni_pers_data["recommendation"]:
            try:
                if http.request("GET", recommend["imageInfo"]["url"]).status == 200:
                    with recognition_result_container2[i%4]:
                        st.image(recommend["imageInfo"]["url"], caption= str(recommend["id"]) + " | "+ str(format(recommend["metadata"]["discountPrice"], ',')) + "원")
                    i=i+1
            except Exception as ex:
                st.text(ex)
        
        st.markdown("""---""")
        omni_pers_url3 = f"https://api.kr.omnicommerce.ai/2023-06/personalization/interest/{prd_no}?deviceId={mem_no}&limit=30&strategy=often-viewed-together&showInfo=IMAGE_INFO&showInfo=METADATA&showInfo=CONTEXT_INFO"
        st.text_input("개인화 추천 (often-viewed-together)", omni_pers_url3)
        omni_pers_resp3 = http.request(
            "GET",
            omni_pers_url3,
            headers={"x-api-key":"gwQVGPN8hZUuUi7M7hAJYZWwy7wEPPd4Bk6GipDu"},
        )
        omni_pers_respData3 = omni_pers_resp3.data.decode("utf-8")
        omni_pers_data3 = json.loads(omni_pers_respData3)

        i=0
        result_container3 = st.container(border=True)
        recognition_result_container3 = result_container3.columns(4)
        for recommend in omni_pers_data3["recommendation"]:
            try:
                if http.request("GET", recommend["imageInfo"]["url"]).status == 200:
                    with recognition_result_container3[i%4]:
                        st.image(recommend["imageInfo"]["url"], caption= str(recommend["id"]) + " | "+ str(format(recommend["metadata"]["discountPrice"], ',')) + "원")
                    i=i+1
            except Exception as ex:
                st.text(ex)
        
        st.markdown("""---""")
        omni_pers_url4 = f"https://api.kr.omnicommerce.ai/2023-06/personalization/interest/{prd_no}?deviceId={mem_no}&limit=30&strategy=recommended-for-you&showInfo=IMAGE_INFO&showInfo=METADATA&showInfo=CONTEXT_INFO"
        st.text_input("개인화 추천 (recommended-for-you)", omni_pers_url3)
        omni_pers_resp4 = http.request(
            "GET",
            omni_pers_url4,
            headers={"x-api-key":"gwQVGPN8hZUuUi7M7hAJYZWwy7wEPPd4Bk6GipDu"},
        )
        omni_pers_respData4 = omni_pers_resp4.data.decode("utf-8")
        omni_pers_data4 = json.loads(omni_pers_respData4)

        i=0
        result_container4 = st.container(border=True)
        recognition_result_container4 = result_container4.columns(4)
        for recommend in omni_pers_data4["recommendation"]:
            try:
                if http.request("GET", recommend["imageInfo"]["url"]).status == 200:
                    with recognition_result_container4[i%4]:
                        st.image(recommend["imageInfo"]["url"], caption= str(recommend["id"]) + " | "+ str(format(recommend["metadata"]["discountPrice"], ',')) + "원")
                    i=i+1
            except Exception as ex:
                st.text(ex)
        st.markdown("""---""")

except Exception as ex:
    st.text(ex)

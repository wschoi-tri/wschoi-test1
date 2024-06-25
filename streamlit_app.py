import streamlit as st
import urllib3

# test url : https://omnicommerce-ktweaetjdkpsnzchqx2dr8.streamlit.app
# 실행 : streamlit run ./api/recommendation.py
# 심각 : 356049403

comtype = st.radio(
    "유사상품 또는 개인화 추천을 선택하세요",
    ["유사상품 추천","개인화 추천","소량재고"]
)

if comtype == "유사상품 추천":
    placetext = "상품"
elif comtype == "개인화 추천":
    placetext = "회원"
else:
    placetext = "소량재고"

prd_no = ""
if comtype != "소량재고":
    prd_no = st.text_input("상품 추천 TEST", placeholder=placetext + "번호를 입력하세요")
    st.write("입력된 " +placetext+ "번호 : ", prd_no)


try:
    http = urllib3.PoolManager()

    oriImage = ""

    if prd_no != "":

        if comtype == "유사상품 추천":
            oridata = http.request("GET", "http://apix.halfclub.com/searches/prdList/?keyword=" + prd_no + "&siteCd=1&device=mc").json()
            oriImage = oridata["data"]["result"]["hits"]["hits"][0]["_source"]["appPrdImgUrl"]
            st.image(oriImage)
            st.markdown("""---""")

        if comtype == "유사상품 추천":
            data = http.request("GET", "http://develop-api.halfclub.com/searches/recommProducts/?prdNo=" + prd_no).json()
        else:
            data = http.request("GET", "http://develop-api.halfclub.com/searches/personalProducts/?memNo=" + prd_no).json()
        
        recommend_list = data["data"]
        #st.json(recommend_list)
        result_container = st.container()
        link_container = st.container()
        recognition_result_container = result_container.columns(4)

        i=0
        for recommend in recommend_list:
            try:
                with recognition_result_container[i%4]:
                    st.image(recommend["appPrdImgUrl"], caption= str(recommend["prdNo"]) + " | "+ str(format(recommend["dcPrcApp"], ',')) + "원")
                    with st.container():
                        st.link_button(str(recommend["prdNo"]), str(recommend["appPrdDtlUrl"]))    
                i=i+1
            except Exception as ex:
                st.text(ex)
                
        st.markdown("""---""")
        st.json(recommend_list)
    else:
        # if comtype == "유사상품 추천":
        #     oridata = http.request("GET", "http://apix.halfclub.com/searches/prdList/?keyword=" + prd_no + "&siteCd=1&device=mc").json()
        #     oriImage = oridata["data"]["result"]["hits"]["hits"][0]["_source"]["appPrdImgUrl"]
        #     st.image(oriImage)
        #     st.markdown("""---""")
        data = http.request("GET", "https://develop-api.halfclub.com/searches/lowStockProductList/").json()

        # if comtype == "유사상품 추천":
        #     data = http.request("GET", "http://develop-api.halfclub.com/searches/recommProducts/?prdNo=" + prd_no).json()
        # else:
        #     data = http.request("GET", "http://develop-api.halfclub.com/searches/personalProducts/?memNo=" + prd_no).json()
        
        recommend_list = data["data"]
        #st.json(recommend_list)
        result_container = st.container()
        link_container = st.container()
        recognition_result_container = result_container.columns(4)

        i=0
        for recommend in recommend_list:
            try:
                with recognition_result_container[i%4]:
                    st.image(recommend["appPrdImgUrl"], caption= str(recommend["prdNo"]) + " | "+ str(format(recommend["dcPrcApp"], ',')) + "원")
                    with st.container():
                        st.link_button(str(recommend["prdNo"]), str(recommend["appPrdDtlUrl"]))    
                i=i+1
            except Exception as ex:
                st.text(ex)
                
        st.markdown("""---""")
        st.json(recommend_list)

except Exception as ex:
    st.text(ex)



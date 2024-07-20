import streamlit as st
import urllib3
import json

import urllib3.util

# test url : https://omnicommerce-ktweaetjdkpsnzchqx2dr8.streamlit.app
# https://wschoi-test1-s9z9dkk1uh.streamlit.app/
# 실행 : streamlit run ./api/recommendation.py
# 심각 : 356049403

comtype = st.radio(
    "조회 구분",
    ["개인화 개편","개인화 개편 전체","소량재고","유사상품 추천","개인화 추천"]
)

if comtype == "유사상품 추천":
    placetext = "상품"
elif comtype == "개인화 추천":
    placetext = "회원"
else:
    placetext = "소량재고" 

st.markdown("""---""")
showJson = st.checkbox("Json 표시", False)
if comtype == "개인화 추천" or comtype == "개인화 개편":
    showOmni = st.checkbox("옴니 표시", True)
    showAsis = st.checkbox("자체 표시", True)

prd_no = ""
mem_no = ""
dispCtgrNo = ""
strategy = ""
strategys = [ "recommend","similar-items","often-viewed-together","recommended-for-you", "popular-items", "frequently-bought-together"]
strategysName = {
        "similar-items":"카테고리 베스트",
        "often-viewed-together":"같이 본 상품",
        "recommended-for-you":"개인화 추천",
        "popular-items":"카테고리 베스트",
        "frequently-bought-together":"같이 구매 상품",
        "recommend":"대체 없음",
}
strategys_noproduct = ["recommended-for-you", "popular-items"]
if comtype != "소량재고":
    st.markdown("""---""")
    if comtype == "유사상품 추천":
        prd_no = st.text_input("상품번호", "354783472", placeholder=placetext + "번호를 입력하세요").strip()
        st.write("입력된 " +placetext+ "번호 : ", prd_no)
        dispCtgrNo = st.text_input("전시번호", "110", placeholder=placetext + "번호를 입력하세요").strip()
        st.write("입력된 전시번호 : ", dispCtgrNo)
    elif comtype == "개인화 추천" or comtype == "개인화 개편" or comtype == "개인화 개편 전체":
        prd_no = st.text_input("상품번호", "354783472", placeholder=placetext + "번호를 입력하세요").strip()
        st.write("입력된 상품번호 : ", prd_no)
        mem_no = st.text_input("회원번호", "11876024", placeholder=placetext + "번호를 입력하세요").strip()
        st.write("입력된 회원번호 : ", mem_no)
        device_id = st.text_input("회원번호 암호화", "7614d21f100cbb15f6cad643077160c5b339b9a3c3a9eb3952782c74d8bd650f", placeholder=placetext + "번호를 입력하세요").strip()
        st.write("입력된 회원번호 암호화 : ", device_id)
        st.markdown("""---""")
        if comtype == "개인화 추천" or comtype == "개인화 개편":
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
    ori_brandCd = ""
    ori_dispCtgrNo = ""
    url = ""
    data = {}

    if prd_no != "":
        st.markdown("""---""")
        try:
            oridata = http.request("GET", "http://apix.halfclub.com/searches/prdList/?keyword=" + prd_no + "&siteCd=1&device=mc")
            oridataJson = oridata.json()
            if oridata.status >= 300 or showJson:
                st.json(json.loads(oridata.data.decode("utf-8")), expanded=False)
            oriImage = oridataJson["data"]["result"]["hits"]["hits"][0]["_source"]["appPrdImgUrl"]
            ori_brandCd = oridataJson["data"]["result"]["hits"]["hits"][0]["_source"]["brandCd"]
            ori_dispCtgrNo = oridataJson["data"]["result"]["hits"]["hits"][0]["_source"]["dpCtgrNo1"][0]
            st.image(oriImage)
        except:
            pass    
    
    if comtype == "유사상품 추천":
        if prd_no != "":
            url = f"http://hapi.halfclub.com/searches/recommProducts/?prdNo={prd_no}&dispCtgrNo={dispCtgrNo}"
        else:
            url = f"http://hapi.halfclub.com/searches/recommProducts/?prdNo=0&dispCtgrNo={dispCtgrNo}"
        
    if comtype == "개인화 추천":
        url = f"http://hapi.halfclub.com/searches/recommend/?deviceID={device_id}&memNo={mem_no}&prdNo={prd_no}&strategy={strategy}"

    if comtype == "개인화 개편":
        url = f"http://hapi.halfclub.com/searches/personalProducts/?deviceID={device_id}&memNo={mem_no}&prdNo={prd_no}&strategy={strategy}"

    if comtype == "소량재고":
        url = "https://hapi.halfclub.com/searches/lowStockProductList/"

    omni_recomm_url = f"https://api.kr.omnicommerce.ai/2023-02/similar-items/recommend/{prd_no}?limit=60"

    urls = []
    strategyList = []
    if comtype != "개인화 개편 전체":
        urls.append(url)
    else:
        if prd_no == "":
            strategyList = strategys_noproduct
        else:
            strategyList = strategys
        for strategyItem in strategyList:
            strategy = strategyItem
            url = f"http://develop-api.halfclub.com/searches/personalProducts/?deviceID={device_id}&memNo={mem_no}&prdNo={prd_no}&strategy={strategy}"
            urls.append(url)
            
    for url in urls:
        st.markdown("""---""")
        st.text_area("Request Search API URL", url)

        data = http.request("GET", url)
        dataJson = data.json()
        if data.status >= 300 or showJson:
            st.json(json.loads(data.data.decode("utf-8")), expanded=False)        
        
        try:
            getType = dataJson["getType"]
            getTypeText = f"getType : {getType}"
            reqStrategy = ""
            reqStrategyNm = ""
            for st1 in strategyList:
                if str(url).find(st1) > -1:
                    reqStrategy = st1
                    break
            if reqStrategy != "":
                getTypeText = f"strategy : {reqStrategy}, getType : {getType}"
                if getType == "self":
                    reqStrategyNm = strategysName[reqStrategy]                
                    getTypeText = f"strategy : {reqStrategy}, getType : {getType} -> 대체 : {reqStrategyNm}"

            st.info(getTypeText)
        except:
            pass

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
                omni_respData = omni_resp.data.decode("utf-8")
                omni_data = json.loads(omni_respData)
                if omni_resp.status >= 300 or showJson:
                    st.json(omni_data, expanded=False)
            
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
    
    try:
        st.info(f"showOmni : {showOmni}")
    except:
        pass
    if showOmni == True and (comtype == "개인화 추천" or comtype == "개인화 개편"):
        st.markdown("""---""")
        for strategy in strategys:
            url = f"https://api.kr.omnicommerce.ai/2023-06/personalization/interest/{prd_no}?deviceId={device_id}&limit=30&strategy={strategy}&showInfo=IMAGE_INFO&showInfo=METADATA&showInfo=CONTEXT_INFO"
            st.text_area(f"{strategy}_옴니커머스", url)
            resp = http.request(
                "GET",
                url,
                headers={"x-api-key":"gwQVGPN8hZUuUi7M7hAJYZWwy7wEPPd4Bk6GipDu"},
            )            
            respData = resp.data.decode("utf-8")
            respJson = json.loads(respData)

            if resp.status >= 300 or showJson:
                st.json(respJson, expanded=False)
            if resp.status >= 300:
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

    try:
        st.info(f"showAsis : {showAsis}")
    except:
        pass
    if showAsis == True and (comtype == "개인화 추천" or comtype == "개인화 개편"):
        st.markdown("""---""")
        targetList = []
        targetList.append(
            {
                "name":"개인화 추천 (회원기준)",
                "url":f"https://hapix.halfclub.com/display/recommend/V2/todayRecommend?memNo={mem_no}&siteCd=1&deviceCd=001&sourceCd=01&sourceDetailCd=01",
                "type":"todayRecommend",
            }
        )
        targetList.append(
            {
                "name":"같은 브랜드 베스트 상품 (상품기준)",
                "url":f"https://hapix.halfclub.com/searches/similarBestProducts/{prd_no}?interval=72&limit=15&is_brand=true&countryCd=001&langCd=001&siteCd=1&deviceCd=001&device=pc",
                "type":"similarBestProducts",
            }
        )
        targetList.append(
            {
                "name":"같은 카테고리 베스트 상품 (상품기준)",
                "url":f"https://hapix.halfclub.com/searches/similarBestProducts/{prd_no}?interval=72&limit=15&is_category=true&countryCd=001&langCd=001&siteCd=1&deviceCd=001&device=pc",
                "type":"similarBestProducts",
            }
        )
        targetList.append(
            {
                "name":"다른 고객이 같이 구매한 상품 (상품기준)",
                "url":f"https://hapix.halfclub.com/product/tTogether/tBuyTogether?productNo={prd_no}&countryCd=001&langCd=001&siteCd=1&deviceCd=003",
                "type":"tBuyTogether",
            }
        )
        targetList.append(
            {
                "name":"다른 고객이 함께 본 상품 (상품기준)",
                "url":f"https://hapix.halfclub.com/display/recommend/V1/tViewTogether?deviceCd=001&mandM=h_half_mo_seo&prdNo={prd_no}&siteCd=1",
                "type":"tViewTogether",
            }
        )

        for target in targetList:
            url = target["url"]
            name = target["name"]
            st.text_area(f"{name}_자체", url)
            resp = http.request(
                "GET",
                url,
            )            
            respData = resp.data.decode("utf-8")
            respJson = json.loads(respData)

            if resp.status >= 300 or showJson:
                st.json(respJson, expanded=False)
            if resp.status >= 300:
                continue

            i=0
            container = st.container(border=True)
            col_container = container.columns(4)

            prdList = []
            if target["type"] == "todayRecommend":
                prdList = respJson["data"]["todayRcommendPrdList"]
            elif target["type"] == "tBuyTogether":
                prdList = respJson["data"]
            elif target["type"] == "tViewTogether":
                prdList = respJson["data"]["tViewTogether"]
            else:
                prdList = respJson

            for row in prdList:
                try:
                    row_prd_no = row["prdNo"]
                    row_image_url = ""
                    if target["type"] == "todayRecommend":
                        row_image_url = row["basicExtUrl"]
                    elif target["type"] == "tBuyTogether":
                         row_image_url = "https://cdn2.halfclub.com/rimg/230x306/cover/" + row["productImage"]["basicExtNm"]
                    elif target["type"] == "tViewTogether":
                         row_image_url = "https://cdn2.halfclub.com/rimg/230x306/cover/" + row["basicExtNm"]
                    else:
                        row_image_url = row["appPrdImgUrl"]

                    if http.request("GET", row_image_url).status == 200:
                        with col_container[i%4]:
                            st.image(row_image_url, caption= str(row_prd_no))
                        i=i+1
                except Exception as ex:
                    st.text(ex)

except Exception as ex:
    st.json(ex)

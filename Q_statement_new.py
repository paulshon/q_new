import streamlit as st
import pandas as pd
import os

# 설명문 추가
st.write("""
# 생성형 AI와 인간의 창작에 관한 설문조사
아래의 표는 Q방법론(주관성연구)의   Q 표본 분류표입니다.   아래의 표를 보시면 -4는 "강한 비동의"를 나타내고, 4는 "강한 동의"를 의미합니다. 각 숫자에 해당하는 의견을 선택하여 설문에 참여해주세요. 예를 들어, -4를 선택하면 "강한 불동의", 0을 선택하면 "중립"을 의미합니다. 이러한 방식으로 당신의 의견을 선택해주세요. 
단, 여기에서 중요한 것은 아래의 칸처럼

-4는 2번
-3은 3번
-2는 4번
-1은 4번
 0 은 5번
+1은 4번
+2는 4번
+3은 3번
+4는 2번

으로  -4의 강한 비동의와  +4의 강한 동의 사이에 선택의 제한이 있습니다.  예를 들면 -4를 2번이상, -3을 3번 이상, -2를 4번이상 선택하시면 안됩니다

예를 들면 아래의 진술문에서

"AI 예술은 예술가와 함께 협력하여 예술의 다양성을 향상시킬 수 있다"에서
+4를 선택했으면

다음 진술문에서 +4를 선택할 수 있는 것은 1번 남았다는 의미입니다

또 다른 예를 들면 아래의 진술문에서
"생성형 AI로 만든 예술 작품을 구매할 의향이 있다"에서
0인 중립을 선택했으면 
다음 진술문에서 0를 선택할 수 있는 것은 4번 남았다는 의미입니다.

진술문을 체크하실때마다 자동으로 강도의 수가 줄어들게 설정되어 있습니다.

아래에서 각 진술문에 대한 응답을 선택하세요. 각 진술문은 다음과 같이 강도를 나타내는 체크박스로 표시됩니다:

- (-4) 강한 비동의
- (-3) 
- (-2) 
- (-1) 
- (0) 중립
- (1) 
- (2) 
- (3) 
- (4) 강한 동의

각 응답은 엑셀 파일로 저장됩니다. 저장된위치는 C:/Users/Public/Documents/입니다.엑셀파일은 sarangred@paran.com으로 보내시면 됩니다.
""")

# 이미지 추가
image_path = "q_st.png"
st.image(image_path, caption="Q 분류표", use_column_width=True)

st.write("""
Q 표본 분류표를 보시면 -4는 "강한 비동의"를 나타내고, 4는 "강한 동의"를 의미합니다. 
각 숫자에 해당하는 의견을 선택하여 설문에 참여해주세요. 
예를 들어, -4를 선택하면 "강한 불동의", 0을 선택하면 "중립"을 의미합니다. 
""")

# 진술문 리스트
statements = [
    "예술가는 AI의 도움을 받아 새로운 시각과 영감을 얻을 수 있으며, 이는 창의성을 촉진할 수 있다",
    # 나머지 진술문들은 생략
]

# 강도 선택 제한
limits = {-4: 2, -3: 3, -2: 4, -1: 4, 0: 5, 1: 4, 2: 4, 3: 3, 4: 2}

# Streamlit 앱 시작
def main():
    st.title("다음은 기본 정보 조사와 진술문에 대한 강도 선택입니다")

    # 사용자 정보 입력 받기
    email = st.text_input("이메일 주소를 입력하세요:")
    age = st.text_input("나이대를 입력하세요:")
    gender = st.radio("성별을 입력하세요:", ("남성", "여성"))
    occupation = st.radio("창작자인가요? 혹은 일반 직업군인가요?:", ("창작자", "일반 직업군"))
    occupation_specific = st.text_input("본인의 직업은 무엇인가요?:")
    ai_usage = st.radio("생성형 AI를 사용한 적이 있나요?:", ("있음", "없음"))

    # 디렉토리 경로
    save_directory = "C:/Users/Public/Documents/"

    responses = {}  # 사용자의 응답을 저장할 딕셔너리

    # 각 진술문에 대한 체크박스 생성
    for statement in statements:
        st.subheader(statement)
        response_selected = False
        for strength in range(-4, 5):
            if limits[strength] > 0:
                checkbox_label = f"{strength} (강한 비동의)" if strength == -4 else f"{strength} (강한 동의)" if strength == 4 else f"{strength} (중립)" if strength == 0 else str(
                    strength)
                checkbox_key = f"{statement}_{strength}"
                checkbox_value = st.checkbox(checkbox_label, key=checkbox_key)
                if checkbox_value:
                    responses[statement] = strength
                    limits[strength] -= 1
                    response_selected = True
                    break  # 하나의 강도가 선택되면 반복 중단
        if not response_selected:
            responses[statement] = "응답 없음"  # 응답이 없는 경우 처리

    if st.button("설문 제출"):
        # 설문 결과를 판다스 데이터프레임으로 변환
        df_responses = pd.DataFrame(list(responses.items()), columns=['진술문', '응답'])
        df_responses['이메일 주소'] = email
        df_responses['나이대'] = age
        df_responses['성별'] = gender
        df_responses['직업'] = occupation
        df_responses['직업(세부)'] = occupation_specific
        df_responses['생성형 AI 사용 여부'] = ai_usage

        # 엑셀 파일로 저장
        if not os.path.exists(save_directory):
            os.makedirs(save_directory)
        excel_file_path = os.path.join(save_directory, "설문_결과.xlsx")
        df_responses.to_excel(excel_file_path, index=False)
        st.success(f"설문 결과가 성공적으로 저장되었습니다: {excel_file_path}")

if __name__ == "__main__":
    main()

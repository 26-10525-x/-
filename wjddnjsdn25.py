import streamlit as st

st.set_page_config(page_title="사전 라포 & 상태 점검", page_icon="🌱", layout="centered")

# 1. 세션 상태 초기화
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'category' not in st.session_state:
    st.session_state.category = ""
if 'emotion' not in st.session_state:
    st.session_state.emotion = ""
if 'depth' not in st.session_state:
    st.session_state.depth = 50
if 'memo' not in st.session_state:
    st.session_state.memo = ""

# --- [Step 1: 메인 화면] ---
if st.session_state.step == 1:
    st.title("🌱 사전 라포 & 상태 점검")
    st.subheader("상담 전, 나를 마주하는 가장 편안한 첫걸음")
    st.info("상담을 받기 전, 무슨 말을 해야 할지 막막하셨나요? 몇 가지 질문을 통해 마음을 편안하게 정리해 보세요.")
    
    if st.button("마음 정리 시작하기"):
        st.session_state.step = 2
        st.rerun()

# --- [Step 2: 고민 카테고리 선택] ---
elif st.session_state.step == 2:
    st.write("### Step 1. 현재 가장 신경 쓰이는 고민 분야는 무엇인가요?")
    category = st.radio(
        "카테고리를 선택해 주세요.",
        ["👥 친구 및 인간관계", "🏠 가족 관계", "📚 학업 및 진로", "🧩 나 자신 (자아/감정)"],
        index=0
    )
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("이전으로"):
            st.session_state.step = 1
            st.rerun()
    with col2:
        if st.button("다음 단계로"):
            st.session_state.category = category
            st.session_state.step = 3
            st.rerun()

# --- [Step 3: 감정 카드 & 고민 깊이 선택] ---
elif st.session_state.step == 3:
    st.write("### Step 2. 지금 당신의 마음 상태를 표현해 주세요.")
    emotion = st.selectbox(
        "현재 마음 상태와 가장 가까운 카드를 선택하세요.",
        [
            "🌧️ 먹구름 - 마음이 답답하고 금방이라도 비가 내릴 것 같아요",
            "🌀 미로 - 어디로 가야 할지 길을 잃은 기분이에요",
            "🌫️ 안개 - 앞날이 불투명하고 불안해요",
            "🔋 방전된 배터리 - 아무것도 할 에너지가 남아있지 않아요",
            "🌋 화산 - 속에서 뭔가가 터질 것만 같아요"
        ]
    )
    depth = st.slider("고민의 무게감 (0: 가벼움 ~ 100: 매우 무거움)", 0, 100, 50)
    memo = st.text_area("상담사에게 미리 전하고 싶은 말이 있다면 적어주세요.", placeholder="예: 요새 잠을 잘 못 자요.")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("이전으로"):
            st.session_state.step = 2
            st.rerun()
    with col2:
        if st.button("요약서 생성하기"):
            st.session_state.emotion = emotion
            st.session_state.depth = depth
            st.session_state.memo = memo
            st.session_state.step = 4
            st.rerun()

# --- [Step 4: 고민 요약서 + 대화창] ---
elif st.session_state.step == 4:
    st.write("### 📋 나의 고민 요약서")
    
    # 상단 고정 요약 카드
    st.success(f"""
    **📌 고민 분야:** {st.session_state.category}  
    **💭 마음 상태:** {st.session_state.emotion}  
    **📊 고민의 무게감:** {st.session_state.depth} / 100  
    **✍️ 사전 메모:** {st.session_state.memo if st.session_state.memo else '작성 내용 없음'}
    """)
    
    st.divider()
    st.write("### 💬 사전 상담 대화")

    # 대화 세션 첫 시작 멘트
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant", 
                "content": f"안녕하세요! 작성해 주신 요약 내용을 잘 확인했습니다. **[{st.session_state.category}]** 고민으로 찾아오셨군요. 최근에 어떤 일 때문에 마음에 걸리셨는지 편하게 이야기해 주실 수 있으신가요?"
            }
        ]

    # 대화 내역 출력
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # 처음으로 돌아가는 버튼
    if st.button("처음으로 돌아가기"):
        st.session_state.step = 1
        if "messages" in st.session_state:
            del st.session_state.messages
        st.rerun()

# --- [대화 처리 엔진] ---
if st.session_state.step == 4:
    if user_input := st.chat_input("하고 싶은 말을 입력해 주세요..."):
        st.session_state.messages.append({"role": "user", "content": user_input})
        text = user_input.strip()
        
        # 1. 단답형 키워드 정확한 일치 검사
        if text in ["어떻게", "해결방법", "치료", "조언", "방법"]:
            reply = "당장 혼자 해결하려고 애쓰기보다는 상처받은 내 마음을 먼저 다독여 주는 게 중요해요. 지금 일어난 상황들을 하나씩 차근차근 이야기 나누어 볼까요, 아니면 먼저 마음을 정돈할 시간이 필요하신가요?"

        # 2. 사생활 / 폰검사 / 감시 관련 공감 (추가된 부분)
        elif any(w in text for w in ["폰검사", "핸드폰 검사", "휴대폰 검사", "훔쳐", "감시", "사생활", "일기", "비밀"]):
            reply = "내 개인적인 공간이나 사생활을 침해당해서 마음이 정말 당황스럽고 상처받았을 것 같아요... 속상하고 억울한 마음이 컸을 텐데, 그 소중한 마음은 상담 선생님께 잘 전달해 드릴게요."

        # 3. 인사
        elif any(w in text for w in ["안녕", "하이", "반가"]):
            reply = "안녕하세요! 오늘 선택하신 고민에 대해 편하게 이야기 나누어 보아요. 최근 어떤 일 때문에 마음이 무거우셨나요?"

        # 4. 다툼 / 싸움 / 갈등
        elif any(w in text for w in ["싸움", "싸웠", "싸우", "때렸", "때리", "맞았", "욕했", "괴롭", "다퉜"]):
            if any(w in text for w in ["부모", "엄마", "아빠", "가족", "동생", "형", "누나", "언니"]):
                reply = "가족과 다투거나 갈등이 있으셨군요... 가족과의 일은 마음이 더 복잡하고 상처도 깊을 텐데, 그때 마음이 많이 속상하거나 슬프셨나요?"
            elif any(w in text for w in ["친구", "애들", "지인"]) or "친구" in st.session_state.category:
                reply = "친구들과 다투거나 마찰이 있으셨군요... 가까운 사람과 다투고 나면 마음도 상하고 생각이 많아지는데, 그 과정에서 마음이 많이 속상하셨나요?"
            else:
                reply = "누군가와 다투거나 갈등이 있으셨군요... 다투고 나면 마음이 정말 복잡하고 힘들었을 텐데, 그때 마음이 많이 속상하셨나요?"

        # 5. 문장형 해결/조언/치료 문의
        elif any(w in text for w in ["해결", "어쩌지", "어떡해", "꿀팁", "팁"]):
            reply = "당장 혼자 해결하려고 애쓰기보다는 상처받은 내 마음을 먼저 다독여 주는 게 중요해요. 지금 일어난 상황들을 하나씩 차근차근 이야기 나누어 볼까요, 아니면 먼저 마음을 정돈할 시간이 필요하신가요?"

        # 6. 대화 지속 요청
        elif any(w in text for w in ["차근차근", "이야기 나누", "이야기해", "이야기하자", "얘기하", "얘기자", "대화하"]):
            reply = "좋아요. 마음을 열고 이야기해 주셔서 감사해요. 지금 가장 마음을 무겁게 만들고 있는 일부터 하나씩 편하게 털어놓아 주시겠어요?"

        # 7. 감정 표현
        elif any(w in text for w in ["슬프", "슬퍼", "슬펐", "속상", "아파", "화났", "화나", "억울", "무서", "눈물", "힘들"]):
            reply = "얼마나 마음이 슬프고 속상하셨을지 충분히 이해해요... 혼자 속으로 그 감정을 참느라 정말 힘들었을 것 같아요. 이야기해 주신 마음은 본 상담 때 선생님께서 따뜻하게 보듬어 주실 수 있도록 잘 기록해 둘게요."

        # 8. 혼잣말 / 되묻기 / 의문 표현
        elif any(w in text for w in ["그런가", "그럴까", "글쎄", "맞나"]):
            reply = "생각이 복잡해서 마음을 정하기 어려우실 수 있어요. 어떤 점이 가장 걱정되시는지 부담 없이 편하게 말씀해 주셔도 괜찮습니다."

        # 9. 사용자 의사 결정 ("마음정리" 관련)
        elif any(w in text for w in ["마음정리", "정리가 될", "정리할래", "정리가 필요", "정리 될", "정리 같아", "정리 같아요", "될 것 같"]):
            reply = "내 마음을 먼저 차분하게 정리해 보는 것은 정말 좋은 선택이에요. 나눠주신 이야기와 현재 마음 상태는 본 상담 때 상담사 선생님과 함께 따뜻하게 다독여 나가실 수 있도록 잘 전달해 두겠습니다."

        # 10. 말물꼬 틔우기
        elif text in ["있잖아", "저기", "그게", "음", "저기요", "있지"]:
            reply = "네, 들을 준비가 되어 있어요. 편안하게 무슨 일이 있었는지 이야기해 주셔도 괜찮아요."

        # 11. 간단한 수긍
        elif text in ["네", "응", "알겠어", "그래", "오케이", "ㅇㅇ"]:
            reply = "네, 편안하게 마음속 이야기를 계속 이어가 주시면 됩니다."

        # 12. 기타 일반 입력 시
        else:
            reply = "솔직하게 이야기를 나누어 주셔서 감사해요. 전해 주신 내용을 바탕으로 본 상담에서 상담 선생님과 더 따뜻하고 깊은 대화를 나누실 수 있도록 잘 기록해 두겠습니다."

        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.rerun()
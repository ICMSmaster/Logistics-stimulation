import streamlit as st
import hashlib
import random
import time
import pandas as pd

# -----------------------------
# 페이지 설정 (고급 UI)
# -----------------------------
st.set_page_config(
    page_title="Logistics Blockchain Simulator",
    page_icon="🚚",
    layout="wide"
)

# -----------------------------
# 로그인 상태 관리
# -----------------------------
if "login" not in st.session_state:
    st.session_state.login = False

if "admin" not in st.session_state:
    st.session_state.admin = False

# -----------------------------
# 로그인 화면
# -----------------------------
if not st.session_state.login:

    st.markdown("""
    # 🎮 Logistics System Login
    ### 가상 물류 기업 시뮬레이터 접속
    """)

    id_input = st.text_input("ID")
    pw_input = st.text_input("Password", type="password")

    if st.button("접속"):
        if id_input == "jinhaeh" and pw_input == "jinhaeh123!!":
            st.session_state.login = True
            st.success("접속 성공")
            st.rerun()
        else:
            st.error("ID 또는 PW 오류")

    st.stop()

# -----------------------------
# 관리자 페이지
# -----------------------------
with st.sidebar:
    st.markdown("## ⚙ 관리자 모드")

    admin_pw = st.text_input("관리자 비밀번호", type="password")

    if admin_pw == "0524":
        st.session_state.admin = True
        st.success("관리자 활성화")

# 관리자 설정 변수
difficulty = 3
reward_multiplier = 1.0

if st.session_state.admin:
    st.sidebar.markdown("### 🔧 관리자 설정")
    difficulty = st.sidebar.slider("채굴 난이도", 2, 5, 3)
    reward_multiplier = st.sidebar.slider("보상 배율", 0.5, 2.0, 1.0)

# -----------------------------
# 블록체인
# -----------------------------
class Block:
    def __init__(self, index, transactions, prev_hash):
        self.index = index
        self.transactions = transactions
        self.prev_hash = prev_hash
        self.nonce = 0
        self.hash = self.mine_block()

    def calculate_hash(self):
        data = str(self.index) + str(self.transactions) + str(self.prev_hash) + str(self.nonce)
        return hashlib.sha256(data.encode()).hexdigest()

    def mine_block(self):
        prefix = "0" * difficulty
        while True:
            hash_val = self.calculate_hash()
            if hash_val.startswith(prefix):
                return hash_val
            self.nonce += 1

class Blockchain:
    def __init__(self):
        self.chain = [Block(0, [], "0")]

    def add_block(self, tx):
        prev = self.chain[-1]
        block = Block(len(self.chain), tx, prev.hash)
        self.chain.append(block)
        return block

# -----------------------------
# 상태 저장
# -----------------------------
if "coins" not in st.session_state:
    st.session_state.coins = 1000
    st.session_state.trucks = 1
    st.session_state.delivery = 0

# -----------------------------
# 상단 UI
# -----------------------------
st.markdown("""
# 🎮 Logistics Blockchain Game
### 연구 + 게임 통합 시뮬레이션
""")

mode = st.radio("모드 선택", ["🎮 게임 모드", "📊 연구 모드"])

# -----------------------------
# 게임 모드
# -----------------------------
if mode == "🎮 게임 모드":

    st.markdown("## 🏬 물류 운영")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("📦 주문 생성"):
            st.session_state.coins += 50
            st.success("+50 코인")

        if st.button("🚚 배송 실행"):
            reward = random.randint(50, 150) * reward_multiplier
            st.session_state.coins += int(reward)
            st.session_state.delivery += 1
            st.success(f"배송 완료 +{int(reward)}")

    with col2:
        st.image("https://cdn-icons-png.flaticon.com/512/1995/1995470.png")

    # 상태창
    st.markdown("## 👤 회사 상태")

    c1, c2, c3 = st.columns(3)
    c1.metric("💰 코인", st.session_state.coins)
    c2.metric("🚚 트럭", st.session_state.trucks)
    c3.metric("📦 배송", st.session_state.delivery)

    # 상점
    st.markdown("## 🏪 상점")

    s1, s2 = st.columns(2)

    with s1:
        if st.button("🚚 트럭 구매 (500)"):
            if st.session_state.coins >= 500:
                st.session_state.coins -= 500
                st.session_state.trucks += 1
                st.success("구매 완료")

    with s2:
        if st.button("🚁 드론 구매 (800)"):
            if st.session_state.coins >= 800:
                st.session_state.coins -= 800
                st.success("드론 구매")

# -----------------------------
# 연구 모드
# -----------------------------
if mode == "📊 연구 모드":

    st.markdown("## 📊 시뮬레이션 분석")

    reward = st.slider("보상", 10, 100, 50)
    fee = st.slider("수수료", 0, 20, 5)

    if st.button("🚀 시뮬레이션 실행"):

        bc = Blockchain()
        times = []
        tx_count = 0

        st.markdown("## ⛏ 채굴 중")
        bar = st.progress(0)

        for i in range(100):
            time.sleep(0.01)
            bar.progress(i+1)

        for _ in range(100):
            if random.random() > fee * 0.02:
                t = 20 - reward * 0.1 + random.uniform(-2,2)
                times.append(max(1,t))
                tx_count += 1
                bc.add_block([{"amount": reward}])

        avg_time = sum(times)/len(times)

        st.markdown("## 📈 결과")

        c1, c2, c3 = st.columns(3)
        c1.metric("📦 거래 수", tx_count)
        c2.metric("🚚 평균 시간", round(avg_time,2))
        c3.metric("🔒 블록 수", len(bc.chain))

        df = pd.DataFrame(times, columns=["time"])

        st.line_chart(df)

        # 최적 보상 찾기
        rewards = list(range(10,101,10))
        result = []

        for r in rewards:
            t = 20 - r * 0.1
            result.append(t)

        best = rewards[result.index(min(result))]
        st.success(f"최적 보상: {best}")

        # CSV 다운로드
        csv = pd.DataFrame({"reward":rewards,"time":result}).to_csv(index=False)
        st.download_button("CSV 다운로드", csv, "result.csv")

        # 보고서
        st.markdown("## 📝 자동 보고서")
        report = f"""
        평균 배송 시간: {round(avg_time,2)}
        총 거래 수: {tx_count}
        최적 보상: {best}

        결론:
        보상이 증가할수록 배송 효율이 증가하며
        블록체인은 거래 신뢰성을 확보한다.
        """
        st.text_area("Report", report, height=200)
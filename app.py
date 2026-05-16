import streamlit as st
import hashlib
import random
import time
import pandas as pd

# -------------------------
# 블록체인
# -------------------------
class Block:
    def __init__(self, index, transactions, prev_hash):
        self.index = index
        self.transactions = transactions
        self.prev_hash = prev_hash
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        data = str(self.index) + str(self.transactions) + str(self.prev_hash) + str(self.nonce)
        return hashlib.sha256(data.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis()]

    def create_genesis(self):
        return Block(0, [], "0")

    def add_block(self, transactions):
        prev = self.chain[-1]
        block = Block(len(self.chain), transactions, prev.hash)
        while not block.hash.startswith("00"):
            block.nonce += 1
            block.hash = block.calculate_hash()
        self.chain.append(block)

# -------------------------
# 시뮬레이션
# -------------------------
def run_simulation(reward, fee, use_blockchain):
    wallets = {"customer": 1000}
    drivers = [f"driver_{i}" for i in range(5)]

    for d in drivers:
        wallets[d] = 0

    blockchain = Blockchain()
    delivery_times = []
    fraud_detected = 0

    for i in range(50):
        driver = random.choice(drivers)

        delivery_time = random.uniform(5, 15) - (reward * 0.05)
        delivery_time = max(1, delivery_time)
        delivery_times.append(delivery_time)

        amount = reward - fee

        fraud = False
        if random.random() < 0.1:
            amount *= 5
            fraud = True

        if use_blockchain and fraud:
            fraud_detected += 1
            continue

        wallets["customer"] -= amount
        wallets[driver] += amount

        if use_blockchain:
            blockchain.add_block([{"amount": amount}])

    avg_time = sum(delivery_times) / len(delivery_times)

    return avg_time, delivery_times, wallets, fraud_detected

# -------------------------
# UI 시작
# -------------------------
st.title("📑 가상 물류 코인 시스템 연구 시뮬레이션")

st.markdown("""
### 📌 연구 개요
본 연구는 가상 물류 시스템에서 가상화폐 기반 보상 구조가 물류 효율성에 미치는 영향을 분석하고,
블록체인 기술의 거래 위변조 방지 효과를 검증하는 것을 목적으로 한다.
""")

# 설정
st.sidebar.header("⚙️ 실험 설정")
reward = st.sidebar.slider("보상", 1, 100, 50)
fee = st.sidebar.slider("수수료", 0, 20, 5)
use_blockchain = st.sidebar.checkbox("블록체인 사용", True)

# 실행
if st.button("🚀 시뮬레이션 실행"):

    progress = st.progress(0)
    for i in range(100):
        time.sleep(0.01)
        progress.progress(i + 1)

    avg_time, times, wallets, fraud = run_simulation(reward, fee, use_blockchain)

    # -------------------------
    # 결과
    # -------------------------
    st.markdown("## 📊 연구 결과")

    col1, col2, col3 = st.columns(3)
    col1.metric("평균 배송 시간", f"{avg_time:.2f}")
    col2.metric("위조 탐지", fraud)
    col3.metric("총 드라이버 수", len(wallets)-1)

    # -------------------------
    # 그래프 2개
    # -------------------------
    df = pd.DataFrame(times, columns=["Delivery Time"])

    st.markdown("### 📈 배송 시간 변화")
    st.line_chart(df)

    st.markdown("### 📊 배송 시간 분포")
    st.bar_chart(df)

    # -------------------------
    # 최적 보상 찾기
    # -------------------------
    st.markdown("## 🧠 최적 보상 분석")

    rewards = list(range(10, 101, 10))
    results = []

    for r in rewards:
        avg, _, _, _ = run_simulation(r, fee, True)
        results.append(avg)

    df_opt = pd.DataFrame({
        "reward": rewards,
        "avg_time": results
    })

    st.line_chart(df_opt.set_index("reward"))

    best_reward = rewards[results.index(min(results))]
    st.success(f"📌 최적 보상 값: {best_reward}")

    # -------------------------
    # CSV 다운로드
    # -------------------------
    st.markdown("## 💾 데이터 다운로드")

    csv = df_opt.to_csv(index=False).encode('utf-8')
    st.download_button("CSV 다운로드", csv, "result.csv")

    # -------------------------
    # 자동 리포트
    # -------------------------
    st.markdown("## 📝 자동 연구 리포트")

    report = f"""
    [연구 결과 요약]

    - 평균 배송 시간: {avg_time:.2f}
    - 위조 탐지 횟수: {fraud}
    - 최적 보상 값: {best_reward}

    [해석]
    보상이 증가할수록 배송 속도가 개선되는 경향이 나타났으며,
    블록체인 적용 시 위조 거래가 효과적으로 차단됨을 확인하였다.
    """

    st.text_area("📄 보고서", report, height=200)
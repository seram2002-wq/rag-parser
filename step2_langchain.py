"""
실습 2: Unstructured 결과를 LangChain Document로 받습니다.
실행: python step2_langchain.py
"""
import os
from dotenv import load_dotenv
from langchain_unstructured import UnstructuredLoader

# ──────────────────────────────────────────────
# 1단계. .env 파일에서 API 키를 읽어옵니다.
#   코드에 키를 직접 쓰지 않는 것이 핵심입니다.
# ──────────────────────────────────────────────
load_dotenv()
API_KEY = os.getenv("UNSTRUCTURED_API_KEY")

# ──────────────────────────────────────────────
# 2단계. 로더를 생성합니다.
#   partition_via_api=True  → 무거운 모델을 내 PC가 아닌 서버에서 실행
#   chunking_strategy       → 제목 단위로 의미를 보존하며 자릅니다
# ──────────────────────────────────────────────
loader = UnstructuredLoader(
    file_path=["./data/sample_table.pdf"],
    api_key=API_KEY,
    url=os.getenv("UNSTRUCTURED_API_URL"), 
    partition_via_api=True,
    strategy="hi_res",
    chunking_strategy="by_title",   # 핵심 옵션
    max_characters=1500,            # 청크 최대 길이
    combine_text_under_n_chars=200, # 짧은 조각은 앞뒤와 합칩니다
)

# ──────────────────────────────────────────────
# 3단계. LangChain Document 리스트로 받습니다.
#   이 형태 그대로 Vector DB에 넣을 수 있습니다.
# ──────────────────────────────────────────────
docs = loader.load()
print(f"총 {len(docs)}개의 청크가 생성되었습니다.\n")

for i, doc in enumerate(docs[:3], start=1):
    print(f"--- 청크 {i} ---")
    print(doc.page_content[:200])
    print(f"출처: {doc.metadata.get('filename')} "
          f"{doc.metadata.get('page_number')}p\n")
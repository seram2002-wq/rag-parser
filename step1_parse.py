"""
실습 1: PDF 한 개를 Element 리스트로 분해하고 품질을 점검합니다.
실행: python step1_parse.py
"""
from collections import Counter
from unstructured.partition.auto import partition

# ──────────────────────────────────────────────
# 1단계. 문서를 Element 리스트로 분해합니다.
#   strategy  : fast / hi_res / ocr_only / auto 중 선택
#   languages : 한글 문서는 반드시 "kor"를 넣어야 합니다
# ──────────────────────────────────────────────
elements = partition(
    filename="./data/sample_table.pdf",
    strategy="hi_res",
    languages=["kor", "eng"],
    infer_table_structure=True,   # 표를 HTML 구조로 보존합니다
)

print(f"총 {len(elements)}개의 Element가 생성되었습니다.\n")

# ──────────────────────────────────────────────
# 2단계. 카테고리 분포를 확인합니다.
#   파싱 품질을 가장 빠르게 눈으로 점검하는 방법입니다.
#   UncategorizedText 비율이 높으면 파싱이 실패한 것입니다.
# ──────────────────────────────────────────────
distribution = Counter(el.category for el in elements)
for category, count in distribution.most_common():
    print(f"  {category:<20} {count}개")

# ──────────────────────────────────────────────
# 3단계. 앞 5개 Element의 내용과 출처를 확인합니다.
# ──────────────────────────────────────────────
print("\n--- 샘플 5개 ---")
for el in elements[:5]:
    preview = el.text[:50].replace("\n", " ")
    print(f"[{el.category}] {preview}")
    print(f"    출처: {el.metadata.filename} {el.metadata.page_number}p")

# ──────────────────────────────────────────────
# 4단계. 표만 골라서 HTML 구조를 확인합니다.
#   카테고리 라벨이 있어서 가능한 작업입니다.
# ──────────────────────────────────────────────
tables = [el for el in elements if el.category == "Table"]
print(f"\n표 {len(tables)}개를 찾았습니다.")
if tables:
    print(tables[0].metadata.text_as_html[:300])
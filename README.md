# 멀티모달 RAG

PDF 파싱, 요약, 다중 벡터 검색을 실험하는 프로젝트입니다.

## 설치 및 설정

1. 기존 `.venv311` 가상환경을 사용합니다. 프로젝트 폴더와 가상환경 이름은 변경하지 않습니다.
2. 의존성 패키지를 설치합니다.

   ```cmd
   .venv311\Scripts\activate.bat
   python -m pip install -r requirements.txt
   ```

3. `.env.example`을 `.env`로 복사한 뒤, 각 서비스에서 발급받은 API 키와 API URL을 입력합니다. `.env`는 Git에 커밋하지 마세요.
4. 원본 PDF를 `data/invest.pdf` 경로에 둡니다.

현재 의존성 목록에는 `src/extract.py`에서 사용하는 `langchain-unstructured`가 포함되어 있지 않습니다. 활성화된 가상환경에서 별도로 설치하세요.

```cmd
python -m pip install langchain-unstructured
```

## 다른 팀원에게 환경 전달하기

Windows CMD에서 새로 저장소를 받은 팀원은 다음 순서로 설정합니다. 저장소 주소를 실제 Git 주소로 바꿔 실행하세요.

```cmd
git clone <저장소 주소> rag-parser
cd rag-parser

python -m venv .venv311
.venv311\Scripts\activate.bat

python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install langchain-unstructured

python -m ipykernel install --user --name multimodal-rag --display-name "Python (multimodal-rag)"

copy .env.example .env
```

`.env`를 열어 실제 API 키와 API URL을 입력하세요. `.env`는 Git에 커밋하지 마세요. 가상환경 폴더와 프로젝트 폴더 이름은 이 저장소에서 사용하는 `.venv311`과 `rag-parser`를 그대로 씁니다.

## 모듈

- `src/extract.py` — Unstructured API로 PDF를 파싱해 LangChain 문서 목록으로 반환합니다.
- `src/summarize.py` — 설정된 OpenAI 채팅 모델로 문서를 요약합니다.
- `src/retriever.py` — Chroma와 OpenAI 임베딩을 사용하는 메모리 기반 다중 벡터 검색기를 생성합니다.

사용 예시:

```python
from src.extract import extract_pdf
from src.retriever import create_multi_vector_retriever
from src.summarize import summarize_documents

documents = extract_pdf("data/invest.pdf")
summary = summarize_documents(documents)
retriever = create_multi_vector_retriever(documents)
```

검색기와 원본 문서 저장소는 메모리에만 유지되며, 실행이 끝나면 저장되지 않습니다.

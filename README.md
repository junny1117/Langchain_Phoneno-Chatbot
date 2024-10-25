# Phoneno-Chatbot_Ollama_gemma2-9b
## 개요
Langchain, Ollama, Streamlit을 활용한 전화번호 정보 제공 챗봇

## 주요 기능

- 사용자가 검색한 전화번호에 대한 정보를 크롤링을 통해 수집
-  문서 유사도 파악을 통해 사용자 질문에 대한 답변 성능 향상
-  언어 모델을 사용하여 사용자의 질문의도 파악 및 자연스러운 답변 가능

## 작동 과정

1. **사용자 입력**:
   - 사용자는 전화번호와 해당 번호에 관해 궁금한 점을 입력
   - 예: 이 번호는 어디서 걸려온 번호니? 등의 질문

2. **웹 크롤링**:
   - `Selenium`을 사용하여 전화번호 정보 공유 사이트 [더콜](https://www.thecall.co.kr)에서 사용자가 입력한 전화번호 관련 정보 크롤링

3. **문서 분할**:
   - 크롤링한 데이터를 문서 형식으로 변환하여 `RecursiveCharacterTextSplitter`를 사용해 효과적으로 검색할 수 있도록 분할

4. **유사도 검색**:
   - `FAISS`를 사용해 유사도 검색 인덱스를 구축하여, 사용자 질문에 맞는 문서 검색.

5. **답변**:
   - `ChatOllama` 라이브러리 및 gemma2:9b 모델을 이용해 검색된 문서의 내용을 바탕으로 자연어로 답변을 생성.

## 사용도구/기술

- **Python**: 개발언어
- **Selenium**: 웹 크롤링
- **Streamlit**: 사용자 인터페이스
- **Langchain**: LLM 활용 애플리케이션 개발 프레임워크
- **gemma2:9b**: 언어모델
- **Visual Studio Code**: 코드 작성
- **Windows**: 운영체제

## 실행 결과 이미지
![스크린샷 2024-10-24 173259](https://github.com/user-attachments/assets/c23f5d3c-38dd-4e0b-923e-863592c03e67)
![스크린샷 2024-10-24 173349](https://github.com/user-attachments/assets/d753a5b4-9c1b-4786-afbb-8b35b958d70f)


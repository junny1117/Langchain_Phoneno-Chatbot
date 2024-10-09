import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.chat_models import ChatOllama
from langchain.chains import RetrievalQA
from langchain.schema.runnable import RunnableMap
from langchain.prompts import ChatPromptTemplate

def phoneno_info(phoneno):
    url = 'https://www.thecall.co.kr/bbs/board.php?bo_table=phone&sca=&sfl=wr_subject&stx={}&sop=and'.format(phoneno)
    options = webdriver.EdgeOptions()
    #options.add_argument("--headless")
    driver = webdriver.Edge(options=options)
    driver.get(url)
    driver.implicitly_wait(10)
    try:
        content = driver.find_element(By.XPATH, "//div[@class='article-content']/p").text
    except:
        content = "미등록 전화번호"
    driver.close()
    app_data = {
        "전화번호정보": content
    }
    return app_data

def main():
    st.title("전화번호 정보 제공 챗봇")
    phoneno = st.text_input("전화번호를 입력하세요:(예: 01012345678)", "")
    query = st.text_input("궁금한 것을 입력하세요(예: 어디 번호)", "")
    
    if st.button("제출"):
        data = phoneno_info(phoneno)

        if data == "미등록 전화번호":
            st.markdown(data)
        else:
            document = Document(page_content="\n".join([f"{key}: {str(data[key])}" for key in ['전화번호정보']]))

            text_splitter = RecursiveCharacterTextSplitter(separators=[","])
            docs = text_splitter.split_documents([document])

            embedding_function = SentenceTransformerEmbeddings(model_name="jhgan/ko-sroberta-multitask")

            db = FAISS.from_documents(docs, embedding_function)
            retriever = db.as_retriever(search_type="similarity", search_kwargs={'k': 100, 'fetch_k': 1000})
            
            if query:
                query_result = retriever.get_relevant_documents(query)

                llm = ChatOllama(model="gemma2:9b", temperature=0.3)

                template = """
                당신은 전화번호정보를 제공하는 챗봇입니다.
                친절하게 답변하세요.
                반드시 번호 관련 질문에만 답변하세요.
                Answer the question based only on the following context:
                {context}

                Question: {question}
                """
                prompt = ChatPromptTemplate.from_template(template)

                chain = RunnableMap({
                    "context": lambda x: "\n".join([doc.page_content for doc in query_result]),
                    "question": lambda x: x['question']
                }) | prompt | llm

                response = chain.invoke({'question': query})
                st.markdown(response.content)

if __name__ == "__main__":
    main()

import glob

from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

database_path = "vectorDB"

def set_vector_db():
    input_dir = 'text'
    txt_files = glob.glob(input_dir + "/*.txt")

    texts = []

    for txt_file in txt_files:
        with open(txt_file, 'r') as fopen:
            sentence = fopen.readline()
            if sentence[-2] == "?" :
                print(sentence)
                continue
            texts.append(fopen.readline())

    text_splitter = CharacterTextSplitter(chunk_size=100, chunk_overlap=10)

    chunks = text_splitter.create_documents(texts)
    print(len(chunks))
    print(chunks[0])

    embeddings_model = HuggingFaceEmbeddings(
        model_name = 'sentence-transformers/all-MiniLM-L6-v2',
        model_kwargs = {'device': 'cuda'},
        encode_kwargs = {'normalize_embeddings': False}
    )

    chromadb = Chroma.from_documents(chunks, embeddings_model, persist_directory=database_path)
    chromadb.persist()
    
    return

def retrieve(user_query):
    print(user_query)
    
    embeddings_model = HuggingFaceEmbeddings(
        model_name = 'sentence-transformers/all-MiniLM-L6-v2',
        model_kwargs = {'device': 'cuda'},
        encode_kwargs = {'normalize_embeddings': False}
    )
    
    chromadb = Chroma(embedding_function=embeddings_model, persist_directory=database_path)
    
    prompts = chromadb.similarity_search_with_score(user_query, 1)
    
    return_message = user_query
    
    if prompts[0][1] >= 0.5:
        print(prompts[0][1])
        return_message = return_message + " " + prompts[0][0].page_content
    
    # print(type(return_message))
    # print(return_message)
    
    return return_message

# run this python file only when a new vector DB is going to be set up
if __name__ == "__main__":
    set_vector_db()
    
    # test the retrieve function
    # user_query = "Tell me about leukemia."
    # retrieve(user_query)

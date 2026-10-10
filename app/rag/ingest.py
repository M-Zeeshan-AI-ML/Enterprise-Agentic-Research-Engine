from pathlib import Path
from app.rag.chroma_store import ChromaRAG
ROOT=Path(__file__).resolve().parents[2]/"sample_data"
def load():
    items=[]
    for path in ROOT.glob("*.md"):
        text=path.read_text(encoding="utf-8")
        for i in range(0,len(text),1600): items.append({"text":text[i:i+1800],"title":f"{path.stem} chunk {i//1600+1}","source":str(path),"source_type":"document"})
    return items
if __name__=="__main__": print("Indexed",ChromaRAG().add_documents(load()),"chunks")

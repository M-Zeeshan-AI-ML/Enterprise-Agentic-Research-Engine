import json
from pathlib import Path
from app.graph.builder import build_graph
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'evaluation_results'; OUT.mkdir(exist_ok=True)
def overlap(a,b):
    aw={x.lower().strip('.,:;!?()') for x in a.split() if len(x)>3}; bw={x.lower().strip('.,:;!?()') for x in b.split() if len(x)>3}; return len(aw&bw)/max(len(aw),1)
def score(item,r):
    answer=r.get('final_answer',''); topics=item.get('expected_topics',[]); hits=sum(x.lower() in answer.lower() for x in topics); relevance=hits/max(len(topics),1)
    return {'answer_relevance_proxy':round(relevance,3),'faithfulness_proxy':round(min(1,len(r.get('intermediate_findings',[]))/3),3),'context_relevance_proxy':round(overlap(item['question'],answer),3),'context_recall_proxy':round(relevance,3),'citation_quality_proxy':round(min(1,len(r.get('citations',[]))/2),3),'tool_call_correctness':1.0 if r.get('selected_tools') else 0.0}
def main():
    rows=[json.loads(x) for x in (ROOT/'evals/dataset.jsonl').read_text().splitlines() if x.strip()]; graph=build_graph(); results=[]
    for i,item in enumerate(rows):
        try:
            r=graph.invoke({'user_query':item['question'],'conversation_id':f'eval-{i}'},config={'configurable':{'thread_id':f'eval-{i}'}}); results.append({'question':item['question'],'scores':score(item,r),'status':'completed'})
        except Exception as e: results.append({'question':item['question'],'status':'error','error':str(e)})
    p=OUT/'latest.json'; p.write_text(json.dumps({'dataset_size':len(rows),'note':'Run-time proxy metrics only; no scores are pre-fabricated. Use Ragas/LangSmith for production evaluation.','results':results},indent=2)); print(p)
if __name__=='__main__': main()

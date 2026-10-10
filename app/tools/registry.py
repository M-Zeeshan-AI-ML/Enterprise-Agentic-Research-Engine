from app.tools.calculator import calculator_tool
from app.tools.retrieval import retrieval_tool
from app.tools.search import web_search_tool
from app.tools.verification import verification_tool
TOOLS=[web_search_tool,retrieval_tool,calculator_tool,verification_tool]
TOOL_MAP={t.name:t for t in TOOLS}
ALLOWED_TOOLS=set(TOOL_MAP)

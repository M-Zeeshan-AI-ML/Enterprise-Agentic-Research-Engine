from app.tools.registry import ALLOWED_TOOLS
def test_tool_allowlist(): assert {'web_search','document_retrieval','calculator','source_verification'} <= ALLOWED_TOOLS

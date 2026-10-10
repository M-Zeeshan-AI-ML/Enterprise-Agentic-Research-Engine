"""Model-provider factory for Google Gemini and OpenAI backends.

Google Gemini is the default so developers can start without an OpenAI key.
The selected provider is used for both chat completion and embeddings.
"""
from app.config.settings import get_settings

def get_llm():
    s = get_settings()
    provider = s.llm_provider.strip().lower()

    if provider == "google":
        if not s.google_api_key:
            raise RuntimeError("GOOGLE_API_KEY is required. Create a key in Google AI Studio or set LLM_PROVIDER=openai and configure OPENAI_API_KEY.")
        from langchain_google_genai import ChatGoogleGenerativeAI
        return ChatGoogleGenerativeAI(
            model=s.google_model,
            temperature=0,
            google_api_key=s.google_api_key,
        )

    if provider == "openai":
        if not s.openai_api_key:
            raise RuntimeError("OPENAI_API_KEY is required when LLM_PROVIDER=openai")
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(model=s.openai_model, temperature=0, api_key=s.openai_api_key)

    raise RuntimeError(f"Unsupported LLM_PROVIDER={s.llm_provider!r}. Choose 'google' or 'openai'.")

def get_embeddings():
    s = get_settings()
    provider = s.llm_provider.strip().lower()

    if provider == "google":
        if not s.google_api_key:
            raise RuntimeError("GOOGLE_API_KEY is required for embeddings. Create a key in Google AI Studio.")
        from langchain_google_genai import GoogleGenerativeAIEmbeddings
        return GoogleGenerativeAIEmbeddings(
            model=s.google_embedding_model,
            google_api_key=s.google_api_key,
        )

    if provider == "openai":
        if not s.openai_api_key:
            raise RuntimeError("OPENAI_API_KEY is required for embeddings when LLM_PROVIDER=openai")
        from langchain_openai import OpenAIEmbeddings
        return OpenAIEmbeddings(model=s.openai_embedding_model, api_key=s.openai_api_key)

    raise RuntimeError(f"Unsupported LLM_PROVIDER={s.llm_provider!r}. Choose 'google' or 'openai'.")

from contextlib import contextmanager
from app.config.settings import get_settings
@contextmanager
def postgres_checkpointer():
    from langgraph.checkpoint.postgres import PostgresSaver
    with PostgresSaver.from_conn_string(get_settings().langgraph_database_url) as saver:
        saver.setup()
        yield saver

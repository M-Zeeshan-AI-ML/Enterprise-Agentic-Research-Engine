import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.services.rate_limit import limiter
from app.api.routes import router
from app.api.demo import demo
from app.config.settings import get_settings
from app.database.session import Base,engine
from app.services.tracing import configure_tracing
from app.graph.builder import build_graph
from app.graph.checkpoint import postgres_checkpointer
logging.basicConfig(level=getattr(logging,get_settings().log_level.upper(),logging.INFO))
@asynccontextmanager
async def lifespan(app):
    configure_tracing(); Base.metadata.create_all(bind=engine)
    try:
        with postgres_checkpointer() as saver:
            app.state.graph=build_graph(saver); yield
    except Exception as exc:
        logging.warning('Postgres checkpointer unavailable: %s',exc); app.state.graph=build_graph(); yield
app=FastAPI(title='Enterprise Research & Decision Agent',version='1.0.0',lifespan=lifespan)
app.state.limiter=limiter
app.include_router(router,prefix=get_settings().api_prefix)
app.add_api_route('/demo',demo,methods=['GET'])
@app.get('/health')
def health(): return {'status':'ok'}
@app.get('/ready')
def ready():
    from sqlalchemy import text
    with engine.connect() as c: c.execute(text('SELECT 1'))
    return {'status':'ready'}

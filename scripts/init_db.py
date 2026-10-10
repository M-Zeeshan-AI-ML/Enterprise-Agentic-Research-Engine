from app.database.session import Base,engine
from app.database import models
if __name__=="__main__": Base.metadata.create_all(bind=engine); print("Database tables created")

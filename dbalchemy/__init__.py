from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine('postgresql://bohdankaminskyi:masterPassword@localhost:5432/ServersDB')
Session = sessionmaker(bind=engine)

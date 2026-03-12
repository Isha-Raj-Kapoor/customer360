from sqlalchemy import create_engine

def get_engine():
    engine = create_engine(
        "mysql+pymysql://root:root@localhost/customer360"
    )
    return engine
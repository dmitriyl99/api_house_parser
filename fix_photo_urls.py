from sqlalchemy import text

from app.dal.repositories import engine


with engine.connect() as connection:
    connection.execute(text("""UPDATE images SET url = REPLACE(url, ';s={width}x{height}', '')"""))


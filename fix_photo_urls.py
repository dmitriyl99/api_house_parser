from sqlalchemy import text

from app.dal.repositories import engine


with engine.connect() as connection:
    connection.execute(text("""SELECT REPLACE(images.url, ';s={width}x{height}', '')
from images
         JOIN buildings b on b.id = images.building_id
WHERE b.source = 'olx'"""))


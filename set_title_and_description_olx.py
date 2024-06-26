import requests
from app.dal.repositories import buildings as building_repository
import re


buildings = building_repository.get_olx_buildings()
clean_html_regex = re.compile('<.*?>')
print("Found", len(buildings), 'buildings')
for building in buildings:
    if building.title:
        continue
    response = requests.get(f'https://www.olx.uz/api/v1/offers/{building.olx_id}')
    if response.status_code == 410:
        continue
    if type(response.json()) is list:
        continue
    try:
        data = response.json()['data']
    except Exception:
        continue
    building_repository.set_title_and_description(
        building.id, data['title'], re.sub(clean_html_regex, '', data['description'])
    )

print("Done.")

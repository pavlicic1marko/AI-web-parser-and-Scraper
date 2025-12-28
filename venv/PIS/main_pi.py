import PIS.pks_download_all_companie_on_page

page_url_list = [
  "https://privredni-imenik.com/pretraga?keyword=&cities_id=0&category_id=8&sub_category_id=431300&page=1",
  "https://privredni-imenik.com/pretraga?keyword=&cities_id=0&category_id=8&sub_category_id=431300&page=2",
  "https://privredni-imenik.com/pretraga?keyword=&cities_id=0&category_id=8&sub_category_id=422100&page=1",
  "https://privredni-imenik.com/pretraga?keyword=&cities_id=0&category_id=8&sub_category_id=422100&page=2"
]

for page_url in page_url_list:
    PIS.pks_download_all_companie_on_page.dowload_comanoes_on_page(page_url)
import PIS.Scrap_all_companyes_on_page_of_PKS
import PIS.scrap_single_company_data
import PIS.write_data_to_file

def dowload_comanoes_on_page(root_url):
    pass

root_url = "https://privredni-imenik.com/pretraga?keyword=&cities_id=0&category_id=8&sub_category_id=431200"

company_list = PIS.Scrap_all_companyes_on_page_of_PKS.get_all_company_links(root_url)
for company_url in company_list:
    company_data = PIS.scrap_single_company_data.scrape_company(company_url)
    PIS.write_data_to_file.write_data(company_data)
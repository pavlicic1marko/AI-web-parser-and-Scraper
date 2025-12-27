import PIS.Scrap_all_companyes_on_page_of_PKS
import PIS.scrap_single_company_data

company_list = PIS.Scrap_all_companyes_on_page_of_PKS.get_all_company_links()
for company in company_list:
    print(company)

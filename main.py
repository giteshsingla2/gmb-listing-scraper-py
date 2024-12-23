from playwright.sync_api import sync_playwright
from dataclasses import dataclass, asdict, field
import pandas as pd
import argparse
import json

l1=[]
l2=[]

Name = ""
Address = ""
Website = ""
Phone_Number = ""
Reviews_Count = 0
Reviews_Average = 0
Store_Shopping = ""
In_Store_Pickup = ""
Store_Delivery = ""
Place_Type = ""
Opens_At = ""
Introduction = ""

names_list=[]
address_list=[]
website_list=[]
phones_list=[]
reviews_c_list=[]
reviews_a_list=[]
store_s_list=[]
in_store_list=[]
store_del_list=[]
place_t_list=[]
open_list=[]
intro_list=[]

def extract_data(xpath, data_list, page):
    if page.locator(xpath).count() > 0:
        data = page.locator(xpath).inner_text()
    else:
        data = ""
    data_list.append(data)

def main(search_query=None):
    global search_for
    if search_query:
        search_for = search_query

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto("https://www.google.com/maps/@32.9817464,70.1930781,3.67z?", timeout=60000)
        page.wait_for_timeout(1000)

        page.locator('//input[@id="searchboxinput"]').fill(search_for)
        page.keyboard.press("Enter")
        page.wait_for_selector('//a[contains(@href, "https://www.google.com/maps/place")]')

        page.hover('//a[contains(@href, "https://www.google.com/maps/place")]')
        
        previously_counted = 0
        while True:
            page.mouse.wheel(0, 10000)
            page.wait_for_selector('//a[contains(@href, "https://www.google.com/maps/place")]')

            current_count = page.locator('//a[contains(@href, "https://www.google.com/maps/place")]').count()
            if current_count == previously_counted:
                listings = page.locator('//a[contains(@href, "https://www.google.com/maps/place")]').all()
                print(f"Found all available listings: {len(listings)}")
                break
            else:
                previously_counted = current_count
                print(f"Currently Found: {current_count}")
       
        # scraping
        for listing in listings:
            listing.click()
            page.wait_for_selector('//div[@class="TIHn2 "]//h1[@class="DUwDvf lfPIob"]')
           
            name_xpath = '//div[@class="TIHn2 "]//h1[@class="DUwDvf lfPIob"]'
            address_xpath = '//button[@data-item-id="address"]//div[contains(@class, "fontBodyMedium")]'
            website_xpath = '//a[@data-item-id="authority"]//div[contains(@class, "fontBodyMedium")]'
            phone_number_xpath = '//button[contains(@data-item-id, "phone:tel:")]//div[contains(@class, "fontBodyMedium")]'
            reviews_count_xpath = '//div[@class="TIHn2 "]//div[@class="fontBodyMedium dmRWX"]//div//span//span//span[@aria-label]'
            reviews_average_xpath = '//div[@class="TIHn2 "]//div[@class="fontBodyMedium dmRWX"]//div//span[@aria-hidden]'
            
            info1='//div[@class="LTs0Rc"][1]'#store
            info2='//div[@class="LTs0Rc"][2]'#pickup
            info3='//div[@class="LTs0Rc"][3]'#delivery
            opens_at_xpath='//button[contains(@data-item-id, "oh")]//div[contains(@class, "fontBodyMedium")]'#time
            opens_at_xpath2='//div[@class="MkV9"]//span[@class="ZDu9vd"]//span[2]'
            place_type_xpath='//div[@class="LBgpqf"]//button[@class="DkEaL "]'#type of place
            intro_xpath='//div[@class="WeS02d fontBodyMedium"]//div[@class="PYvSYb "]'
          
            
            if page.locator(intro_xpath).count() > 0:
                Introduction = page.locator(intro_xpath).inner_text()
                intro_list.append(Introduction)
            else:
                Introduction = ""
                intro_list.append("None Found")
            
            if page.locator(reviews_count_xpath).count() > 0:
                temp = page.locator(reviews_count_xpath).inner_text()
                temp=temp.replace('(','').replace(')','').replace(',','')
                Reviews_Count=int(temp)
                reviews_c_list.append(Reviews_Count)
            else:
                Reviews_Count = ""
                reviews_c_list.append(Reviews_Count)

            if page.locator(reviews_average_xpath).count() > 0:
                temp = page.locator(reviews_average_xpath).inner_text()
                temp=temp.replace(' ','').replace(',','.')
                Reviews_Average=float(temp)
                reviews_a_list.append(Reviews_Average)
            else:
                Reviews_Average = ""
                reviews_a_list.append(Reviews_Average)


            if page.locator(info1).count() > 0:
                temp = page.locator(info1).inner_text()
                temp=temp.split('·')
                check=temp[1]
                check=check.replace("\n","")
                if 'shop' in check:
                    Store_Shopping=check
                    store_s_list.append("Yes")
                elif 'pickup' in check:
                    In_Store_Pickup=check
                    in_store_list.append("Yes")
                elif 'delivery' in check:
                    Store_Delivery=check
                    store_del_list.append("Yes")
            else:
                Store_Shopping = ""
                store_s_list.append("No")

            if page.locator(info2).count() > 0:
                temp = page.locator(info2).inner_text()
                temp=temp.split('·')
                check=temp[1]
                check=check.replace("\n","")
                if 'pickup' in check:
                    In_Store_Pickup=check
                    in_store_list.append("Yes")
                elif 'shop' in check:
                    Store_Shopping=check
                    store_s_list.append("Yes")
                elif 'delivery' in check:
                    Store_Delivery=check
                    store_del_list.append("Yes")
            else:
                In_Store_Pickup = ""
                in_store_list.append("No")
            
            if page.locator(info3).count() > 0:
                temp = page.locator(info3).inner_text()
                temp=temp.split('·')
                check=temp[1]
                
                check=check.replace("\n","")
                # l1.append(check)
                if 'Delivery' in check:
                    Store_Delivery=check
                    store_del_list.append("Yes")
                elif 'pickup' in check:
                    In_Store_Pickup=check
                    in_store_list.append("Yes")
                elif 'shop' in check:
                    Store_Shopping=check
                    store_s_list.append("Yes")
            else:
                # l1.append("")
                Store_Delivery = ""
                store_del_list.append("No")
            

            if page.locator(opens_at_xpath).count() > 0:
                opens = page.locator(opens_at_xpath).inner_text()
                
                opens=opens.split('⋅')
                
                if len(opens)!=1:
                    opens=opens[1]
               
                else:
                    opens = page.locator(opens_at_xpath).inner_text()
                    # print(opens)
                opens=opens.replace("\u202f","")
                Opens_At=opens
                open_list.append(Opens_At)
               
            else:
                Opens_At = ""
                open_list.append(Opens_At)
            if page.locator(opens_at_xpath2).count() > 0:
                opens = page.locator(opens_at_xpath2).inner_text()
                
                opens=opens.split('⋅')
                opens=opens[1]
                opens=opens.replace("\u202f","")
                Opens_At=opens
                open_list.append(Opens_At)

            extract_data(name_xpath, names_list, page)
            extract_data(address_xpath, address_list, page)
            extract_data(website_xpath, website_list, page)
            extract_data(phone_number_xpath, phones_list, page)
            extract_data(place_type_xpath, place_t_list, page)
  
        # Create a list to store all results
        results = []
        for i in range(len(names_list)):
            result = {
                "id": i + 1,
                "name": names_list[i],
                "website": website_list[i],
                "introduction": intro_list[i],
                "phone_number": phones_list[i],
                "address": address_list[i],
                "review_count": reviews_c_list[i],
                "average_review": reviews_a_list[i],
                "store_shopping": store_s_list[i],
                "in_store_pickup": in_store_list[i],
                "delivery": store_del_list[i],
                "type": place_t_list[i],
                "opens_at": open_list[i]
            }
            results.append(result)

        # Create the final JSON structure
        json_output = {
            search_for: {
                "results": results
            }
        }

        # Save to JSON file
        with open('results.json', 'w', encoding='utf-8') as f:
            json.dump(json_output, f, indent=2, ensure_ascii=False)

        browser.close()
        print(f"Successfully scraped {len(results)} results and saved to results.json")



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--search", type=str)
    args = parser.parse_args()

    if args.search:
        search_for = args.search
    else:
        search_for = "turkish stores in toronto Canada"

    main()

import os
from typing import Dict, List

import requests
from bs4 import BeautifulSoup


def parse_search_list(
    url: str, basic_info_list: List[Dict[str, str]]
) -> List[Dict[str, str]]:
    list_page = BeautifulSoup(requests.get(url).content, "html.parser")
    for unit in list_page.find_all("h2", class_="property_unit-title"):
        basic_info_list.append(
            parse_basic_info(os.environ["ORIGIN"] + unit.find("a").get("href"))
        )
    for pagination in list_page.find("div", class_="pagination_set").find_all("a"):
        if "次へ" in pagination.text:
            return parse_search_list(
                os.environ["ORIGIN"] + pagination.get("href"), basic_info_list
            )
    return basic_info_list


def parse_basic_info(url: str) -> Dict[str, str]:
    unit_page = BeautifulSoup(requests.get(url).content, "html.parser")
    main_contents = unit_page.find("div", id="mainContents")
    for section in main_contents.find_all("div", class_="section_h2"):
        if "物件概要" in section.find("button").text:
            break
    basic_info = {"URL": url}
    for th, td in zip(section.find_all("th"), section.find_all("td")):
        key = th.get_text(strip=True).replace("ヒント", "")
        value = td.get_text(strip=True)
        basic_info[key] = value
    return basic_info

import os
from typing import Dict, List, Optional

import requests
from bs4 import BeautifulSoup, Tag


def parse_search_list(
    url: str, basic_info_list: List[Dict[str, str]]
) -> List[Dict[str, str]]:
    list_page = BeautifulSoup(requests.get(url).content, "html.parser")
    for unit in list_page.find_all("h2", class_="property_unit-title"):
        basic_info_list += parse_detail(
            os.environ["ORIGIN"] + unit.find("a").get("href")
        )
    for pagination in list_page.find("div", class_="pagination_set").find_all("a"):
        if "次へ" in pagination.text:
            return parse_search_list(
                os.environ["ORIGIN"] + pagination.get("href"), basic_info_list
            )
    return basic_info_list


def parse_detail(url: str) -> List[Dict[str, str]]:
    detail_page = BeautifulSoup(requests.get(url).content, "html.parser")
    main_contents = detail_page.find("div", id="mainContents")
    summary = parse_summary(url, main_contents)
    layouts = parse_layouts(main_contents)
    return [layout | summary for layout in layouts]


def parse_summary(url: str, main_contents: Tag) -> Dict[str, str]:
    option_summary: Optional[Tag] = None
    for div_tag in main_contents.find_all("div", class_="section_h2"):
        if "物件概要" in div_tag.find("button").text:
            option_summary = div_tag
            break
    if option_summary is None:
        raise RuntimeError("Summary is None.")
    summary: Tag = option_summary
    result = {"URL": url}
    for th, td in zip(summary.find_all("th"), summary.find_all("td")):
        key = th.get_text(strip=True).replace("ヒント", "")
        value = (
            td.get_text(strip=True)
            .replace("[乗り換え案内]", "/")
            .replace("[□支払シミュレーション]", "")
        )
        result[key] = value
    return result


def parse_layouts(main_contents: Tag) -> List[Dict[str, str]]:
    layout = None
    for div_tag in main_contents.find_all("div", class_="mt20"):
        h3_tag = div_tag.find("h3")
        if h3_tag and "間取り図" in h3_tag:
            layout = div_tag
            break
    if not layout:
        return [{}]
    results = []
    for li in layout.find_all("li"):
        result = {}
        result["name"] = li.find("div", class_="icLoupeSide").get_text(strip=True)
        for dt, dd in zip(li.find_all("dt"), li.find_all("dd")):
            key = dt.get_text(strip=True).replace("\r\n", "").replace("\t", "")
            value = (
                dd.get_text(strip=True)
                .replace("\r\n", "")
                .replace("\t", "")
                .replace("：", "")
            )
            result[f"{key}_"] = value
        results.append(result)
    return results

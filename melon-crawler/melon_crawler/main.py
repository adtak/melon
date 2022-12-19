import datetime as dt
import os

import pandas as pd
from dotenv import load_dotenv

from melon_crawler.page import parse_search_list


def main() -> None:
    basic_info_list = parse_search_list(os.environ["REQUEST_URL"], [])
    today = dt.date.today().isoformat()
    df = pd.DataFrame(basic_info_list)
    df.to_csv(f"data/raw_data_{today}.csv", index=False)
    concat_original_data(df)


def concat_original_data(latest_data: pd.DataFrame) -> None:
    original_data = pd.read_csv("data/raw_data.csv", dtype="str")
    df = pd.concat(
        [latest_data, original_data],
        axis=0,
    ).drop_duplicates(subset=["URL", "name"], keep="first")
    df.to_csv("data/raw_data.csv", index=False)


if __name__ == "__main__":
    load_dotenv(".env")
    main()

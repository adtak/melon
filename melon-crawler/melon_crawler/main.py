import os

import pandas as pd
from dotenv import load_dotenv

from melon_crawler.page import parse_search_list


def main() -> None:
    basic_info_list = []
    parse_search_list(os.environ["REQUEST_URL"], basic_info_list)
    pd.DataFrame(basic_info_list).to_csv("raw_data.csv", index=False)


if __name__ == "__main__":
    load_dotenv(".env")
    main()

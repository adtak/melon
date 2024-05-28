import { Handler } from "aws-lambda";

import axios, { AxiosResponse } from "axios";
import * as cheerio from "cheerio";

export const handler: Handler = async (event, context) => {
  const url = "";
  console.log(`url: ${url}`);
  try {
    const res: AxiosResponse = await axios.get(url);
    const $ = cheerio.load(res.data);
    const span = $("span").filter((_, element) => {
      return $(element).text().includes("カートに追加する");
    });
    if (span.text()) {
      console.log("in stock");
    } else {
      console.log("sold out");
    }
  } catch (e) {
    if (axios.isAxiosError(e)) {
      console.log(e.message);
    } else {
      console.log("unknown error");
    }
  }
};

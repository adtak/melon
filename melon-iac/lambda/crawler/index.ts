import "dotenv/config";
import { Handler } from "aws-lambda";
import axios, { AxiosResponse } from "axios";
import * as cheerio from "cheerio";

export const handler: Handler = async (event, context) => {
  const urlT = process.env.SITE_T;
  if (!urlT) {
    throw new Error("urlT is undefined.");
  }
  console.log(`url: ${urlT}`);
  try {
    const res: AxiosResponse = await axios.get(urlT);
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

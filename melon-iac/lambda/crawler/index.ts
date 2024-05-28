import { Handler } from "aws-lambda";

import axios, { AxiosResponse } from "axios";
import * as cheerio from "cheerio";

export const handler: Handler = async (event, context) => {
  const url = "https://www.google.com";
  console.log(`url: ${url}`);
  try {
    const res: AxiosResponse = await axios.get(url);
    const $ = cheerio.load(res.data);
    const title = $("title").text();
    console.log(`title: ${title}`);
  } catch (e) {
    if (axios.isAxiosError(e)) {
      console.log(e.message);
    } else {
      console.log("unknown error");
    }
  }
};

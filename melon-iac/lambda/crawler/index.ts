import { Handler } from "aws-lambda";

import axios, { AxiosError, AxiosResponse } from "axios";
import * as cheerio from "cheerio";

export const handler: Handler = async (event, context) => {
  const url = "https://www.google.com";
  console.log(url);
  axios
    .get(url)
    .then((res: AxiosResponse) => {
      const { data } = res;
      const $ = cheerio.load(data);
      const title = $("title").text();
      console.log(title);
    })
    .catch((e: AxiosError) => {
      console.log(e.message);
    });
};

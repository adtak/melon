import "dotenv/config";
import { Handler } from "aws-lambda";
import { SNS } from "aws-sdk";
import axios, { AxiosResponse } from "axios";
import * as cheerio from "cheerio";

const sns = new SNS();

export const handler: Handler = async (event, context) => {
  const snsTopicArn = process.env.SNS_TOPIC_ARN;
  const urlT = process.env.SITE_T;
  if (!urlT) {
    throw new Error("urlT is undefined.");
  }
  const instockUrls = [];

  const instockUrl = await crawlSpan(urlT);
  if (instockUrl) {
    instockUrls.push(instockUrl);
  }

  for (const url of instockUrls) {
    const params = {
      TopicArn: snsTopicArn,
      Subject: "[Melon] In Stock",
      Message: `URL: ${url}`,
    };
    await sns.publish(params).promise();
  }
};

const crawlSpan = async (url: string) => {
  console.log(`Crawling span tag. URL: ${url}`);
  const res: AxiosResponse = await axios.get(url);
  const $ = cheerio.load(res.data);
  const span = $("span").filter((_, element) => {
    return $(element).text().includes("カートに追加する");
  });
  if (span.text()) {
    console.log("in stock");
    return url;
  } else {
    console.log("sold out");
    return undefined;
  }
};

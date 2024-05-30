import "dotenv/config";
import { Handler } from "aws-lambda";
import { SNS } from "aws-sdk";
import axios, { AxiosResponse } from "axios";
import * as chardet from "chardet";
import * as cheerio from "cheerio";
import * as iconv from "iconv-lite";

const sns = new SNS();

export const handler: Handler = async (event, context) => {
  const snsTopicArn = process.env.SNS_TOPIC_ARN;
  const instockUrls = [];

  const urlT = process.env.SITE_T;
  if (urlT) {
    const instockUrl = await crawlSpan(urlT);
    if (instockUrl) {
      instockUrls.push(instockUrl);
    }
  }
  const urlK = process.env.SITE_K;
  if (urlK) {
    const instockUrl = await crawlButton(urlK);
    if (instockUrl) {
      instockUrls.push(instockUrl);
    }
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

const crawlButton = async (url: string) => {
  console.log(`Crawling button tag. URL: ${url}`);
  const res: AxiosResponse = await axios.get(url, {
    responseType: "arraybuffer",
    transformResponse: (data) => {
      const encoding = chardet.detect(data);
      if (!encoding) {
        throw new Error("chardet failed to detect encoding");
      } else {
        console.log(`This site encoding: ${encoding}`);
      }
      return iconv.decode(data, encoding);
    },
  });
  const $ = cheerio.load(res.data);
  const span = $("button").filter((_, element) => {
    return $(element).text().includes("カートに入れる");
  });
  if (span.text()) {
    console.log("in stock");
    return url;
  } else {
    console.log("sold out");
    return undefined;
  }
};

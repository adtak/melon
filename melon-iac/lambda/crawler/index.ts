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
    const instockUrl = await crawlingSpan(urlT, "カートに追加する");
    if (instockUrl) {
      instockUrls.push(instockUrl);
    }
  }
  const urlK = process.env.SITE_K;
  if (urlK) {
    const instockUrl = await crawlingButton(urlK, "カートに入れる");
    if (instockUrl) {
      instockUrls.push(instockUrl);
    }
  }
  const urlF = process.env.SITE_F;
  if (urlF) {
    const instockUrl = await crawlingSpan(urlF, "カートに入れる");
    if (instockUrl) {
      instockUrls.push(instockUrl);
    }
  }

  if (instockUrls.length) {
    const params = {
      TopicArn: snsTopicArn,
      Subject: "[Melon] In Stock",
      Message:
        "Some items are in stock. Details are as follows.\n" +
        instockUrls.map((url) => `URL: ${url}`).join("\n"),
    };
    await sns.publish(params).promise();
  }
};

const crawlingSpan = async (url: string, keyword: string) => {
  const parseFunc = (res: AxiosResponse) => {
    const $ = cheerio.load(res.data);
    const span = $("span").filter((_, element) => {
      return $(element).text().includes(keyword);
    });
    return span.text();
  };
  return await crawlingURL(url, parseFunc);
};

const crawlingButton = async (url: string, keyword: string) => {
  const parseFunc = (res: AxiosResponse) => {
    const $ = cheerio.load(res.data);
    const button = $("button").filter((_, element) => {
      return $(element).text().includes(keyword);
    });
    return button.text();
  };
  return await crawlingURL(url, parseFunc);
};

const crawlingURL = async (
  url: string,
  parseFunc: (res: AxiosResponse) => string | undefined
) => {
  console.log(`Crawling URL: ${url}`);
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
  const text = parseFunc(res);
  if (text) {
    console.log("in stock");
    return url;
  } else {
    console.log("sold out");
    return undefined;
  }
};

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
  console.log(`url: ${urlT}`);
  try {
    const res: AxiosResponse = await axios.get(urlT);
    const $ = cheerio.load(res.data);
    const span = $("span").filter((_, element) => {
      return $(element).text().includes("カートに追加する");
    });
    if (span.text()) {
      console.log("in stock");
      const params = {
        TopicArn: snsTopicArn,
        Subject: "[Melon] In Stock",
        Message: `URL: ${urlT}`,
      };
      await sns.publish(params).promise();
    } else {
      console.log("sold out");
    }
  } catch (e) {
    throw e;
  }
};

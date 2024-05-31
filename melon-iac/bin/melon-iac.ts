#!/usr/bin/env node
import "source-map-support/register";
import "dotenv/config";
import * as cdk from "aws-cdk-lib";
import { MelonStack } from "../lib/melon-iac-stack";

const app = new cdk.App();
const env = {
  account: process.env.AWS_ACCOUNT,
  region: "ap-northeast-1",
};
new MelonStack(
  app,
  "MelonStack",
  {
    siteT: process.env.URL_T ? process.env.URL_T : "",
    siteK1: process.env.URL_K1 ? process.env.URL_K1 : "",
    siteK2: process.env.URL_K2 ? process.env.URL_K2 : "",
    siteF1: process.env.URL_F1 ? process.env.URL_F1 : "",
    siteF2: process.env.URL_F2 ? process.env.URL_F2 : "",
  },
  { env }
);

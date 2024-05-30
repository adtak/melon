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
    siteK: process.env.URL_K ? process.env.URL_K : "",
  },
  { env }
);

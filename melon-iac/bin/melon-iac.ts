#!/usr/bin/env node
import "source-map-support/register";
import "dotenv/config";
import * as cdk from "aws-cdk-lib";
import { MelonIacStack } from "../lib/melon-iac-stack";

const app = new cdk.App();
const env = {
  account: process.env.AWS_ACCOUNT,
  region: "ap-northeast-1",
};
new MelonIacStack(app, "MelonIacStack", { env });

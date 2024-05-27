#!/usr/bin/env node
import "source-map-support/register";
import * as cdk from "aws-cdk-lib";
import { MelonIacStack } from "../lib/melon-iac-stack";

const app = new cdk.App();
const env = {
  account: "111111111111",
  region: "ap-northeast-1",
};
new MelonIacStack(app, "MelonIacStack", { env });

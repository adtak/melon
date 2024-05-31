import * as cdk from "aws-cdk-lib";
import { Construct } from "constructs";

import * as events from "aws-cdk-lib/aws-events";
import * as targets from "aws-cdk-lib/aws-events-targets";
import * as iam from "aws-cdk-lib/aws-iam";
import * as lambda from "aws-cdk-lib/aws-lambda";
import * as sns from "aws-cdk-lib/aws-sns";
import { NodejsFunction } from "aws-cdk-lib/aws-lambda-nodejs";
import { SnsDestination } from "aws-cdk-lib/aws-lambda-destinations";

export type CrawlingURL = {
  siteT: string;
  siteK1: string;
  siteK2: string;
  siteF1: string;
  siteF2: string;
};

export class MelonStack extends cdk.Stack {
  constructor(
    scope: Construct,
    id: string,
    crawlingURL: CrawlingURL,
    props?: cdk.StackProps
  ) {
    super(scope, id, props);

    const errorTopic = new sns.Topic(this, "errorTopic", {
      topicName: "errorTopic",
      displayName: "errorTopic",
    });
    errorTopic.addToResourcePolicy(
      new iam.PolicyStatement({
        effect: iam.Effect.ALLOW,
        actions: ["sns:Publish"],
        principals: [new iam.ServicePrincipal("events.amazonaws.com")],
        resources: [errorTopic.topicArn],
      })
    );

    const instockTopic = new sns.Topic(this, "instockTopic", {
      topicName: "instockTopic",
      displayName: "instockTopic",
    });
    instockTopic.addToResourcePolicy(
      new iam.PolicyStatement({
        effect: iam.Effect.ALLOW,
        actions: ["sns:Publish"],
        principals: [new iam.ServicePrincipal("lambda.amazonaws.com")],
        resources: [instockTopic.topicArn],
      })
    );

    const crawlerFunc = new NodejsFunction(this, "crawlerFunction", {
      functionName: "melonCrawlerFunction",
      entry: "lambda/crawler/index.ts",
      handler: "handler",
      runtime: lambda.Runtime.NODEJS_LATEST,
      memorySize: 512,
      timeout: cdk.Duration.seconds(60 * 10),
      environment: {
        SNS_TOPIC_ARN: instockTopic.topicArn,
        SITE_T: crawlingURL.siteT,
        SITE_K1: crawlingURL.siteK1,
        SITE_K2: crawlingURL.siteK2,
        SITE_F1: crawlingURL.siteF1,
        SITE_F2: crawlingURL.siteF2,
      },
      onFailure: new SnsDestination(errorTopic),
    });
    crawlerFunc.addToRolePolicy(
      new iam.PolicyStatement({
        effect: iam.Effect.ALLOW,
        actions: ["sns:Publish"],
        resources: [instockTopic.topicArn],
      })
    );
    const crawlerRule = new events.Rule(this, "crawlerRule", {
      schedule: events.Schedule.cron({ minute: "0", hour: "0,3,6,9,12,15" }),
    });
    crawlerRule.addTarget(new targets.LambdaFunction(crawlerFunc));
  }
}

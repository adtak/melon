import * as cdk from "aws-cdk-lib";
import { Construct } from "constructs";

import * as iam from "aws-cdk-lib/aws-iam";
import * as lambda from "aws-cdk-lib/aws-lambda";
import * as sns from "aws-cdk-lib/aws-sns";
import { NodejsFunction } from "aws-cdk-lib/aws-lambda-nodejs";
import { SnsDestination } from "aws-cdk-lib/aws-lambda-destinations";

export class MelonIacStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
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

    new NodejsFunction(this, "crawlerFunction", {
      functionName: "melonCrawlerFunction",
      entry: "lambda/crawler/index.ts",
      handler: "handler",
      runtime: lambda.Runtime.NODEJS_LATEST,
      timeout: cdk.Duration.seconds(60 * 10),
      environment: {},
      onFailure: new SnsDestination(errorTopic),
    });
  }
}

import aws_cdk as cdk

from melon_iac.melon_iac_stack import MelonIacStack

app = cdk.App()
MelonIacStack(app, "MelonIacStack")

app.synth()

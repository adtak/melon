.PHONY: synth
synth:
				cdk synth

.PHONY: diff
diff:
				cdk duff

.PHONY: deploy
deploy:
				cdk deploy

.PHONY: run-local
run-local:
				sam local invoke -t ./cdk.out/MelonStack.template.json --container-host 127.0.0.1
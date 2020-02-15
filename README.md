# ECS Agent Update

This script will find any ECS clusters, then find the EC2 instances behind them and ask the ECS API to do a container update.

To run locally, clone this repo and then run the following

```
pip3 install -r requirements.txt
python3 lambda_function.py
```

## Terraform

There is a terraform module which will deploy this in your AWS account.  You can find it here: https://github.com/richardjkendall/tf-modules/tree/master/modules/ecs-agent-updater
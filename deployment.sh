#!/bin/bash -ex
echo "Login to AWS ECR"
eval $(aws ecr get-login --no-include-email --region us-east-1)

echo "build docker image hello-world:hello-world-1-1"
docker build -t sagar/hello-world:hello-world-1-1 .

echo "Push docker image"
docker push ${account_number}.dkr.ecr.us-east-1.amazonaws.com/sagar/hello-world:hello-world-1-1

echo "deploying hello-world:hello-world-1-1"
ecs-deploy -r us-east-1 -c  service-cluster -n hello-world -i ${account_number}.dkr.ecr.us-east-1.amazonaws.com/sagar/hello-world:hello-world-1-1 --aws-instance-profile -t 240

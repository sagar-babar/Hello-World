# HTTP-based API "Hello-World"

## System Diagram

#### Install dependencies
```bash
$ pip install -r requirements.txt
```

## Running the app locally
Requires a DB created
```bash
$ sqlite3 user.db < user-schema.sql
$ python run_app.py
```

## Test
```bash
$ make test
```


## Deploy service on AWS-ECS using GoCD/Jenkins with No Downtime

We will be deploying "Hello-World" as using GoCD/Jenkins in AWS with ecs-deploy.

ecs-service deployment with ecs-deploy will be no downtime deployment(blue/green deployment)

####Pipeline Stages
**Unit Test**
```bash
$make test
```
**Build**
```bash
eval $(aws ecr get-login --no-include-email --region us-east-1)
docker build -t sagar/hello-world:hello-world-1-1 .
docker push ${account_number}.dkr.ecr.us-east-1.amazonaws.com/sagar/hello-world:hello-world-1-1
```
**Deploy**
```bash
echo "deploying hello-world:hello-world-1-1"
ecs-deploy -r us-east-1 -c  service-cluster -n hello-world -i ${account_number}.dkr.ecr.us-east-1.amazonaws.com/sagar/hello-world:hello-world-1-1 --aws-instance-profile -t 240
```

## Output Images

**Create user with response code 204 No Content**
![](https://github.com/sagar-babar/Hello-World/blob/master/output-images/1.png)

**Validation: User not available**
![](https://github.com/sagar-babar/Hello-World/blob/master/output-images/7.png)

**Validation: User name must contains only letters**
![](https://github.com/sagar-babar/Hello-World/blob/master/output-images/2.png)

**Validation: DOB should be before todays date**
![](https://github.com/sagar-babar/Hello-World/blob/master/output-images/3.png)

**User Output: Number of days for Birthday**
![](https://github.com/sagar-babar/Hello-World/blob/master/output-images/4.png)

**User Output: Today Birthday**
![](https://github.com/sagar-babar/Hello-World/blob/master/output-images/5.png)

**User Output: Today Birthday**
![](https://github.com/sagar-babar/Hello-World/blob/master/output-images/5.png)
![](https://github.com/sagar-babar/Hello-World/blob/master/output-images/6.png)

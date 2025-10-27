# Creating Docker image locally

- From root directory (containing Dockerfile):

```
docker build -t webapp:latest .
```

# Below are the AWS commands used to create "AWS App Runner" service 

- Creating a ECR (Elastic Container Registry) repo named "dsti_project":

```
aws ecr create-repository --repository-name dsti_project
```

  - output:

{
    "repository": {
        "repositoryArn": "arn:aws:ecr:eu-west-3:175416526520:repository/dsti_project",
        "registryId": "175416526520",
        "repositoryName": "dsti_project",
        "repositoryUri": "175416526520.dkr.ecr.eu-west-3.amazonaws.com/dsti_project",
        "createdAt": "2025-10-24T11:35:46.144000+02:00",
        "imageTagMutability": "MUTABLE",
        "imageScanningConfiguration": {
            "scanOnPush": false
        },
        "encryptionConfiguration": {
            "encryptionType": "AES256"
        }
    }
}


- Getting AWS account:

```
(powershell)
$AWS_ACCOUNT_ID = (aws sts get-caller-identity --query Account --output text) 
```

- Checking: 

```
(powershell)
AWS_ACCOUNT_ID
```

  - output:

175416526520

- Setting AWS region:

```
(powershell)
$REGION = "eu-west-3"
```

- Tagging local image before pushing it to AWS:

```
(powershell)
$repo = "$($AWS_ACCOUNT_ID).dkr.ecr.$($REGION).amazonaws.com/dsti_project"
docker tag webapp:latest "$($repo):latest"
```

- Check:

```
docker images
```

  - output:

REPOSITORY                                                  TAG       IMAGE ID       CREATED         SIZE
175416526520.dkr.ecr.eu-west-3.amazonaws.com/dsti_project   latest    8eea29913c9b   21 hours ago    3.86GB


- Making Docker authenticate with AWS:

```
(powershell)
aws ecr get-login-password --region $REGION | docker login --username AWS --password-stdin "$($AWS_ACCOUNT_ID).dkr.ecr.$($REGION).amazonaws.com"
```

  - output:

Login Succeeded


- Pushing Docker image to ECR:

```
(powershell)
docker push $($AWS_ACCOUNT_ID).dkr.ecr.$($REGION).amazonaws.com/dsti_project:latest
```

  - output:

The push refers to repository [175416526520.dkr.ecr.eu-west-3.amazonaws.com/dsti_project]
e268421f9ff1: Pushed
38513bd72563: Pushed
a9ffe18d7fdb: Pushed
e73850a50582: Pushed
cdf1c9c52360: Pushed
19fb8589da02: Pushed
f715043ecdca: Pushed
192491262b0c: Pushed
5c0e45c97498: Pushed
dc35cf302abe: Pushed
latest: digest: sha256:8eea29913c9bd552ebc88c79554dcd8e96cb68c4ece9c552da91590fbbc66ca6 size: 856

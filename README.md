# terraform

Practice repo for learning Terraform against AWS — safely, using LocalStack
(a local AWS API emulator), before ever touching a real AWS account.

## One-time setup

1. Install Terraform (already done if `terraform -version` works).

2. Install Colima + Docker CLI (lightweight Docker runtime, no Docker Desktop needed):

   ```
   brew install colima docker
   ```

3. Start Colima:

   ```
   colima start
   ```

   Verify Docker works:

   ```
   docker ps
   ```

4. Start LocalStack (pinned to `3.4`, the last community-only tag that doesn't
   require a LocalStack account/auth token):
   ```
   docker run -d --name localstack \
     -p 4566:4566 -p 4510-4559:4510-4559 \
     localstack/localstack:3.4
   ```
   Check it's healthy:
   ```
   curl -s http://localhost:4566/_localstack/health
   ```

## Every time you want to practice

1. Make sure Colima is running:

   ```
   colima status || colima start
   ```

2. Make sure the LocalStack container is up:

   ```
   docker start localstack   # if it already exists but stopped
   # or, if you removed it, re-run the `docker run` command from setup step 4
   ```

3. Run Terraform as normal:

   ```
   terraform init
   terraform plan
   terraform apply
   terraform destroy
   ```

   Everything targets `http://localhost:4566` (see the `provider "aws"` block
   in `main.tf`), so nothing ever hits real AWS or costs money.

4. When done, optionally stop things to free resources:
   ```
   docker stop localstack
   colima stop
   ```

## Switching to real AWS later

`main.tf`'s `provider "aws"` block currently points at LocalStack with fake
credentials (`access_key = "test"`, etc.) and custom `endpoints`. To point at
real AWS instead:

1. Create an IAM user in the AWS Console with programmatic access.
2. Run `aws configure --profile terraform-practice` and enter the access
   key / secret key.
3. Replace the `provider "aws"` block with:
   ```hcl
   provider "aws" {
     region  = "us-east-1"
     profile = "terraform-practice"
   }
   ```
4. Re-run `terraform init` then `terraform plan` — review carefully before
   ever running `terraform apply` against a real account.

Check state
terraform state list

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region  = "us-east-1"
  profile = "terraform-practice"
}

module "network" {
  source = "./modules/network"

  name = "terraform-practice"
}

module "storage" {
  source = "./modules/storage"

  bucket_name = "tewen-terraform-practice-bucket-tewen"
}

module "loadbalancer" {
  source = "./modules/loadbalancer"

  name              = "terraform-practice"
  vpc_id            = module.network.vpc_id
  subnet_ids        = module.network.subnet_ids
  security_group_id = module.network.lb_security_group_id
}

module "compute" {
  source = "./modules/compute"

  name              = "terraform-practice"
  security_group_id = module.network.instance_security_group_id
}

resource "aws_lb_target_group_attachment" "practice" {
  target_group_arn = module.loadbalancer.target_group_arn
  target_id        = module.compute.instance_id
  port             = 80
}

variable "name" {
  type = string
}

variable "instance_type" {
  type    = string
  default = "t3.micro"
}

variable "security_group_id" {
  type = string
}

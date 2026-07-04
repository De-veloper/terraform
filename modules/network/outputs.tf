output "vpc_id" {
  value = data.aws_vpc.default.id
}

output "subnet_ids" {
  value = data.aws_subnets.default.ids
}

output "lb_security_group_id" {
  value = aws_security_group.lb.id
}

output "instance_security_group_id" {
  value = aws_security_group.instance.id
}

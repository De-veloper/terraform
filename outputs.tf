output "bucket_id" {
  value = module.storage.bucket_id
}

output "bucket_arn" {
  value = module.storage.bucket_arn
}

output "instance_id" {
  value = module.compute.instance_id
}

output "load_balancer_dns_name" {
  value = module.loadbalancer.dns_name
}

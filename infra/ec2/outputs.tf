output "ec2_ip_address" {
  description = "Ip address of the vpc"
  value       = module.ec2_instance.private_ip
}

output "instance_id" {
  value       = module.ec2_instance.id
  description = "Instance id"
}

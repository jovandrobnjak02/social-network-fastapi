output "app_security_group_id" {
  description = "Id of the security group"
  value       = module.app_security_group.security_group_id
}

output "lb_security_group_id" {
  description = "Id of the security group"
  value       = module.load_balancer_group.security_group_id
}

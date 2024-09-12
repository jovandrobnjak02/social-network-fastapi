output "github_role_arn" {
  value       = module.iam_assumable_role_with_oidc.iam_role_arn
  description = "ARN of the github role"
}
output "ec2_policy_arn" {
  value       = module.iam_policy_for_ec2.arn
  description = "ARN of the ec2 policy"
}

output "ec2_policy_name" {
  value       = module.iam_policy_for_ec2.name
  description = "Name of the ec2 policy"
}

output "loadbalacer_policy_name" {
  value       = module.iam_policy_for_load_balancer.name
  description = "Name of the ec2 policy"
}
output "loadbalacer_policy_arn" {
  value       = module.iam_policy_for_load_balancer.arn
  description = "ARN of the ec2 policy"
}

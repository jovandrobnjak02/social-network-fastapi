output "vpc_id" {
  description = "Id of the vpc"
  value       = module.vpc.vpc_id
}

output "public_subnet" {
  description = "Public subnet"
  value       = module.vpc.public_subnets[0]
}

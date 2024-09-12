module "app_security_group" {
  source = "terraform-aws-modules/security-group/aws"

  name        = "app-security-group"
  description = "Security group for ec2 instance running the kubernetes cluster"
  vpc_id      = var.vpc_id

  ingress_with_cidr_blocks = [
    {
      rule        = "all-all"
      description = "All traffic from my ip"
      cidr_blocks = var.my_cidr_block
    },
  ]
  ingress_with_source_security_group_id = [
    {
      rule                     = "http-80-tcp"
      source_security_group_id = module.load_balancer_group.security_group_id
    },
  ]

  egress_with_cidr_blocks = [
    {
      rule        = "https-443-tcp"
      cidr_blocks = "0.0.0.0/0"
    }
  ]
}

module "load_balancer_group" {
  source = "terraform-aws-modules/security-group/aws"

  name        = "lb-security-group"
  description = "Security group for the load balancer instance"
  vpc_id      = var.vpc_id

  ingress_with_cidr_blocks = [
    {
      rule        = "all-all"
      description = "All traffic from my ip"
      cidr_blocks = var.my_cidr_block
    },
    # {
    #   rule        = "https-443-tcp"
    #   description = "Allow HTTPS traffic"
    #   cidr_blocks = "0.0.0.0/0"
    # },
    # {
    #   rule        = "http-80-tcp"
    #   description = "Allow HTTP traffic"
    #   cidr_blocks = "0.0.0.0/0"
    # }
  ]
  ingress_with_source_security_group_id = [
    {
      rule                     = "all-all"
      source_security_group_id = module.app_security_group.security_group_id
    }
  ]

  egress_with_cidr_blocks = [
    {
      rule        = "https-443-tcp"
      cidr_blocks = "0.0.0.0/0"
    }
  ]
}

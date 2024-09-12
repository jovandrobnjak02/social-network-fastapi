data "aws_availability_zones" "available_zones" {
  state = "available"
}

module "subnet_addrs" {
  source          = "hashicorp/subnets/cidr"
  base_cidr_block = var.base_cidr_block
  networks = [
    {
      name     = "public"
      new_bits = 8
    }
  ]
}

module "vpc" {
  source = "terraform-aws-modules/vpc/aws"

  name = var.vpc_name
  cidr = module.subnet_addrs.base_cidr_block
  azs  = data.aws_availability_zones.available_zones.names

  public_subnets = [lookup(module.subnet_addrs.network_cidr_blocks, "public", "what?")]

  create_igw = true

}



module "ec2_instance" {
  source = "terraform-aws-modules/ec2-instance/aws"

  name = var.instance_name

  instance_type               = var.instance_type
  monitoring                  = true
  vpc_security_group_ids      = [var.security_group_id]
  subnet_id                   = var.subnet_id
  iam_role_policies           = var.iam_role_policies
  create_iam_instance_profile = true
  iam_role_name               = var.iam_role_name
  associate_public_ip_address = true
  ami                         = "ami-0e872aee57663ae2d"

  tags = {
    Purpose = var.tag_value
  }
}

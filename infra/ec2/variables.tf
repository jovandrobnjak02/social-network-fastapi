variable "instance_name" {
  description = "Name of the instance"
  type        = string
}

variable "instance_type" {
  description = "Name of the instance type"
  type        = string
}

variable "tag_value" {
  description = "Tag value"
  type        = string
}

variable "subnet_id" {
  description = "Subnet id"
  type        = string
}

variable "security_group_id" {
  description = "Security group id"
  type        = string
}
variable "iam_role_name" {
  description = "Name of the iam role"
  type        = string
}

variable "iam_role_policies" {
  type        = map(string)
  description = "Iam policies to attach to the machine"
}

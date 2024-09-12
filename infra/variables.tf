variable "instance_id" {
  description = "Id of the instance that gets the eip"
  type        = string
}

variable "domain_name" {
  description = "Name of the domain"
  type        = string
}

variable "hosted_zone" {
  description = "Name of the hosted zone"
  type        = string
}

variable "ttl" {
  description = "Time to live"
  type        = number
}

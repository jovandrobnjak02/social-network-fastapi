variable "device_name" {
  type        = string
  description = "Name of the device"
}

variable "instance_id" {
  type        = string
  description = "Id of an instance"
}
variable "tag_value" {
  type        = string
  description = "Value of the Name tag"
}
variable "size" {
  type        = number
  description = "Size of the volume"
}

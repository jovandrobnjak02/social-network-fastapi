data "aws_availability_zones" "available_zones" {
  state = "available"
}

resource "aws_ebs_volume" "kubernetes_volume" {
  availability_zone = data.aws_availability_zones.available_zones.names[0]
  size              = var.size
  tags = {
    Name = var.tag_value
  }
}

resource "aws_volume_attachment" "kubernetes_volume_attachment" {
  device_name = var.device_name
  volume_id   = aws_ebs_volume.kubernetes_volume.id
  instance_id = var.instance_id
}

data "aws_route53_zone" "omage_hosted_zone" {
  name = var.hosted_zone
}

module "acm" {
  source  = "terraform-aws-modules/acm/aws"
  version = "~> 4.0"

  domain_name = var.domain_name
  zone_id     = data.aws_route53_zone.omage_hosted_zone.zone_id

  validation_method = "DNS"

  wait_for_validation = true

}

resource "aws_eip" "lb" {
  instance = var.instance_id
}

resource "aws_route53_record" "load_balancer_domain" {
  zone_id = data.aws_route53_zone.omage_hosted_zone.zone_id
  name    = "jovan-drobnjak.omega.devops.sitesstage.com"
  type    = "A"
  ttl     = var.ttl

  records = [aws_eip.lb.public_ip]
}

resource "aws_route53_record" "prometheus_domain" {
  zone_id = data.aws_route53_zone.omage_hosted_zone.zone_id
  name    = "prometheus-jovan-drobnjak.omega.devops.sitesstage.com"
  type    = "A"
  ttl     = var.ttl

  records = [aws_eip.lb.public_ip]
}

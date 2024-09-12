module "iam_policy" {
  source = "terraform-aws-modules/iam/aws//modules/iam-policy"

  name        = var.github_policy_name
  description = "Policy for pushing images into ECR with GitHub Actions"
  path        = "/"

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ecr:GetAuthorizationToken",
                "ecr:BatchGetImage",
                "ecr:InitiateLayerUpload",
                "ecr:UploadLayerPart",
                "ecr:CompleteLayerUpload",
                "ecr:BatchCheckLayerAvailability",
                "ecr:GetDownloadUrlForLayer",
                "ecr:PutImage",
                "ecr:DescribeImages"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "sts:AssumeRoleWithWebIdentity"
            ],
            "Resource": "*"
        }
    ]
}
EOF

}

module "iam_github_oidc_provider" {
  source = "terraform-aws-modules/iam/aws//modules/iam-github-oidc-provider"
}

module "iam_assumable_role_with_oidc" {
  source = "terraform-aws-modules/iam/aws//modules/iam-assumable-role-with-oidc"

  oidc_subjects_with_wildcards = ["repo:jovandrobnjak/Social-Network-FastApi:*"]

  create_role = true

  role_name = var.oidc_role_name

  tags = {
    Role = "role-with-oidc"
  }

  provider_url = module.iam_github_oidc_provider.url

  number_of_role_policy_arns = 1

  role_policy_arns = [module.iam_policy.arn]

  oidc_fully_qualified_audiences = ["sts.amazonaws.com"]
}

module "iam_policy_for_ec2" {
  source = "terraform-aws-modules/iam/aws//modules/iam-policy"

  name        = "EC2ECRPolicy"
  description = "Policy for pulling images from ECR"
  path        = "/"

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ecr:GetAuthorizationToken",
                "ecr:BatchGetImage",
                "ecr:InitiateLayerUpload",
                "ecr:UploadLayerPart",
                "ecr:CompleteLayerUpload",
                "ecr:BatchCheckLayerAvailability",
                "ecr:GetDownloadUrlForLayer",
                "ecr:PutImage",
                "ecr:DescribeImages"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "ec2:DescribeInstances"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
              "ec2:CreateTags"
            ],
            "Resource": "*"
        }
    ]
}
EOF

}
module "iam_policy_for_load_balancer" {
  source = "terraform-aws-modules/iam/aws//modules/iam-policy"

  name        = "EC2LBPolicy"
  description = "Policy for creating log streams"
  path        = "/"

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
       {
        "Effect": "Allow",
        "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents",
        "logs:DescribeLogGroups",
        "logs:DescribeLogStreams",
        "logs:PutRetentionPolicy",
        "logs:PutMetricFilter"
      ],
        "Resource": "*"
    }
    ]
}
EOF

}

resource "aws_iam_role" "civicshield_eks_role" {
  name = "civicshield-eks-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "eks.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "civicshield_eks_cluster_policy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
  role       = aws_iam_role.civicshield_eks_role.name
}

resource "aws_iam_role_policy_attachment" "civicshield_eks_service_policy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSServicePolicy"
  role       = aws_iam_role.civicshield_eks_role.name
}

resource "aws_iam_role" "civicshield_eks_node_role" {
  name = "civicshield-eks-node-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "civicshield_eks_worker_node_policy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy"
  role       = aws_iam_role.civicshield_eks_node_role.name
}

resource "aws_iam_role_policy_attachment" "civicshield_eks_cni_policy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy"
  role       = aws_iam_role.civicshield_eks_node_role.name
}

resource "aws_iam_role_policy_attachment" "civicshield_ec2_container_registry_readonly" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
  role       = aws_iam_role.civicshield_eks_node_role.name
}

resource "aws_iam_role" "civicshield_rds_role" {
  name = "civicshield-rds-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "rds.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "civicshield_rds_policy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonRDSReadOnlyAccess"
  role       = aws_iam_role.civicshield_rds_role.name
}
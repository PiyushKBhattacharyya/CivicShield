terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.0"
    }
    helm = {
      source  = "hashicorp/helm"
      version = "~> 2.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

provider "kubernetes" {
  host                   = var.kubernetes_host
  token                  = var.kubernetes_token
  cluster_ca_certificate = var.kubernetes_ca_certificate
}

provider "helm" {
  kubernetes {
    host                   = var.kubernetes_host
    token                  = var.kubernetes_token
    cluster_ca_certificate = var.kubernetes_ca_certificate
  }
}

# VPC
resource "aws_vpc" "civicshield_vpc" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "civicshield-vpc"
  }
}

# Internet Gateway
resource "aws_internet_gateway" "civicshield_igw" {
  vpc_id = aws_vpc.civicshield_vpc.id

  tags = {
    Name = "civicshield-igw"
  }
}

# Public Subnets
resource "aws_subnet" "civicshield_public_subnets" {
  count                   = length(var.public_subnet_cidrs)
  vpc_id                  = aws_vpc.civicshield_vpc.id
  cidr_block              = var.public_subnet_cidrs[count.index]
  availability_zone       = var.availability_zones[count.index]
  map_public_ip_on_launch = true

  tags = {
    Name = "civicshield-public-${count.index}"
  }
}

# Private Subnets
resource "aws_subnet" "civicshield_private_subnets" {
  count             = length(var.private_subnet_cidrs)
  vpc_id            = aws_vpc.civicshield_vpc.id
  cidr_block        = var.private_subnet_cidrs[count.index]
  availability_zone = var.availability_zones[count.index]

  tags = {
    Name = "civicshield-private-${count.index}"
  }
}

# Route Tables
resource "aws_route_table" "civicshield_public_rt" {
  vpc_id = aws_vpc.civicshield_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.civicshield_igw.id
  }

  tags = {
    Name = "civicshield-public-rt"
  }
}

resource "aws_route_table_association" "civicshield_public_rt_assoc" {
  count          = length(aws_subnet.civicshield_public_subnets)
  subnet_id      = aws_subnet.civicshield_public_subnets[count.index].id
  route_table_id = aws_route_table.civicshield_public_rt.id
}

# Security Groups
resource "aws_security_group" "civicshield_sg" {
  name        = "civicshield-sg"
  description = "Security group for CivicShield platform"
  vpc_id      = aws_vpc.civicshield_vpc.id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.ssh_access_cidr]
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "civicshield-sg"
  }
}

# EKS Cluster
resource "aws_eks_cluster" "civicshield_eks" {
  name     = "civicshield-eks"
  role_arn = aws_iam_role.civicshield_eks_role.arn

  vpc_config {
    subnet_ids = aws_subnet.civicshield_private_subnets[*].id
  }

  depends_on = [
    aws_iam_role_policy_attachment.civicshield_eks_cluster_policy,
    aws_iam_role_policy_attachment.civicshield_eks_service_policy,
  ]
}

# EKS Node Group
resource "aws_eks_node_group" "civicshield_node_group" {
  cluster_name    = aws_eks_cluster.civicshield_eks.name
  node_group_name = "civicshield-node-group"
  node_role_arn   = aws_iam_role.civicshield_eks_node_role.arn
  subnet_ids      = aws_subnet.civicshield_private_subnets[*].id

  scaling_config {
    desired_size = 3
    max_size     = 10
    min_size     = 1
  }

  update_config {
    max_unavailable = 1
  }

  depends_on = [
    aws_iam_role_policy_attachment.civicshield_eks_worker_node_policy,
    aws_iam_role_policy_attachment.civicshield_eks_cni_policy,
    aws_iam_role_policy_attachment.civicshield_ec2_container_registry_readonly,
  ]
}

# RDS Instance
resource "aws_db_instance" "civicshield_rds" {
  identifier             = "civicshield-rds"
  allocated_storage      = 100
  engine                 = "postgres"
  engine_version         = "13"
  instance_class         = "db.t3.medium"
  db_name                = "civicshield"
  username               = "civicshield_user"
  password               = var.db_password
  skip_final_snapshot    = true
  vpc_security_group_ids = [aws_security_group.civicshield_sg.id]
  db_subnet_group_name   = aws_db_subnet_group.civicshield_db_subnet_group.name

  tags = {
    Name = "civicshield-rds"
  }
}

# RDS Subnet Group
resource "aws_db_subnet_group" "civicshield_db_subnet_group" {
  name       = "civicshield-db-subnet-group"
  subnet_ids = aws_subnet.civicshield_private_subnets[*].id

  tags = {
    Name = "civicshield-db-subnet-group"
  }
}

# Elasticache Redis
resource "aws_elasticache_cluster" "civicshield_redis" {
  cluster_id           = "civicshield-redis"
  engine               = "redis"
  node_type            = "cache.t3.micro"
  num_cache_nodes      = 1
  parameter_group_name = "default.redis6.x"
  engine_version       = "6.2"
  port                 = 6379
  subnet_group_name    = aws_elasticache_subnet_group
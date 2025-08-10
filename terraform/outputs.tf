output "vpc_id" {
  description = "VPC ID"
  value       = aws_vpc.civicshield_vpc.id
}

output "public_subnet_ids" {
  description = "Public subnet IDs"
  value       = aws_subnet.civicshield_public_subnets[*].id
}

output "private_subnet_ids" {
  description = "Private subnet IDs"
  value       = aws_subnet.civicshield_private_subnets[*].id
}

output "security_group_id" {
  description = "Security group ID"
  value       = aws_security_group.civicshield_sg.id
}

output "eks_cluster_endpoint" {
  description = "EKS cluster endpoint"
  value       = aws_eks_cluster.civicshield_eks.endpoint
}

output "eks_cluster_certificate_authority" {
  description = "EKS cluster certificate authority"
  value       = aws_eks_cluster.civicshield_eks.certificate_authority[0].data
}

output "rds_endpoint" {
  description = "RDS endpoint"
  value       = aws_db_instance.civicshield_rds.endpoint
}

output "redis_endpoint" {
  description = "Redis endpoint"
  value       = aws_elasticache_cluster.civicshield_redis.cache_nodes[0].address
}

output "elasticsearch_endpoint" {
  description = "Elasticsearch endpoint"
  value       = aws_elasticsearch_domain.civicshield_elasticsearch.endpoint
}
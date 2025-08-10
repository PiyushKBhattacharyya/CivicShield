resource "aws_elasticsearch_domain" "civicshield_elasticsearch" {
  domain_name           = "civicshield-elasticsearch"
  elasticsearch_version = "7.10"

  cluster_config {
    instance_type = var.elasticsearch_instance_type
    instance_count = var.elasticsearch_instance_count
  }

  ebs_options {
    ebs_enabled = true
    volume_type = "gp2"
    volume_size = 100
  }

  encrypt_at_rest {
    enabled    = true
    kms_key_id = aws_kms_key.civicshield_kms_key.id
  }

  node_to_node_encryption {
    enabled = true
  }

  domain_endpoint_options {
    enforce_https       = true
    tls_security_policy = "Policy-Min-TLS-1-2-2019-07"
  }

  advanced_security_options {
    enabled                        = true
    internal_user_database_enabled = true
    master_user_options {
      master_user_name     = "civicshield"
      master_user_password = var.elasticsearch_password
    }
  }

  tags = {
    Name = "civicshield-elasticsearch"
  }
}

resource "aws_kms_key" "civicshield_kms_key" {
  description             = "KMS key for CivicShield Elasticsearch"
  deletion_window_in_days = 10
}

resource "aws_kms_alias" "civicshield_kms_alias" {
  name          = "alias/civicshield-elasticsearch"
  target_key_id = aws_kms_key.civicshield_kms_key.key_id
}
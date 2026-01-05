terraform {
    required_providers {
        github = {
            source  = "integrations/github"
            version = "~> 5.0"
        }
    }
}

provider "github" {
    owner = "LukaszSawa"
}

locals {
    service_file_names = concat(
        fileset("${path.module}/service_requests", "*.yml"),
        fileset("${path.module}/service_requests", "*.yaml")
    )
    
    requests = { for file_name in local.service_file_names :
        file_name => yamldecode(file("${path.module}/service_requests/${file_name}"))
    }
}

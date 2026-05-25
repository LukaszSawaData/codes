variable "environment" {
  description = "The environment to deploy (dev, stage, analytics, poc, test)."
  type        = string
  default     = "test"
  validation {
    condition     = contains(["dev", "stage", "analytics", "poc", "test"], var.environment)
    error_message = "Environment must be one of: dev, stage, analytics, poc, test."
  }
}


variable "location" {
  description = "The Azure region to deploy resources into."
  type        = string
  default     = "germanywestcentral"
}

locals {
  # Environment-specific naming
  env_suffix = var.environment

resource_group_name        = "contoso-${var.environment}-databricks-rg-01"

  common_tags = {
    ApplicationName = "Databricks"
    BusinessOwner   = "Your Business Owner"
    CreatedBy       = "Your Name"
    Environment     = title(var.environment)
    Region          = "Canada central"
    Sensitivity     = "Protected"
    DeploymentType  = "Terraform"
    Department      = "Your Department"
  }

  vnet_name = "contoso-${var.environment}-vnet-01"
  subnet_databricks_public_name = "databricks-public-subnet"
  subnet_databricks_private_name = "databricks-private-subnet"        
  subnet_pep_name = "pep-subnet"
  vnet_address_space = ["10.0.0.0/16"]  
    subnet_databricks_public_address_prefix = ["10.0.1.0/24"]
    subnet_databricks_private_address_prefix = ["10.0.2.0/24"]
    subnet_pep_address_prefix = ["10.0.3.0/24"] 

}
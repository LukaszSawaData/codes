terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {}
  subscription_id = "fa136590-6fc9-454b-98e8-b83b7d9583dd"
}

resource "azurerm_resource_group" "rg" {
  name     = "nowa_rg1"
  location = "germanywestcentral"
}

resource "azurerm_storage_account" "sa" {
  name                     = "salsawabestoptionpolska"
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  account_kind             = "StorageV2"

  public_network_access_enabled = true
}
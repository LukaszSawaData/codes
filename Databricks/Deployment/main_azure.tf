resource "azurerm_resource_group" "main" {
  name     = local.resource_group_name
  location = var.location
  tags     = local.common_tags
}

resource "azurerm_virtual_network" "main" {
  name                = local.vnet_name
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  address_space       = local.vnet_address_space
  tags                = local.common_tags
}

resource "azurerm_subnet" "databricks_public" {
  name                 = local.subnet_databricks_public_name
  resource_group_name  = azurerm_resource_group.main.name
  virtual_network_name = azurerm_virtual_network.main.name
  address_prefixes     = local.subnet_databricks_public_address_prefix
}

resource "azurerm_subnet" "databricks_private" {
  name                 = local.subnet_databricks_private_name
  resource_group_name  = azurerm_resource_group.main.name
  virtual_network_name = azurerm_virtual_network.main.name
  address_prefixes     = local.subnet_databricks_private_address_prefix
}

resource "azurerm_subnet" "pep" {
  name                 = local.subnet_pep_name
  resource_group_name  = azurerm_resource_group.main.name
  virtual_network_name = azurerm_virtual_network.main.name
  address_prefixes     = local.subnet_pep_address_prefix
}




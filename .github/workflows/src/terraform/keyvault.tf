resource "azurerm_key_vault" "this" {
  name                     = "${var.prefix}-${var.environment}-${random_string.storage_name.result}"
  location                 = "${var.location}"
  resource_group_name      = azurerm_resource_group.this.name
  enabled_for_disk_encryption = true
  tenant_id                   = data.azurerm_client_config.current.tenant_id
  soft_delete_retention_days  = 7
  purge_protection_enabled    = false

  sku_name = "standard"

}

resource "azurerm_key_vault_access_policy" "terraform-user" {
  key_vault_id = azurerm_key_vault.this.id
  tenant_id    = data.azurerm_client_config.current.tenant_id
  object_id    = data.azurerm_client_config.current.object_id
  

  secret_permissions = [
    "Backup", "Delete", "Get", "List",  "Set","Purge", "Restore"
  ]
}
resource "azurerm_key_vault_access_policy" "function-user" {
  key_vault_id = azurerm_key_vault.this.id
  tenant_id    = data.azurerm_client_config.current.tenant_id
  object_id    = azurerm_user_assigned_identity.functions.principal_id
  

  # Secret
  secret_permissions = [
    "Get",
    "List"
  ]
}
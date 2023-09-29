resource "azurerm_application_insights" "insight" {
  name  = "${var.prefix}-${var.environment}"
  location            = azurerm_resource_group.this.location
  resource_group_name = azurerm_resource_group.this.name
  application_type    = "web"

}


resource "azurerm_resource_group" "this" {
  name  = "${var.prefix}-${var.environment}"
  location = "${var.location}"
}

resource "azurerm_storage_account" "storage" {
  name                     = "${random_string.storage_name.result}"
  location                 = "${var.location}"
  resource_group_name      = azurerm_resource_group.this.name
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_service_plan" "fn_app_service_plan" {
  name = "${var.prefix}-${var.environment}"
  resource_group_name = azurerm_resource_group.this.name
  location            = var.location
  os_type             = "Linux"
  sku_name            = "Y1"
}


data "azurerm_client_config" "current" {}

resource "azurerm_user_assigned_identity" "functions" {
  location            = var.location
  name = "${var.prefix}-${var.environment}"
  resource_group_name = azurerm_resource_group.this.name
}


resource "azurerm_linux_function_app" "fn_app" {
  name = "${var.prefix}-${var.environment}"
  location = "${var.location}"
  resource_group_name = azurerm_resource_group.this.name

  storage_account_name = azurerm_storage_account.storage.name
  storage_account_access_key = azurerm_storage_account.storage.primary_access_key
  service_plan_id = azurerm_service_plan.fn_app_service_plan.id

  site_config {
    application_stack {
      python_version = "3.0"
      
    }
    cors {
        allowed_origins = ["https://portal.azure.com"]
        support_credentials = true
      }
  }

  app_settings = {
    "WEBSITE_RUN_FROM_PACKAGE" = 1
    "APPINSIGHTS_INSTRUMENTATIONKEY"= azurerm_application_insights.insight.instrumentation_key

  }

  identity {
    type = "SystemAssigned,  UserAssigned"
    identity_ids = [azurerm_user_assigned_identity.functions.id]
  }
}

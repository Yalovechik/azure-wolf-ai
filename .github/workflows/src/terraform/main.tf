

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

resource "azurerm_api_management" "api-management" {
  name  = "${var.prefix}-${var.environment}"
  location            = azurerm_resource_group.this.location
  resource_group_name = azurerm_resource_group.this.name
  publisher_name      = "ai-comp"
  publisher_email     = "Yalovechik2012@gmail.com"
  sku_name = "Developer_1"
}

# data "azurerm_api_management" "this" {
#   name                = "${var.prefix}-${var.environment}"
#   resource_group_name = azurerm_resource_group.this.name
# }



resource "azurerm_api_management_api" "api_management_api_public" {
  name = "${var.prefix}-${var.environment}"
  api_management_name = azurerm_api_management.api-management.name
  resource_group_name   = azurerm_resource_group.this.name
  revision = 1
  display_name = "Public"
  path = ""
  protocols = ["https"]
  service_url = "https://${azurerm_linux_function_app.fn_app.default_hostname}/api"
  subscription_required = false
}

resource "azurerm_api_management_api_operation" "api_management_api_operation_public" {
  operation_id = "public-hello-word"
  api_name = azurerm_api_management_api.api_management_api_public.name
  api_management_name = azurerm_api_management.api-management.name
  resource_group_name = azurerm_resource_group.this.name
  display_name = "Hello word ENDPOINT"
  method = "GET"
  url_template = "/test"

}




resource "azurerm_linux_function_app" "fn_app" {
  name = "${var.prefix}-${var.environment}"
  location = "${var.location}"
  resource_group_name = azurerm_resource_group.this.name

  storage_account_name = azurerm_storage_account.storage.name
  storage_account_access_key = azurerm_storage_account.storage.primary_access_key
  service_plan_id = azurerm_service_plan.fn_app_service_plan.id

  site_config {
      application_insights_key = azurerm_application_insights.insight.instrumentation_key
      application_insights_connection_string = azurerm_application_insights.insight.connection_string
    application_stack {
      python_version = "3.10"
      
    }
    cors {
        allowed_origins = ["https://woof-ai-dev.azure-api.net/**", "https://portal.azure.com"]
        support_credentials = true
      }
  }

  app_settings = {
    WEBSITE_RUN_FROM_PACKAGE = 1
    # SCM_DO_BUILD_DURING_DEPLOYMENT=true
    # "APPINSIGHTS_INSTRUMENTATIONKEY"= azurerm_application_insights.insight.instrumentation_key

  }

  identity {
    type = "SystemAssigned, UserAssigned"
    identity_ids = [azurerm_user_assigned_identity.functions.id]
  }
}

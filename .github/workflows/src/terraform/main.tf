

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

# Text container
resource "azurerm_storage_container" "imagecontainer" {
  name                  = "imagecontainer-${var.prefix}-${var.environment}"  
  storage_account_name  = azurerm_storage_account.storage.name
  container_access_type = "private"  
}

# resource "azurerm_storage_blob" "imagecontainer" {
#   name                   = "imagecontainer-${var.prefix}-${var.environment}" 
#   storage_account_name   = azurerm_storage_account.storage.name
#   storage_container_name = azurerm_storage_container.imagecontainer.name
#   type                   = "Block"
# }

#image container

resource "azurerm_storage_container" "textcontainer" {
  name                  = "textcontainer-${var.prefix}-${var.environment}"  
  storage_account_name  = azurerm_storage_account.storage.name
  container_access_type = "private"  
}

# resource "azurerm_storage_blob" "blob_scraping" {
#   name                   = "blob_scraping-${var.prefix}-${var.environment}" 
#   storage_account_name   = azurerm_storage_account.storage.name
#   storage_container_name = azurerm_storage_container.textcontainer.name
#   type                   = "Block"
# }

#Table

resource "azurerm_storage_table" "table_scraping" {
  name                 = "scrapingtableAI"
  storage_account_name = azurerm_storage_account.storage.name
}

# resource "azurerm_storage_table_entity" "table_entity_scraping" {
#   storage_account_name = azurerm_storage_account.storage.name
#   table_name           = azurerm_storage_table.table_scraping.name
#    depends_on = [azurerm_storage_table.table_scraping]
# }

resource "azurerm_service_plan" "fn_app_service_plan" {
  name = "${var.prefix}-${var.environment}"
  resource_group_name = azurerm_resource_group.this.name
  location            = var.location
  os_type             = "Linux"
  sku_name            = "Y1"
}




# current changes
data "azurerm_client_config" "current" {}

resource "azurerm_user_assigned_identity" "functions" {
  location            = var.location
  name = "${var.prefix}-${var.environment}"
  resource_group_name = azurerm_resource_group.this.name
}

resource "azurerm_api_management" "api-management" {
  name  = "api-management-${var.prefix}-${var.environment}"
  location            = azurerm_resource_group.this.location
  resource_group_name = azurerm_resource_group.this.name
  publisher_name      = "ai-comp"
  publisher_email     = "Yalovechik2012@gmail.com"
  sku_name = "Developer_1"
  #  identity {
  #   type = "SystemAssigned"
  # }
}

# data "azurerm_api_management" "this" {
#   name                = "${var.prefix}-${var.environment}"
#   resource_group_name = azurerm_resource_group.this.name
# }



resource "azurerm_api_management_api" "api_management_api_public" {
  name = "api-management-api-${var.prefix}-${var.environment}"
  api_management_name = azurerm_api_management.api-management.name
  resource_group_name   = azurerm_resource_group.this.name
  revision = 1
  display_name = "Public"
  path = ""
  protocols = ["https"]
  service_url = "https://${azurerm_linux_function_app.fn_app.default_hostname}/api"
  subscription_required = false
}


# data "azurerm_api_management_api" "api_management_api_public" {
#   name                = "${var.prefix}-${var.environment}"
#   resource_group_name = azurerm_resource_group.this.name
#   api_management_name = azurerm_api_management.api-management.name
#   revision = "part"
# }


resource "azurerm_api_management_api_operation" "api_management_api_operation_public" {
  operation_id = "public-hello-word"
  api_name = azurerm_api_management_api.api_management_api_public.name
  api_management_name = azurerm_api_management.api-management.name
  resource_group_name = azurerm_resource_group.this.name
  display_name = "Hello word ENDPOINT"
  method = "GET"
  url_template = "/test"

}

resource "azurerm_api_management_api_policy" "api_management_api_policy_api_public" {
  api_name             = azurerm_api_management_api.api_management_api_public.name
  api_management_name  = azurerm_api_management.api-management.name
  resource_group_name  = azurerm_resource_group.this.name

#   xml_content = <<XML
# <policies>
#   <inbound>
#     <base />
#     <authentication-managed-identity resource="bf08044d-25d8-4f89-bbef-4010507f0d6a" ignore-error="false" />
#   </inbound>
# </policies>
# XML
}

# Create an Application Object for the function app

# resource "azuread_application" "ad_application_function_app" {
#   name = "${var.prefix}-${var.environment}-dev"
#   type = "webapp/api"
#   prevent_duplicate_names = true
# }

#here



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
  depends_on = [ azurerm_storage_table.table_scraping ]

  app_settings = {
    TABLE_NAME = "${azurerm_storage_table.table_scraping.name}"
    BLOB_STORAGE_IMAGE_NAME = "${azurerm_storage_container.imagecontainer.name}"
    BLOB_STORAGE_TEXT_NAME = "${azurerm_storage_container.textcontainer.name}"
    STORAGE_CONNECTION_STRING = "${azurerm_storage_account.storage.primary_connection_string}"
    # WEBSITE_RUN_FROM_PACKAGE = 1
    # ENABLE_ORYX_BUILD=true
    # SCM_DO_BUILD_DURING_DEPLOYMENT=true
    # SCM_DO_BUILD_DURING_DEPLOYMENT=true
    # "APPINSIGHTS_INSTRUMENTATIONKEY"= azurerm_application_insights.insight.instrumentation_key

  }

  identity {
    type = "SystemAssigned, UserAssigned"
    identity_ids = [azurerm_user_assigned_identity.functions.id]
  }

  # auth_settings {
  #   enabled = true
  #   issuer = "https://login.microsoftonline.com/${data.azurerm_client_config.current.tenant_id}"
  #   default_provider = "AzureActiveDirectory"
  #    active_directory {
  #   # client_id = azuread_application.ad_application_function_app.application_id
  #   client_id = "bf08044d-25d8-4f89-bbef-4010507f0d6a"
  # }
  # unauthenticated_client_action = "RedirectToLoginPage"

  # }
}

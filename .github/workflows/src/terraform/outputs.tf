output "resource_group_name" {
    value = azurerm_resource_group.this.name
}


output "function_name" {
    value = azurerm_linux_function_app.fn_app.name
}

# output "api_management_id" {
#   value = data.azurerm_api_management.this.gateway_url
# }

output "table_name" {
  value = azurerm_storage_table.table_scraping.name
}

output "imagecontainer_name" {
  value = azurerm_storage_container.imagecontainer.name
}


output "textcontainer_name" {
  value = azurerm_storage_container.textcontainer.name
}


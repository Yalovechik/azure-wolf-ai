output "resource_group_name" {
    value = azurerm_resource_group.this.name
}


output "function_name" {
    value = azurerm_linux_function_app.fn_app.name
}
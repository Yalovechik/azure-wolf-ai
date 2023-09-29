variable "prefix" {
    type = string
    description = "prefix the name of our project"
}

variable "location" {
    type = string
    description = "default region for our infrastructure"
}

variable "environment" {
    type = string
    description = "environemnt which we are cyrrently using dev/prod/test"
}

variable "functionapp" {
    type = string
    default = "./build/functionapp.zip"
}

resource "random_string" "storage_name" {
    length = 24
    upper = false
    lower = true
    number = true
    special = false
}

variable "storage_account_access_key" {
  description = "The access key for your Azure Storage Account."
}

variable "location" {
  default = "centralindia"
}

variable "vm_size" {
  default = "Standard_B2pls_v2"
}

variable "resource_group_name" {
  default = "smart-garden-rg"
}

variable "acr_name" {
  default = "smartgardenacr"
}

variable "container_name" {
  default = "smart-garden-app"
}
variable "groq_api_key" {
  description = "Groq API Key"
  sensitive   = true
}

variable "mongo_url" {
  description = "MongoDB Atlas connection string"
  sensitive   = true
}
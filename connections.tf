provider "google-beta" {
  credentials = file("sap-ds-demo-f1e20ee7706d.json")
  project     = var.host_project_id
  region      = var.region
}

provider "google" {
  credentials = file("sap-ds-demo-f1e20ee7706d.json")
  project     = var.host_project_id
  region      = var.region
}

/* 
provider "google" {
  credentials = file("~/.ssh/asset-management-test-3f8007228cc5.json")
  project     = var.project_id
  region      = var.region
}
*/

provider "google-beta" {
  credentials = file("/opt/app/data/service-account.json")
  project     = var.host_project_id
  region      = var.region
}

provider "google" {
  credentials = file("/opt/app/data/service-account.json")
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

resource "google_data_fusion_instance" "extended_instance" {
  count       = var.enable_datafusion ? 1 : 0
  provider    = "google-beta"
  name        = "google-fusion"
  description = "Data Fusion instance"
  region      = var.region
  type        = "BASIC"
  version     = "6.1.1"
}

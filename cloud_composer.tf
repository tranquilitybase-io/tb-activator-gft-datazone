resource "google_composer_environment" "composer" {
  count  = var.enable_composer ? 1 : 0
  name   = "composer"
  region = "europe-west2"

  config {

    node_count = 3
    node_config {
      zone         = var.zone
      machine_type = "n1-standard-1"
      #   subnetwork   = var.host_project_id
    }

    software_config {
      airflow_config_overrides = {
        core-load_example = "True"
      }

      pypi_packages = {
        numpy  = "==1.19.1"
        scipy  = "==1.1.0"
        pandas = "==1.1.0"
      }
    }
  }
}

# resource "google_composer_environment" "test" {
#   name   = "mycomposer"
#   region = "us-central1"
#   config {
#     node_count = 4

#     node_config {
#       zone         = "us-central1-a"
#       machine_type = "n1-standard-1"

#       network    = google_compute_network.test.id
#       subnetwork = google_compute_subnetwork.test.id

#       service_account = google_service_account.test.name
#     }
#   }

#   depends_on = [google_project_iam_member.composer-worker]
# }

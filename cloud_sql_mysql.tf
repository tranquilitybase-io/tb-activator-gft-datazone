### Cloud SQL MySQL instance ###

resource "random_id" "db_name_suffix" {
  byte_length = 4
}

resource "google_sql_database_instance" "mysql" {
  region           = var.region
  database_version = "MYSQL_5_7"
  name             = "experiment-tracking-db-${random_id.db_name_suffix.hex}"
  project          = var.host_project_id

  settings {
    tier              = "db-n1-standard-2"
    availability_type = "ZONAL"
    disk_autoresize   = true
    disk_size         = 250

    #     ip_configuration {
    #       ipv4_enabled    = false
    #       private_network = var.standard_subnetwork
    #     }

    location_preference {
      zone = var.zone
    }
  }

}


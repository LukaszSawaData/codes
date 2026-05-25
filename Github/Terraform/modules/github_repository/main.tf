resource "github_repository" "example" {
    name               = var.repository_name
    description        = var.repository_description
    visibility         = var.repository_visibility
    has_issues         = true
    has_projects       = true
    has_wiki           = false
    is_template        = false
    auto_init          = true
    gitignore_template = "Terraform"
    license_template   = "MIT"

    depends_on = [github_repository.example]
}

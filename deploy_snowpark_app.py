import sys
import os
import yaml

# Folders to skip
ignore_folders = ['.git', '__pycache__', '.ipynb_checkpoints']
snowflake_project_config_filename = 'snowflake.yml'

# Ensure root path is provided
if len(sys.argv) != 2:
    print("❌ Error: Root directory is required.")
    print("Usage: python deploy_snowpark_apps.py <root_directory>")
    sys.exit(1)

root_directory = sys.argv[1]
print(f"🚀 Deploying all Snowpark apps in root directory: {root_directory}\n")

# Walk through the directory structure
for (directory_path, directory_names, file_names) in os.walk(root_directory):
    base_name = os.path.basename(directory_path)

    # Skip ignored folders
    if base_name in ignore_folders:
        continue

    # Check for snowflake.yml to detect project
    if snowflake_project_config_filename not in file_names:
        continue

    print(f"✅ Found Snowflake project in folder: {directory_path}")

    # Load snowflake.yml
    project_settings = {}
    with open(os.path.join(directory_path, snowflake_project_config_filename), "r") as yamlfile:
        project_settings = yaml.load(yamlfile, Loader=yaml.FullLoader)

    # Check if it's a Snowpark project
    if 'snowpark' not in project_settings:
        print(f"⚠️ Skipping non-Snowpark project: {base_name}")
        continue

    print(f"📦 Project name: {project_settings['snowpark']['project_name']}")
    print(f"📤 Deploying project using Snow CLI...")

    # Change to project directory
    os.chdir(directory_path)

    # Build the Snowpark app
    os.system(
        f"snow snowpark build --temporary-connection "
        f"--account $SNOWFLAKE_ACCOUNT --user $SNOWFLAKE_USER --role $SNOWFLAKE_ROLE "
        f"--warehouse $SNOWFLAKE_WAREHOUSE --database $SNOWFLAKE_DATABASE"
    )

    # Deploy the app
    os.system(
        f"snow snowpark deploy --replace --temporary-connection "
        f"--account $SNOWFLAKE_ACCOUNT --user $SNOWFLAKE_USER --role $SNOWFLAKE_ROLE "
        f"--warehouse $SNOWFLAKE_WAREHOUSE --database $SNOWFLAKE_DATABASE"
    )

    print(f"✅ Deployed: {project_settings['snowpark']['project_name']}\n")

print("🎉 All projects deployed successfully.")
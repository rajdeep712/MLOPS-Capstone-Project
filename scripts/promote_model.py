# promote model

import os
import mlflow


def promote_model():
    # Set up DagsHub credentials for MLflow tracking
    dagshub_token = os.getenv("CAPSTONE_TEST")
    if not dagshub_token:
        raise EnvironmentError("CAPSTONE_TEST environment variable is not set")

    os.environ["MLFLOW_TRACKING_USERNAME"] = dagshub_token
    os.environ["MLFLOW_TRACKING_PASSWORD"] = dagshub_token

    dagshub_url = "https://dagshub.com"
    repo_owner = os.getenv("DAGSHUB_REPO_OWNER")
    repo_name = os.getenv("DAGSHUB_REPO_NAME")

    # Set up MLflow tracking URI
    mlflow.set_tracking_uri(f"{dagshub_url}/{repo_owner}/{repo_name}.mlflow")

    client = mlflow.MlflowClient()
    model_name = "my_model"

    try:
        # 1. Get the version currently marked as 'staging'
        staging_version_details = client.get_model_version_by_alias(
            model_name, alias="staging"
        )
        target_version = staging_version_details.version
    except mlflow.exceptions.MlflowException:
        print(
            f"No model version found with alias 'staging' for {model_name}. Aborting promotion."
        )
        return

    # 2. Find the current production model and archive it
    try:
        current_prod_details = client.get_model_version_by_alias(
            model_name, alias="production"
        )
        old_prod_version = current_prod_details.version

        # Remove the production alias from it
        client.delete_registered_model_alias(name=model_name, alias="production")

        # Explicitly tag it as archived so you don't lose track of past deployment states
        client.set_model_version_tag(
            name=model_name, version=old_prod_version, key="lifecycle", value="archived"
        )
        print(f"Archived previous production model (Version {old_prod_version})")
    except mlflow.exceptions.MlflowException:
        # This blocks triggers smoothly if there is no current production model
        print("No existing production model found to archive.")

    # 3. Promote the staging model to production
    client.set_registered_model_alias(
        name=model_name, alias="production", version=target_version
    )

    # 4. Clean up the staging alias since it's now in production
    client.delete_registered_model_alias(name=model_name, alias="staging")

    print(f"Model version {target_version} successfully promoted to Production!")


if __name__ == "__main__":
    promote_model()

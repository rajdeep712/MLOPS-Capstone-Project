import os
import mlflow
from dotenv import load_dotenv

load_dotenv()


def promote_model():
    # ------------------------------------------------------------------
    # Configure MLflow
    # ------------------------------------------------------------------
    token = os.getenv("CAPSTONE_TEST")
    if not token:
        raise EnvironmentError("CAPSTONE_TEST environment variable is not set")

    os.environ["MLFLOW_TRACKING_USERNAME"] = token
    os.environ["MLFLOW_TRACKING_PASSWORD"] = token

    mlflow.set_tracking_uri(
        f"https://dagshub.com/{os.getenv('DAGSHUB_REPO_OWNER')}/{os.getenv('DAGSHUB_REPO_NAME')}.mlflow"
    )

    client = mlflow.MlflowClient()

    model_name = "my_model"

    # ------------------------------------------------------------------
    # Find latest model in Staging
    # ------------------------------------------------------------------
    versions = list(client.search_model_versions(f"name='{model_name}'"))

    staging_versions = [v for v in versions if v.current_stage == "Staging"]

    if not staging_versions:
        raise Exception("No model found in Staging.")

    latest_staging = max(
        staging_versions,
        key=lambda v: int(v.version),
    )

    latest_staging_version = latest_staging.version

    print(f"Latest Staging Version : {latest_staging_version}")

    # ------------------------------------------------------------------
    # Archive all Production models
    # ------------------------------------------------------------------
    production_versions = [v for v in versions if v.current_stage == "Production"]

    for version in production_versions:
        client.transition_model_version_stage(
            name=model_name,
            version=version.version,
            stage="Archived",
        )
        print(f"Archived Version : {version.version}")

    # ------------------------------------------------------------------
    # Promote latest staging model
    # ------------------------------------------------------------------
    client.transition_model_version_stage(
        name=model_name,
        version=latest_staging_version,
        stage="Production",
    )

    print(f"Successfully promoted Version {latest_staging_version} to Production.")


if __name__ == "__main__":
    promote_model()

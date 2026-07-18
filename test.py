import os
import pickle
import unittest

import mlflow
import pandas as pd
from dotenv import load_dotenv
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
)

load_dotenv()


class TestModelLoading(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        token = os.getenv("CAPSTONE_TEST")

        if token is None:
            raise EnvironmentError("CAPSTONE_TEST environment variable not found.")

        os.environ["MLFLOW_TRACKING_USERNAME"] = token
        os.environ["MLFLOW_TRACKING_PASSWORD"] = token

        mlflow.set_tracking_uri(
            "https://dagshub.com/rajdeep712/MLOPS-Capstone-Project.mlflow"
        )

        cls.client = mlflow.MlflowClient()

        cls.model_name = "my_model"

        # --------------------------------------------------------------
        # Find latest model in Staging
        # --------------------------------------------------------------

        versions = list(cls.client.search_model_versions(f"name='{cls.model_name}'"))

        staging_versions = [v for v in versions if v.current_stage == "Staging"]

        if len(staging_versions) == 0:
            raise Exception("No model found in Staging stage.")

        latest = max(
            staging_versions,
            key=lambda x: int(x.version),
        )

        cls.model_version = latest.version

        print(f"\nLoading Model Version : {cls.model_version}")

        cls.model_uri = f"models:/{cls.model_name}/{cls.model_version}"

        cls.model = mlflow.pyfunc.load_model(cls.model_uri)

        cls.vectorizer = pickle.load(open("models/vectorizer.pkl", "rb"))

        cls.holdout_data = pd.read_csv("data/processed/test_bow.csv")

    # ------------------------------------------------------------------

    def test_model_loaded(self):
        self.assertIsNotNone(self.model)

    # ------------------------------------------------------------------

    def test_model_signature(self):

        text = "hi how are you"

        vector = self.vectorizer.transform([text])

        df = pd.DataFrame(
            vector.toarray(),
            columns=[str(i) for i in range(vector.shape[1])],
        )

        pred = self.model.predict(df)

        self.assertEqual(
            df.shape[1],
            len(self.vectorizer.get_feature_names_out()),
        )

        self.assertEqual(
            len(pred),
            1,
        )

    # ------------------------------------------------------------------

    def test_model_performance(self):

        X = self.holdout_data.iloc[:, :-1]
        y = self.holdout_data.iloc[:, -1]

        pred = self.model.predict(X)

        accuracy = accuracy_score(y, pred)
        precision = precision_score(y, pred)
        recall = recall_score(y, pred)
        f1 = f1_score(y, pred)

        print("\nAccuracy :", accuracy)
        print("Precision:", precision)
        print("Recall   :", recall)
        print("F1 Score :", f1)

        self.assertGreaterEqual(accuracy, 0.40)
        self.assertGreaterEqual(precision, 0.40)
        self.assertGreaterEqual(recall, 0.40)
        self.assertGreaterEqual(f1, 0.40)


if __name__ == "__main__":
    unittest.main(verbosity=2)

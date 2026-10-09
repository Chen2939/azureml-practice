"""
Train a heart-disease classifier inside the responsibleai-tabular environment
and save it as an MLflow model, so the RAI dashboard components can load it.
"""
import argparse
import glob
import os
import shutil
import tempfile

import mlflow.sklearn
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--train_data", type=str, help="Folder containing the training parquet")
    parser.add_argument("--target_column", type=str, help="Name of the label column")
    parser.add_argument("--model_output", type=str, help="Folder to write the MLflow model to")
    return parser.parse_args()


def main(args):
    files = glob.glob(os.path.join(args.train_data, "*.parquet"))
    print("Reading", files)
    df = pd.concat(pd.read_parquet(f) for f in files)

    y = df[args.target_column]
    X = df.drop(columns=args.target_column)

    # thal is a string category -> one-hot; every other column is already numeric
    model = Pipeline(
        steps=[
            (
                "prep",
                ColumnTransformer(
                    [("cat", OneHotEncoder(handle_unknown="ignore"), ["thal"])],
                    remainder="passthrough",
                ),
            ),
            ("clf", GradientBoostingClassifier(n_estimators=50, max_depth=2, random_state=0)),
        ]
    )
    model.fit(X, y)
    print("Train accuracy:", model.score(X, y))

    # The output folder already exists, and save_model refuses to write into an
    # existing folder, so save to a temp folder first and copy over.
    with tempfile.TemporaryDirectory() as tmp:
        tmp_model = os.path.join(tmp, "model")
        mlflow.sklearn.save_model(model, tmp_model)
        shutil.copytree(tmp_model, args.model_output, dirs_exist_ok=True)


if __name__ == "__main__":
    main(parse_args())

import asyncpg
import docker
import mlflow
import os
import re
from prefect import flow, task

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV, train_test_split

db_conn_str = os.environ["RSS_DB"]
ml_server_regex = re.compile("mlpredictserver")

@flow(log_prints=True)
async def train():
    """
    Main flow for training new model
    """
    source_id, content = await get_data()
    model_uri = model_fit(source_id, content)
    print(model_uri)
    restart_ml_server()
    return True

@task
async def get_data():
    source_id = []
    content = []
    conn = await asyncpg.connect(db_conn_str)
    async with conn.transaction():
        async for r in conn.cursor("select source_id, content from content"):
            source_id.append(r[0])
            content.append(r[1])
    await conn.close()
    return source_id, content

@task
def model_fit(source_id, content):
    """
    """
    mlflow.set_tracking_uri("http://mlflow:8080")
    mlflow.sklearn.autolog()
    experiment_name = "rss"
    if mlflow.get_experiment_by_name(experiment_name) is None:
        experiment_id = mlflow.create_experiment(experiment_name)
    else:
        experiment_id = mlflow.get_experiment_by_name(experiment_name).experiment_id
    # TODO grid search for best model?
    # svc = SVC()
    # parameters = {"kernel": ("linear", "rbf"), "C": [1, 10]}
    # clf = GridSearchCV(svc, parameters)
    with mlflow.start_run(experiment_id=experiment_id):
        pipe = Pipeline([("vectorize", TfidfVectorizer(ngram_range=(1, 2))), ("model", SVC())])
        X_train, X_test, y_train, y_test = train_test_split(content, source_id, test_size=0.2)
        pipe.fit(X_train, y_train)
        y_pred = pipe.predict(X_test)
        mlflow.log_metrics({"test_accuracy": accuracy_score(y_test, y_pred)})
        model = mlflow.sklearn.log_model(
            sk_model=pipe,
            artifact_path="rss_model",
            input_example=X_train[0],
            registered_model_name=f"rss_model",
        )
    return model.model_uri

@task
def restart_ml_server():
    """
    Restart model serving
    """
    client = docker.DockerClient()
    for container in client.containers.list():
        if bool(ml_server_regex.search(container.name)):
            container.restart()
    return True

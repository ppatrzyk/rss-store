import asyncpg
from datetime import datetime, timezone
import mlflow
import os
from prefect import flow, task

from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV, train_test_split

db_conn_str = os.environ["RSS_DB"]

@flow(log_prints=True)
async def train():
    """
    Main flow for training new model
    """
    source_id, content = await get_data()
    model_fit(source_id, content)
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
    run_ts = datetime.isoformat(datetime.now(timezone.utc))
    mlflow.set_tracking_uri("http://mlflow:8080")
    mlflow.sklearn.autolog()
    # TODO grid search for best model?
    # svc = SVC()
    # parameters = {"kernel": ("linear", "rbf"), "C": [1, 10]}
    # clf = GridSearchCV(svc, parameters)
    with mlflow.start_run():
        tfidf = TfidfVectorizer(ngram_range=(1, 2))
        terms = tfidf.fit_transform(content)
        X_train, X_test, y_train, y_test = train_test_split(terms, source_id, test_size=0.2, random_state=666)
        model = SVC()
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        mlflow.log_metrics({"accuracy": accuracy_score(y_test, y_pred)})
        # model.predict(tfidf.transform(["skandal hańba wstyd", ]))
        mlflow.sklearn.log_model(
            sk_model=model,
            artifact_path="rss_model",
            registered_model_name=f"rss_model_{run_ts}",
        )
    return True

import os
from flask import jsonify
from google.cloud import storage
from fastai.learner import load_learner
from fastai.vision.core import PILImage


storage_client = storage.Client()
bucket = storage_client.get_bucket("model-chef-oeuvre")
blob = bucket.blob("model.pkl")
model_path = "/tmp/model.pkl"
blob.download_to_filename(model_path)
learner = load_learner(model_path, cpu=True)


def run(request):

    files = request.data
    label, label_idx, preds = learner.predict(PILImage.create(files))
    preds = preds.numpy()

    if os.path.exists(model_path):
        os.remove(model_path)

    return jsonify(
        label=label,
        confidence=round(preds[label_idx] * 100, 2),
    )

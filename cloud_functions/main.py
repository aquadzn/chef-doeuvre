import os
from flask import jsonify
from google.cloud import storage
from fastai.learner import load_learner
from fastai.vision.core import PILImage


storage_client = storage.Client()
bucket = storage_client.get_bucket("model-chef-oeuvre")
blob = bucket.blob("model.pkl")
blob.download_to_filename("/tmp/model.pkl")
learner = load_learner("/tmp/model.pkl", cpu=True)


def run(request):

    files = request.data
    label, label_idx, preds = learner.predict(PILImage.create(files))
    preds = preds.numpy()

    os.remove("/tmp/model.pkl")

    return jsonify(
        label=label,
        confidence=round(preds[label_idx] * 100, 2),
    )

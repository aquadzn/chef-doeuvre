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

    return jsonify(
        label=label,
        confidence=round(preds[label_idx] * 100, 2),
    )


# URL version
# --------------
# def run(request):

#     response = r.get(
#         request.args["image"],
#         headers={
#             "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) \
# AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
#         },
#     )

#     label, label_idx, preds = learner.predict(PILImage.create(response.content))

#     return {
#         "label": f"{label.capitalize().replace('_', ' ')}",
#         "confidence": f"{preds[label_idx] * 100:.2f}%",
#     }

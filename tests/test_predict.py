import time
from fastai.vision.all import load_learner, PILImage


def predict(filename):
    img = PILImage.create(filename)
    learner = load_learner("model.pkl")

    return learner.predict(img)


def test_predict():
    preds = predict("/home/william/Desktop/chef-oeuvre/tests/guacamole.jpg")
    assert preds is not None and len(preds) == 3


def test_prediction_time():
    start = time.time()
    _ = predict("/home/william/Desktop/chef-oeuvre/tests/guacamole.jpg")
    exec_time = time.time() - start
    assert exec_time <= 2.0

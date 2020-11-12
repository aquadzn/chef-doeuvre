from fastai.vision.all import load_learner, PILImage


def predict(filename):
    img = PILImage.create(filename)
    learner = load_learner("model.pkl")

    return learner.predict(img)


def test_predict():
    preds = predict("/home/william/Desktop/chef-oeuvre/tests/guacamole.jpg")
    assert preds is not None and len(preds) == 3

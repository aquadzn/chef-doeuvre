from fastai.vision.all import load_learner


learner = load_learner("model.pkl", cpu=True)

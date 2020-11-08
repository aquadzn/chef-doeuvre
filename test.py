import os
from fastai.vision.all import load_learner


model = load_learner("model.pkl", cpu=True)
pred = model.predict("app/static/img/user.png")

print(pred)

model.export(os.path.abspath("./gcp_model.pkl"))

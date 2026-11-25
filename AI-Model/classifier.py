import torch, timm, json
from torchvision import transforms

classes = json.load(open("classes.json"))
model = timm.create_model("efficientnet_b0", num_classes=len(classes))
model.load_state_dict(torch.load("model.pth", map_location="cpu"))
model.eval()

tf = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485,0.456,0.406],[0.229,0.224,0.225]),
])

healthy_idx = [i for i, c in enumerate(classes) if "healthy" in c.lower()]

def predict(image):
    x = tf(image.convert("RGB")).unsqueeze(0)
    with torch.no_grad():
        probs = torch.softmax(model(x), dim=1)[0]
    conf, idx = probs.max(0)
    disease_prob = 1 - sum(probs[i].item() for i in healthy_idx)
    if conf < 0.6:
        return "Unclear - photo dobara lo", conf.item(), 0.0
    return classes[idx], conf.item(), disease_prob
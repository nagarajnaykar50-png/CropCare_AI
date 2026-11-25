import timm, torch, json
from torchvision import datasets, transforms
from torch.utils.data import DataLoader, random_split, Subset
import random

MAX_PER_CLASS = 400   # CPU ke liye chhota; GPU ho to 100000 kar do
EPOCHS = 4

device = "cuda" if torch.cuda.is_available() else "cpu"
print("Using:", device)

tf = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.RandomHorizontalFlip(),
    transforms.ColorJitter(0.3, 0.3, 0.3),
    transforms.ToTensor(),
    transforms.Normalize([0.485,0.456,0.406],[0.229,0.224,0.225]),
])
ds = datasets.ImageFolder("data/tomato_potato", transform=tf)

# har class se max MAX_PER_CLASS images (balance + speed)
by_class = {}
for i, (_, y) in enumerate(ds.samples):
    by_class.setdefault(y, []).append(i)
idx = []
for y, lst in by_class.items():
    random.shuffle(lst)
    idx += lst[:MAX_PER_CLASS]
sub = Subset(ds, idx)

n_val = int(0.2 * len(sub))
train_ds, val_ds = random_split(sub, [len(sub) - n_val, n_val])
train = DataLoader(train_ds, batch_size=32, shuffle=True)
val = DataLoader(val_ds, batch_size=32)

model = timm.create_model("efficientnet_b0", pretrained=True,
                          num_classes=len(ds.classes)).to(device)
opt = torch.optim.AdamW(model.parameters(), lr=1e-3)
loss_fn = torch.nn.CrossEntropyLoss()

for epoch in range(EPOCHS):
    model.train()
    for x, y in train:
        x, y = x.to(device), y.to(device)
        opt.zero_grad()
        loss_fn(model(x), y).backward()
        opt.step()
    model.eval(); correct = 0
    with torch.no_grad():
        for x, y in val:
            correct += (model(x.to(device)).argmax(1).cpu() == y).sum().item()
    print("epoch", epoch, "val acc:", correct / n_val)

json.dump(ds.classes, open("classes.json", "w"))
torch.save(model.state_dict(), "model.pth")
print("Saved model.pth and classes.json")
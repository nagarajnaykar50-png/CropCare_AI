import numpy as np
from pytorch_grad_cam import GradCAM
from pytorch_grad_cam.utils.image import show_cam_on_image
from classifier import model, tf

cam = GradCAM(model=model, target_layers=[model.conv_head])

def gradcam(image):
    img = image.convert("RGB")
    rgb = np.array(img.resize((224, 224))).astype(np.float32) / 255.0
    heat = cam(input_tensor=tf(img).unsqueeze(0))[0]
    return show_cam_on_image(rgb, heat, use_rgb=True)
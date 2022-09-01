import os
import json
from io import BytesIO

import click
import requests
from PIL import Image
from timm.models import create_model
from torch.nn.functional import softmax
from torchvision import transforms


IMAGENET_DEFAULT_MEAN = (0.485, 0.456, 0.406)
IMAGENET_DEFAULT_STD = (0.229, 0.224, 0.225)

@click.command()
@click.option("--model", default="resnet152", help="mode name to be used for infrence")
@click.option("--image", help="image url or path")
def main(model, image):
    labels2class = json.load(open("imagenet1000_labels.json", "r"))

    model = create_model(
        model, pretrained=True)

    if "http" in image:
        response = requests.get(image)
        img = Image.open(BytesIO(response.content)).convert("RGB")
    else:
        img = Image.open(image).convert("RGB")
    
    # print(img.size)
    img.save("down.png")
    augs = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(), 
        transforms.Normalize(IMAGENET_DEFAULT_MEAN, IMAGENET_DEFAULT_STD)
    ])

    img = augs(img).unsqueeze(0)
    out = model(img)
    out = softmax(out, dim=1)
    idx = out.argmax().item()
    # print(out)
    # print(out.shape)
    # print(out[0,idx])
    print(json.dumps({"predicted": labels2class[str(idx)], "confidence": out[0,idx].item()}))

if __name__=="__main__":
    main()

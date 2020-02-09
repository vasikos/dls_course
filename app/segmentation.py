from PIL import Image, ImageDraw
import numpy as np
import matplotlib.pyplot as plt
import torch
from torchvision import models
import torchvision.transforms as T


class Segmentator():
  def __init__(self, image_path):
    self.im_path = image_path
    l = self.load_img()
    print('Image loaded')
    s = self.segment_img(l)
    print('Image segmented')
    self.save_img(s)
    print('Image saved')
    del self

  def load_img(self):
    img = Image.open(self.im_path)
    trf = T.Compose([T.Resize(300),
                     T.ToTensor(),
                     T.Normalize(mean=[0.485, 0.456, 0.406],
                                 std=[0.229, 0.224, 0.225])])
    inp = trf(img).unsqueeze(0)
    return inp

  def segment_img(self, img):
    fcn = models.segmentation.fcn_resnet101(pretrained=True).eval()
    out = fcn(img)['out']
    del fcn
    om = torch.argmax(out.squeeze(), dim=0).detach().cpu().numpy()
    return om

  def save_img(self, img):
    color_voc = {0: (0, 0, 0), 1:(128, 0, 0), 2:(0, 128, 0), 
            3:(128, 128, 0), 4:(0, 0, 128), 5:(128, 0, 128),
            6:(0, 128, 128), 7:(128, 128, 128), 8:(64, 0, 0), 
            9:(192, 0, 0), 10:(64, 128, 0), 11:(192, 128, 0), 
            12:(64, 0, 128), 13:(192, 0, 128), 14:(64, 128, 128), 
            15:(192, 128, 128), 16:(0, 64, 0), 17:(128, 64, 0), 
            18:(0, 192, 0), 19:(128, 192, 0), 20:(0, 64, 128)}
    base = T.Resize(300)(Image.open(self.im_path))
    draw = ImageDraw.Draw(base)
    for i in range(base.size[0]):
        for j in range(base.size[1]):
            draw.point((i, j), color_voc[img[j, i]])
    base.save('static/segmented/' + self.im_path.split('/')[-1])


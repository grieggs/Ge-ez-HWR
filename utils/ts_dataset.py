import json

import torch
from torch.utils.data import Dataset
import os
from PIL import Image
import numpy as np
import glob
import utils.string_utils as string_utils

PADDING_CONSTANT = 1

def collate(batch):
    batch = [b for b in batch if b is not None]
    #These all should be the same size or error
    # print(len(set([b['line_img'].shape[0] for b in batch])))
    # print(len(set([b['line_img'].shape[2] for b in batch])))
    if len(set([b['line_img'].shape[0] for b in batch])) == 0 or len(set([b['line_img'].shape[2] for b in batch])) == 0:
        return None
    try:
        assert len(set([b['line_img'].shape[0] for b in batch])) == 1
        assert len(set([b['line_img'].shape[2] for b in batch])) == 1
    except AssertionError:
        print("BAD!")

    dim0 = batch[0]['line_img'].shape[0]
    dim1 = max([b['line_img'].shape[1] for b in batch])
    dim1 = dim1 + (dim0 - (dim1 % dim0))
    dim2 = batch[0]['line_img'].shape[2]

    input_batch = np.full((len(batch), dim0, dim1, dim2), PADDING_CONSTANT).astype(np.float32)
    for i in range(len(batch)):
        b_img = batch[i]['line_img']
        input_batch[i,:,:b_img.shape[1],:] = b_img

    line_imgs = input_batch.transpose([0,3,1,2])
    line_imgs = torch.from_numpy(line_imgs)

    return {
        "line_imgs": line_imgs,
        'image_path': [b['image_path'] for b in batch]
    }

class TsDataset(Dataset):
    def __init__(self,  char_to_idx, img_height=32, root_path="."):
        # {"gt": "\u120d\u12a6\u1361\u12c8\u12ed\u1264\u120e\u1361\u12a2\u1275\u12c8\u12f5\u12a5\u1361\u120a", "image_path": "images/1542.jpg", "err": false}
        self.root_path = root_path
        self.img_height = img_height
        self.char_to_idx = char_to_idx
        self.data = sorted(glob.glob(os.path.join(root_path,"*")))
        #remove text files
        self.data = [num for num in self.data if num[-3:] != 'txt' and num[-3:] != 'csv']


    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        item = self.data[idx]
        test = item
        try:
            img = Image.open(test).convert("RGB")
        except:
            print("Error loading file: ", item, "Is it an image?")
            return None
        if img is None:
            print("Warning: image is None:", item)
            return None
        percent = float(self.img_height) / img.size[1]
        img = np.asarray(img.resize((int(img.size[0]*percent),self.img_height), Image.ANTIALIAS))

        img = img.astype(np.float32)
        img = img / 128.0 - 1.0

        return {
            "line_img": img,
            "image_path": item
        }

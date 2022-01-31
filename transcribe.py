from __future__ import print_function
import json
import utils.character_set as character_set
import sys
import utils.ts_dataset as ts_dataset
from utils.ts_dataset import TsDataset
import csv
import utils.crnn as crnn
import os
import torch
from torch.utils.data import DataLoader
from torch.autograd import Variable
import utils.error_rates as error_rates
import utils.string_utils as string_utils
import time
import numpy as np
from torch.utils import data
import sys
sys.path.insert(0, 'CTCDecoder/src')
from tqdm import tqdm


def main():


    torch.manual_seed(68)
    torch.backends.cudnn.deterministic = True

    print(torch.LongTensor(10).random_(0, 10))

    config_path = sys.argv[1]
    print(config_path)
    RIMES = (config_path.find('rimes') != -1)
    print(RIMES)
    with open(config_path) as f:
        config = json.load(f)

    with open(config_path) as f:
        paramList = f.readlines()

    baseMessage = ""

    for line in paramList:
        baseMessage = baseMessage + line


    idx_to_char, char_to_idx = character_set.load_char_set(config['character_set_path'])
    print(idx_to_char)
    val_dataset = TsDataset(char_to_idx, img_height=config['network']['input_height'], root_path=config['image_root_directory'])

    val_dataloader = DataLoader(val_dataset, batch_size=config['batch_size'], shuffle=False, num_workers=1,
                                 collate_fn=ts_dataset.collate)
    hw = crnn.create_model({
        'input_height': config['network']['input_height'],
        'cnn_out_size': config['network']['cnn_out_size'],
        'num_of_channels': 3,
        'num_of_outputs': len(idx_to_char) + 1
    })
    state_dict = torch.load(config['model_load_path'])
    hw.load_state_dict(state_dict)

    if torch.cuda.is_available():
        hw.cuda()
        dtype = torch.cuda.FloatTensor
        print("Using GPU")
    else:
        dtype = torch.FloatTensor
        print("No GPU detected")
    output = {}
    tot_ce = 0.0
    tot_we = 0.0
    sum_loss = 0.0
    sum_wer = 0.0
    steps = 0.0
    hw.eval()
    for x in tqdm(val_dataloader, total=len(val_dataloader)):
        if x is None:
            continue
        with torch.no_grad():
            line_imgs = Variable(x['line_imgs'].type(dtype), requires_grad=False)
            preds = hw(line_imgs)
            output_batch = preds.permute(1, 0, 2)
            out = output_batch.data.cpu().numpy()
            for i, image_path in enumerate(x['image_path']):
                logits = out[i, ...]
                pred, raw_pred = string_utils.naive_decode(logits)
                pred_str = string_utils.label2str(pred, idx_to_char, False)
                output[os.path.basename(image_path)] = pred_str
                steps += 1

    for x in output:
        print(x +": " + output[x])
    out = os.path.join(config['image_root_directory'],'out.csv')
    print(out)
    with open(out, 'w') as f:
        field_names = ['image','transcription']
        dict_writer = csv.DictWriter(f, fieldnames=field_names)
        dict_writer.writeheader()
        for x in output:
            dict_writer.writerow({'image': x, 'transcription': output[x]})

    hw.eval()

if __name__ == "__main__":
    main()
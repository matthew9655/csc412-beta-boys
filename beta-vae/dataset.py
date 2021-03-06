"""dataset.py"""

import os
import numpy as np

import torch
from torch.utils.data import Dataset, DataLoader
from torchvision.datasets import ImageFolder
from torchvision import transforms


def is_power_of_2(num):
    return ((num & (num - 1)) == 0) and num != 0


class CustomImageFolder(ImageFolder):
    def __init__(self, root, transform=None):
        super(CustomImageFolder, self).__init__(root, transform)

    def __getitem__(self, index):
        path = self.imgs[index][0]
        img = self.loader(path)
        if self.transform is not None:
            img = self.transform(img)

        return img


class CustomTensorDataset(Dataset):
    def __init__(self, data_tensor):
        self.data_tensor = data_tensor

    def __getitem__(self, index):
        return self.data_tensor[index]

    def __len__(self):
        return self.data_tensor.size(0)


def return_data(dset, dset_dir, batch_size, num_workers, image_size):
    name = dset
    dset_dir = dset_dir
    batch_size = batch_size
    num_workers = num_workers
    image_size = image_size
    assert image_size == 64, 'currently only image size of 64 is supported'

    if name.lower() == 'celeba':
        root = os.path.join(dset_dir, 'celebA.pt')
        data = torch.load(root)
        data = data.unsqueeze(1).float()
        train_kwargs = {'data_tensor':data}
        dset = CustomTensorDataset

    elif name.lower() == 'dsprites':
        root = os.path.join(dset_dir, 'dsprites_ndarray_co1sh3sc6or40x32y32_64x64.npz')
        if not os.path.exists(root):
            print('dsprites npz file does not exist')
        data = np.load(root, encoding='bytes')
        rand = np.random.permutation(737280)[:150000]
        data = torch.from_numpy(data['imgs'][rand]).unsqueeze(1).float()
        train_kwargs = {'data_tensor':data}
        dset = CustomTensorDataset

    else:
        raise NotImplementedError


    train_data = dset(**train_kwargs)
    train_loader = DataLoader(train_data,
                              batch_size=batch_size,
                              shuffle=True,
                              num_workers=num_workers,
                              pin_memory=True,
                              drop_last=True)

    data_loader = train_loader

    return data_loader, len(train_data)

if __name__ == '__main__':
    pass

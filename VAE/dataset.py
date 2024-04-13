import pandas as pd
import numpy as np
import torch
from torch.utils.data import Dataset

class TSDataset(Dataset):
    def __init__(self, split, datasets_root, cont_vars=None, cat_vars=None, lbl_as_feat=True):
        super().__init__()
        assert split in ['train', 'test', 'both']
        self.datasets_root = datasets_root
        self.lbl_as_feat = lbl_as_feat
        if split == 'train':
            self.df = pd.read_csv(self.datasets_root / 'train.csv')
        elif split == 'test':
            self.df = pd.read_csv(self.datasets_root / 'test.csv')
        else:
            df1 = pd.read_csv(self.datasets_root / 'train.csv')
            df2 = pd.read_csv(self.datasets_root / 'test.csv')
            self.df = pd.concat((df1, df2), ignore_index=True)

        # Select continuous variables to use
        if cont_vars:
            self.cont_vars = cont_vars
            # If we want to use 'value' as a feature, ensure it is returned
            if self.lbl_as_feat:
                try:
                    assert 'Битрейт (КБ/сек)' in self.cont_vars
                except AssertionError:
                    self.cont_vars.insert(0, 'Битрейт (КБ/сек)')
            # If not, ensure it not returned as a feature
            else:
                try:
                    assert 'Битрейт (КБ/сек)' not in self.cont_vars
                except AssertionError:
                    self.cont_vars.remove('Битрейт (КБ/сек)')

        else:  # if no list provided, use all available
            self.cont_vars = ['Ширина', 'Высота', 'Шаг', 'Время', 'Битрейт (КБ/сек)']

        # Select categorical variables to use
        if cat_vars:
            self.cat_vars = cat_vars
        else:  # if no list provided, use all available
            self.cat_vars = ['day', 'month', 'Кодек']

        # Finally, make two Numpy arrays for continuous and categorical
        # variables, respectively:
        if self.lbl_as_feat:
            self.cont = self.df[self.cont_vars].copy().to_numpy(dtype=np.float32)
        else:
            self.cont = self.df[self.cont_vars].copy().to_numpy(dtype=np.float32)
            self.lbl = self.df['Битрейт (КБ/сек)'].copy().to_numpy(dtype=np.float32)
        self.cat = self.df[self.cat_vars].copy().to_numpy(dtype=np.int64)

    def __getitem__(self, idx):
        if self.lbl_as_feat:  # for VAE training
            return torch.tensor(self.cont[idx]), torch.tensor(self.cat[idx])
        else:  # for supervised prediction
            return torch.tensor(self.cont[idx]), torch.tensor(self.cat[idx]), torch.tensor(self.lbl[idx])

    def __len__(self):
        return self.df.shape[0]
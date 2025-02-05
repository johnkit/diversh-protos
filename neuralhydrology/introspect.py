""""""

import argparse

import torch

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Introspect pytorch model')
    parser.add_argument('pt_file', help='Pytorch model file (.pt)')
    args = parser.parse_args()

    model = torch.load(args.pt_file, weights_only=True)
    print(type(model))
    # print(model)
    print()

    for key, value in model.items():
        print(key, value.shape)
    print()

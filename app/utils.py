from visdom import Visdom
import numpy as np

import time
import warnings

from os.path import exists, join, dirname, abspath
import os


class VisdomLinePlotter(object):
    """Plots to Visdom"""
    def __init__(self, env_name='main'):
        self.viz = Visdom()
        self.env = env_name
        self.plots = {}
    def plot(self, var_name, split_name, title_name, x, y):
        if var_name not in self.plots:
            self.plots[var_name] = self.viz.line(X=x, Y=y, env=self.env, opts=dict(
                legend=[split_name],
                title=title_name,
                xlabel='Epochs',
                ylabel=var_name
            ))
        else:
            self.viz.line(X=x, Y=y, env=self.env, win=self.plots[var_name], name=split_name, update = 'replace')




def get_package_path(package_name=None):
    # if the package name is none, it returns path to aml folder
    if package_name is None:

        package_name = '/'.join(dirname(dirname(abspath(__file__))).split('/'))

    else:

        package_name = '/'.join(dirname(dirname(abspath(__file__))).split('/')) + '/' + package_name

    return package_name


def get_abs_path(path):
    return abspath(path)


def crawl(path, extension_filter='jpg'):
    crawled_paths = {}
    for dirpath, subs, files in os.walk(path):
        for file in files:
            # file_tmp = file.split('_')
            # print("ftmp: ", file_tmp)
            # file_fixed = "%0.4d_%s_%s"%(int(file_tmp[0]),file_tmp[1],file_tmp[2])
            # print(file_fixed)
            if extension_filter is None:
                crawled_paths[file] = os.path.join(dirpath, file)
            elif file.split('.')[-1] == extension_filter:
                crawled_paths[file] = os.path.join(dirpath, file)

    return crawled_paths
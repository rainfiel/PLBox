# -*- coding: utf-8 -*-

import os

def update(path):
	return os.system("svn up %s"%path) == 0

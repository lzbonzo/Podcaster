# -*- coding: utf-8 -*-

import daemon
import PodcasterBot

with daemon.DaemonContext():
    PodcasterBot()

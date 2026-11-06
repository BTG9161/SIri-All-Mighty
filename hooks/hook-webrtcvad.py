import os
import glob
import webrtcvad

module_dir = os.path.dirname(webrtcvad.__file__)

binaries = [
    (path, ".")
    for path in glob.glob(
        os.path.join(module_dir, "_webrtcvad*.so")
    )
]

datas = []
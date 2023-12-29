import shutil


def cp_files(f,t):
    original = f
    target   = t
    shutil.copyfile(original, target)
#cp_files('c:/xaos.csv','./tmp/xas1.csv')
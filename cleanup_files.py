import os
# screenshots deletion basic script
filespath = os.path.expandvars('$HOME/Desktop')


def main():
    filelist = [files for files in os.listdir(filespath) if files.endswith(".png")]
    if len(filelist) == 0:
        print(f"No screenshots to delete in {filespath}")
    else:
        print("Screenshots to delete:", filelist)
        for files in filelist:
            os.remove(os.path.join(filespath, files))


if __name__ == '__main__':
    main()

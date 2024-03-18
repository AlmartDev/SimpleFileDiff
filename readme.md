# Simple File Diff
Compare two files with this simple python script!
No extra modules needed, just plain python!

# Usage
Make sure you have python and git installed!
```sh
git clone https://github.com/AlmartDev/SimpleFileDiff.git sfd
cd sfd
python compareDiff.py <file 1> <file 2>
```

### Arguments
```
usage: Simple File Diff [-h] [--version] [--clear] <file1> <file2>

positional arguments:
  file1          The first file to compare
  file2          The second file to compare

options:
  -h, --help     show this help message and exit
  --version, -v  show program's version number and exit
  --clear, -c    Clear the screen before showing the diff

```

# TODO
- the program adds lines to the shorter file to make them even to prevent out of index errors, what makes the last empty lines not count as modifyed!

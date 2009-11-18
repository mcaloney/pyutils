import os, os.path, sys, shutil
from hashlib import md5
from optparse import OptionParser

def hash_directory(hashes, directory, files):
    for filename in files:
        fullpath = os.path.join(directory, filename)
        if not os.path.isdir(fullpath):
            m = md5()
            m.update(open(fullpath).read())
            if hashes.has_key(m.hexdigest()):
                print 'DUPLICATE FOUND FOR', m.hexdigest()
                hashes[m.hexdigest()].append(fullpath)
            else:
                hashes[m.hexdigest()] = [fullpath]

def print_files_and_md5(arg, directory, files):
    for filename in files:
        fullpath = os.path.join(directory, filename)
        if not os.path.isdir(fullpath):
            m = md5()
            m.update(open(fullpath).read())
            print fullpath, m.hexdigest()

def print_all_files(arg, directory, files):
    for filename in files:
        print os.path.join(directory, filename)

def dump_to_file(data, filename):
    output_file = open(filename, 'w')
    output_file.write(repr(data))
    output_file.close()

def main():
    usage = 'usage: %prog [options] folder'
    parser = OptionParser(usage)
    parser.add_option('-o', '--output', dest='output_dir',
                      help='output directory')
    parser.add_option('-v', '--verbose', dest='verbose',
                      default=True, help='verbose mode')
    (options, args) = parser.parse_args()
    if len(args) != 1:
        parser.error('incorrect number of arguments')

if __name__ == '__main__':
    # options:
    #   - base output directory
    #   - location of files to check
    #   - whether to rename originals or try to choose a representative "intelligently"
    #       - this would need to be consistent across similarly-named duplicate items
    #   - file type filter

    hashes = {}
    # walk through the directory structure, hashing the files in each subdir
#    os.path.walk(os.path.expandvars('$HOME/Desktop/iPhoto Library'), hash_directory, hashes)
#    # dump the hashes to a separate file so I don't have to keep regenerating them
#    # while testing this
#    dump_to_file(hashes, '/Users/mcaloney/src/pyutils/hash_values')
#    sys.exit(0)

    # while testing, use our cached hashes list
    hashes = eval(open('/Users/mcaloney/src/pyutils/hash_values', 'r').read())

    # sort the files: pick a representative from each equiv class and
    # put it in an 'originals' dir with its hashcode as its filename
    # the rest go in hashcode-distinguished subdirs of 'duplicates'
    # so that they can be "easily" verified.
    output_dir = '/Users/mcaloney/images'
    duplicates_dir_name = 'duplicates'
    originals_dir_name = 'originals'
    duplicates_dir = os.path.join(output_dir, duplicates_dir_name)
    originals_dir = os.path.join(output_dir, originals_dir_name)
    try:
        os.makedirs(duplicates_dir)
        os.makedirs(originals_dir)
    except OSError, e:
        print e
        sys.exit(1)

    for hash, files in hashes.items():
        extension = os.path.splitext(files[0])[1]
        original_name = os.path.join(originals_dir, hash + extension)
        shutil.copy(files[0], original_name)

        # if there were multiple files with this hashcode, copy all
        # of them to the duplicates dir
        if len(files) > 1:
            os.mkdir(os.path.join(duplicates_dir, hash))
            for index in range(len(files)):
                shutil.copy(files[index], os.path.join(duplicates_dir, hash, str(index) + extension))

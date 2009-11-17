import os.path
from hashlib import md5

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

if __name__ == '__main__':
    hashes = {}
    # walk through the directory structure, hashing the files in each subdir
#    os.path.walk(os.path.expandvars('$HOME/Desktop/test_docs'), hash_directory, hashes)
#    # dump the hashes to a separate file so I don't have to keep regenerating them
#    # while testing this
#    dump_to_file(hashes, '/Users/mcaloney/src/pyutils/hash_values')

    # while testing, use our cached hashes list
    hashes = eval(open('/Users/mcaloney/src/pyutils/hash_values', 'r').read())

    # sort the files; pick a representative from each equiv class and
    # put it in an 'originals' dir with its hashcode as its filename
    # the rest go in hashcode-distinguished subdirs of 'duplicates'
    # so that they can be "easily" verified.
    output_dir = '/Users/mcaloney/images'
    duplicates_dir_name = 'duplicates'
    originals_dir_name = 'originals'
    duplicates_dir = os.path.join(output_dir, duplicates_dir_name)
    for hash, files in hashes.items():
        original_name = hash + splitext(basename(files[0]))[1]

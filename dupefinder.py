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

def split_duplicates(items, filter_fn):
    originals = []
    duplicates = []
    for duplicate_list in items:
        orig, dupe = filter_fn(duplicate_list)
        originals.append(orig)
        duplicates.extend(dupe)
    return originals, duplicates

def print_all_files(arg, directory, files):
    for filename in files:
        print os.path.join(directory, filename)

if __name__ == '__main__':
    hashes = {}
    # walk through the directory structure, hashing the files in each subdir
    os.path.walk(os.path.expandvars('$HOME/Desktop/test_docs'), hash_directory, hashes)

    # in a separate processing step, need to iterate through the hashes
    # determining which of the duplicate files is the "original".
    # Since all files have a common base directory, the "original":
    #   - has the shallowest directory structure, and
    #   - the earliest creation date

    def file_list_cmp(x, y):
        # compare the filenames by number of path components, then ctime
        x_path_len = x.count(os.path.sep)
        y_path_len = y.count(os.path.sep)
        if x_path_len != y_path_len:
            return cmp(x_path_len, y_path_len)
        return cmp(os.path.getctime(x), os.path.getctime(y))

    def file_list_filter(filenames):
        if len(filenames) == 0:
            raise IndexError
        # sort the filenames by our ranking criteria
        filenames.sort(file_list_cmp)
        return filenames[0], filenames[1:]

    originals, duplicates = split_duplicates(hashes.values(), file_list_filter)

    # dump the hashes to a separate file so I don't have to keep regenerating them
    # while testing this
    output_file = open(os.path.expandvars('$HOME/Desktop/test_docs/hash_values'), 'w')
    output_file.write(repr(hashes))
    output_file.close()

    # sanity testing
#    print 'Finished gathering duplicates; checking ...'
#    for k,v in hashes.items():
#        if len(v) > 1:
#           filenames = map(os.path.basename, v)
#           if (len(set(filenames)) > 1):
#               print 'COLLISION:', ','.join(filenames)

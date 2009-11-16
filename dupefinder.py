import os.path
from hashlib import md5

def find_duplicates(hashes, directory, files):
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

if __name__ == '__main__':
    hashes = {}
    os.path.walk(os.path.expandvars('$HOME/Desktop/test_docs'), find_duplicates, hashes)

    # dump the hashes to a separate file so I don't have to keep regenerating them
    # while testing this
    output_file = open(os.path.expandvars('$HOME/Desktop/test_docs/hash_values'), 'w')
    output_file.write(repr(hashes))
    output_file.close()

    # sanity testing
#    print 'Finished gathering duplicates; checking ...'
#    for k,v in hashes.items():
#        if len(v) > 1:
#           filenames = zip(map(os.path.split, v))[1]
#           if (len(set(filenames)) > 1):
#               print 'COLLISION:', ','.join(filenames)

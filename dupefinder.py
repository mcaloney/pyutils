import os, os.path, sys, shutil
from hashlib import md5
from optparse import OptionParser

def hash_all_orientations(filename):
    import Image
    img_hashes = []
    try:
        img = Image.open(filename)
        
        # compute hashes for all four orientations
        # we explicitly rotate the image four times (rather than just hashing
        # the original image and three 90 degree rotations) because Image.save()
        # throws away EXIF data, so we need all four hashes to be without EXIF
        # data.
        for i in range(4):
            img = img.transpose(Image.ROTATE_90)
            m = md5()
            m.update(img.tostring())
            img_hashes.append(m.hexdigest())
    except IOError, e:
        print 'Failed to open file %s: %s' % (filename, e)

    return img_hashes

def hash_directory(hashes, directory, files):
    for filename in files:
        fullpath = os.path.join(directory, filename)
        if not os.path.isdir(fullpath):
            img_hashes = hash_all_orientations(fullpath)
            for hash_val in img_hashes:
                if hashes.has_key(hash_val):
                    print 'DUPLICATE FOUND FOR', hash_val
                    hashes[hash_val].append(fullpath)
                else:
                    hashes[hash_val] = [fullpath]

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
    parser.add_option('--hashes', dest='hashes_file',
                      help='load precomputed duplicate list from a separate file')
    parser.add_option('-n', '--dry-run',
                      action='store_true', dest='dry_run', default=False,
                      help='do not copy files; output list of duplicates and exit')
    parser.add_option('-o', '--output', dest='output_dir',
                      help='output directory')
    parser.add_option('-v', '--verbose',
                      action='store_true', dest='verbose', default=False,
                      help='verbose mode')
    (options, args) = parser.parse_args()
    if len(args) != 1:
        parser.error('incorrect number of arguments')
    
    # if precomputed hashes are provided, don't recompute them
    if options.hashes_file:
        options.hashes_file = options.hashes_file if os.path.isabs(options.hashes_file) else os.path.abspath(options.hashes_file)
        hashes = eval(open(options.hashes_file).read())
    else:
        # normalize the path we've been sent
        search_root = args[0] if os.path.isabs(args[0]) else os.path.abspath(args[0])
        hashes = dict()
        # walk through the directory structure, hashing the files in each subdir
        os.path.walk(search_root, hash_directory, hashes)

        # dump the hashes to a separate file for testing
        dump_to_file(hashes, os.path.expandvars('$HOME/dupefinder_hashes'))

        # if we need to output the hashes to stdout
        if options.dry_run or options.verbose:
            for hash, files in hashes.items():
                print hash, '\n\t', '\n\t'.join(files)

        # if it's a dry run, then we're finished
        if options.dry_run:
            sys.exit(0)

    # sort the files
    if not options.dry_run:
        sort_files(options.output_dir, hashes, return_first)

def sort_files(base_directory, hashes, original_selector):
    # sort the files: pick a representative from each equiv class and
    # put it in an 'originals' dir with its hashcode as its filename
    # the rest go in hashcode-distinguished subdirs of 'duplicates'
    # so that they can be "easily" verified.
    duplicates_dir_name = 'duplicates'
    originals_dir_name = 'originals'
    duplicates_dir = os.path.join(base_directory, duplicates_dir_name)
    originals_dir = os.path.join(base_directory, originals_dir_name)
    try:
        os.makedirs(duplicates_dir)
        os.makedirs(originals_dir)
    except OSError, e:
        print e
        sys.exit(1)

    for hash, files in hashes.items():
        original_file = original_selector(files)
        extension = os.path.splitext(original_file)[1]
        original_name = os.path.join(originals_dir, hash + extension)
        shutil.copy(original_file, original_name)

        # if there were multiple files with this hashcode, copy all
        # of them to the duplicates dir
        if len(files) > 1:
            os.mkdir(os.path.join(duplicates_dir, hash))
            for index in range(len(files)):
                shutil.copy(files[index], os.path.join(duplicates_dir, hash, str(index) + extension))

def return_first(a_list):
    return a_list[0]

if __name__ == '__main__':
    main()

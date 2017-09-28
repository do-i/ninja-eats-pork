#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This script is a utility tool to re-organize files and directories.
Original purpose was to reduce number of sub directories and increase number of files in each sub directory.
"""

import argparse
import os


def zero_pad_dir(input_dir, dir_prefix):
    """
    Rename 1 level sub directory under input_dir to zero padded.
    It is required that all sub directory name must be numerical and less than 1000.
    TODO remove hardcoded fill size of 4 and pass it in as an argument.
    """
    for dir_name in os.listdir(input_dir):
        dir_name_zero_filled = dir_name.zfill(4)
        new_dir_name = dir_prefix + '_' + dir_name_zero_filled
        os.rename(os.path.join(input_dir, dir_name), os.path.join(input_dir, new_dir_name))


def prefix_file(input_dir):
    """
    Rename files under sub directory of input_dir to include file's parent directory name.
    """
    for dir_name in os.listdir(input_dir):
        for file_name in os.listdir(os.path.join(input_dir, dir_name)):
            new_file_name = dir_name + '_' + file_name
            os.rename(os.path.join(input_dir, dir_name, file_name), os.path.join(input_dir, dir_name, new_file_name))


def group_files(input_dir, output_dir, size_dir, dir_prefix):
    """
    Scan all files under input_dir and move them to output_dir's sub directory.
    The destination sub directories are automatically created so that each directory will have files upto size_dir.
    The destination sub directory name is 3 digit zero padded sequential number prefixed by dir_prefix.
    """
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)
    total_num_files_counter = 0
    subdir_counter = 1
    out_subdir_size_counter = size_dir
    for root, dirs, files in sorted(os.walk(input_dir)):
        for file_name in sorted(files):
            if out_subdir_size_counter == 0:
                subdir_counter += 1
                out_subdir_size_counter = size_dir
            else:
                out_subdir_size_counter -= 1
            dest_dir = os.path.join(output_dir, dir_prefix + '_' + str(subdir_counter).zfill(3))
            if not os.path.isdir(dest_dir):
                os.mkdir(dest_dir)
            dest_file = os.path.join(dest_dir, file_name)
            os.rename(os.path.join(root, file_name), dest_file)
            total_num_files_counter += 1
        print(subdir_counter)
    print('total_num_files_counter: ', total_num_files_counter )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input-dir', required=True, help='Input directory')
    parser.add_argument('-o', '--output-dir', default='/tmp')
    parser.add_argument('-p', '--dir-prefix', default='id', help='prefix to new subdir name')
    parser.add_argument('-s', '--size-dir', default=128, type=int, help='max number of files per subdir')
    args = parser.parse_args()
    input_dir = args.input_dir
    output_dir = args.output_dir
    print 'input_dir: %s, output_dir %s' % (input_dir, output_dir)
    zero_pad_dir(input_dir, args.dir_prefix)
    prefix_file(input_dir)
    group_files(input_dir, output_dir, args.size_dir, args.dir_prefix)


if __name__ == '__main__':
    main()

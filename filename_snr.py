#!/usr/bin/env python3

import argparse
import os
import sys


# http://stackoverflow.com/a/14063074
def is_hidden(p):
    if os.name == 'nt':
        import win32api, win32con
        attribute = win32api.GetFileAttributes(p)
        return attribute & (win32con.FILE_ATTRIBUTE_HIDDEN | win32con.FILE_ATTRIBUTE_SYSTEM)
    else:
        return p[0] == "."


def to_full_paths(d, files):
    return [(os.path.join(d, f1), os.path.join(d, f2)) for (f1, f2) in files]


def disp_changed(args, changed):
    for (f1, f2) in to_full_paths(args.search_dir, changed):
        print("%s\t-->\t%s" % (f1, f2))

    if args.dry_run:
        print("=== Dry Run: no files have been changed ===")


def snr(args, changed):
    for (f1, f2) in to_full_paths(args.search_dir, changed):
        if os.path.exists(f2) and not args.force:
            sys.stderr.write("File or directory already exists: %s. Aborting.\n" % f2)
            sys.exit(1)
        os.rename(f1, f2)


def main():
    parser = argparse.ArgumentParser()
    # parser.add_argument("search_dir", metavar="SEARCH_DIR",
    #                     nargs="?", default=".",
    #                     help="Directory to search. Default: .")
    parser.add_argument("search", metavar="SEARCH", help="Search term")
    parser.add_argument("replace", metavar="REPLACE", help="Replace term")
    parser.add_argument("-d", "--dir",
                        default=".", nargs="?", metavar="SEARCH_DIR",
                        help="Directory to search. Default: .")
    parser.add_argument("--allow-hidden", action="store_true",
                        help="allow hidden files. hidden files are ignored by default.")
    parser.add_argument("--force", action="store_true",
                        help="Will overwrite any existing files. This is DANGEROUS.")
    parser.add_argument("--dry-run", action="store_true",
                        help="Dry run (do not rename any files)")
    parser.add_argument("-q", "--quiet", action="store_true",
                        help="Produce no output.")

    args = parser.parse_args()

    items = os.listdir(args.search_dir)

    changed = [(f, f.replace(args.search, args.replace)) for f in items]
    changed = list(filter(lambda tup: tup[0] != tup[1], changed))

    if not args.allow_hidden:
        changed = list(filter(lambda tup: not is_hidden(tup[0]), changed))

    if not args.quiet:
        disp_changed(args, changed)

    if not args.dry_run:
        snr(args, changed)


if __name__ == "__main__":
    main()

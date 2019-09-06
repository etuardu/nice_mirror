#!/usr/bin/env python3

from pathlib import Path
import re
import itertools
import sys

external_path = "nice_mirror_external_path"

def edit_file(f, depth):
    """Edit the file f to do some text replacements:
    - references to any "index.html" are changed to "." (the parent directory)
    - references to external files, i.e. outside the path depth, are changed to the
      external_path directory.
    @param {string} f - The file name
    @param {int} depth - The deph of the file relative to the website root
    """
    
    with open(f) as infile:
        txt = infile.read()

    txt = re.sub(
        r'(\b)index\.html',
        r'\1.',
        txt,
        flags=re.IGNORECASE
    )
    # replace occurrencies of "index.html" with "." in the source, e.g.:
    # <a href="sub/index.html#hash"> => <a href="sub/.#hash">
    # <meta content='URL=index.html'> => <meta content='URL=.'>
    #
    # We replace with dot instead of empty string because that would lead
    # to problems in some cases, e.g. in non-quoted href attributes:
    # <a href=index.html> => <a href=> [wrong syntax!]
    # Dots seem to work better.

    if depth > 0:
        txt = txt.replace(
            "../"*depth,
            "../"*(depth-1) + external_path + "/"
        )
    # replace references to the external paths to
    # the "external_path" directory, e.g.
    #   <img src="../../img/test.png">
    #   =>
    #   <img src="../nice_mirror_external_path/img/test.png">

    with open(f, "w") as outfile:
        # update file content
        outfile.write(txt)

def nice_urls(root):
    
    glob_iter = itertools.chain(*(
        Path(root).glob(pattern) for pattern in (
            "**/*.html",
            "**/*.css"
        )
    ))
    # recursive find *.html and *.css files inside the root
    
    for filename in glob_iter:
        # for each files mathing the patterns
        
        filename_relative = str(filename)[len(root):]
        # the file path relative to the root directory
        # e.g. "/home/user/root/index.html" => "/index.html"

        depth = filename_relative.count("/")-1
        # the depth of the file in the directory three
        # e.g. "/sub/sub/page.html" => 2

        print("Processing {}...".format(filename_relative))
        
        edit_file(filename, depth)

    print("Finish.\n")
    print("You should move any external folder inside '{}'".format(
        external_path
    ))
    print("Example: '/dir/lib' => '/dir/website/{}/lib'".format(
        external_path
    ))

if __name__ == '__main__':
    nice_urls(sys.argv[1])

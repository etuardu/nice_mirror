# nice_mirror
Script to keep the urls nice when making a static copy of a website

When mirroring a website using tools like `httrack`, the urls got `/index.html`
appended to its address and any external resource, if mirrored, is placed
outside of the website root.

This script aims to fix this, in order to keep the urls as they were originally.

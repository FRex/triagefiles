import collections
import sys
import os

# TODO: 1. other sort options than by extension
# TODO: 2. subcommand to create triage/ dir and subdirs automatically
# TODO: 3. config file in triage/ dir
# TODO: 4. way to handle only some file extensions, some files, mv to another triage dir?
# TODO: 5. on windows print paths with / or using shlex so they are git bash safe


def _main() -> int | None:
    goaldir = "triage/by/extension"
    if not os.path.exists(goaldir):
        print(f"dir {goaldir} doesn't exist", file=sys.stderr)
        return 1

    files = sorted(filter(os.path.isfile, os.listdir()))

    files_by_extension = collections.defaultdict(list)
    for x in files:
        ext = os.path.splitext(x)[1]
        ext = ext.lstrip(".")
        if ext:  # ignore files with no extension
            files_by_extension[ext].append(x)

    for ext, files in files_by_extension.items():
        extgoaldir = os.path.join(goaldir, ext)
        os.makedirs(extgoaldir, exist_ok=True)

        for file in files:
            extgoalfile = os.path.join(extgoaldir, file)
            if not os.path.exists(extgoalfile):
                os.rename(file, extgoalfile)
            else:
                # TODO: try do hashrename on file first if its small?
                print(
                    f"Cannot move {file} - file {extgoalfile} already exists",
                    file=sys.stderr,
                )


if __name__ == "__main__":
    sys.exit(_main() or 0)

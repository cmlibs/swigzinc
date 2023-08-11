import re
import sys


def _extract_zinc_version(rc, stdout, stderr):
    version = '0.0.0.dev0'
    if rc == 0:
        lines = stdout.split('\n')
        for line in lines:
            result = re.search("Version: '([^']+)'", line.strip())
            if result:
                version = result.group(1)

    return {'release_version': version}


def main():
    args = sys.argv[:]
    cmake_output_file = args.pop()

    with open(cmake_output_file) as f:
        cmake_output = f.read()

    result = _extract_zinc_version(0, cmake_output, None)
    print(result['release_version'])


if __name__ == "__main__":
    main()


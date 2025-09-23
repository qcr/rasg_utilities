#!/usr/bin/env python3

# Copyright (C) 2025 Queensland University of Technology
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#    http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# 

# Author:  Alec Tutin
# Date:	   2025-09-19
# Version: 1.0
#
# Apply a license to code files according to standard practice.

import logging

from argparse import ArgumentParser
from datetime import datetime
from logging import Logger
from os import linesep
from pathlib import Path
from typing import Callable, List

software_name: str = 'apply_license'
software_version: str = '1.0'
software_tag: str = f'{software_name} v{software_version}'

def get_copyright_declaration(rights_holder: str) -> str:
    year: int = datetime.now().year

    return f'Copyright (C) {year} {rights_holder}'

def as_header(license_text: str, copyright_text: str, line_comment: str = '#') -> List[str]:
    lines: List[str] = [copyright_text, '']
    lines.extend(license_text.splitlines())

    if lines[-1].strip() != '':
        lines.append('')

    for i in range(len(lines)):
        lines[i] = f'{line_comment} {lines[i]}{linesep}'

    return lines

def apply_header(file: Path, license_text: str, copyright_text: str) -> None:
    with file.open('r') as f:
        contents: List[str] = f.readlines()

    # Leave the shebang at the top
    insert_index: int = 1 if contents[0].startswith('#!') else 0

    result: List[str] = contents[0 : insert_index]

    if insert_index != 0:
        result.append(linesep)

    result.extend(as_header(license_text, copyright_text))

    if contents[insert_index].strip() != '':
        result.append(linesep)

    result.extend(contents[insert_index:])

    with file.open('w') as f:
        f.writelines(result)

def apply_header_simple(file: Path, license_text: str, copyright_text: str, line_comment: str) -> None:
    with file.open('r') as f:
        contents: List[str] = f.readlines()
    
    result: List[str] = []

    result.extend(as_header(license_text, copyright_text, line_comment))
    result.append(linesep)
    result.extend(contents)

    with file.open('w') as f:
        f.writelines(result)

def apply_header_dart(file: Path, license_text: str, copyright_text: str) -> None:
    apply_header_simple(file, license_text, copyright_text, '//')

def apply_header_bat(file: Path, license_text: str, copyright_text: str) -> None:
    apply_header_simple(file, license_text, copyright_text, '::')

processor_map: dict[str, Callable[[Path, str, str], None]] = {
    '.py': apply_header,
    '.sh': apply_header,
    '.dart': apply_header_dart,
    '.bat': apply_header_bat
}

ignored_names: List[str] = [
    '__init__'
]

def main() -> None:
    logging.basicConfig()
    logger: Logger = logging.getLogger(software_name)
    logger.setLevel(logging.INFO)

    parser = ArgumentParser(software_tag, description='Apply a license to code files according to standard practice')
    parser.add_argument('-l', '--license', metavar='license', required=True, help='Path to the license file to insert into the code file headers')
    parser.add_argument('-e', '--extension', metavar='extension', action="extend", nargs="+", help=f'Limit file search to specified extensions [{", ".join(processor_map.keys())}]')
    parser.add_argument('-c', '--copyright', metavar='copyright', required=True, help='Name of the copyright holder')
    parser.add_argument('project', metavar='project', help='/path/to/project/directory/')

    args = parser.parse_args()

    license_path = Path(args.license).expanduser()
    license_text: str = license_path.read_text()
    extensions: List[str] = args.extension
    copyright_text: str = get_copyright_declaration(args.copyright)

    project_path = Path(args.project).expanduser()

    if extensions is None or len(extensions) == 0:
        extensions = processor_map.keys()
    else:
        for extension in extensions:
            if extension not in processor_map.keys():
                logger.error(f'Files of type "{extension}" are not supported!')
                exit(1)

    if not license_path.exists():
        logger.error(f'license does not exist at "{str(license_path)}"!')
        exit(1)

    if not project_path.is_dir():
        logger.error(f'Specified project is not a directory!')
        exit(1)

    logger.info(f'Searching for files in {str(project_path)}...')

    for extension in extensions:
        for file in project_path.rglob(f'*{extension}'):
            if not file.is_file():
                logger.warning(f'Input file "{str(file)}" is not a file!')

                continue

            if file.stem in ignored_names:
                continue

            answer: str = input(f'Process "{str(file)}"? (y/N) ').lower()

            if answer in ['yes', 'y']:
                processor_map[file.suffix](file, license_text, copyright_text)

    logger.info('Done!')

if __name__ == '__main__':
    main()

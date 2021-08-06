import re
from os import path

import click
import git

__author__ = "Silas S Silva"

_repositories = {
    'hub-travel-app': 'https://github.com/silassansil/hub-travel-app.git',
    'nubank-chanllenge-authorizer': 'https://github.com/silassansil/nubank-chanllenge-authorizer.git',
    'bowling-java-challenge': 'https://github.com/silassansil/bowling-java-challenge.git',
}


def major_increase(_last_version):
    return f'v{int(_last_version[0]) + 1}.0.0'


def minor_increase(_last_version):
    return f'v{_last_version[0]}.{int(_last_version[1]) + 1}.0'


def patch_increase(_last_version):
    return f'v{_last_version[0]}.{_last_version[1]}.{int(_last_version[2]) + 1}'


_update_version = {
    'major': major_increase,
    'minor': minor_increase,
    'patch': patch_increase,
}


@click.command()
def main():
    click.echo('lets generate a new version for our project?? :D')
    _repo_name = input(f'what repo do you like generate a tag?? \n {list(_repositories.keys())} \n')
    _repo_name_temp = f'{_repo_name}-temp'

    click.echo(f'please, wait while are pulling the last version from {_repo_name}....')

    if path.exists(_repo_name_temp):
        _git_repo = git.Repo(_repo_name_temp)
        _git_repo.remotes.origin.pull()
    else:
        git.Repo.clone_from(_repositories[_repo_name], _repo_name_temp)
        _git_repo = git.Repo(_repo_name_temp)

    _tags = _git_repo.tags

    if _tags:
        _last_tag_version = re.sub(
            r'\D', '', str(_tags[-1])
        )
    else:
        _last_tag_version = '000'

    _tag_message = input(
        'please inform the list of jira cards that was publish in this tag... e.g XPTO-123, XPTO-002, XPTO-432\n')

    _new_version = None
    while not _new_version:
        click.echo('sure, lets increase the tag version...')
        _version = input('what is it version? (major, minor, patch)\n')

        if _version.lower() in ['major', 'minor', 'patch']:
            _new_version = _update_version[_version.lower()](_last_tag_version)

            _confirmation = input(f'do you confirm the new version [y/n]?? {_new_version}\n')

            if _confirmation == 'y':
                _new_tag = _git_repo.create_tag(_new_version, message=_tag_message)
                _git_repo.remotes.origin.push(_new_tag)
            else:
                _new_version = None

    click.echo(f'nice, tag {_new_version} created with success... cya')


if __name__ == '__main__':
    main()

import re

RE_README = re.compile(
    r"""
    \#{1}\sWelcome\sto\s(?P<project_name>.+)!\n{2}
    (?P<description>(?:.+\n)+)\n
    \#{3}\s.+\((?P<homepage>.+)\).+\n{2}
    \#{3}\s.+\((?P<docupage>.+)\).+\n{2}
    (?P<author_name>.+)\n{2}
    (?P<license_name>.+)\n{2}
    \#{1}\sTL;DR.*\n(?P<installation>(?:.+\n)+)\n{1}
    \#{1}\sUsage.*\n(?P<usage>(?:.+\n)+)\n{1}
    \#{1}\sHow\sto\stest.*\n(?P<test>(?:.+\n)+)\n{1}
    """,
    re.VERBOSE,
)


def get_single_line() -> str:
    return input()


def get_multiline() -> str:
    content = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        content.append(line)
    return "\n".join(content)


def add_md_header(block: str, md_lvl: int) -> str:
    return ("#" * md_lvl + " " if md_lvl > 0 else "") + block


def gen_style_dict(readme_dict: dict) -> dict:
    style_dict = {
        'project_name': {'f_line':f"Welcome to {readme_dict['project_name']}!\n",'md_lvl': 1},
        'description':  {'f_line':f"{readme_dict['description']}",'md_lvl' : 0},
        'homepage':     {'f_line':f"Project homepage is located at [{readme_dict['homepage']}]({readme_dict['homepage']}).\n",'md_lvl' : 3},
        'docupage':     {'f_line':f"For documentation please visit [{readme_dict['docupage']}]({readme_dict['docupage']}).\n",'md_lvl' : 3},
        'author_name':  {'f_line':f"{readme_dict['author_name']}\n",'md_lvl' : 0},
        'license_name': {'f_line':f"{readme_dict['license_name']}\n",'md_lvl' : 0},
        'installation': {'f_line':f"TL;DR How to install\n{readme_dict['installation']}",'md_lvl' : 1},
        'usage':        {'f_line':f"Usage\n{readme_dict['usage']}",'md_lvl' : 1},
        'test':         {'f_line':f"How to test\n{readme_dict['test']}",'md_lvl' : 1}
    }
    return style_dict
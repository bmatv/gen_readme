
import os
import re
import click

re_expression = re.compile(r'''
    \#{1}\sWelcome\sto\s(?P<project_name>.+)!\n{2}
    (?P<description>(?:.+\n)+)\n
    \#{3}\s.+\((?P<homepage>.+)\).+\n{2}
    \#{3}\s.+\((?P<docupage>.+)\).+\n{2}
    (?P<author_name>.+)\n{2}
    (?P<license_name>.+)\n{2}
    \#{1}\sTL;DR.*\n(?P<installation>(?:.+\n)+)\n{1}
    \#{1}\sUsage.*\n(?P<usage>(?:.+\n)+)\n{1}
    \#{1}\sHow\sto\stest.*\n(?P<test>(?:.+\n)+)\n{1}
    ''', re.VERBOSE)

def get_single_line():
    return input()

def get_multiline():
    content = []
    while True:
        try: 
            line = input()
        except EOFError:
                break
        content.append(line)
    return '\n'.join(content)


def add_md_header(block,md_lvl):
    return ('#'*md_lvl + ' ' if md_lvl > 0 else '') + block

@click.command()
@click.option('-f', '--filepath', default=None, help='path to readme file')
def gen_readme(filepath):
    """A simple utility to interactively generate a README.md file"""
    # TODO get_multiline to be used, through dict?
    # TODO change some instances of print to logging
    # TODO skip empty blocks, e.g. if project_name == '' -> skip project_name ?

    readme_path = os.path.join(os.curdir,'README.md') if filepath is None else filepath
    if os.path.exists(readme_path):
        print('File found. Reading...')
        with open(readme_path,'r') as file:
            readme_file = file.read()

        readme_dict = re_expression.search(readme_file).groupdict()

    else:
        readme_dict = dict.fromkeys(['project_name', 'description', 'homepage', 'docupage', 'author_name', 'license_name', 'installation', 'usage', 'test'])


    for block_name in readme_dict.keys():
        if readme_dict[block_name] is not None:
            print("Input already present in the file:", readme_dict[block_name])
            choice = input("Would you like to change?(y/[n]):")
            if choice.lower() == '' or choice.lower() == 'n':
                print('You chose not to change')
            elif choice.lower() == 'y':
                print('You chose to change')
                print(f"Input the content for the {block_name} below.") # Press Ctrl-D when finished.
                if block_name in ['description','installation', 'usage', 'test']:
                    readme_dict[block_name] = get_multiline()
                else:
                    readme_dict[block_name] = get_single_line()

            else:
                raise ValueError(f"invalid default answer: {choice}. Considering as No")
        else:
            print(f"Input the content for the {block_name} below.") # Press Ctrl-D when finished.
            readme_dict[block_name] = get_single_line()



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

    buf = []
    for entry in style_dict:
        buf.append(add_md_header(block=style_dict[entry]['f_line'],md_lvl=style_dict[entry]['md_lvl']))

    out_readme_path = os.path.join(os.path.dirname(readme_path),'README_NEW.md')
    print(f'writing to {out_readme_path}')
    with open(out_readme_path,'w') as file:
        file.write('\n'.join(buf))
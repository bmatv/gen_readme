import os

import click

import aux


@click.command()
@click.option("-f", "--filepath", default=None, help="path to readme file")
@click.option(
    "-s",
    "--skip-empty",
    is_flag=True,
    show_default=True,
    default=False,
    help="skip blocks if no info was provided",
)
def gen_readme(filepath: str, skip_empty: bool):
    """A simple utility to interactively generate a README.md file"""
    # TODO change some instances of print to logging
    # TODO skip empty blocks, e.g. if project_name == '' -> skip project_name ?

    readme_path = os.path.join(os.curdir, "README.md") if filepath is None else filepath
    if os.path.exists(readme_path):
        print("File found. Reading...")
        with open(readme_path, "r") as file:
            README_FILE = file.read()

        readme_dict = aux.RE_README.search(README_FILE).groupdict()

    else:
        readme_dict = dict.fromkeys(
            [
                "project_name",
                "description",
                "homepage",
                "docupage",
                "author_name",
                "license_name",
                "installation",
                "usage",
                "test",
            ]
        )

    for block_name in readme_dict.keys():
        if readme_dict[block_name] is not None:
            print(
                f"Input for the '{block_name}' already present in the file:\n{'-'*80}\n{readme_dict[block_name]}\n{'-'*80}"
            )
            choice = input("Would you like to change?(y/[n]):")
            if choice.lower() == "y":
                print(f"Input the content for the {block_name} below.")  #
                if block_name in ["description", "installation", "usage", "test"]:
                    print(
                        "Input is multiline. Press Enter to create a newline and Ctrl-D right after when finished."
                    )
                    readme_dict[block_name] = aux.get_multiline()
                else:
                    readme_dict[block_name] = aux.get_single_line()

            else:
                if choice.lower() != "" and choice.lower() != "n":
                    print(
                        f"invalid default answer: {choice}. Considering as No"
                    )  # Used to be raise ValueError
                continue
        else:
            print(f"Input the content for the {block_name} below.")
            readme_dict[block_name] = aux.get_single_line()

    style_dict = aux.gen_style_dict(readme_dict)
    if skip_empty: aux.pop_empty(readme_dict, style_dict)

    buf = []
    for entry in style_dict:
        buf.append(
            aux.add_md_header(
                block=style_dict[entry]["f_line"], md_lvl=style_dict[entry]["md_lvl"]
            )
        )

    out_readme_path = os.path.join(os.path.dirname(readme_path), "README_NEW.md")
    print(f"writing to {out_readme_path}")
    with open(out_readme_path, "w") as file:
        file.write("\n".join(buf))

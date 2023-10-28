#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import pickle
import recettes


def compare_files(file1, file2):
    with open(file1, "r") as f1, open(file2, "r") as f2:
        lines1 = f1.readlines()
        lines2 = f2.readlines()

        if len(lines1) > len(lines2):
            print("The first file has more lines than the second.")
        elif len(lines2) > len(lines1):
            print("The second file has more lines than the first.")

        for line_nb, (line_str1, line_str2) in enumerate(zip(lines1, lines2)):
            if len(line_str1) != len(line_str2):
                print(f"Lines {line_nb} differ in length.")
            for char_nb, (char1, char2) in enumerate(zip(line_str1, line_str2)):
                if char1 != char2:
                    print(
                        f"Line {line_nb}, col. {char_nb}: characters differ ({char1 if char1.strip() != '' else '<invis>'} != {char2 if char2.strip() != '' else '<invis>'})."
                    )
                    return

        print("Files have the same content.")


def triple_spaces(in_file, out_file):
    with open(in_file, "r") as f_in, open(out_file, "w") as f_out:
        contents = f_in.read()
        contents = contents.replace(" ", "   ")
        f_out.write(contents)


def append_mentions(mention_ranges_path, in_path, out_path):
    mention_ranges = {}
    with open(mention_ranges_path, "r") as f_ranges:
        mention_ranges = json.load(f_ranges)

    if mention_ranges == {}:
        print("Invalide mention ranges file.")
        return

    with open(in_path, "r") as f_in, open(out_path, "w") as f_out:
        for line in f_in.readlines():
            grade = int(line.strip())
            for mention_name, mention_range in mention_ranges.items():
                if mention_range[0] <= grade < mention_range[1]:
                    f_out.write(f"{str(grade)} {mention_name}\n")
                    break


def manage_recipes(file_path):
    extension = file_path.strip().split(".")[-1]
    if extension == "p":
        with open(file_path, "rb") as f_in:
            donnees = pickle.load(f_in)
    elif extension == "json":
        with open(file_path, "r") as f_in:
            donnees = json.load(f_in)
    else:
        print("Extension de fichier non reconnue.")
        return

    recettes.run_interactive(donnees)

    if extension == "p":
        with open(file_path, "wb") as f_out:
            pickle.dump(donnees, f_out)
    else:
        with open(file_path, "w") as f_out:
            json.dump(donnees, f_out)


def extract_numbers(file_path):
    numbers = []

    with open(file_path, "r") as f_in:
        contents = f_in.read().split()
        for v in contents:
            if v.isdigit() or (v.startswith("-") and v[1:].isdigit()):
                numbers.append(int(v))
            else:
                try:
                    numbers.append(float(v))
                except Exception:
                    pass

    numbers.sort()
    return numbers


def copy_half_lines(in_path, out_path):
    with open(in_path, "r") as f_in, open(out_path, "w") as f_out:
        for i, line in enumerate(f_in.readlines()):
            if i % 2 == 1:
                continue
            f_out.write(line)


if __name__ == "__main__":
    if not os.path.exists("output"):
        os.mkdir("output")
    print("Comparaison des exercices: ")
    compare_files("./exercice.py", "./_exercice_version_prof.py")
    print("Comparaison des exemples 0 et 2: ")
    compare_files("./data/exemple.txt", "./data/exemple2.txt")
    print("Comparaison des exemples 0 et 1: ")
    compare_files("./data/exemple.txt", "./data/exemple1.txt")

    triple_spaces("./data/exemple.txt", "./output/exemple_triple.txt")

    append_mentions(
        "./data/seuils.json", "./data/notes.txt", "./output/notes_annotees.txt"
    )

    manage_recipes("./data/recettes.json")
    manage_recipes("./data/recettes.p")

    print(
        f"Les chiffres dans le fichier sont: {extract_numbers('./data/exemple.txt')}."
    )

    copy_half_lines("./data/exemple.txt", "./output/demi_exemple.txt")

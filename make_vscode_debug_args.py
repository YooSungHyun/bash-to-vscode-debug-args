import sys
import argparse
import re


def main(argv, args):
    debug_sh = args.input
    script_vars = dict()
    result = list()
    with open(debug_sh, "r") as f:
        script_lines = f.readlines()

        for script_line in script_lines:
            is_python_var = script_line.find("--") > -1 or script_line.find(" \\") > -1
            script_line = script_line.strip()
            script_line = script_line.replace('"', "")
            script_line = script_line.replace(" \\", "")
            upper_chk = re.compile("[A-Z_-]+")
            upper_match = upper_chk.match(script_line)
            if upper_match and not is_python_var:
                var_key, var_value = script_line.split("=")
                script_vars[var_key] = var_value
            elif is_python_var:
                script_var_idx = script_line.find("$")
                if script_var_idx > -1:
                    var_name = script_line[script_var_idx + 1 :]
                    assert var_name in script_vars.keys(), "python uses script var, but can not find!!!"
                    script_line = script_line.replace("$" + var_name, script_vars[var_name])
                result.append(script_line)

    with open(args.output, "w") as f:
        for idx, line in enumerate(result):
            f.write('"' + line + '"')
            if idx < len(result) - 1:
                f.write(",\n")


if __name__ == "__main__":
    argv = sys.argv
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", help=" : input script")
    parser.add_argument("--output", help=" : output text", default="./vscode_debug_args.txt")
    args = parser.parse_args()
    main(argv, args)

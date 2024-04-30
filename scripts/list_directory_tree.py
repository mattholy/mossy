import os
import pathspec


def load_gitignore_rules(startpath):
    gitignore_path = os.path.join(startpath, '.gitignore')
    try:
        with open(gitignore_path, 'r') as file:
            ignore_lines = file.readlines()
        # 确保 .git 和 __pycache__ 目录在所有层级都被忽略
        ignore_lines.append('.git/')
        ignore_lines.append('__pycache__/')
        return pathspec.PathSpec.from_lines('gitwildmatch', ignore_lines)
    except FileNotFoundError:
        # 如果找不到 .gitignore 文件，默认忽略 .git 和 __pycache__
        return pathspec.PathSpec.from_lines('gitwildmatch', ['.git/', '__pycache__/'])


def list_files(startpath, output_file):
    spec = load_gitignore_rules(startpath)
    with open(output_file, 'w') as f:
        for root, dirs, files in os.walk(startpath, topdown=True):
            # 过滤目录
            dirs[:] = [d for d in dirs if not spec.match_file(
                os.path.join(root, d))]
            # 忽略路径中的 __pycache__ 目录
            if '__pycache__' in dirs:
                dirs.remove('__pycache__')
            level = root.replace(startpath, '').count(os.sep)
            indent = ' ' * 4 * (level)
            f.write('{}{}/\n'.format(indent, os.path.basename(root)))
            subindent = ' ' * 4 * (level + 1)
            # 过滤文件
            for file in files:
                if not spec.match_file(os.path.join(root, file)):
                    f.write('{}{}\n'.format(subindent, file))


if __name__ == "__main__":
    startpath = '.'  # 默认当前目录
    output_file = 'structure.txt'
    list_files(startpath, output_file)

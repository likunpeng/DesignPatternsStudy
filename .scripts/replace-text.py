#!/usr/bin/env python3
import os
import re

def replace_in_file(filepath, old_text, new_text):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if old_text in content:
        new_content = content.replace(old_text, new_text)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated: {filepath}")
        return True
    return False

def main():
    root_dir = '/Users/likunpeng/Documents/AI/study'
    old_text = '学习笔记'
    new_text = '教程'
    
    count = 0
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # 跳过隐藏目录
        dirnames[:] = [d for d in dirnames if not d.startswith('.')]
        
        for filename in filenames:
            if filename.endswith(('.html', '.md')):
                filepath = os.path.join(dirpath, filename)
                if replace_in_file(filepath, old_text, new_text):
                    count += 1
    
    print(f"\nTotal {count} files updated.")

if __name__ == '__main__':
    main()
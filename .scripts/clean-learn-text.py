#!/usr/bin/env python3
import os
import re

def clean_lead_text(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 替换 "今天学习XX模式" 为更简洁的表达
    patterns = [
        (r'今天学习([\u4e00-\u9fa5]+模式)', r'\1'),
        (r'今天学习([\u4e00-\u9fa5]+基础)', r'\1'),
        (r'今天学习([\u4e00-\u9fa5]+原则)', r'\1'),
    ]
    
    changed = False
    for old_pattern, new_pattern in patterns:
        new_content, count = re.subn(old_pattern, new_pattern, content)
        if count > 0:
            content = new_content
            changed = True
    
    if changed:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated: {filepath}")
        return True
    return False

def main():
    root_dir = '/Users/likunpeng/Documents/AI/study'
    
    count = 0
    for dirpath, dirnames, filenames in os.walk(root_dir):
        dirnames[:] = [d for d in dirnames if not d.startswith('.')]
        
        for filename in filenames:
            if filename.endswith('.html'):
                filepath = os.path.join(dirpath, filename)
                if clean_lead_text(filepath):
                    count += 1
    
    print(f"\nTotal {count} files updated.")

if __name__ == '__main__':
    main()
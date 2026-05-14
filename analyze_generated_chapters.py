#!/usr/bin/env python3
import os
import re
from pathlib import Path
import statistics
from bs4 import BeautifulSoup

def count_paragraphs_in_html(html_file):
    """统计HTML文件中的段落数"""
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 使用BeautifulSoup解析
        soup = BeautifulSoup(content, 'html.parser')
        
        # 找到content div
        content_div = soup.find('div', class_='content')
        if not content_div:
            return 0
            
        # 统计<p>标签数量（排除广告相关的）
        paragraphs = content_div.find_all('p')
        return len(paragraphs)
    except Exception as e:
        print(f"错误: {html_file} - {e}")
        return 0

def analyze_generated_chapters():
    docs_dir = Path('docs/novels')
    all_paragraph_counts = []
    book_stats = []
    
    if not docs_dir.exists():
        print("docs/novels 目录不存在")
        return
    
    # 遍历所有书籍目录
    for book_dir in sorted(docs_dir.iterdir()):
        if not book_dir.is_dir():
            continue
            
        book_name = book_dir.name
        book_paragraphs = []
        chapter_files = []
        
        # 查找所有章节HTML文件
        for chapter_file in sorted(book_dir.glob('chapter-*.html')):
            if '-clean.html' in str(chapter_file):
                continue  # 跳过clean版本
                
            para_count = count_paragraphs_in_html(chapter_file)
            if para_count > 0:
                book_paragraphs.append(para_count)
                all_paragraph_counts.append(para_count)
                chapter_files.append((chapter_file.name, para_count))
        
        if book_paragraphs:
            book_avg = statistics.mean(book_paragraphs)
            book_median = statistics.median(book_paragraphs)
            book_stats.append({
                'book': book_name,
                'chapters': len(book_paragraphs),
                'avg': book_avg,
                'median': book_median,
                'min': min(book_paragraphs),
                'max': max(book_paragraphs),
                'files': chapter_files
            })
    
    # 计算总体统计
    if all_paragraph_counts:
        overall_avg = statistics.mean(all_paragraph_counts)
        overall_median = statistics.median(all_paragraph_counts)
        overall_min = min(all_paragraph_counts)
        overall_max = max(all_paragraph_counts)
        total_chapters = len(all_paragraph_counts)
        
        print("=" * 80)
        print("📊 已生成HTML章节的段落统计分析")
        print("=" * 80)
        print(f"\n总章节数: {total_chapters:,}")
        print(f"总书籍数: {len(book_stats)}")
        print(f"\n【总体统计】")
        print(f"  平均段落数: {overall_avg:.2f} 段")
        print(f"  中位数段落数: {overall_median:.2f} 段")
        print(f"  最少段落数: {overall_min} 段")
        print(f"  最多段落数: {overall_max} 段")
        
        # 计算分位数
        if len(all_paragraph_counts) >= 4:
            percentiles = [25, 50, 75, 90, 95]
            print(f"\n【分位数分析】")
            sorted_counts = sorted(all_paragraph_counts)
            for p in percentiles:
                idx = int(len(sorted_counts) * p / 100)
                if idx >= len(sorted_counts):
                    idx = len(sorted_counts) - 1
                value = sorted_counts[idx]
                print(f"  {p}%: {value} 段")
        
        # 段落数分布
        ranges = [(0, 10), (11, 20), (21, 30), (31, 40), (41, 50), (51, 100), (101, float('inf'))]
        print(f"\n【段落数分布】")
        for start, end in ranges:
            if end == float('inf'):
                count = sum(1 for x in all_paragraph_counts if x > start)
                print(f"  {start}+ 段: {count} 章 ({count/total_chapters*100:.1f}%)")
            else:
                count = sum(1 for x in all_paragraph_counts if start <= x <= end)
                print(f"  {start}-{end} 段: {count} 章 ({count/total_chapters*100:.1f}%)")
        
        # 显示所有书籍统计
        print(f"\n【书籍详细统计】")
        print(f"{'书名':<50} {'章节':<8} {'平均':<8} {'中位数':<8} {'最小':<8} {'最大':<8}")
        print("-" * 95)
        
        for stat in book_stats:
            book_name = stat['book'][:48] + '..' if len(stat['book']) > 50 else stat['book']
            print(f"{book_name:<50} {stat['chapters']:<8} {stat['avg']:<8.1f} {stat['median']:<8.1f} {stat['min']:<8} {stat['max']:<8}")
        
        print("=" * 80)
        
        # 广告位置分析（基于中位数）
        print(f"\n【当前广告插入位置分析】（基于中位数 {overall_median:.0f} 段）")
        print(f"  位置1 (固定第1段后): 第 1 段后")
        print(f"  位置2 (20%位置): 第 {max(int(overall_median * 0.20), 3)} 段后")
        print(f"  位置3 (37%位置): 第 {max(int(overall_median * 0.37), 5)} 段后")
        print(f"  位置4 (53%位置): 第 {max(int(overall_median * 0.53), 7)} 段后")
        print(f"  位置5 (70%位置): 第 {max(int(overall_median * 0.70), 9)} 段后")
        print(f"  位置6 (87%位置): 第 {max(int(overall_median * 0.87), 11)} 段后")
        
        # 显示一些样本章节的详细信息
        print(f"\n【样本章节详情】（前3本书的章节）")
        for stat in book_stats[:3]:
            print(f"\n📖 {stat['book']} (共 {stat['chapters']} 章)")
            for filename, para_count in stat['files'][:5]:  # 只显示前5章
                print(f"   - {filename}: {para_count} 段")
            if len(stat['files']) > 5:
                print(f"   ... 还有 {len(stat['files']) - 5} 章")
        
    else:
        print("未找到任何已生成的章节HTML文件")

if __name__ == '__main__':
    analyze_generated_chapters()

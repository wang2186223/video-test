#!/usr/bin/env python3
import os
import json
from pathlib import Path
import statistics

def count_paragraphs(content):
    """统计非空段落数"""
    paragraphs = content.split('\n')
    non_empty = [p for p in paragraphs if p.strip()]
    return len(non_empty)

def analyze_all_books():
    source_dir = Path('source')
    all_paragraph_counts = []
    book_stats = []
    
    # 遍历所有书籍目录
    for book_dir in sorted(source_dir.iterdir()):
        if not book_dir.is_dir():
            continue
            
        book_name = book_dir.name
        book_paragraphs = []
        chapter_count = 0
        
        # 遍历该书的所有章节文件
        for chapter_file in sorted(book_dir.glob('*.txt')):
            try:
                with open(chapter_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    para_count = count_paragraphs(content)
                    book_paragraphs.append(para_count)
                    all_paragraph_counts.append(para_count)
                    chapter_count += 1
            except Exception as e:
                print(f"错误读取 {chapter_file}: {e}")
        
        if book_paragraphs:
            book_avg = statistics.mean(book_paragraphs)
            book_median = statistics.median(book_paragraphs)
            book_stats.append({
                'book': book_name,
                'chapters': chapter_count,
                'avg': book_avg,
                'median': book_median,
                'min': min(book_paragraphs),
                'max': max(book_paragraphs)
            })
    
    # 计算总体统计
    if all_paragraph_counts:
        overall_avg = statistics.mean(all_paragraph_counts)
        overall_median = statistics.median(all_paragraph_counts)
        overall_min = min(all_paragraph_counts)
        overall_max = max(all_paragraph_counts)
        total_chapters = len(all_paragraph_counts)
        
        print("=" * 80)
        print("📊 所有书籍章节段落统计分析")
        print("=" * 80)
        print(f"\n总章节数: {total_chapters:,}")
        print(f"总书籍数: {len(book_stats)}")
        print(f"\n【总体统计】")
        print(f"  平均段落数: {overall_avg:.2f}")
        print(f"  中位数段落数: {overall_median:.2f}")
        print(f"  最少段落数: {overall_min}")
        print(f"  最多段落数: {overall_max}")
        
        # 计算分位数
        percentiles = [25, 50, 75, 90, 95, 99]
        print(f"\n【分位数分析】")
        for p in percentiles:
            value = statistics.quantiles(all_paragraph_counts, n=100)[p-1] if p < 100 else max(all_paragraph_counts)
            print(f"  {p}%: {value:.0f} 段")
        
        # 段落数分布
        ranges = [(0, 20), (21, 40), (41, 60), (61, 80), (81, 100), (101, 150), (151, 200), (201, float('inf'))]
        print(f"\n【段落数分布】")
        for start, end in ranges:
            if end == float('inf'):
                count = sum(1 for x in all_paragraph_counts if x > start)
                print(f"  {start}+ 段: {count} 章 ({count/total_chapters*100:.1f}%)")
            else:
                count = sum(1 for x in all_paragraph_counts if start <= x <= end)
                print(f"  {start}-{end} 段: {count} 章 ({count/total_chapters*100:.1f}%)")
        
        # 显示部分书籍统计（前10本和后10本）
        print(f"\n【部分书籍详细统计】（共{len(book_stats)}本）")
        print(f"{'书名':<50} {'章节':<8} {'平均':<8} {'中位数':<8} {'最小':<8} {'最大':<8}")
        print("-" * 95)
        
        # 前10本
        for stat in book_stats[:10]:
            book_name = stat['book'][:48] + '..' if len(stat['book']) > 50 else stat['book']
            print(f"{book_name:<50} {stat['chapters']:<8} {stat['avg']:<8.1f} {stat['median']:<8.1f} {stat['min']:<8} {stat['max']:<8}")
        
        if len(book_stats) > 20:
            print("  ...")
            # 后10本
            for stat in book_stats[-10:]:
                book_name = stat['book'][:48] + '..' if len(stat['book']) > 50 else stat['book']
                print(f"{book_name:<50} {stat['chapters']:<8} {stat['avg']:<8.1f} {stat['median']:<8.1f} {stat['min']:<8} {stat['max']:<8}")
        elif len(book_stats) > 10:
            for stat in book_stats[10:]:
                book_name = stat['book'][:48] + '..' if len(stat['book']) > 50 else stat['book']
                print(f"{book_name:<50} {stat['chapters']:<8} {stat['avg']:<8.1f} {stat['median']:<8.1f} {stat['min']:<8} {stat['max']:<8}")
        
        print("=" * 80)
        
        # 广告位置分析
        print(f"\n【广告插入位置分析】（基于中位数 {overall_median:.0f} 段）")
        print(f"  位置1 (固定): 第 1 段后")
        print(f"  位置2 (20%): 第 {max(int(overall_median * 0.20), 3)} 段后")
        print(f"  位置3 (37%): 第 {max(int(overall_median * 0.37), 5)} 段后")
        print(f"  位置4 (53%): 第 {max(int(overall_median * 0.53), 7)} 段后")
        print(f"  位置5 (70%): 第 {max(int(overall_median * 0.70), 9)} 段后")
        print(f"  位置6 (87%): 第 {max(int(overall_median * 0.87), 11)} 段后")
        
    else:
        print("未找到任何章节数据")

if __name__ == '__main__':
    analyze_all_books()

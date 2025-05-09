import os
import re
from collections import Counter
from datetime import datetime

EPSILON = 1e-2


def analyze_time_differences(directory_path="."):
    data_files = []
    pattern = re.compile(r'data_(\d{2})-(\d{2})_(\d{2})-(\d{2})\.json')
    
    for filename in os.listdir(directory_path):
        match = pattern.match(filename)
        if match:
            day, month, hour, minute = map(int, match.groups())
            current_year = datetime.now().year
            file_time = datetime(current_year, month, day, hour, minute)
            data_files.append((filename, file_time))
    
    data_files.sort(key=lambda x: x[1])
    
    time_differences = []
    if len(data_files) >= 2:
        for i in range(1, len(data_files)):
            prev_time = data_files[i-1][1]
            curr_time = data_files[i][1]
            diff_minutes = (curr_time - prev_time).total_seconds() / 60
            time_differences.append((data_files[i-1][0], data_files[i][0], diff_minutes))
    
    diff_values = [diff for _, _, diff in time_differences]
    counts = Counter(diff_values)
    
    return time_differences, counts

def print_analysis_results(time_differences, counts):
    print(f"Total files analyzed: {len(time_differences) + 1}")
    print(f"Total time differences: {len(time_differences)}")
    
    print("\nFrequency of Time Differences:")
    for diff, count in counts.most_common():
        print(f"{diff:.2f} minutes: {count} occurrences")
    
    print("\nSummary:")
    if counts:
        avg_diff = sum(diff * count for diff, count in counts.items()) / sum(counts.values())
        print(f"Average time difference: {avg_diff:.2f} minutes")
        print(f"Most common time difference: {counts.most_common(1)[0][0]:.2f} minutes " 
              f"({counts.most_common(1)[0][1]} occurrences)")
        
    
    for prev_file, curr_file, diff in time_differences:
        if abs(diff - counts.most_common(1)[0][0]) > EPSILON:
            print(f"Outlier: {prev_file} → {curr_file}: {diff:.5f} minutes")
        


def routine(directory:str):
    time_diffs, counts = analyze_time_differences(directory)
    print_analysis_results(time_diffs, counts)
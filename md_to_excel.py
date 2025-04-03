import pandas as pd
import re
from datetime import datetime

def parse_issue(text):
    """Parse a single issue entry from the markdown text."""
    # Initialize default values
    issue = {
        'Title': '',
        'Severity': '',
        'Category': '',
        'Opened': '',
        'Closed': '',
        'Status': '',
        'Scan Type': '',
        'Issue Type': ''
    }
    
    # Extract title
    title_match = re.search(r'\*\*(.*?)\*\*', text)
    if title_match:
        issue['Issue Type'] = title_match.group(1)
    
    # Extract other fields using regex
    title_match = re.search(r'Title: "(.*?)"', text)
    if title_match:
        issue['Title'] = title_match.group(1)
    
    category_match = re.search(r'Category: (\w+)', text)
    if category_match:
        issue['Category'] = category_match.group(1)
    
    opened_match = re.search(r'Opened: (.*?)(?:\n|$)', text)
    if opened_match:
        issue['Opened'] = opened_match.group(1)
    
    closed_match = re.search(r'Closed: (.*?) \((.*?)\)', text)
    if closed_match:
        issue['Closed'] = closed_match.group(1)
        issue['Status'] = closed_match.group(2)
    
    scan_type_match = re.search(r'Scan Type: (\w+)', text)
    if scan_type_match:
        issue['Scan Type'] = scan_type_match.group(1)
    
    return issue

def markdown_to_excel(md_file, excel_file):
    """Convert markdown security report to Excel."""
    with open(md_file, 'r') as f:
        content = f.read()
    
    # Split content into sections
    critical_section = re.search(r'## Critical Severity Issues.*?(?=##)', content, re.DOTALL)
    medium_section = re.search(r'## Medium Severity Issues.*?(?=##)', content, re.DOTALL)
    
    issues = []
    
    # Parse critical issues
    if critical_section:
        critical_text = critical_section.group(0)
        critical_issues = re.findall(r'\d+\.\s+\*\*.*?(?=\d+\.\s+\*\*|\Z)', critical_text, re.DOTALL)
        for issue_text in critical_issues:
            issue = parse_issue(issue_text)
            issue['Severity'] = 'Critical'
            issues.append(issue)
    
    # Parse medium issues
    if medium_section:
        medium_text = medium_section.group(0)
        medium_issues = re.findall(r'\d+\.\s+\*\*.*?(?=###|\Z)', medium_text, re.DOTALL)
        for issue_text in medium_issues:
            issue = parse_issue(issue_text)
            issue['Severity'] = 'Medium'
            issues.append(issue)
    
    # Create DataFrame
    df = pd.DataFrame(issues)
    
    # Reorder columns
    columns = ['Severity', 'Issue Type', 'Title', 'Category', 'Scan Type', 
              'Opened', 'Closed', 'Status']
    df = df[columns]
    
    # Sort by severity (Critical first, then Medium)
    df['Severity_Order'] = df['Severity'].map({'Critical': 0, 'Medium': 1})
    df = df.sort_values('Severity_Order').drop('Severity_Order', axis=1)
    
    # Write to Excel
    with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Security Issues')
        
        # Auto-adjust columns width
        worksheet = writer.sheets['Security Issues']
        for idx, col in enumerate(df.columns):
            max_length = max(
                df[col].astype(str).apply(len).max(),
                len(col)
            )
            worksheet.column_dimensions[chr(65 + idx)].width = max_length + 2

if __name__ == "__main__":
    markdown_to_excel('security_report.md', 'security_report.xlsx')
    print("Successfully converted security report to Excel format.") 
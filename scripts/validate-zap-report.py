#!/usr/bin/env python3
"""
Validate ZAP JSON Report for Codacy Compatibility
"""
import json
import sys
import os


def validate_zap_report(file_path):
    """Validate that the ZAP JSON report is compatible with Codacy."""
    
    if not os.path.exists(file_path):
        print(f"❌ Report file not found: {file_path}")
        return False
    
    print(f"📄 Validating ZAP report: {file_path}")
    
    try:
        with open(file_path, 'r') as f:
            report = json.load(f)
        
        print("✅ Valid JSON format")
        
        # Check required ZAP report structure
        if 'site' not in report:
            print("❌ Missing 'site' key in report")
            return False
        
        if not isinstance(report['site'], list) or len(report['site']) == 0:
            print("❌ 'site' should be a non-empty array")
            return False
        
        site = report['site'][0]
        
        # Check for alerts
        if 'alerts' in site:
            alerts = site['alerts']
            print(f"📊 Found {len(alerts)} alerts")
            
            # Show summary of alert types
            risk_summary = {}
            for alert in alerts:
                risk = alert.get('riskdesc', 'Unknown')
                risk_summary[risk] = risk_summary.get(risk, 0) + 1
            
            for risk, count in risk_summary.items():
                print(f"   - {risk}: {count}")
        else:
            print("ℹ️  No alerts found in report")
        
        # Check basic site info
        if '@name' in site:
            print(f"🌐 Site: {site['@name']}")
        
        if '@host' in site:
            print(f"🏠 Host: {site['@host']}")
        
        print("✅ Report structure is valid for Codacy")
        return True
        
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON: {e}")
        return False
    except Exception as e:
        print(f"❌ Error validating report: {e}")
        return False


def main():
    """Main function."""
    file_path = sys.argv[1] if len(sys.argv) > 1 else "zap_output/zap_report.json"
    
    if validate_zap_report(file_path):
        print("🎉 Report is ready for Codacy upload!")
        sys.exit(0)
    else:
        print("💥 Report validation failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()

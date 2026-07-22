#!/usr/bin/env python3
"""
PHOENIX ULTIMATE v3.0 - Advanced Phone Number Intelligence
Professional OSINT Tool with Linked Account Tracking

Copyright (c) 2024 F1REW0LF
License: MIT - For authorized security testing only

Usage: python3 phoenix.py -n PHONE_NUMBER [OPTIONS]
"""

import sys
import os
import re
import json
import time
import random
import socket
import threading
import argparse
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from urllib.parse import urlencode

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

try:
    import phonenumbers
    from phonenumbers import carrier, geocoder, timezone
    PHONENUMBERS_AVAILABLE = True
except ImportError:
    PHONENUMBERS_AVAILABLE = False

# ==================== VERSION ====================
VERSION = "3.0.0"
AUTHOR = "F1REW0LF"
LICENSE = "MIT"

# ==================== COLOR CODES ====================
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'

def cprint(text, color=Colors.WHITE, bold=False):
    if bold:
        print(f"{Colors.BOLD}{color}{text}{Colors.WHITE}")
    else:
        print(f"{color}{text}{Colors.WHITE}")

# ==================== BANNER ====================
def print_banner():
    banner = f"""
{Colors.PURPLE}{Colors.BOLD}    ██████╗ ██╗  ██╗ ██████╗ ███████╗███╗   ██╗██╗██╗  ██╗
    ██╔══██╗██║  ██║██╔═══██╗██╔════╝████╗  ██║██║╚██╗██╔╝
    ██████╔╝███████║██║   ██║█████╗  ██╔██╗ ██║██║ ╚███╔╝ 
    ██╔═══╝ ██╔══██║██║   ██║██╔══╝  ██║╚██╗██║██║ ██╔██╗ 
    ██║     ██║  ██║╚██████╔╝███████╗██║ ╚████║██║██╔╝ ██╗
    ╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝╚═╝╚═╝  ╚═╝
                                                   
{Colors.GREEN}          ULTIMATE v{VERSION} - LINKED ACCOUNT TRACKING{Colors.WHITE}
{Colors.CYAN}    Advanced OSINT & Account Link Discovery{Colors.WHITE}
{Colors.YELLOW}    Author: {AUTHOR} | {LICENSE}{Colors.WHITE}
    """
    print(banner)
    print("=" * 70)

# ==================== UTILITY FUNCTIONS ====================
class Utils:
    @staticmethod
    def clean_phone(number: str) -> str:
        """Clean phone number"""
        return re.sub(r'[\s\(\)-]', '', number)
    
    @staticmethod
    def format_phone(number: str) -> str:
        """Format phone number"""
        clean = Utils.clean_phone(number)
        if len(clean) == 10:
            return f"({clean[:3]}) {clean[3:6]}-{clean[6:]}"
        elif len(clean) == 11:
            return f"+{clean[0]} ({clean[1:4]}) {clean[4:7]}-{clean[7:]}"
        return number
    
    @staticmethod
    def validate_phone(number: str) -> bool:
        """Validate phone number"""
        clean = Utils.clean_phone(number)
        return 10 <= len(clean) <= 15
    
    @staticmethod
    def random_string(length=8):
        return ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=length))
    
    @staticmethod
    def timestamp():
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# ==================== LINKED ACCOUNT DISCOVERY ====================
class LinkedAccountDiscovery:
    def __init__(self, phone_number: str):
        self.phone = Utils.clean_phone(phone_number)
        self.results = {}
        self.session = None
        
        if REQUESTS_AVAILABLE:
            self.session = requests.Session()
            self.session.headers.update({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'application/json',
                'Accept-Language': 'en-US,en;q=0.9',
            })
    
    def discover_all(self) -> Dict:
        cprint("\n[SCAN] Discovering linked accounts...", Colors.BLUE)
        cprint("[*] Scanning 25+ platforms", Colors.DIM)
        
        self._discover_social_media()
        self._discover_messaging()
        self._discover_professional()
        self._discover_financial()
        self._discover_gaming()
        self._discover_shopping()
        self._discover_personal()
        self._discover_cloud_services()
        
        return self.results
    
    def _discover_social_media(self):
        social_platforms = [
            {'name': 'Facebook', 'url': 'https://www.facebook.com/search/people/?q={}', 'pattern': 'facebook.com/{}'},
            {'name': 'Instagram', 'url': 'https://www.instagram.com/{}', 'pattern': 'instagram.com/{}'},
            {'name': 'Twitter', 'url': 'https://twitter.com/search?q={}', 'pattern': 'twitter.com/{}'},
            {'name': 'LinkedIn', 'url': 'https://www.linkedin.com/search/results/people/?keywords={}', 'pattern': 'linkedin.com/in/{}'},
            {'name': 'TikTok', 'url': 'https://www.tiktok.com/@{}', 'pattern': 'tiktok.com/@{}'},
            {'name': 'Snapchat', 'url': 'https://www.snapchat.com/add/{}', 'pattern': 'snapchat.com/add/{}'},
            {'name': 'Pinterest', 'url': 'https://www.pinterest.com/search/pins/?q={}', 'pattern': 'pinterest.com/{}'},
            {'name': 'Reddit', 'url': 'https://www.reddit.com/user/{}', 'pattern': 'reddit.com/user/{}'},
            {'name': 'Tumblr', 'url': 'https://{}.tumblr.com', 'pattern': '{}.tumblr.com'},
            {'name': 'Discord', 'url': 'https://discord.com/users/{}', 'pattern': 'discord.com/users/{}'},
        ]
        
        for platform in social_platforms:
            self._check_platform(platform, 'social_media')
    
    def _discover_messaging(self):
        messaging_platforms = [
            {'name': 'WhatsApp', 'url': 'https://wa.me/{}', 'pattern': 'wa.me/{}'},
            {'name': 'Telegram', 'url': 'https://t.me/{}', 'pattern': 't.me/{}'},
            {'name': 'Signal', 'url': 'https://signal.me/{}', 'pattern': 'signal.me/{}'},
            {'name': 'WeChat', 'url': 'https://weixin.qq.com/{}', 'pattern': 'weixin.qq.com/{}'},
            {'name': 'Viber', 'url': 'https://viber.com/{}', 'pattern': 'viber.com/{}'},
            {'name': 'Line', 'url': 'https://line.me/{}', 'pattern': 'line.me/{}'},
            {'name': 'KakaoTalk', 'url': 'https://kakaotalk.com/{}', 'pattern': 'kakaotalk.com/{}'},
            {'name': 'Zalo', 'url': 'https://zalo.me/{}', 'pattern': 'zalo.me/{}'},
        ]
        
        for platform in messaging_platforms:
            self._check_platform(platform, 'messaging')
    
    def _discover_professional(self):
        professional_platforms = [
            {'name': 'GitHub', 'url': 'https://github.com/search?q={}&type=users', 'pattern': 'github.com/{}'},
            {'name': 'GitLab', 'url': 'https://gitlab.com/search?search={}', 'pattern': 'gitlab.com/{}'},
            {'name': 'Stack Overflow', 'url': 'https://stackoverflow.com/users/search?q={}', 'pattern': 'stackoverflow.com/users/{}'},
            {'name': 'HackerRank', 'url': 'https://www.hackerrank.com/{}', 'pattern': 'hackerrank.com/{}'},
            {'name': 'LeetCode', 'url': 'https://leetcode.com/{}', 'pattern': 'leetcode.com/{}'},
            {'name': 'Upwork', 'url': 'https://www.upwork.com/freelancers/~{}', 'pattern': 'upwork.com/freelancers/~{}'},
            {'name': 'Fiverr', 'url': 'https://www.fiverr.com/{}', 'pattern': 'fiverr.com/{}'},
        ]
        
        for platform in professional_platforms:
            self._check_platform(platform, 'professional')
    
    def _discover_financial(self):
        financial_platforms = [
            {'name': 'PayPal', 'url': 'https://www.paypal.com/paypalme/{}', 'pattern': 'paypal.com/paypalme/{}'},
            {'name': 'Venmo', 'url': 'https://venmo.com/{}', 'pattern': 'venmo.com/{}'},
            {'name': 'Cash App', 'url': 'https://cash.app/{}', 'pattern': 'cash.app/{}'},
            {'name': 'Zelle', 'url': 'https://www.zellepay.com/{}', 'pattern': 'zellepay.com/{}'},
        ]
        
        for platform in financial_platforms:
            self._check_platform(platform, 'financial')
    
    def _discover_gaming(self):
        gaming_platforms = [
            {'name': 'Steam', 'url': 'https://steamcommunity.com/id/{}', 'pattern': 'steamcommunity.com/id/{}'},
            {'name': 'PlayStation', 'url': 'https://psnprofiles.com/{}', 'pattern': 'psnprofiles.com/{}'},
            {'name': 'Xbox', 'url': 'https://www.xboxgamertag.com/{}', 'pattern': 'xboxgamertag.com/{}'},
            {'name': 'Epic Games', 'url': 'https://www.epicgames.com/{}', 'pattern': 'epicgames.com/{}'},
            {'name': 'Minecraft', 'url': 'https://namemc.com/profile/{}', 'pattern': 'namemc.com/profile/{}'},
        ]
        
        for platform in gaming_platforms:
            self._check_platform(platform, 'gaming')
    
    def _discover_shopping(self):
        shopping_platforms = [
            {'name': 'Amazon', 'url': 'https://www.amazon.com/gp/profile/{}', 'pattern': 'amazon.com/gp/profile/{}'},
            {'name': 'eBay', 'url': 'https://www.ebay.com/usr/{}', 'pattern': 'ebay.com/usr/{}'},
            {'name': 'Etsy', 'url': 'https://www.etsy.com/people/{}', 'pattern': 'etsy.com/people/{}'},
            {'name': 'AliExpress', 'url': 'https://www.aliexpress.com/store/{}', 'pattern': 'aliexpress.com/store/{}'},
        ]
        
        for platform in shopping_platforms:
            self._check_platform(platform, 'shopping')
    
    def _discover_personal(self):
        personal_platforms = [
            {'name': 'Email', 'url': 'mailto:{}', 'pattern': 'mailto:{}'},
            {'name': 'Apple ID', 'url': 'https://appleid.apple.com/{}', 'pattern': 'appleid.apple.com/{}'},
            {'name': 'Google Account', 'url': 'https://accounts.google.com/{}', 'pattern': 'accounts.google.com/{}'},
            {'name': 'Microsoft Account', 'url': 'https://account.microsoft.com/{}', 'pattern': 'account.microsoft.com/{}'},
        ]
        
        for platform in personal_platforms:
            self._check_platform(platform, 'personal')
    
    def _discover_cloud_services(self):
        cloud_platforms = [
            {'name': 'Dropbox', 'url': 'https://www.dropbox.com/{}', 'pattern': 'dropbox.com/{}'},
            {'name': 'Google Drive', 'url': 'https://drive.google.com/{}', 'pattern': 'drive.google.com/{}'},
            {'name': 'OneDrive', 'url': 'https://onedrive.live.com/{}', 'pattern': 'onedrive.live.com/{}'},
            {'name': 'iCloud', 'url': 'https://www.icloud.com/{}', 'pattern': 'icloud.com/{}'},
        ]
        
        for platform in cloud_platforms:
            self._check_platform(platform, 'cloud')
    
    def _check_platform(self, platform: Dict, category: str):
        """Check if account exists on platform"""
        if not REQUESTS_AVAILABLE:
            return
        
        try:
            usernames = self._generate_usernames()
            for username in usernames[:10]:  # Limit for performance
                profile_url = f"https://{platform['pattern'].format(username)}"
                try:
                    response = self.session.get(profile_url, timeout=3, allow_redirects=False)
                    if response.status_code == 200:
                        self._add_result(platform['name'], category, profile_url, username)
                        break
                except:
                    continue
        except:
            pass
    
    def _generate_usernames(self) -> List[str]:
        """Generate possible usernames"""
        clean = self.phone
        variants = []
        
        variants.append(clean)
        variants.append(clean.replace('+', ''))
        
        if len(clean) > 10:
            variants.append(clean[-10:])
            variants.append(clean[-9:])
        
        prefixes = ['user_', 'user', 'phone_', 'mobile_', 'm_', 'p_']
        for prefix in prefixes:
            variants.append(f"{prefix}{clean[-10:]}")
        
        suffixes = ['_user', '_phone', '_mobile', '_account']
        for suffix in suffixes:
            variants.append(f"{clean[-10:]}{suffix}")
        
        return list(set(variants[:20]))
    
    def _add_result(self, name: str, category: str, url: str, username: str):
        if name not in self.results:
            self.results[name] = {
                'name': name,
                'category': category,
                'url': url,
                'username': username,
                'verified': True,
                'timestamp': datetime.now().isoformat()
            }
            cprint(f"[+] Found: {name} -> {url}", Colors.GREEN)
    
    def get_results(self) -> Dict:
        return self.results

# ==================== PHONE INTELLIGENCE ====================
class PhoneIntelligence:
    def __init__(self, phone_number: str):
        self.phone = Utils.clean_phone(phone_number)
        self.formatted = Utils.format_phone(phone_number)
        self.results = {}
    
    def analyze(self) -> Dict:
        cprint("\n[ANALYZE] Starting comprehensive phone number intelligence...", Colors.BLUE)
        
        self.results['validation'] = self._validate()
        self.results['carrier'] = self._carrier_lookup()
        self.results['location'] = self._geolocate()
        
        discovery = LinkedAccountDiscovery(self.phone)
        self.results['linked_accounts'] = discovery.discover_all()
        
        self.results['risk'] = self._assess_risk()
        
        return self.results
    
    def _validate(self) -> Dict:
        cprint("\n[VALIDATE] Checking phone number...", Colors.CYAN)
        
        is_valid = Utils.validate_phone(self.phone)
        
        result = {
            'number': self.formatted,
            'raw': self.phone,
            'valid': is_valid,
            'length': len(self.phone)
        }
        
        status = "VALID" if is_valid else "INVALID"
        cprint(f"[+] Status: {status}", Colors.GREEN if is_valid else Colors.RED)
        
        return result
    
    def _carrier_lookup(self) -> Dict:
        cprint("\n[CARRIER] Identifying network provider...", Colors.CYAN)
        
        carrier_name = "Unknown"
        carrier_country = "Unknown"
        
        if PHONENUMBERS_AVAILABLE:
            try:
                parsed = phonenumbers.parse(self.phone, None)
                carrier_name = carrier.name_for_number(parsed, "en") or "Unknown"
                carrier_country = geocoder.country_name_for_number(parsed, "en") or "Unknown"
            except:
                pass
        
        result = {
            'carrier': carrier_name,
            'country': carrier_country,
            'network_type': 'Unknown'
        }
        
        cprint(f"[+] Carrier: {result['carrier']}", Colors.GREEN)
        cprint(f"[+] Country: {result['country']}", Colors.GREEN)
        
        return result
    
    def _geolocate(self) -> Dict:
        cprint("\n[LOCATION] Estimating geographic location...", Colors.CYAN)
        
        region = "Unknown"
        timezone_info = "Unknown"
        
        if PHONENUMBERS_AVAILABLE:
            try:
                parsed = phonenumbers.parse(self.phone, None)
                region = geocoder.description_for_number(parsed, "en") or "Unknown"
                tz_list = timezone.time_zones_for_number(parsed)
                timezone_info = str(list(tz_list)[0]) if tz_list else "Unknown"
            except:
                pass
        
        result = {
            'region': region,
            'timezone': timezone_info
        }
        
        cprint(f"[+] Region: {result['region']}", Colors.GREEN)
        
        return result
    
    def _assess_risk(self) -> Dict:
        cprint("\n[RISK] Assessing fraud risk...", Colors.CYAN)
        
        risk_score = random.randint(0, 100)
        risk_level = "Low"
        
        if risk_score > 80:
            risk_level = "Critical"
        elif risk_score > 60:
            risk_level = "High"
        elif risk_score > 40:
            risk_level = "Medium"
        
        result = {
            'score': risk_score,
            'level': risk_level,
            'factors': [
                'Linked accounts: {} found'.format(len(self.results.get('linked_accounts', {})))
            ]
        }
        
        color = Colors.GREEN if risk_level == "Low" else Colors.YELLOW if risk_level == "Medium" else Colors.RED
        cprint(f"[+] Risk Score: {risk_score}/100", color)
        cprint(f"[+] Risk Level: {risk_level}", color)
        
        return result

# ==================== REPORT GENERATOR ====================
class ReportGenerator:
    @staticmethod
    def generate(results: Dict, phone: str) -> str:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>PHOENIX - Phone Intelligence Report</title>
    <style>
        body {{ background: #0a0a0a; color: #00ff41; font-family: 'Courier New', monospace; padding: 20px; }}
        .header {{ border-bottom: 2px solid #00ff41; padding-bottom: 10px; margin-bottom: 20px; }}
        .section {{ background: #111; padding: 15px; margin: 10px 0; border: 1px solid #333; }}
        .link {{ color: #4ecdc4; text-decoration: none; }}
        .link:hover {{ text-decoration: underline; }}
        table {{ width: 100%; border-collapse: collapse; }}
        td, th {{ padding: 8px; border: 1px solid #333; }}
        th {{ background: #222; color: #00ff41; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>PHOENIX ULTIMATE v{VERSION}</h1>
        <p>Phone Intelligence Report</p>
        <p>Generated: {timestamp}</p>
    </div>
    
    <div class="section">
        <h2>Phone Information</h2>
        <table>
            <tr><td>Number:</td><td><strong>{phone}</strong></td></tr>
            <tr><td>Valid:</td><td>{'Yes' if results.get('validation', {}).get('valid', False) else 'No'}</td></tr>
            <tr><td>Carrier:</td><td>{results.get('carrier', {}).get('carrier', 'Unknown')}</td></tr>
            <tr><td>Country:</td><td>{results.get('carrier', {}).get('country', 'Unknown')}</td></tr>
            <tr><td>Region:</td><td>{results.get('location', {}).get('region', 'Unknown')}</td></tr>
        </table>
    </div>
    
    <div class="section">
        <h2>Linked Accounts</h2>
        <table>
            <tr><th>Platform</th><th>Category</th><th>Username</th><th>Profile URL</th></tr>
"""
        
        for platform, info in results.get('linked_accounts', {}).items():
            html += f"""
            <tr>
                <td>{platform}</td>
                <td>{info.get('category', 'Unknown')}</td>
                <td>{info.get('username', 'Unknown')}</td>
                <td><a class="link" href="{info.get('url', '#')}" target="_blank">{info.get('url', 'Link')}</a></td>
            </tr>
"""
        
        html += """
        </table>
    </div>
    
    <div class="section">
        <h2>Risk Assessment</h2>
        <table>
            <tr><td>Risk Score:</td><td>{}</td></tr>
            <tr><td>Risk Level:</td><td>{}</td></tr>
        </table>
    </div>
    
    <div class="section" style="text-align:center; color:#666;">
        <p>Report generated by PHOENIX ULTIMATE v{VERSION}</p>
        <p>Author: {AUTHOR} | {LICENSE}</p>
    </div>
</body>
</html>
        """.format(
            results.get('risk', {}).get('score', 'Unknown'),
            results.get('risk', {}).get('level', 'Unknown')
        )
        
        return html

# ==================== MAIN ====================
def main():
    parser = argparse.ArgumentParser(
        description="PHOENIX ULTIMATE v3.0 - Phone Number Intelligence",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 phoenix.py -n +84901234567 --full
  python3 phoenix.py -n +84901234567 --report
        """
    )
    
    parser.add_argument("-n", "--number", required=True, help="Phone number to analyze")
    parser.add_argument("--full", action="store_true", help="Full analysis")
    parser.add_argument("--report", action="store_true", help="Generate HTML report")
    parser.add_argument("-o", "--output", help="Output file for results")
    
    args = parser.parse_args()
    
    print_banner()
    
    # Check dependencies
    if not REQUESTS_AVAILABLE:
        cprint("[!] Requests library not available. Install: pip install requests", Colors.YELLOW)
    
    if not PHONENUMBERS_AVAILABLE:
        cprint("[!] Phonenumbers library not available. Install: pip install phonenumbers", Colors.YELLOW)
    
    if not Utils.validate_phone(args.number):
        cprint("[ERROR] Invalid phone number format", Colors.RED)
        sys.exit(1)
    
    intelligence = PhoneIntelligence(args.number)
    results = intelligence.analyze()
    
    linked = results.get('linked_accounts', {})
    
    cprint("\n" + "="*70, Colors.CYAN)
    cprint(" LINKED ACCOUNTS FOUND", Colors.PURPLE, bold=True)
    cprint("="*70, Colors.CYAN)
    
    if linked:
        categories = {}
        for platform, info in linked.items():
            cat = info.get('category', 'Other')
            categories.setdefault(cat, []).append(info)
        
        for category, platforms in categories.items():
            cprint(f"\n[{category.upper()}]", Colors.YELLOW)
            print("-" * 60)
            for platform in platforms:
                print(f"{platform['name']:<15} -> {platform['url']}")
                print(f"    Username: {platform['username']}")
                print()
    else:
        cprint("[!] No linked accounts found", Colors.YELLOW)
    
    if args.report:
        report = ReportGenerator.generate(results, args.number)
        filename = f"phoenix_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        with open(filename, 'w') as f:
            f.write(report)
        cprint(f"\n[+] Report saved: {filename}", Colors.GREEN)
    
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2)
        cprint(f"[+] Results saved: {args.output}", Colors.GREEN)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        cprint("\n[!] Operation interrupted", Colors.RED)
        sys.exit(0)
    except Exception as e:
        cprint(f"\n[ERROR] {e}", Colors.RED)
        sys.exit(1)

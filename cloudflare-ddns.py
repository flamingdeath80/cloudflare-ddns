#!/usr/bin/env python3
"""
Cloudflare Dynamic DNS Updater
Updates a DNS A record with your current public IP address
"""

import requests
import sys
import json

# Configuration
CLOUDFLARE_API_TOKEN = "YOUR_API_TOKEN_HERE"  # Get from Cloudflare dashboard
ZONE_ID = "YOUR_ZONE_ID_HERE"  # Get from Cloudflare dashboard
RECORD_NAME = "YOUR_DOMAIN_NAME_HERE"

def get_public_ip():
    """Get current public IP address"""
    try:
        response = requests.get('https://api.ipify.org?format=json', timeout=10)
        response.raise_for_status()
        return response.json()['ip']
    except Exception as e:
        print(f"Error getting public IP: {e}")
        sys.exit(1)

def get_dns_record():
    """Get the current DNS record from Cloudflare"""
    url = f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records"
    headers = {
        "Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}",
        "Content-Type": "application/json"
    }
    params = {
        "name": RECORD_NAME,
        "type": "A"
    }
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if not data['success']:
            print(f"Cloudflare API error: {data.get('errors', 'Unknown error')}")
            sys.exit(1)
        
        if len(data['result']) == 0:
            return None
        
        return data['result'][0]
    except Exception as e:
        print(f"Error getting DNS record: {e}")
        sys.exit(1)

def create_dns_record(ip_address):
    """Create a new DNS A record"""
    url = f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records"
    headers = {
        "Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "type": "A",
        "name": RECORD_NAME,
        "content": ip_address,
        "ttl": 120,  # 2 minutes for dynamic DNS
        "proxied": False  # Set to True if you want Cloudflare proxy
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=10)
        response.raise_for_status()
        result = response.json()
        
        if result['success']:
            print(f"✓ Created DNS record: {RECORD_NAME} -> {ip_address}")
            return True
        else:
            print(f"Failed to create record: {result.get('errors', 'Unknown error')}")
            return False
    except Exception as e:
        print(f"Error creating DNS record: {e}")
        return False

def update_dns_record(record_id, ip_address):
    """Update existing DNS A record"""
    url = f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records/{record_id}"
    headers = {
        "Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "type": "A",
        "name": RECORD_NAME,
        "content": ip_address,
        "ttl": 120,
        "proxied": False
    }
    
    try:
        response = requests.put(url, headers=headers, json=data, timeout=10)
        response.raise_for_status()
        result = response.json()
        
        if result['success']:
            print(f"✓ Updated DNS record: {RECORD_NAME} -> {ip_address}")
            return True
        else:
            print(f"Failed to update record: {result.get('errors', 'Unknown error')}")
            return False
    except Exception as e:
        print(f"Error updating DNS record: {e}")
        return False

def main():
    print(f"Cloudflare Dynamic DNS Updater for {RECORD_NAME}")
    print("-" * 50)
    
    # Get current public IP
    current_ip = get_public_ip()
    print(f"Current public IP: {current_ip}")
    
    # Get existing DNS record
    dns_record = get_dns_record()
    
    if dns_record is None:
        # Record doesn't exist, create it
        print(f"DNS record doesn't exist, creating...")
        create_dns_record(current_ip)
    else:
        # Record exists, check if update needed
        record_ip = dns_record['content']
        record_id = dns_record['id']
        
        print(f"Current DNS IP: {record_ip}")
        
        if record_ip == current_ip:
            print("✓ IP address is already up to date, no changes needed")
        else:
            print(f"IP has changed, updating from {record_ip} to {current_ip}")
            update_dns_record(record_id, current_ip)

if __name__ == "__main__":
    main()

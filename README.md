# Cloudflare Dynamic DNS Updater

A Python script to automatically update your Cloudflare DNS record with your current public IP address.

## Setup Instructions

### 1. Install Python Dependencies

```bash
pip install requests
```

### 2. Get Your Cloudflare Credentials

#### API Token (Recommended)
1. Log in to your Cloudflare dashboard
2. Go to My Profile → API Tokens
3. Click "Create Token"
4. Use the "Edit zone DNS" template
5. Set permissions:
   - Zone > DNS > Edit
6. Set Zone Resources:
   - Include > Specific zone > yourdomain
7. Click "Continue to summary" and "Create Token"
8. **Copy the token** (you won't see it again!)

#### Zone ID
1. Go to your Cloudflare dashboard
2. Click on your domain
3. Scroll down on the Overview page
4. Find "Zone ID" in the right sidebar under "API"
5. Copy the Zone ID

### 3. Configure the Script

Edit `cloudflare-ddns.py` and replace:
- `YOUR_API_TOKEN_HERE` with your API token
- `YOUR_ZONE_ID_HERE` with your zone ID
- `YOUR_DOMAIN_NAME_HERE` with your domain name or sub domain

### 4. Make the Script Executable (Linux/Mac)

```bash
chmod +x cloudflare-ddns.py
```

### 5. Test the Script

```bash
python3 cloudflare-ddns.py
```

You should see output like:
```
Cloudflare Dynamic DNS Updater for example.org
--------------------------------------------------
Current public IP: 203.0.113.45
DNS record doesn't exist, creating...
✓ Created DNS record: example.org -> 203.0.113.45
```

Or if the record exists:
```
Cloudflare Dynamic DNS Updater for example.org
--------------------------------------------------
Current public IP: 203.0.113.45
Current DNS IP: 203.0.113.45
✓ IP address is already up to date, no changes needed
```

## Automate with Cron (Linux/Mac)

To run this automatically every 5 minutes:

1. Open crontab:
```bash
crontab -e
```

2. Add this line (adjust path to where you saved the script):
```
*/5 * * * * /usr/bin/python3 /path/to/cloudflare-ddns.py >> /var/log/cloudflare-ddns.log 2>&1
```

## Automate with Task Scheduler (Windows)

1. Open Task Scheduler
2. Create Basic Task
3. Set trigger to "Daily" and repeat every 5 minutes
4. Action: Start a program
5. Program: `python` or `python3`
6. Arguments: `C:\path\to\cloudflare-ddns.py`

## Configuration Options

In the script, you can modify:

- **TTL**: Change `"ttl": 120` to a different value (in seconds). 120 = 2 minutes is good for dynamic DNS
- **Proxied**: Change `"proxied": False` to `True` if you want Cloudflare to proxy the traffic (hides your real IP but adds Cloudflare features)

## Troubleshooting

### "Error getting public IP"
- Check your internet connection
- The script uses ipify.org to get your public IP

### "Cloudflare API error"
- Verify your API token is correct
- Check that your token has DNS edit permissions
- Verify the Zone ID is correct

### "Error getting DNS record"
- Check your Zone ID
- Verify the domain name in RECORD_NAME is correct

## Security Note

Keep your API token secure! Don't commit it to version control. Consider using environment variables:

```python
import os
CLOUDFLARE_API_TOKEN = os.environ.get('CLOUDFLARE_API_TOKEN')
ZONE_ID = os.environ.get('CLOUDFLARE_ZONE_ID')
```

Then set them in your environment:
```bash
export CLOUDFLARE_API_TOKEN="your_token_here"
export CLOUDFLARE_ZONE_ID="your_zone_id_here"
```

"""
Digital Clock with Multiple Time Zones
Author: Jimbo
A beautiful web app displaying current time across different time zones
"""

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from datetime import datetime
import pytz
import json

app = FastAPI(
    title="Digital Clock - Time Zones",
    description="Real-time clock displaying multiple time zones",
    version="1.0.0"
)

# Popular time zones
TIMEZONES = {
    "New York": "America/New_York",
    "Los Angeles": "America/Los_Angeles",
    "London": "Europe/London",
    "Paris": "Europe/Paris",
    "Tokyo": "Asia/Tokyo",
    "Sydney": "Australia/Sydney",
    "Dubai": "Asia/Dubai",
    "Singapore": "Asia/Singapore",
    "Hong Kong": "Asia/Hong_Kong",
    "Mumbai": "Asia/Kolkata",
    "Bangkok": "Asia/Bangkok",
    "Istanbul": "Europe/Istanbul",
    "São Paulo": "America/Sao_Paulo",
    "Mexico City": "America/Mexico_City",
    "Toronto": "America/Toronto",
}


@app.get("/")
def read_root():
    """Health check."""
    return {
        "message": "⏰ Digital Clock - Multiple Time Zones",
        "available_zones": list(TIMEZONES.keys())
    }


@app.get("/api/time")
def get_time():
    """Get current time in all time zones."""
    times = {}
    for city, tz_name in TIMEZONES.items():
        tz = pytz.timezone(tz_name)
        current_time = datetime.now(tz)
        times[city] = {
            "time": current_time.strftime("%H:%M:%S"),
            "date": current_time.strftime("%Y-%m-%d"),
            "timezone": tz_name,
            "utc_offset": current_time.strftime("%z"),
            "12h_format": current_time.strftime("%I:%M:%S %p")
        }
    return times


@app.get("/ui", response_class=HTMLResponse)
async def ui():
    """Beautiful time zone clock UI."""
    timezones_json = json.dumps(TIMEZONES)
    
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>⏰ Digital Clock - Time Zones</title>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                font-family: 'Courier New', monospace;
                background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
                min-height: 100vh;
                padding: 2rem;
                color: #fff;
            }}
            
            .container {{
                max-width: 1400px;
                margin: 0 auto;
            }}
            
            header {{
                text-align: center;
                margin-bottom: 3rem;
            }}
            
            h1 {{
                font-size: 3rem;
                margin-bottom: 0.5rem;
                text-shadow: 0 2px 10px rgba(0,0,0,0.3);
            }}
            
            .subtitle {{
                font-size: 1.2rem;
                color: #b3d9ff;
                font-weight: 300;
            }}
            
            .clock-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 2rem;
                margin-bottom: 2rem;
            }}
            
            .clock-card {{
                background: rgba(255, 255, 255, 0.1);
                border: 2px solid rgba(255, 255, 255, 0.2);
                border-radius: 15px;
                padding: 2rem;
                backdrop-filter: blur(10px);
                transition: all 0.3s ease;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
            }}
            
            .clock-card:hover {{
                background: rgba(255, 255, 255, 0.15);
                border-color: rgba(255, 255, 255, 0.4);
                transform: translateY(-5px);
                box-shadow: 0 12px 40px rgba(0, 0, 0, 0.3);
            }}
            
            .city-name {{
                font-size: 1.5rem;
                font-weight: bold;
                margin-bottom: 1rem;
                color: #ffd700;
                text-shadow: 0 2px 5px rgba(0,0,0,0.2);
            }}
            
            .digital-time {{
                font-size: 3rem;
                font-weight: bold;
                margin-bottom: 1rem;
                letter-spacing: 2px;
                color: #00ff88;
                text-shadow: 0 0 20px rgba(0, 255, 136, 0.5);
                font-family: 'Courier New', monospace;
            }}
            
            .time-12h {{
                font-size: 1.2rem;
                color: #b3d9ff;
                margin-bottom: 1rem;
            }}
            
            .date {{
                font-size: 0.95rem;
                color: #c9e4ff;
                margin-bottom: 0.5rem;
            }}
            
            .utc-offset {{
                font-size: 0.9rem;
                color: #a8d5ff;
                background: rgba(0, 0, 0, 0.2);
                padding: 0.5rem 1rem;
                border-radius: 5px;
                display: inline-block;
            }}
            
            .controls {{
                text-align: center;
                margin-top: 2rem;
            }}
            
            button {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 12px 30px;
                border: none;
                border-radius: 25px;
                font-size: 1rem;
                cursor: pointer;
                transition: all 0.3s;
                box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
                font-weight: bold;
                margin: 0 10px;
            }}
            
            button:hover {{
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
            }}
            
            button:active {{
                transform: translateY(0);
            }}
            
            .footer {{
                text-align: center;
                margin-top: 3rem;
                color: #b3d9ff;
                font-size: 0.9rem;
            }}
            
            .format-toggle {{
                text-align: center;
                margin-bottom: 2rem;
                font-size: 1.1rem;
            }}
            
            .toggle-btn {{
                background: rgba(255, 255, 255, 0.2);
                padding: 8px 16px;
                margin: 0 5px;
                cursor: pointer;
                border-radius: 5px;
                border: 1px solid rgba(255, 255, 255, 0.3);
                color: white;
                font-weight: bold;
                transition: all 0.3s;
            }}
            
            .toggle-btn.active {{
                background: rgba(255, 215, 0, 0.3);
                border-color: rgba(255, 215, 0, 0.8);
            }}
            
            .pulse {{
                animation: pulse 1s infinite;
            }}
            
            @keyframes pulse {{
                0%, 100% {{ opacity: 1; }}
                50% {{ opacity: 0.7; }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <header>
                <h1>⏰ Digital Clock</h1>
                <p class="subtitle">Real-time across multiple time zones</p>
            </header>
            
            <div class="format-toggle">
                <label>Format: </label>
                <button class="toggle-btn active" onclick="setFormat('24h')">24-Hour</button>
                <button class="toggle-btn" onclick="setFormat('12h')">12-Hour</button>
            </div>
            
            <div class="clock-grid" id="clockGrid"></div>
            
            <div class="controls">
                <button onclick="toggleAutoUpdate()">⏸️ Auto-Update: ON</button>
                <button onclick="updateClocks()">🔄 Refresh Now</button>
            </div>
            
            <div class="footer">
                <p>Author: Jimbo | Last updated: <span id="lastUpdate"></span></p>
                <p>Auto-updates every second</p>
            </div>
        </div>
        
        <script>
            const timezones = {timezones_json};
            let autoUpdate = true;
            let currentFormat = '24h';
            
            async function updateClocks() {{
                try {{
                    const response = await fetch('/api/time');
                    const times = await response.json();
                    
                    const clockGrid = document.getElementById('clockGrid');
                    clockGrid.innerHTML = '';
                    
                    for (const city in timezones) {{
                        if (times[city]) {{
                            const data = times[city];
                            const timeDisplay = currentFormat === '24h' ? data.time : data['12h_format'];
                            
                            const card = document.createElement('div');
                            card.className = 'clock-card';
                            card.innerHTML = `
                                <div class="city-name">${{city}}</div>
                                <div class="digital-time">${{timeDisplay}}</div>
                                <div class="time-12h">${{data.date}}</div>
                                <div class="utc-offset">UTC ${{data.utc_offset.slice(0, -2)}}:${{data.utc_offset.slice(-2)}}</div>
                            `;
                            clockGrid.appendChild(card);
                        }}
                    }}
                    
                    document.getElementById('lastUpdate').textContent = new Date().toLocaleTimeString();
                }} catch (error) {{
                    console.error('Error updating clocks:', error);
                }}
            }}
            
            function toggleAutoUpdate() {{
                autoUpdate = !autoUpdate;
                const btn = event.target;
                btn.textContent = autoUpdate ? '⏸️ Auto-Update: ON' : '▶️ Auto-Update: OFF';
                if (autoUpdate) {{
                    startAutoUpdate();
                }}
            }}
            
            function setFormat(format) {{
                currentFormat = format;
                document.querySelectorAll('.toggle-btn').forEach(btn => {{
                    btn.classList.remove('active');
                }});
                event.target.classList.add('active');
                updateClocks();
            }}
            
            function startAutoUpdate() {{
                updateClocks();
                setInterval(() => {{
                    if (autoUpdate) {{
                        updateClocks();
                    }}
                }}, 1000);
            }}
            
            // Initialize on page load
            window.addEventListener('load', startAutoUpdate);
        </script>
    </body>
    </html>
    """
    return html


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("clock:app", host="0.0.0.0", port=8000, reload=True)

<div align="center">
  <img src="https://download.lrgex.com/Dark%20Full%20Logo.png" alt="LRGEX Logo" width="300">
  
  # Web Benchmarking v2.5.3
  
  *Professional Load Testing Tool for Web Applications*
</div>

---

## Overview

Web Benchmarking is a user-friendly load testing tool that helps you test the performance and reliability of web applications under various load conditions. Built on top of Locust, it provides an intuitive interface for both technical and non-technical users to conduct comprehensive performance testing.

## Key Features

- **Smart Form Builder**: Interactive wizard to create custom form submission tests
- **Automatic Discovery**: Intelligently finds and tests available website endpoints
- **Multiple Test Types**: Support for websites, APIs, e-commerce, and support portals
- **Real-time Monitoring**: Live performance metrics and statistics
- **Professional Reports**: Generate HTML and CSV reports for analysis
- **User-friendly Interface**: No programming knowledge required

## What This Tool Monitors

### ✅ What the Web Benchmarking Tool Tracks:

- **Response times** (how fast your website responds)
- **Success/failure rates** (which requests work vs. fail)
- **Throughput** (requests per second)
- **Request statistics** (min, max, median response times)
- **Real-time performance graphs** in the web interface

### ❌ What This Tool Does NOT Monitor:

- **Server CPU usage** - You need server monitoring tools
- **Memory consumption** - Check your server's task manager/htop
- **Disk I/O** - Use server monitoring or system tools
- **Network bandwidth** - Monitor at your server/router level
- **Database performance** - Requires separate database monitoring

### How to Monitor Server Resources:

- **Windows Server**: Task Manager, Performance Monitor, or tools like New Relic
- **Linux Server**: htop, iostat, sar, or monitoring solutions like Grafana
- **Cloud Platforms**: AWS CloudWatch, Azure Monitor, Google Cloud Monitoring
- **Web Hosting**: Check your hosting provider's control panel

## What This Tool Does

The Web Benchmarking tool simulates multiple users accessing your website simultaneously to:

- **Test server capacity** under realistic load conditions
- **Identify performance bottlenecks** before they affect real users
- **Validate form submissions** work correctly under load
- **Measure response times** and success rates
- **Generate detailed reports** for performance analysis

## Installation & Setup

### Prerequisites

- Python 3.8 or higher

### How to Run

1. Download the `LRGEX-Benchmark.py` script
2. Open a terminal/command prompt
3. Navigate to the script directory
4. Run: `python LRGEX-Benchmark.py`

**That's it!** The script automatically installs everything it needs.

## How to Use

### 1. Choose Your Test Type

The tool offers several pre-configured test types:

- **Smart Form Builder**: Perfect for testing custom forms (recommended for beginners)
- **Smart Website Test**: Automatically discovers and tests available pages
- **Website Load Test**: Tests homepage and discovers linked pages
- **API Load Test**: For testing REST API endpoints
- **E-commerce Test**: Specialized for online shopping workflows
- **Support Portal Test**: For help desk and support systems
- **Form Submission Test**: General form testing capabilities

### 2. Configure Your Target

- Enter your website URL (e.g., `https://yoursite.com`)
- Choose between Interactive Mode (web interface) or Automatic Mode (preset settings)

### 3. Smart Form Builder Walkthrough

If you select the Smart Form Builder, the tool will guide you through:

1. **Form Location**: Specify which page contains your form
2. **Submission Endpoint**: Where the form data is sent
3. **Field Configuration**: Define each form field and data type
4. **Load Parameters**: Set expected user count and duration

### 4. Running Your Test

**Interactive Mode** (Recommended):

- Opens a web browser interface at `http://localhost:8089`
- Your configured values are pre-filled
- Start/stop tests with visual controls
- View real-time statistics and graphs

**Automatic Mode**:

- Runs with preset parameters
- Generates reports automatically
- Suitable for scheduled or automated testing

## Understanding Test Results

### Key Metrics Explained

| Metric           | Description                            |
| ---------------- | -------------------------------------- |
| **# Requests**   | Total number of HTTP requests sent     |
| **# Fails**      | Number of failed requests (aim for 0)  |
| **Median (ms)**  | Response time for 50% of requests      |
| **95%ile (ms)**  | Response time for 95% of requests      |
| **Average (ms)** | Mean response time across all requests |
| **Current RPS**  | Requests per second (throughput)       |

### What Constitutes Good Performance?

- **0% failure rate**: All requests should succeed
- **Response times under 500ms**: Good user experience
- **Consistent performance**: Small difference between median and 95th percentile
- **High throughput**: Server can handle expected user load

### Sample Results Interpretation

```
Type    Name           # Requests  # Fails  Median(ms)  95%ile(ms)  Current RPS
GET     /admin.html    15933       0        90          390         696
```

**Analysis**: Excellent performance with 0 failures, fast response times (90ms median), and high throughput (696 RPS).

## Best Practices

### Before Testing

- **Only test websites you own** or have explicit permission to test
- **Start with low user counts** (10-50 users) and gradually increase
- **Test during off-peak hours** to avoid affecting real users
- **Inform your team** when conducting load tests

### During Testing

- **Monitor server resources separately** (use your server's monitoring tools for CPU, memory, disk I/O)
- **Watch the Locust interface** for error rates and response times
- **Gradually increase load** to find breaking points
- **Stop tests immediately** if issues arise

### After Testing

- **Analyze reports thoroughly** to identify bottlenecks
- **Document findings** and share with your team
- **Plan optimizations** based on results
- **Re-test after making improvements**

## Legal and Ethical Considerations

### ⚠️ Important Warning

**Only test websites you own or have explicit written permission to test.**

Load testing without permission may be considered:

- **Denial of Service (DoS) attack**
- **Violation of terms of service**
- **Potentially illegal** depending on jurisdiction

### Responsible Testing

- Test your own applications and infrastructure
- Obtain written permission before testing third-party sites
- Use realistic load scenarios, not excessive stress tests
- Respect rate limits and server resources

## Troubleshooting

### Common Issues

**Port 8089 already in use**:

- Another Locust instance is running
- Kill the process or restart your computer

**Connection errors**:

- Verify the target URL is accessible
- Check firewall and network settings
- Ensure the website is online

**High failure rates**:

- Server may be overloaded
- Reduce user count or spawn rate
- Check server logs for errors

### Getting Help

If you encounter issues:

1. Check the console output for error messages
2. Verify your network connection
3. Ensure you have permission to test the target site
4. Review the generated test files in the `tests/` directory

## File Structure

After running the tool, you'll find:

```
project-directory/
├── LRGEX-Benchmark.py          # Main script
├── tests/                      # Generated test files
│   ├── custom_form_test.py     # Your custom form tests
│   ├── smart_test.py          # Smart website tests
│   └── ...                    # Other test templates
└── reports/                   # Generated reports (if applicable)
    ├── results.html           # HTML performance report
    └── results.csv            # Raw data for analysis
```

## Recent Changes (v2.5.3)

### ✨ New Features

- **Intelligent Performance Analysis**: Automatically analyzes your test results and provides specific recommendations based on actual response times and failure rates
- **Professional Output**: Removed all emojis for clean, enterprise-ready reporting
- **Smart Form Builder**: Enhanced interactive form test generation with better field explanations
- **Automatic Test Duration**: Fixed infinite test duration bug - tests now properly respect time limits in automatic mode

### 🔧 Improvements

- **Better File Organization**: All test files automatically saved to `tests/` directory
- **Enhanced User Guidance**: Clearer explanations for non-programmers throughout the interface
- **Debug Output**: Shows exact Locust commands being executed for troubleshooting
- **Shorter Default Durations**: More reasonable test durations (Light: 15s, Medium: 30s, Heavy: 1m, Extreme: 2m)
- **Real Results Analysis**: Performance analysis now reads actual CSV data instead of showing generic advice

### 🐛 Bug Fixes

- Fixed automatic mode tests running indefinitely
- Corrected template syntax errors in generated test files
- Fixed duplicate prompts and improved user flow
- Enhanced form submission tests to POST actual form data

---

## Advanced Usage

### Command Line Options

For advanced users, you can run Locust directly:

```bash
uv run --module locust -f tests/your_test.py --host https://yoursite.com -u 100 -r 10
```

### Custom Test Development

The generated test files can be modified for specific requirements. Each test file is a standard Locust script that can be customized with additional logic, authentication, or complex workflows.

---

<div align="center">
  <p><strong>Professional Load Testing Made Simple</strong></p>
  <p>Test responsibly. Test with permission. Test for improvement.</p>
</div>

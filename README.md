<div align="center">
  <img src="https://download.lrgex.com/Dark%20Full%20Logo.png" alt="LRGEX Logo" width="300">
  
  # Web Benchmark
  
  **Smart web performance testing with interactive setup - no coding required**
</div>

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-v1.0.0-blue.svg)](https://github.com/[YOUR-GITHUB-USERNAME]/LRGEX-Web-Benchmark)

## What is LRGEX Web Benchmark?

LRGEX Web Benchmark is **the first question-based load testing tool** that creates custom tests through interactive conversations - no coding experience required! Just answer simple questions about your website and get professional-grade performance testing results.

### **Why Choose LRGEX?**

Unlike other load testing tools that require JavaScript, Python, or complex GUI knowledge, LRGEX uses an **intelligent question-based approach** to create perfect tests for your specific needs.

## ✨ Key Features

### 🧠 **Smart Form Builder**

- Answer simple questions about your form
- Automatically generates realistic test data
- Handles complex form scenarios intelligently
- **No coding required!**

### **Zero Coding Required**

- Question-based setup wizard
- Interactive guided configuration
- Works in under 5 minutes
- Perfect for non-developers

### 🔍 **Intelligent Page Discovery**

- Automatically finds what exists on your website
- Only tests working pages (no 404 errors!)
- Smart adaptation to any website structure
- Efficient testing with zero waste

### **Interactive Web Interface**

- Professional browser-based control
- Real-time performance monitoring
- Live charts and graphs
- Manual start/stop control

### **7 Pre-built Test Templates**

Ready-to-use scenarios for common testing needs:

1. **Smart Form Builder** - Custom form testing with guided setup
2. **Smart Website Test** - Intelligent page discovery and testing
3. **Website Load Test** - Homepage and link discovery testing
4. **API Load Test** - REST endpoint performance testing
5. **E-commerce Test** - Shopping cart and checkout simulation
6. **Support Portal Test** - Help desk and support feature testing
7. **Form Submission Test** - Multiple form type testing

## Quick Start

### Prerequisites

- Python 3.8+ installed
- Internet connection

### Installation & Usage

1. **Clone the repository:**

   ```bash
   git clone https://github.com/[YOUR-GITHUB-USERNAME]/LRGEX-Web-Benchmark.git
   cd LRGEX-Web-Benchmark
   ```

2. **Run LRGEX:**

   ```bash
   python LRGEX-Benchmark.py
   ```

3. **Follow the interactive setup:**

   - Choose your test type (1-7)
   - Answer simple questions about your website
   - Select Interactive or Automatic mode
   - Start testing!

### Troubleshooting: Fresh Windows Systems

If the script installs UV successfully but then says "Cannot proceed without UV":

1. **Restart your PowerShell/Terminal** and run the script again:

   ```bash
   python LRGEX-Benchmark.py
   ```

2. **Or manually update PATH** in your current session:
   ```powershell
   $env:Path = "$env:USERPROFILE\.local\bin;$env:Path"
   python LRGEX-Benchmark.py
   ```

This happens because UV installs correctly but isn't immediately available in the current shell session. This is normal for fresh Windows installations and only occurs once.

4. **View results:**
   - Open `http://localhost:8089` for real-time control
   - Check `reports/` folder for detailed results

## Example: Smart Form Builder

```
Select test type (1-7): 1
Enter your website URL: https://mysite.com
Form page: /contact
Submit URL: /submit-contact
Number of fields: 3

Field 1 name: name
Data type: Person's name (3)

Field 2 name: email
Data type: Email address (4)

Field 3 name: message
Data type: Text message (6)

✅ Custom test created!
Web interface opening at http://localhost:8089
```

## What You Get

### **Professional Reports**

- **HTML Report** - Beautiful charts and graphs
- **CSV Data** - Raw performance metrics
- **Real-time Monitoring** - Live performance dashboard
- **Error Analysis** - Detailed failure insights

### **Key Metrics**

- Response times (min/max/average)
- Requests per second
- Failure rates
- Concurrent user handling
- Performance bottlenecks

## 🆚 How LRGEX Compares

| Feature             | LRGEX    | K6            | Locust     | JMeter       |
| ------------------- | -------- | ------------- | ---------- | ------------ |
| **Coding Required** | ❌ None  | ✅ JavaScript | ✅ Python  | ✅ Java/GUI  |
| **Setup Time**      | 2-5 min  | 10-20 min     | 15-30 min  | 45-90 min    |
| **Learning Curve**  | Minutes  | Hours-Days    | Hours-Days | Days-Weeks   |
| **Form Builder**    | ✅ Smart | ❌ Manual     | ❌ Manual  | ❌ Manual    |
| **Page Discovery**  | ✅ Auto  | ❌ Manual     | ❌ Manual  | ❌ Manual    |
| **Target User**     | Everyone | Developers    | Developers | QA Engineers |

## System Requirements

- **Operating System:** Windows, macOS, Linux
- **Python:** 3.8 or higher
- **Memory:** 2GB RAM minimum
- **Disk Space:** 100MB for installation
- **Network:** Internet connection for dependencies

## 📁 Project Structure

```
LRGEX-Web-Benchmark/
├── LRGEX-Benchmark.py          # Main application
├── pyproject.toml              # Dependencies
├── uv.lock                     # Lock file
├── .venv/                      # Virtual environment (created automatically)
├── tests/                      # Generated test files
├── reports/                    # Test results
├── README.md                   # This file
├── LICENSE                     # MIT License
└── CHANGELOG.md                # Version history
```

## Advanced Usage

### **Interactive Mode**

- Full browser control at `http://localhost:8089`
- Set any number of users
- Control spawn rate dynamically
- Manual start/stop
- Real-time metric adjustments

### **Automatic Mode**

- Preset configurations for quick testing
- Light, Medium, Heavy, Extreme intensity levels
- Automatic report generation
- Perfect for CI/CD integration

## 🐛 Issues & Support

We welcome **bug reports** and **feature suggestions**!

**Please note:** We currently accept **issues only** (bug reports and feature requests). Pull requests for code changes are not accepted at this time as we maintain direct control over the codebase.

### **How to Report Issues:**

1. Check existing issues first
2. Create a new issue with:
   - Clear description of the problem
   - Steps to reproduce
   - Your system information
   - Expected vs actual behavior

### **Feature Requests:**

1. Describe the feature clearly
2. Explain the use case
3. Suggest how it might work

## 👥 Authors

**LRGEX Team:**

- **Hesham M Alahdal** - lrg@lrgex.com
- **Nidhal A Brniyah** - n1a1b1@lrgex.com

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Why LRGEX?

**LRGEX Web Benchmark is like "Wix for Load Testing"** - it democratizes professional performance testing for everyone, not just developers!

### **Perfect For:**

- ✅ **Students** learning about web performance
- ✅ **Business owners** testing their websites
- ✅ **Developers** who want quick results
- ✅ **QA teams** needing accessible tools
- ✅ **Anyone** curious about website performance

### **Unique Value:**

- **Zero technical barriers** - anyone can use it
- **Professional results** - enterprise-grade testing
- **Instant gratification** - working in minutes
- **Smart automation** - handles complexity for you

---

**Ready to test your website's performance? Get started in under 5 minutes!**

```bash
git clone https://github.com/[YOUR-GITHUB-USERNAME]/LRGEX-Web-Benchmark.git
cd LRGEX-Web-Benchmark
python LRGEX-Benchmark.py
```

## Overview

LRGEX Web Benchmark is a user-friendly load testing tool that helps you test the performance and reliability of web applications under various load conditions. Built on top of Locust, it provides an intuitive interface for both technical and non-technical users to conduct comprehensive performance testing.

## Key Features

- **Smart Form Builder**: Interactive wizard to create custom form submission tests
- **Automatic Discovery**: Intelligently finds and tests available website endpoints
- **Multiple Test Types**: Support for websites, APIs, e-commerce, and support portals
- **Real-time Monitoring**: Live performance metrics and statistics
- **Professional Reports**: Generate HTML and CSV reports for analysis
- **User-friendly Interface**: No programming knowledge required

## What This Tool Monitors

### ✅ What LRGEX Web Benchmark Tracks:

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

The LRGEX Web Benchmark tool simulates multiple users accessing your website simultaneously to:

- **Test server capacity** under realistic load conditions
- **Identify performance bottlenecks** before they affect real users
- **Validate form submissions** work correctly under load
- **Measure response times** and success rates
- **Generate detailed reports** for performance analysis

## Installation & Setup

### Prerequisites

- Python 3.8+ installed
- git (optional, for cloning the repository)

### How to Run

1. Download the `LRGEX-Benchmark.py` script or clone the repository
2. Navigate to the LRGEX-WEB-Benchmark folder in terminal/command prompt
3. Run: `python LRGEX-Benchmark.py`

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

### Important Warning

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

## Recent Changes (v1.0.0)

### ✨ New Features

- **Intelligent Performance Analysis**: Automatically analyzes your test results and provides specific recommendations based on actual response times and failure rates
- **Professional Output**: Clean, enterprise-ready reporting
- **Smart Form Builder**: Enhanced interactive form test generation with better field explanations
- **Automatic Test Duration**: Tests properly respect time limits in automatic mode

### Improvements

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

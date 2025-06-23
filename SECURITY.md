# Security Policy

## ⚠️ Responsible Use

This tool is intended for ethical, authorized load and performance testing only.

**Do not use it to test or attack systems you do not own or have explicit permission to test.**

Unauthorized use is illegal and strictly prohibited. The authors and contributors of this project are not responsible for any misuse.

## Supported Versions

We actively support and provide security updates for the following versions of LRGEX Web Benchmark:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | ✅ Fully Supported |
| < 1.0   | ❌ Not Supported   |

## Security Features

### Built-in Security Measures

- **Local Execution**: All tests run locally on your machine by default
- **No Data Collection**: LRGEX does not collect or transmit personal data
- **Safe Test Generation**: Generated test files use sanitized inputs
- **Network Isolation**: Tests only connect to URLs you explicitly specify
- **Dependency Management**: Automatic security updates via UV package manager

### Data Privacy

- **Your URLs**: Only used for testing - never transmitted to external services
- **Form Data**: Generated test data is fake/synthetic - no real user data used
- **Reports**: Stored locally in your `reports/` folder
- **Logs**: All logging happens locally on your system

## Reporting Security Vulnerabilities

We take security seriously and appreciate responsible disclosure of security vulnerabilities.

### How to Report

**DO NOT** create a public GitHub issue for security vulnerabilities.

Instead, please report security issues privately:

1. **Email**: Send details to **lrg@lrgex.com**
2. **Subject Line**: `[SECURITY] LRGEX Web Benchmark - [Brief Description]`
3. **Include**:
   - Description of the vulnerability
   - Steps to reproduce (if applicable)
   - Potential impact assessment
   - Your contact information
   - Any suggested fixes (optional)

### What to Expect

1. **Acknowledgment**: We'll respond within 48 hours
2. **Assessment**: We'll investigate and assess the issue
3. **Communication**: We'll keep you updated on our progress
4. **Resolution**: We'll work on a fix and coordinate disclosure timing
5. **Credit**: We'll acknowledge your contribution (unless you prefer to remain anonymous)

### Response Timeline

- **Critical**: 24-48 hours response, patch within 7 days
- **High**: 48-72 hours response, patch within 14 days
- **Medium**: 3-5 days response, patch within 30 days
- **Low**: 5-7 days response, patch in next regular release

## 🔐 Security Best Practices for Users

### Safe Usage

1. **Test Environments**:

   - Use test/staging environments when possible
   - Avoid testing production systems without proper authorization

2. **Network Security**:

   - Be cautious when testing internal/private networks
   - Ensure you have permission to test target systems
   - Consider firewall implications for high-load tests

3. **Resource Management**:

   - Start with low user counts to avoid overwhelming target systems
   - Monitor system resources during tests
   - Use appropriate test duration settings

4. **Data Protection**:
   - Don't use real personal data in custom form configurations
   - Be mindful of sensitive URLs in test configurations
   - Regularly clean up test reports if they contain sensitive information

### Responsible Testing

- **Authorization**: Only test systems you own or have explicit permission to test
- **Rate Limits**: Respect target system limitations and rate limits
- **Legal Compliance**: Ensure testing complies with applicable laws and regulations
- **Ethical Use**: Use LRGEX for legitimate performance testing purposes only

## 🔄 Security Updates

### Automatic Updates

- LRGEX uses UV for dependency management with automatic security updates
- We regularly monitor dependencies for known vulnerabilities
- Security patches are prioritized in our release schedule

### Staying Updated

1. **Watch**: Star/watch our GitHub repository for update notifications
2. **Releases**: Check the [Releases](https://github.com/LRGEX/LRGEX-Web-Benchmark/releases) page regularly
3. **Changelog**: Review [CHANGELOG.md](CHANGELOG.md) for security-related updates
4. **Dependencies**: Run `uv sync` periodically to update dependencies

## Security Checklist for Contributors

If you're considering contributing to LRGEX (via issues/suggestions):

- [ ] Does this feature/change introduce new network connections?
- [ ] Could this change expose sensitive user data?
- [ ] Are input validations sufficient for new features?
- [ ] Does this change affect the security model of the application?
- [ ] Are there any new dependencies that should be security-reviewed?

## Known Limitations

### Current Security Considerations

1. **Local Web Server**: LRGEX runs a local web server on port 8089

   - **Risk**: Accessible to other users on the same machine
   - **Mitigation**: Server binds to localhost only by default

2. **Generated Test Files**: Test files are created in the `tests/` directory

   - **Risk**: May contain target URLs and configuration details
   - **Mitigation**: Add sensitive test files to `.gitignore`

3. **Test Reports**: HTML/CSV reports may contain target system information
   - **Risk**: Potential information disclosure if shared inappropriately
   - **Mitigation**: Review reports before sharing externally

## 🆘 Emergency Response

In case of critical security issues affecting active users:

1. **Immediate**: Email lrg@lrgex.com with "URGENT SECURITY" in subject
2. **Escalation**: We'll assess and respond within 12 hours for critical issues
3. **Mitigation**: We may release emergency patches outside normal release cycles
4. **Communication**: We'll notify users via GitHub releases and security advisories

## 📞 Contact Information

- **Security Email**: lrg@lrgex.com
- **General Contact**: n1a1b1@lrgex.com
- **GitHub Issues**: [Report non-security issues](https://github.com/LRGEX/LRGEX-Web-Benchmark/issues)

---

**Thank you for helping keep LRGEX Web Benchmark secure for everyone!**

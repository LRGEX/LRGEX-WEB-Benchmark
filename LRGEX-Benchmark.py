import os
import subprocess
import sys
from pathlib import Path
import time

# Version information
VERSION = "v2.5.3"

# Pre-defined test templates
TEST_TEMPLATES = {
    "custom_form": {
        "name": "Smart Form Builder",
        "description": "I'll ask you questions and build a custom form test for you!",
        "filename": "custom_form_test.py",
        "interactive": True,  # Special flag for interactive creation
    },
    "smart": {
        "name": "Smart Website Test",
        "description": "Automatically finds what exists and ONLY tests that",
        "filename": "smart_test.py",
        "code": '''from locust import HttpUser, task, between
import random
import time
import os

class SmartWebsiteUser(HttpUser):
    wait_time = between(1, 3)
    working_paths = set()
    
    def on_start(self):
        """Find what actually exists on this website"""
        # Check if there's a duration limit set via environment variable
        if hasattr(self.environment, 'parsed_options') and hasattr(self.environment.parsed_options, 'run_time'):
            self.run_time = self.environment.parsed_options.run_time
        else:
            self.run_time = None
        
        self.start_time = time.time()
        
        # Always test homepage first
        self.working_paths.add("/")
        
        # Test common paths but ONLY keep ones that work
        test_paths = [
            "/about", "/contact", "/services", "/products",
            "/help", "/support", "/blog", "/news", "/faq", 
            "/login", "/api", "/search"
        ]
        
        print("Discovering what exists on this website...")
        for path in test_paths:
            try:
                # Silent test - don't count as requests in report
                response = self.client.get(path, catch_response=True, name="discovery")
                if response.status_code == 200:
                    self.working_paths.add(path)
                    print(f"Found: {path}")
                response.success()  # Always mark discovery as success
            except:
                pass
        
        print(f"Will test {len(self.working_paths)} working pages")
        
        # If only homepage works, focus entirely on homepage
        if len(self.working_paths) == 1:
            print("Simple website detected - focusing on homepage performance")
    
    @task
    def visit_pages(self):
        """Visit pages that actually exist"""
        if len(self.working_paths) == 1:
            # Only homepage exists - just test that
            self.client.get("/")
        else:
            # Multiple pages exist - test them all
            path = random.choice(list(self.working_paths))
            self.client.get(path)
''',
    },
    "website": {
        "name": "Website Load Test",
        "description": "Test homepage and discover available pages",
        "filename": "website_test.py",
        "code": '''from locust import HttpUser, task, between
import random
import re
from urllib.parse import urljoin, urlparse

class SmartWebsiteUser(HttpUser):
    wait_time = between(1, 3)
    discovered_links = set()
    safe_paths = ["/", "/home", "/index", "/main"]
    
    def on_start(self):
        """Discover available links from homepage"""
        try:
            response = self.client.get("/", catch_response=True)
            if response.status_code == 200:
                # Extract links from HTML - handle both quote types
                links1 = re.findall(r'href="([^"]+)"', response.text)
                links2 = re.findall(r"href='([^']+)'", response.text)
                links = links1 + links2
                for link in links:
                    if link.startswith('/') and not link.startswith('//'):
                        # Only internal links, avoid anchors and external
                        clean_link = link.split('#')[0].split('?')[0]
                        if len(clean_link) > 1 and len(clean_link) < 50:
                            self.discovered_links.add(clean_link)
                
                # Add some common fallback paths
                common_paths = ["/about", "/contact", "/services", "/products", 
                              "/help", "/support", "/blog", "/news"]
                self.discovered_links.update(common_paths)
            response.success()
        except Exception:
            # If discovery fails, use safe defaults
            self.discovered_links = {"/", "/home", "/about", "/contact"}
    
    @task(5)
    def homepage(self):
        """Visit homepage - always safe"""
        self.client.get("/")
    
    @task(3)
    def browse_discovered_pages(self):
        """Visit discovered pages with error handling"""
        if self.discovered_links:
            path = random.choice(list(self.discovered_links))
            with self.client.get(path, catch_response=True) as response:
                if response.status_code == 404:
                    # Remove 404 pages from future requests
                    self.discovered_links.discard(path)
                    response.failure("Page not found - removed from rotation")
                elif response.status_code >= 500:
                    response.failure("Server error")
                else:
                    response.success()
        else:
            # Fallback to homepage
            self.client.get("/")
    
    @task(1)
    def safe_navigation(self):
        """Always use known safe paths"""
        safe_path = random.choice(self.safe_paths)
        with self.client.get(safe_path, catch_response=True) as response:
            if response.status_code >= 400:
                response.failure(f"Error {response.status_code}")
            else:
                response.success()
''',
    },
    "api": {
        "name": "API Load Test",
        "description": "Test REST API endpoints",
        "filename": "api_test.py",
        "code": '''from locust import HttpUser, task, between
import json
import random

class APIUser(HttpUser):
    wait_time = between(0.5, 2)
    
    def on_start(self):
        """Setup headers for API calls"""
        self.client.headers.update({"Content-Type": "application/json"})
    
    @task(3)
    def get_users(self):
        """Get list of users"""
        self.client.get("/api/users")
    
    @task(2)
    def get_user_by_id(self):
        """Get specific user"""
        user_id = random.randint(1, 100)
        self.client.get(f"/api/users/{user_id}")
    
    @task(1)
    def create_user(self):
        """Create new user"""
        user_data = {
            "name": f"TestUser{random.randint(1000, 9999)}",
            "email": f"test{random.randint(1000, 9999)}@example.com"
        }
        self.client.post("/api/users", json=user_data)
    
    @task(1)
    def health_check(self):
        """Check API health"""
        self.client.get("/api/health")
''',
    },
    "ecommerce": {
        "name": "E-commerce Test",
        "description": "Test shopping, cart, and checkout",
        "filename": "ecommerce_test.py",
        "code": '''from locust import HttpUser, task, between
import random

class ShopperUser(HttpUser):
    wait_time = between(1, 4)
    
    @task(4)
    def browse_products(self):
        """Browse product catalog"""
        categories = ["electronics", "clothing", "books", "sports"]
        category = random.choice(categories)
        self.client.get(f"/products?category={category}")
    
    @task(3)
    def view_product(self):
        """View product details"""
        product_id = random.randint(1, 50)
        self.client.get(f"/product/{product_id}")
    
    @task(2)
    def add_to_cart(self):
        """Add item to cart"""
        product_id = random.randint(1, 50)
        self.client.post(f"/cart/add/{product_id}")
    
    @task(1)
    def view_cart(self):
        """View shopping cart"""
        self.client.get("/cart")
    
    @task(1)
    def search_products(self):
        """Search for products"""
        search_terms = ["laptop", "phone", "book", "shoes", "watch"]
        term = random.choice(search_terms)
        self.client.get(f"/search?q={term}")
''',
    },
    "support": {
        "name": "Support Portal Test",
        "description": "Test help desk and support features",
        "filename": "support_test.py",
        "code": '''from locust import HttpUser, task, between
import random

class SupportUser(HttpUser):
    wait_time = between(1, 3)
    
    @task(4)
    def view_knowledge_base(self):
        """Browse help articles"""
        self.client.get("/help")
    
    @task(3)
    def search_help(self):
        """Search for help topics"""
        search_terms = ["password", "login", "billing", "account", "error"]
        term = random.choice(search_terms)
        self.client.get(f"/help/search?q={term}")
    
    @task(2)
    def view_article(self):
        """Read specific help article"""
        article_id = random.randint(1, 20)
        self.client.get(f"/help/article/{article_id}")
    
    @task(1)
    def contact_form(self):
        """Submit contact form with test data"""
        # First get the contact form page
        response = self.client.get("/contact")
        
        # Submit the form with test data
        form_data = {
            "name": f"Test User {random.randint(1000, 9999)}",
            "email": f"test{random.randint(100, 999)}@example.com",
            "subject": random.choice([
                "Technical Support Request",
                "Billing Question", 
                "General Inquiry",
                "Feature Request",
                "Bug Report"
            ]),
            "message": "This is a test message from load testing. Please ignore."
        }
        self.client.post("/contact", data=form_data)
    
    @task(1)
    def newsletter_signup(self):
        """Test newsletter subscription form"""
        signup_data = {
            "email": f"newsletter{random.randint(1000, 9999)}@example.com",
            "name": f"Test Subscriber {random.randint(100, 999)}"
        }
        self.client.post("/newsletter/subscribe", data=signup_data)
    
    @task(1)
    def search_form_submit(self):
        """Submit search form"""
        search_terms = ["password", "login", "billing", "account", "error", "help"]
        search_data = {
            "q": random.choice(search_terms),
            "category": random.choice(["all", "technical", "billing", "general"])
        }
        self.client.post("/search", data=search_data)
    
    @task(1)
    def faq(self):
        """View FAQ section"""
        self.client.get("/faq")
''',
    },
    "forms": {
        "name": "Form Submission Test",
        "description": "Test various form submissions (contact, login, signup, etc.)",
        "filename": "forms_test.py",
        "code": '''from locust import HttpUser, task, between
import random
import string

class FormTestUser(HttpUser):
    wait_time = between(1, 3)
    
    # CUSTOM FORM URLS - Edit these for your specific website
    CUSTOM_FORMS = {
        # Format: "form_name": {"get_url": "page_url", "post_url": "submit_url"}
        "contact": {"get_url": "/contact", "post_url": "/contact"},
        "login": {"get_url": "/login", "post_url": "/login"},
        "newsletter": {"get_url": "/newsletter", "post_url": "/newsletter"},
        "search": {"get_url": "/search", "post_url": "/search"},
        # Add your custom forms here:
        # "custom_form": {"get_url": "/your-form-page", "post_url": "/whatever"},
        # "feedback": {"get_url": "/feedback", "post_url": "/submit-feedback"},
        # "quote": {"get_url": "/quote", "post_url": "/process-quote"},
    }
    
    def generate_fake_email(self):
        """Generate a fake email for testing"""
        domains = ["example.com", "test.com", "fake.org", "demo.net"]
        username = ''.join(random.choices(string.ascii_lowercase, k=8))
        return f"{username}@{random.choice(domains)}"
    
    def generate_fake_name(self):
        """Generate a fake name for testing"""
        first_names = ["John", "Jane", "Mike", "Sarah", "David", "Lisa", "Chris", "Emma"]
        last_names = ["Smith", "Johnson", "Brown", "Davis", "Wilson", "Moore", "Taylor", "Anderson"]
        return f"{random.choice(first_names)} {random.choice(last_names)}"
    
    @task(3)
    def contact_form_submission(self):
        """Submit contact form - tries both custom and common URLs"""
        # First try custom URLs if specified
        if "contact" in self.CUSTOM_FORMS:
            custom = self.CUSTOM_FORMS["contact"]
            with self.client.get(custom["get_url"], catch_response=True) as response:
                if response.status_code == 200:
                    form_data = {
                        "name": self.generate_fake_name(),
                        "email": self.generate_fake_email(),
                        "subject": random.choice([
                            "Technical Support", "General Inquiry", "Bug Report",
                            "Feature Request", "Billing Question"
                        ]),
                        "message": "This is a test message from automated load testing. Please disregard.",
                        "phone": f"555-{random.randint(100, 999)}-{random.randint(1000, 9999)}"
                    }
                    
                    with self.client.post(custom["post_url"], data=form_data, catch_response=True) as post_response:
                        if post_response.status_code in [200, 201, 302]:
                            post_response.success()
                            return
                response.success()
                return
          # Use custom URLs if provided, otherwise fall back to common URLs
        if hasattr(self, 'CUSTOM_FORM_URLS') and self.CUSTOM_FORM_URLS:
            contact_urls = self.CUSTOM_FORM_URLS
        else:
            contact_urls = ["/contact", "/contact-us", "/support", "/help/contact"]
        for url in contact_urls:
            with self.client.get(url, catch_response=True) as response:
                if response.status_code == 200:
                    form_data = {
                        "name": self.generate_fake_name(),
                        "email": self.generate_fake_email(),
                        "subject": "Test Support Request",
                        "message": "This is a test message from automated load testing. Please disregard."
                    }
                    
                    # Try multiple post URLs
                    post_urls = [url, f"{url}/submit", "/contact/submit", "/submit-contact"]
                    for post_url in post_urls:
                        with self.client.post(post_url, data=form_data, catch_response=True) as post_response:
                            if post_response.status_code in [200, 201, 302]:
                                post_response.success()
                                return
                    response.success()
                    break
    
    @task(2)
    def custom_form_test(self):
        """Test any custom forms you've defined"""
        # Skip contact, login, newsletter, search as they have dedicated tasks
        custom_forms = {k: v for k, v in self.CUSTOM_FORMS.items() 
                       if k not in ["contact", "login", "newsletter", "search"]}
        
        if not custom_forms:
            return  # No custom forms defined
            
        form_name, form_config = random.choice(list(custom_forms.items()))
        
        # Get the form page
        with self.client.get(form_config["get_url"], catch_response=True) as response:
            if response.status_code == 200:
                # Generic form data that works for most forms
                form_data = {
                    "name": self.generate_fake_name(),
                    "email": self.generate_fake_email(),
                    "message": f"Test submission to {form_name} form",
                    "subject": f"Test {form_name}",
                    "comments": "This is a test submission from load testing",
                    "phone": f"555-{random.randint(100, 999)}-{random.randint(1000, 9999)}",
                    "company": "Test Company Inc.",
                    "title": random.choice(["Mr.", "Ms.", "Dr."]),
                    "submit": "1",
                    "action": "submit"
                }
                
                # Submit to the custom post URL
                with self.client.post(form_config["post_url"], data=form_data, catch_response=True) as post_response:
                    if post_response.status_code in [200, 201, 302, 422]:  # 422 = validation error but form processed
                        post_response.success()
                    else:
                        post_response.failure(f"Custom form {form_name} failed: {post_response.status_code}")
            response.success()
    
    @task(2)
    def newsletter_signup(self):
        """Test newsletter/email subscription forms"""
        # Try custom newsletter URL first
        if "newsletter" in self.CUSTOM_FORMS:
            custom = self.CUSTOM_FORMS["newsletter"]
            with self.client.get(custom["get_url"], catch_response=True) as response:
                if response.status_code == 200:
                    signup_data = {
                        "email": self.generate_fake_email(),
                        "name": self.generate_fake_name(),
                        "subscribe": "1"
                    }
                    with self.client.post(custom["post_url"], data=signup_data, catch_response=True) as post_response:
                        if post_response.status_code in [200, 201, 302]:
                            post_response.success()
                            return
                response.success()
                return
        
        # Fallback to common URLs
        # Use custom URLs if provided, otherwise fall back to common URLs
        if hasattr(self, 'CUSTOM_FORM_URLS') and self.CUSTOM_FORM_URLS:
            signup_urls = self.CUSTOM_FORM_URLS
        else:
            signup_urls = ["/newsletter", "/subscribe", "/signup", "/newsletter/signup"]
        for url in signup_urls:
            with self.client.get(url, catch_response=True) as response:
                if response.status_code == 200:
                    signup_data = {
                        "email": self.generate_fake_email(),
                        "name": self.generate_fake_name(),
                        "subscribe": "1"
                    }
                    
                    post_urls = [url, f"{url}/submit", "/newsletter/subscribe", "/api/subscribe"]
                    for post_url in post_urls:
                        with self.client.post(post_url, data=signup_data, catch_response=True) as post_response:
                            if post_response.status_code in [200, 201, 302]:
                                post_response.success()
                                return
                    response.success()
                    break''',
    },
}


def build_custom_form_test(existing_host=None):
    """Interactive form builder - asks user questions and generates custom test"""
    print("\n" + "=" * 50)
    print("   SMART FORM BUILDER")
    print("=" * 50)
    print("I'll ask you some questions and build a perfect test for your form!")
    print("Don't worry - I'll explain everything step by step.")
    print()

    # Collect form information
    form_info = {}

    # 1. Website and form URLs
    print("STEP 1: Tell me about your form")
    print("-" * 40)

    # Use existing host if provided, otherwise ask
    if existing_host:
        form_info["website"] = existing_host
        print(f"Using your website: {existing_host}")
    else:
        form_info["website"] = input(
            "What's your main website URL? (e.g., https://mysite.com): "
        ).strip()

    form_info["form_page"] = input(
        "What page has your form? (e.g., /student-form, /contact): "
    ).strip()
    form_info["submit_url"] = input(
        "Where does the form submit to? (e.g., /submit, /process-form): "
    ).strip()

    print(f"\nGot it! Form at {form_info['website']}{form_info['form_page']}")
    print(f"   Submits to: {form_info['website']}{form_info['submit_url']}")

    # 2. Form fields
    print("\nSTEP 2: Tell me about your form fields")
    print("-" * 40)
    print("I need to know what data your form expects.")
    print("Don't worry - I'll generate fake test data automatically!")
    print()

    try:
        num_fields = int(
            input("How many fields does your form have? (e.g., 3, 5): ").strip()
        )
    except ValueError:
        print("Using 3 fields as default...")
        num_fields = 3

    fields = []
    print(f"\nGreat! Now tell me about each of the {num_fields} fields:")

    for i in range(num_fields):
        print(f"\n--- Field {i+1} ---")
        field_name = input(
            f"Field {i+1} name (what the server expects, e.g., 'student_id', 'email'): "
        ).strip()

        print("What type of data should I generate for this field?")
        print("  1. Student/ID number (e.g., 12345)")
        print("  2. University/Institution ID (e.g., UNI67890)")
        print("  3. Person's name (e.g., John Smith)")
        print("  4. Email address (e.g., test@example.com)")
        print("  5. Phone number (e.g., 555-123-4567)")
        print("  6. Text message (e.g., 'Test submission')")
        print("  7. Custom text (I'll ask you what to send)")

        try:
            data_type = int(input("Choose type (1-7): ").strip())
        except ValueError:
            data_type = 6  # Default to text message

        field_info = {"name": field_name, "type": data_type}

        if data_type == 7:  # Custom text
            custom_text = input("What text should I send for this field? ").strip()
            field_info["custom_text"] = custom_text

        fields.append(field_info)
        print(f"Added field '{field_name}'")

    form_info["fields"] = fields

    # 3. Test configuration
    print("\nSTEP 3: Test settings")
    print("-" * 40)
    print("How many students/users will use your form in real life?")
    try:
        max_users = int(
            input("Maximum expected users (e.g., 100, 500, 2000): ").strip()
        )
    except ValueError:
        max_users = 100

    print("\nOver how many minutes will they submit?")
    try:
        duration = int(input("Duration in minutes (e.g., 30, 60, 120): ").strip())
    except ValueError:
        duration = 60

    form_info["max_users"] = max_users
    form_info["duration"] = duration  # Generate the test code
    print("\nGENERATING YOUR CUSTOM TEST...")
    test_code = generate_custom_form_code(form_info)

    # Summary
    print("\n" + "=" * 50)
    print("   YOUR CUSTOM TEST IS READY!")
    print("=" * 50)
    print(f"Website: {form_info['website']}")
    print(f"Form: {form_info['form_page']}")
    print(f"Submit: {form_info['submit_url']}")
    print(f"Fields: {len(fields)} custom fields")
    print(f"Max Users: {max_users}")
    print(f"Duration: {duration} minutes")
    print()

    return {"code": test_code, "form_info": form_info}


def sanitize_field_name_for_function(field_name):
    """Convert field name to valid Python function name"""
    # Replace spaces and special characters with underscores
    import re

    sanitized = re.sub(r"[^a-zA-Z0-9]", "_", field_name.lower())
    # Remove multiple consecutive underscores
    sanitized = re.sub(r"_+", "_", sanitized)
    # Remove leading/trailing underscores
    sanitized = sanitized.strip("_")
    # Ensure it doesn't start with a number
    if sanitized and sanitized[0].isdigit():
        sanitized = "field_" + sanitized
    return sanitized


def generate_custom_form_code(form_info):
    """Generate Python code for the custom form test"""

    # Build field generators
    field_generators = []
    form_data_fields = []

    for field in form_info["fields"]:
        field_name = field["name"]
        field_type = field["type"]
        # Create a safe function name
        safe_function_name = sanitize_field_name_for_function(field_name)

        if field_type == 1:  # Student ID
            field_generators.append(
                f"""
    def generate_{safe_function_name}(self):
        \"\"\"Generate fake {field_name} for testing\"\"\"
        return f"{{random.randint(10000, 99999)}}\""""
            )
            form_data_fields.append(
                f'        "{field_name}": self.generate_{safe_function_name}(),'
            )

        elif field_type == 2:  # University ID
            field_generators.append(
                f"""
    def generate_{safe_function_name}(self):
        \"\"\"Generate fake {field_name} for testing\"\"\"
        return f"UNI{{random.randint(10000, 99999)}}\""""
            )
            form_data_fields.append(
                f'        "{field_name}": self.generate_{safe_function_name}(),'
            )

        elif field_type == 3:  # Name
            form_data_fields.append(
                f'        "{field_name}": self.generate_fake_name(),'
            )

        elif field_type == 4:  # Email
            form_data_fields.append(
                f'        "{field_name}": self.generate_fake_email(),'
            )

        elif field_type == 5:  # Phone
            field_generators.append(
                f"""
    def generate_{safe_function_name}(self):
        \"\"\"Generate fake {field_name} for testing\"\"\"
        return f"555-{{random.randint(100, 999)}}-{{random.randint(1000, 9999)}}\""""
            )
            form_data_fields.append(
                f'        "{field_name}": self.generate_{safe_function_name}(),'
            )

        elif field_type == 6:  # Text message
            form_data_fields.append(
                f'        "{field_name}": "Test submission from load testing - please disregard",'
            )

        elif field_type == 7:  # Custom text
            custom_text = field.get("custom_text", "Test data")
            form_data_fields.append(f'        "{field_name}": "{custom_text}",')

    # Build the complete test code
    test_code = f'''from locust import HttpUser, task, between
import random
import string

class CustomFormUser(HttpUser):
    wait_time = between(1, 3)
    
    def generate_fake_email(self):
        """Generate a fake email for testing"""
        domains = ["example.com", "test.com", "fake.org", "demo.net"]
        username = ''.join(random.choices(string.ascii_lowercase, k=8))
        return f"{{username}}@{{random.choice(domains)}}"
    
    def generate_fake_name(self):
        """Generate a fake name for testing"""
        first_names = ["John", "Jane", "Mike", "Sarah", "David", "Lisa", "Chris", "Emma"]
        last_names = ["Smith", "Johnson", "Brown", "Davis", "Wilson", "Moore", "Taylor", "Anderson"]
        return f"{{random.choice(first_names)}} {{random.choice(last_names)}}"
{''.join(field_generators)}
    
    @task
    def submit_custom_form(self):
        """Submit your custom form with realistic test data"""
        # Load the form page first
        with self.client.get("{form_info['form_page']}", catch_response=True) as response:
            if response.status_code == 200:
                # Prepare form data with your specific fields
                form_data = {{
{chr(10).join(form_data_fields)}
        "submit": "1"
                }}
                  # Submit the form
                with self.client.post("{form_info['submit_url']}", data=form_data, catch_response=True) as post_response:
                    if post_response.status_code in [200, 201, 302]:
                        post_response.success()
                        print(f"Form submitted successfully! Response: {{post_response.status_code}}")
                    elif post_response.status_code == 422:
                        # Validation error but form was processed
                        post_response.success()
                        print(f"Form submitted with validation warnings: {{post_response.status_code}}")
                    else:
                        post_response.failure(f"Form submission failed: {{post_response.status_code}}")
                        print(f"Form submission failed: {{post_response.status_code}}")
            else:
                response.failure(f"Could not load form page: {{response.status_code}}")
            response.success()

# Configuration for your test:
# Website: {form_info['website']}
# Expected Users: {form_info['max_users']}
# Duration: {form_info['duration']} minutes
# 
# Recommended Locust settings:
# - Start with 10 users
# - Ramp up to {min(form_info['max_users'] // 4, 100)} users over 2 minutes  
# - Test for {form_info['duration']} minutes
# - Monitor your database and server performance!
'''

    return test_code


def get_user_input():
    print("LRGEX WEB Benchmark Test Configuration")
    time.sleep(3)
    """Get user configuration for the benchmark test"""
    print("=" * 70)
    print("      __   __   ___         __   ___       __       ")
    print(r"|    |__) / _` |__  \_/ __ |__) |__  |\ | /  ` |__| ")
    print(r"|___ |  \ \__> |___ / \    |__) |___ | \| \__, |  | ")
    print(f"                                           {VERSION}")
    print("=" * 70)
    print()
    time.sleep(3)
    config = {}  # 1. Select test type
    print("")

    print()
    templates = list(TEST_TEMPLATES.keys())
    for i, template_key in enumerate(templates, 1):
        template = TEST_TEMPLATES[template_key]
        print(f"  {i}. {template['name']}")
        print(f"     {template['description']}")
        print()
        time.sleep(0.4)  # Pause between menu options for smooth display

    while True:
        try:
            choice = input(f"Select test type (1-{len(templates)}): ").strip()
            if choice.isdigit() and 1 <= int(choice) <= len(templates):
                selected_template = templates[int(choice) - 1]
                config["template"] = selected_template
                print(f"Selected: {TEST_TEMPLATES[selected_template]['name']}")
                break
            else:
                print("Please enter a number between 1 and", len(templates))
        except ValueError:
            print("Please enter a valid number")
    # 2. Ask for target website
    print("\nWhat's your website URL?")
    print(
        "Examples: https://example.com, http://localhost:3000, https://api.mysite.com"
    )

    default_hosts = [
        "https://support.lrg4you.com",
        "http://localhost:3000",
        "http://localhost:8080",
        "https://jsonplaceholder.typicode.com",  # For API testing
    ]

    print("\nQuick options:")
    for i, host in enumerate(default_hosts, 1):
        print(f"  {i}. {host}")
    print(f"  {len(default_hosts) + 1}. Enter custom URL")

    while True:
        try:
            choice = input(f"\nSelect option (1-{len(default_hosts) + 1}): ").strip()
            if choice.isdigit() and 1 <= int(choice) <= len(default_hosts):
                config["host"] = default_hosts[int(choice) - 1]
                print(f"Target: {config['host']}")
                break
            elif choice == str(len(default_hosts) + 1):
                custom_url = input("Enter your website URL: ").strip()
                if custom_url:
                    if not custom_url.startswith(("http://", "https://")):
                        custom_url = "https://" + custom_url
                    config["host"] = custom_url
                    print(f"Target: {config['host']}")
                    break
                else:
                    print("Please enter a valid URL")
            else:
                print("Please enter a valid option number")
        except ValueError:
            print("Please enter a valid number")

    # 3. Test mode FIRST - determines what settings we need
    print("\nHow do you want to run the test?")
    print("  1. Interactive Mode - Open web interface (you control everything)")
    print("  2. Automatic Mode - Run with preset settings")
    while True:
        mode = input("\nSelect mode (1-2): ").strip()
        if mode == "1":
            config["headless"] = False
            print("Interactive mode - You'll control users/duration in browser")
            print(
                "No intensity settings needed - you'll set everything in the web interface!"
            )
            # Set default values for display purposes (actual values set in browser)
            config["users"] = "Set in browser"
            config["spawn_rate"] = "Set in browser"
            config["duration"] = "Set in browser"
            break
        elif mode == "2":
            config["headless"] = True
            print("Automatic mode - Now let's set intensity...")

            # Only ask for intensity in automatic mode
            print("\nHow intense should the test be?")
            test_levels = {
                "1": {
                    "name": "Light Test",
                    "users": 5,
                    "spawn": 1,
                    "duration": "15s",
                },
                "2": {
                    "name": "Medium Test",
                    "users": 25,
                    "spawn": 3,
                    "duration": "30s",
                },
                "3": {
                    "name": "Heavy Test",
                    "users": 100,
                    "spawn": 10,
                    "duration": "1m",
                },
                "4": {
                    "name": "Extreme Test",
                    "users": 500,
                    "spawn": 20,
                    "duration": "2m",
                },
            }

            for key, level in test_levels.items():
                print(
                    f"  {key}. {level['name']} - {level['users']} users, {level['duration']}"
                )

            while True:
                choice = input("\nSelect intensity (1-4): ").strip()
                if choice in test_levels:
                    selected_level = test_levels[choice]
                    config["users"] = selected_level["users"]
                    config["spawn_rate"] = selected_level["spawn"]
                    config["duration"] = selected_level["duration"]
                    print(f"Selected: {selected_level['name']}")
                    break
                else:
                    print("Please enter 1, 2, 3, or 4")

            # Ask for specific URLs/forms to test in automatic mode
            print()
            if config["template"] == "forms":
                print(
                    "What forms do you want to test? (Enter URLs separated by commas)"
                )
                print(
                    "Examples: /login.php, /register, /contact-form.html, /newsletter-signup"
                )
                custom_urls = input("Form URLs to test: ").strip()
                if custom_urls:
                    config["custom_urls"] = [
                        url.strip() for url in custom_urls.split(",")
                    ]
                else:
                    config["custom_urls"] = []

            elif config["template"] == "ecommerce":
                print(
                    "What e-commerce pages do you want to test? (Enter URLs separated by commas)"
                )
                print(
                    "Examples: /shop, /cart, /checkout, /products, /category/electronics"
                )
                custom_urls = input("E-commerce URLs to test: ").strip()
                if custom_urls:
                    config["custom_urls"] = [
                        url.strip() for url in custom_urls.split(",")
                    ]
                else:
                    config["custom_urls"] = []

            elif config["template"] == "support":
                print(
                    "What support pages do you want to test? (Enter URLs separated by commas)"
                )
                print("Examples: /help, /support, /tickets, /faq, /contact-support")
                custom_urls = input("Support URLs to test: ").strip()
                if custom_urls:
                    config["custom_urls"] = [
                        url.strip() for url in custom_urls.split(",")
                    ]
                else:
                    config["custom_urls"] = []

            elif config["template"] == "api":
                print(
                    "What API endpoints do you want to test? (Enter URLs separated by commas)"
                )
                print("Examples: /api/users, /api/posts, /api/login, /api/data")
                custom_urls = input("API endpoints to test: ").strip()
                if custom_urls:
                    config["custom_urls"] = [
                        url.strip() for url in custom_urls.split(",")
                    ]
                else:
                    config["custom_urls"] = []
            else:
                config["custom_urls"] = []

            break
        else:
            print(
                "Please enter 1 or 2"
            )  # 5. Always generate reports in auto mode - in reports folder
    if config["headless"]:
        # Create reports folder if it doesn't exist
        os.makedirs("reports", exist_ok=True)
        config["csv"] = "reports/benchmark_results.csv"
        config["html"] = "reports/benchmark_report.html"
        print("Reports will be saved in 'reports' folder")

    # 6. Keep it simple - use INFO log level
    config["log_level"] = "INFO"

    return config


def create_test_file(config):
    """Create the test file based on selected template"""
    template_key = config["template"]
    template = TEST_TEMPLATES[template_key]

    # Create tests directory if it doesn't exist
    tests_dir = "tests"
    os.makedirs(tests_dir, exist_ok=True)

    # Create the file path in the tests directory
    test_file_path = os.path.join(
        tests_dir, template["filename"]
    )  # Handle interactive custom form creation
    if template.get("interactive", False):
        print("\nStarting Smart Form Builder...")
        # Pass existing host to avoid asking twice
        existing_host = config.get("host", None)
        custom_result = build_custom_form_test(existing_host)

        print(f"\nCreating custom test file: {test_file_path}")
        with open(test_file_path, "w", encoding="utf-8") as f:
            f.write(custom_result["code"])

        print("Custom form test created successfully!")
        print(
            "This test is perfectly tailored for YOUR form!"
        )  # Update config with custom form info
        form_info = custom_result["form_info"]
        if "website" in form_info and form_info["website"]:
            config["host"] = form_info["website"]
            print(f"Auto-set target to: {config['host']}")

        # Update config with user's test settings
        if "max_users" in form_info:
            config["users"] = form_info["max_users"]
            print(f"Auto-set users to: {config['users']}")

        if "duration" in form_info:
            # Convert minutes to seconds for Locust
            duration_seconds = f"{form_info['duration']}m"
            config["duration"] = duration_seconds
            print(f"Auto-set duration to: {form_info['duration']} minutes")

        # Set a reasonable spawn rate (10% of max users, minimum 1, maximum 50)
        if "max_users" in form_info:
            spawn_rate = max(1, min(50, form_info["max_users"] // 10))
            config["spawn_rate"] = spawn_rate
            print(f"Auto-set spawn rate to: {spawn_rate}/second")
    else:
        # Regular template creation
        print(f"\nCreating test file: {test_file_path}")

        # Get the template code
        template_code = template["code"]

        # Inject custom URLs if provided
        if config.get("custom_urls"):
            custom_urls = config["custom_urls"]
            print(f"Using your custom URLs: {', '.join(custom_urls)}")

            # Add custom URLs to the template
            if template_key == "forms":
                # Add custom form URLs to the forms template
                custom_forms_code = f'''
    # Custom form URLs specified by user
    CUSTOM_FORM_URLS = {custom_urls}
    
    def get_custom_form_urls(self):
        """Use user-specified form URLs"""
        return self.CUSTOM_FORM_URLS'''

                # Insert after the class definition
                template_code = template_code.replace(
                    "class FormTestUser(HttpUser):",
                    f"class FormTestUser(HttpUser):{custom_forms_code}",
                )

            elif template_key == "ecommerce":
                # Add custom e-commerce URLs
                custom_urls_code = f"""
    # Custom e-commerce URLs specified by user  
    CUSTOM_ECOMMERCE_URLS = {custom_urls}"""

                template_code = template_code.replace(
                    "class EcommerceUser(HttpUser):",
                    f"class EcommerceUser(HttpUser):{custom_urls_code}",
                )

            elif template_key == "support":
                # Add custom support URLs
                custom_urls_code = f"""
    # Custom support URLs specified by user
    CUSTOM_SUPPORT_URLS = {custom_urls}"""

                template_code = template_code.replace(
                    "class SupportUser(HttpUser):",
                    f"class SupportUser(HttpUser):{custom_urls_code}",
                )

            elif template_key == "api":
                # Add custom API endpoints
                custom_urls_code = f"""
    # Custom API endpoints specified by user
    CUSTOM_API_ENDPOINTS = {custom_urls}"""

                template_code = template_code.replace(
                    "class APIUser(HttpUser):",
                    f"class APIUser(HttpUser):{custom_urls_code}",
                )

        with open(test_file_path, "w", encoding="utf-8") as f:
            f.write(template_code)

        print("Test file created successfully!")
        print(f"The test will simulate users {template['description'].lower()}")

    # Return the path for use in the command
    return test_file_path


def build_command(config):
    """Build the locust command based on user configuration"""
    # Create reports directory if it doesn't exist
    os.makedirs("reports", exist_ok=True)

    cmd = ["uv", "run", "--module", "locust", "-f", config["test_file"]]

    # Add host
    cmd.extend(["--host", config["host"]])  # Add headless mode options
    if config["headless"]:
        cmd.append("--headless")
        cmd.extend(["-u", str(config["users"])])
        cmd.extend(["-r", str(config["spawn_rate"])])

        # Always add duration in headless mode (automatic mode)
        if "duration" in config and config["duration"]:
            cmd.extend(["-t", config["duration"]])
            print(f"Duration set to: {config['duration']}")
        else:
            print("WARNING: No duration set - test will run indefinitely!")
    else:
        # Interactive mode: pass user settings as defaults for the web UI
        if isinstance(config["users"], int) and config["users"] > 0:
            cmd.extend(["-u", str(config["users"])])
        if isinstance(config["spawn_rate"], (int, float)) and config["spawn_rate"] > 0:
            cmd.extend(["-r", str(config["spawn_rate"])])
        # Note: Duration cannot be pre-filled in web UI mode, it's set manually
    # Add CSV output
    if "csv" in config:
        cmd.extend(
            ["--csv", config["csv"].replace(".csv", "")]
        )  # Locust adds .csv automatically

    # Add HTML report
    if "html" in config:
        cmd.extend(["--html", config["html"]])  # Add log level
    cmd.extend(["--loglevel", config["log_level"]])

    # Debug: Show the command being executed
    print(f"\nDEBUG: Running command: {' '.join(cmd)}")

    return cmd


def display_summary(config):
    """Display test configuration summary"""
    print("\n" + "=" * 70)
    print("SMART TEST CONFIGURATION")
    print("=" * 70)
    print(f"Test Type: {TEST_TEMPLATES[config['template']]['name']}")
    print(f"Target: {config['host']}")
    print(f"Mode: {'Interactive (Browser)' if not config['headless'] else 'Automatic'}")

    # Show different info for Interactive vs Automatic mode
    if config["headless"]:
        # Automatic mode - show actual values
        print(f"Users: {config['users']}")
        print(f"Spawn Rate: {config['spawn_rate']}/second")
        print(f"Duration: {config['duration']}")
        print(f"CSV Report: {config['csv']}")
        print(f"HTML Report: {config['html']}")
    else:  # Interactive mode - show recommended values
        if isinstance(config["users"], int) and config["users"] > 1:
            print("DEFAULT VALUES SET for Web UI:")
            print(f"  Number of Users: {config['users']} (already pre-filled)")
            print(f"  Spawn Rate: {config['spawn_rate']}/second (already pre-filled)")
            if "duration" in config and config["duration"] != "Set in browser":
                duration_display = (
                    config["duration"].replace("m", " minutes").replace("s", " seconds")
                )
                print(f"  Duration: {duration_display} (enter this manually)")
            print()
            print("The web interface will open with your values pre-filled!")
        else:
            print(f"Users: {config['users']}")
            print(f"Spawn Rate: {config['spawn_rate']}/second")
            print(f"Duration: {config['duration']}")

    print("=" * 70)


def analyze_performance_and_advise():
    """Analyze actual test results and provide specific recommendations"""
    import csv
    import os

    print("\n" + "=" * 70)
    print("YOUR TEST RESULTS ANALYSIS")
    print("=" * 70)

    # Try to read the actual CSV results
    csv_file = "reports/benchmark_results_stats.csv"
    if os.path.exists(csv_file):
        try:
            with open(csv_file, "r") as f:
                reader = csv.DictReader(f)
                stats = list(reader)

            if stats:
                # Get the aggregated row (last row usually)
                main_stats = None
                for row in stats:
                    if row.get("Name") == "Aggregated" or "Aggregated" in row.get(
                        "Name", ""
                    ):
                        main_stats = row
                        break

                if not main_stats:
                    main_stats = stats[-1]  # Use last row if no Aggregated found

                # Parse the data
                avg_time = float(main_stats.get("Average Response Time", 0))
                min_time = float(main_stats.get("Min Response Time", 0))
                max_time = float(main_stats.get("Max Response Time", 0))
                total_requests = int(main_stats.get("Request Count", 0))
                failures = int(main_stats.get("Failure Count", 0))
                failure_rate = (
                    (failures / total_requests * 100) if total_requests > 0 else 0
                )

                print("ACTUAL TEST RESULTS:")
                print(f"• Total Requests: {total_requests:,}")
                print(f"• Failed Requests: {failures:,} ({failure_rate:.1f}%)")
                print(f"• Average Response Time: {avg_time:.0f}ms")
                print(f"• Response Time Range: {min_time:.0f}ms - {max_time:.0f}ms")
                print()

                # Analyze response times
                print("PERFORMANCE VERDICT:")
                if avg_time < 100:
                    print("🚀 EXCELLENT - Your server is blazing fast!")
                    print(f"   Average {avg_time:.0f}ms is outstanding performance")
                    print("   Your server CPU and I/O are handling load very well")
                elif avg_time < 200:
                    print("✅ VERY GOOD - Fast and responsive server")
                    print(f"   Average {avg_time:.0f}ms shows healthy performance")
                    print("   Server resources are in good shape")
                elif avg_time < 500:
                    print("⚠️ ACCEPTABLE - Server working but showing some strain")
                    print(f"   Average {avg_time:.0f}ms indicates moderate load")
                    print("   Monitor server resources during peak times")
                else:
                    print("🔍 CONCERNING - Server struggling under load")
                    print(f"   Average {avg_time:.0f}ms suggests resource constraints")
                    print("   Investigate server CPU, memory, or disk I/O immediately")

                print()

                # Analyze failure rate
                if failure_rate == 0:
                    print("✅ RELIABILITY: Perfect - No failed requests!")
                elif failure_rate < 1:
                    print(f"⚠️ RELIABILITY: Good - Only {failure_rate:.1f}% failures")
                elif failure_rate < 5:
                    print(
                        f"🔍 RELIABILITY: Concerning - {failure_rate:.1f}% failure rate"
                    )
                else:
                    print(
                        f"❌ RELIABILITY: Poor - {failure_rate:.1f}% failure rate needs attention"
                    )

                print()

                # Specific recommendations
                print("WHAT THIS MEANS FOR YOUR SERVER:")
                if avg_time < 200 and failure_rate == 0:
                    print("🎯 Your server is healthy and can likely handle MORE load")
                    print("🎯 Try testing with 2x or 3x more users to find your limits")
                    print("🎯 Current performance suggests good server optimization")
                elif avg_time < 500 and failure_rate < 1:
                    print("📊 Server is coping but may be near capacity")
                    print("📊 Monitor server resources during real traffic spikes")
                    print(
                        "📊 Consider performance optimization if response times increase"
                    )
                else:
                    print("⚡ Server needs attention - investigate bottlenecks")
                    print("⚡ Check CPU usage, memory consumption, and disk I/O")
                    print("⚡ May need code optimization or hardware upgrades")

        except Exception as e:
            print(f"Could not analyze results file: {e}")
            print("Check the HTML report for detailed performance graphs")
    else:
        print("No CSV results file found to analyze")
        print("The test may have been interrupted or files moved")

    print("=" * 70)


def install_uv_if_missing():
    """Check if UV is installed, and install it automatically if missing"""
    try:
        # Try to run UV to see if it's installed
        subprocess.run(["uv", "--version"], capture_output=True, check=True, timeout=10)
        print("UV is already installed!")
        return True
    except (
        subprocess.CalledProcessError,
        FileNotFoundError,
        subprocess.TimeoutExpired,
    ):
        print("UV package manager not found. Installing UV automatically...")

        try:
            # Detect platform and install UV accordingly
            if sys.platform.startswith("win"):
                # Windows installation using PowerShell
                print("Installing UV for Windows...")
                cmd = [
                    "powershell",
                    "-ExecutionPolicy",
                    "ByPass",
                    "-Command",
                    "irm https://astral.sh/uv/install.ps1 | iex",
                ]
                subprocess.run(cmd, check=True, timeout=120)
            else:
                # Unix-like systems (Linux, macOS)
                print("Installing UV for Unix-like system...")
                cmd = ["curl", "-LsSf", "https://astral.sh/uv/install.sh", "|", "sh"]
                subprocess.run(" ".join(cmd), shell=True, check=True, timeout=120)

            print("✅ UV installed successfully!")

            # Verify installation
            subprocess.run(
                ["uv", "--version"], capture_output=True, check=True, timeout=10
            )
            print("✅ UV installation verified!")
            return True

        except subprocess.TimeoutExpired:
            print("❌ UV installation timed out")
            print(
                "Please install UV manually from: https://docs.astral.sh/uv/getting-started/installation/"
            )
            return False
        except Exception as e:
            print(f"❌ Failed to install UV automatically: {e}")
            print("Please install UV manually:")
            if sys.platform.startswith("win"):
                print(
                    '  PowerShell: powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"'
                )
            else:
                print("  Unix/Linux: curl -LsSf https://astral.sh/uv/install.sh | sh")
            print("Or visit: https://docs.astral.sh/uv/getting-started/installation/")
            return False


def check_and_install_dependencies():
    """Smart dependency installer - installs UV first, then syncs dependencies"""
    print("Checking dependencies...")

    # Step 1: Install UV if missing
    if not install_uv_if_missing():
        print("❌ Cannot proceed without UV. Please install it manually and try again.")
        sys.exit(1)

    # Step 2: Try to sync dependencies from pyproject.toml first
    try:
        print("Syncing dependencies from pyproject.toml...")
        subprocess.run(["uv", "sync"], check=True, timeout=120)
        print("✅ Dependencies synced successfully!")

        # Verify Locust is available
        subprocess.run(
            ["uv", "run", "--module", "locust", "--version"],
            capture_output=True,
            check=True,
            timeout=10,
        )
        print("✅ Locust is ready!")

    except (subprocess.CalledProcessError, FileNotFoundError):
        # Fallback: Install Locust directly if sync fails
        print("Sync failed, installing Locust directly...")
        try:
            subprocess.run(["uv", "add", "locust"], check=True, timeout=60)
            print("✅ Locust installed successfully!")
        except Exception as e:
            print(f"❌ Failed to install Locust: {e}")
            sys.exit(1)

    print("✅ All dependencies ready!")


def main():
    """Main function to run the smart benchmark"""
    try:
        time.sleep(1)
        print("Launching systems...")
        time.sleep(1)

        # Smart dependency installation
        check_and_install_dependencies()

        print("")
        print("Loaded successfully!")
        print("")
        config = get_user_input()

        # Create test file automatically and get the path
        test_file_path = create_test_file(config)
        config["test_file"] = test_file_path

        # Build command
        cmd = build_command(config)
        # Display summary
        display_summary(config)

        # Auto-confirm or ask
        if config["headless"]:
            print("\nStarting automatic test...")
            confirm = True
        else:
            print("\nThis will open the Locust web interface at http://localhost:8089")
            print("You can control the test from there!")
            print("\nWeb UI Field Explanations:")
            print(
                "• Number of Users: How many virtual users will hit your site simultaneously"
            )
            print("• Spawn Rate: How many users to add per second (ramp-up speed)")
            print("• Duration (Advanced): For reference only - you must STOP manually!")
            print(
                "\nIMPORTANT: The test will run indefinitely until you click 'STOP' in the web UI"
            )  # Show performance analysis guidance
            analyze_performance_and_advise()

            confirm = input("\nReady to start? (Y/n): ").strip().lower()
            confirm = confirm in ["", "y", "yes"]

        if confirm:
            print("\nStarting benchmark test...")
            if not config["headless"]:
                print("Browser will open shortly...")
                print("Go to http://localhost:8089 if it doesn't open automatically")
            print("Press Ctrl+C to stop the test anytime\n")

            # Run the command with proper error handling
            try:
                result = subprocess.run(cmd, check=False)
                if result.returncode != 0 and not config["headless"]:
                    print(f"\nWarning: Locust exited with code {result.returncode}")
            except Exception as e:
                print(f"\nError running Locust: {e}")
                print("Make sure Locust is properly installed with: uv add locust")
                return

            if config["headless"]:
                print("\n" + "=" * 50)
                print("TEST COMPLETED SUCCESSFULLY!")
                print("=" * 50)
                print("Results saved:")
                print(f"   HTML Report: {config['html']}")
                print(f"   CSV Data: {config['csv']}")
                print("\nOpen the HTML file in your browser to see charts!")

                # Show intelligent performance analysis
                print("\n" + "=" * 50)
                print("PERFORMANCE ANALYSIS")
                print("=" * 50)
                analyze_performance_and_advise()
        else:
            print("Test cancelled.")

    except KeyboardInterrupt:
        print("\n\nTest stopped by user.")
        print("Any results generated have been saved.")
    except Exception as e:
        print(f"\nError: {e}")
        print("Try running the script again or check your internet connection.")
        sys.exit(1)


if __name__ == "__main__":
    main()

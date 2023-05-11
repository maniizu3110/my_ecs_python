import unittest
from .get_domain_detail import get_domain_and_subdomain

class TestDomainUtils(unittest.TestCase):

    def test_get_domain_and_subdomain(self):
        # Test case 1: No subdomain
        result = get_domain_and_subdomain("example.com")
        self.assertEqual(result, {"main_domain": "example.com", "subdomain": None})

        # Test case 2: With subdomain
        result = get_domain_and_subdomain("www.example.com")
        self.assertEqual(result, {"main_domain": "example.com", "subdomain": "www"})

        # Test case 3: With multiple subdomains
        result = get_domain_and_subdomain("blog.sub.example.com")
        self.assertEqual(result, {"main_domain": "example.com", "subdomain": "blog.sub"})

if __name__ == "__main__":
    unittest.main()
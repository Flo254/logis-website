from django.test import TestCase, Client
from django.urls import reverse


class TemplateRenderingTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_all_pages_render_successfully(self):
        routes = [
            ('index', 'index.html', 'index-page'),
            ('about', 'about.html', 'about-page'),
            ('contact', 'contact.html', 'contact-page'),
            ('services', 'services.html', 'services-page'),
            ('service_details', 'service_details.html', 'service-details-page'),
            ('getaquote', 'getaquote.html', 'get-a-quote-page'),
            ('starterpage', 'starterpage.html', 'starter-page-page'),
            ('pricing', 'pricing.html', 'pricing-page'),
        ]
        for route_name, template_name, body_class in routes:
            with self.subTest(route=route_name):
                url = reverse(route_name)
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)
                self.assertTemplateUsed(response, template_name)
                self.assertTemplateUsed(response, 'base.html')
                content = response.content.decode('utf-8')
                self.assertIn(body_class, content)
                self.assertIn('/static/style/main.css', content)
                self.assertIn('/static/js/main.js', content)
                self.assertIn('<header id="header"', content)
                self.assertIn('<footer id="footer"', content)
                # Verify Kenya details and phone numbers
                self.assertIn('+254 712 345 678', content)
                self.assertIn('Kenya', content)
                # Verify BootstrapMade credits are removed
                self.assertNotIn('Designed by <a href="https://bootstrapmade.com/">BootstrapMade</a>', content)
                # Verify Quick Links and Our Services footer links are removed
                self.assertNotIn('<h4>Quick Links</h4>', content)
                self.assertNotIn('<h4>Our Services</h4>', content)
                # Verify dummy Latin text is removed
                self.assertNotIn('Lorem Ipsum', content)
                self.assertNotIn('consectetur', content)

    def test_root_url_renders_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertTemplateUsed(response, 'base.html')

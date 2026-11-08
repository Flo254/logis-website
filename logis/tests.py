from django.test import TestCase, Client
from django.urls import reverse
from django.core import mail
from django.test import override_settings
from unittest.mock import patch


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

    @override_settings(
        EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',
        DEFAULT_FROM_EMAIL='quotes@example.com',
        QUOTE_RECIPIENT_EMAIL='info@example.com',
    )
    def test_quote_request_sends_email_then_shows_success(self):
        response = self.client.post(reverse('getaquote'), {
            'departure': 'Nairobi',
            'delivery': 'Mombasa',
            'weight': '500 kg',
            'dimensions': '100 x 80 x 60 cm',
            'name': 'Test Customer',
            'email': 'customer@example.com',
            'phone': '+254700000000',
            'message': 'Handle with care',
        }, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Your quote request has been sent successfully.')
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ['info@example.com'])
        self.assertEqual(mail.outbox[0].reply_to, ['customer@example.com'])
        self.assertIn('Nairobi', mail.outbox[0].body)

    def test_quote_request_rejects_invalid_email(self):
        response = self.client.post(reverse('getaquote'), {
            'departure': 'Nairobi',
            'delivery': 'Mombasa',
            'weight': '500 kg',
            'dimensions': '100 x 80 x 60 cm',
            'name': 'Test Customer',
            'email': 'not-an-email',
            'phone': '+254700000000',
            'message': 'Handle with care',
        })

        self.assertEqual(response.status_code, 400)
        self.assertContains(response, 'Please check the form details', status_code=400)
        self.assertEqual(len(mail.outbox), 0)

    @override_settings(
        EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',
        DEFAULT_FROM_EMAIL='quotes@example.com',
        QUOTE_RECIPIENT_EMAIL='info@example.com',
    )
    @patch('logis.views.send_mail', side_effect=OSError('SMTP unavailable'))
    def test_quote_request_shows_error_when_email_fails(self, send_mail_mock):
        response = self.client.post(reverse('getaquote'), {
            'departure': 'Nairobi',
            'delivery': 'Mombasa',
            'weight': '500 kg',
            'dimensions': '100 x 80 x 60 cm',
            'name': 'Test Customer',
            'email': 'customer@example.com',
            'phone': '+254700000000',
            'message': 'Handle with care',
        })

        self.assertEqual(response.status_code, 503)
        self.assertContains(response, "We couldn't send your request right now", status_code=503)
        send_mail_mock.assert_called_once()

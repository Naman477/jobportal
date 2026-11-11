import re
from pathlib import Path
from django.test import TestCase
from django.urls import reverse

from adminapp.models import JobInfo
from mainapp.models import Enquiry, JobSeeker, LoginInfo
from userapp.models import AppliedJob, Response


class MobileResponsivenessTemplateTests(TestCase):
    """Verify public, user, and admin pages render valid, mobile-safe HTML and CSS."""

    def setUp(self):
        LoginInfo.objects.create(usertype="admin", username="admin@test.com", password="secret")
        LoginInfo.objects.create(usertype="jobseeker", username="user@test.com", password="secret")
        JobSeeker.objects.create(
            name="Test User",
            gender="Female",
            contactno="9876543210",
            emailaddress="user@test.com",
            qualification="B.Tech",
            experience="2 years",
            keyskill="Python, Django",
            address="Lucknow",
        )
        job = JobInfo.objects.create(
            title="Python Developer",
            description="Backend engineer",
            location="Remote",
            salary=50000,
            jobtype="Full time",
            lastdate="2026-12-31",
            posteddate="11/11/2026",
        )
        Enquiry.objects.create(
            name="Visitor",
            contactno="9876500000",
            emailaddress="visitor@test.com",
            enquirytext="Looking for openings",
            posteddate="11/11/2026",
        )
        Response.objects.create(
            name="Test User",
            contactno="9876543210",
            responsetype="feed",
            subject="Great site",
            responsetext="Works well",
            posteddate="11/11/2026",
        )
        AppliedJob.objects.create(
            jobid=job.id,
            title=job.title,
            description=job.description,
            name="Test User",
            contactno="9876543210",
            emailaddress="user@test.com",
            qualification="B.Tech",
            experience="2 years",
            keyskill="Python, Django",
            applieddate="11/11/2026",
        )

    def _assert_valid_single_document(self, html: str, route: str):
        lower = html.lower()
        self.assertEqual(lower.count("<!doctype html>"), 1, f"{route} has duplicate doctype")
        self.assertEqual(len(re.findall(r"<body[\s>]", lower)), 1, f"{route} has duplicate body tag")
        self.assertEqual(len(re.findall(r"<head[\s>]", lower)), 1, f"{route} has duplicate head tag")
        self.assertEqual(
            lower.count('name="viewport"'), 1, f"{route} missing or duplicate viewport meta"
        )

    def test_public_pages_valid_structure_and_mobile_fixes(self):
        routes = [reverse("index"), reverse("about"), reverse("contact"), reverse("login"), reverse("register")]
        forbidden_patterns = [
            'style="height:50px;"',
            '<span class="navbar-toggler-icon">Menu</span>',
            "margin-left: 150px",
            "margin-left: 100px",
            "margin-left: 250px",
            "margin-left: 110px",
            "width: 900px",
            "width: 500px",
            "margin: 50px;",
            "<Portal></Portal>",
            "<marquee",
        ]
        for route in routes:
            resp = self.client.get(route)
            self.assertEqual(resp.status_code, 200, f"GET {route} failed")
            html = resp.content.decode("utf-8")
            self._assert_valid_single_document(html, route)
            self.assertEqual(
                html.count("bootstrap.bundle"),
                1,
                f"{route} should load bootstrap.bundle exactly once",
            )
            if route == reverse("index"):
                self.assertIn("width: auto;", html)
            for pattern in forbidden_patterns:
                self.assertNotIn(pattern, html, f"{route} still contains mobile-breaking pattern: {pattern}")

    def test_global_css_prevents_horizontal_overflow_and_navbar_collision(self):
        css_path = Path(__file__).resolve().parent / "static" / "css" / "style.css"
        css = css_path.read_text(encoding="utf-8")
        self.assertIn("overflow-x: hidden", css)
        self.assertIn(".site-navbar", css)
        self.assertNotIn("font-size: 120%", css)
        self.assertNotIn("height: 100vh", css)

    def test_public_forms_still_work(self):
        resp_contact = self.client.post(
            reverse("contact"),
            {
                "name": "Asha",
                "contactno": "9999999999",
                "emailaddress": "asha@test.com",
                "enquirytext": "Need details",
            },
        )
        self.assertEqual(resp_contact.status_code, 302)
        self.assertTrue(Enquiry.objects.filter(emailaddress="asha@test.com").exists())

        resp_reg = self.client.post(
            reverse("register"),
            {
                "name": "Rahul",
                "gender": "Male",
                "contactno": "8888888888",
                "emailaddress": "rahul@test.com",
                "qualification": "MCA",
                "experience": "1",
                "keyskill": "SQL",
                "address": "Kanpur",
                "password": "pass",
            },
        )
        self.assertEqual(resp_reg.status_code, 302)
        self.assertTrue(JobSeeker.objects.filter(emailaddress="rahul@test.com").exists())

        resp_login = self.client.post(
            reverse("login"),
            {"username": "user@test.com", "password": "secret"},
        )
        self.assertEqual(resp_login.status_code, 302)
        self.assertEqual(resp_login.url, reverse("userdash"))

    def test_authenticated_user_pages_mobile_responsive(self):
        session = self.client.session
        session["userid"] = "user@test.com"
        session.save()

        for name in ["userdash", "viewjobs", "userprofile", "giveresponse", "changeuserpwd"]:
            resp = self.client.get(reverse(name))
            self.assertEqual(resp.status_code, 200, f"User route {name} failed")
            html = resp.content.decode("utf-8")
            self._assert_valid_single_document(html, name)
            self.assertNotIn('role="alert>', html)
            if name in ("viewjobs", "userprofile"):
                self.assertIn("table-responsive", html)

    def test_authenticated_admin_pages_mobile_responsive(self):
        session = self.client.session
        session["adminid"] = "admin@test.com"
        session.save()

        table_routes = ["jobseeker", "postedjob", "enquiries", "viewfeedback", "viewcomplaint", "appliedjob"]
        for name in ["admindash", "postjob", "changeadminpwd", *table_routes]:
            resp = self.client.get(reverse(name))
            self.assertEqual(resp.status_code, 200, f"Admin route {name} failed")
            html = resp.content.decode("utf-8")
            self._assert_valid_single_document(html, name)
            if name in table_routes:
                self.assertIn("table-responsive", html)

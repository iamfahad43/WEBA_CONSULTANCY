from flask import Flask, render_template, request, redirect, url_for, flash
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from config import Config

app = Flask(__name__)
app.config.from_object(Config)


# ---------- Simple data for services, testimonials, FAQ, blog, etc. ----------

SERVICES = [
    {
        "title": "Accounting Services",
        "slug": "accounting",
        "description": "Monthly bookkeeping, ledger management and financial documentation for SMEs and individuals."
    },
    {
        "title": "Monthly VAT Reporting",
        "slug": "vat-reporting",
        "description": "Accurate VAT calculations, monthly filings and compliance with Finnish tax authorities."
    },
    {
        "title": "Annual Book Closing & Tax Returns",
        "slug": "annual-book-closing",
        "description": "Year-end financial statements, tax return filing, profit & loss and balance sheet preparation."
    },
    {
        "title": "Business Startup & SME Launch Guidance",
        "slug": "business-startup",
        "description": "Step-by-step support to register, structure and launch new businesses in Finland."
    },
    {
        "title": "Immigration Guidance (Finland & EU)",
        "slug": "immigration",
        "description": "Residence and work permit guidance, documentation review and process support for Finland and EU."
    },
]

TESTIMONIALS = [
    {
        "name": "Ahmed, Small Business Owner",
        "location": "Helsinki, Finland",
        "rating": 5,
        "text": "WEBA Consultants handled my VAT and bookkeeping with zero stress. Clear communication and reliable service."
    },
    {
        "name": "Sara, Student",
        "location": "Pakistan → Finland",
        "rating": 5,
        "text": "Their immigration guidance helped me understand every step of the residence permit process."
    },
    {
        "name": "Mikael, Entrepreneur",
        "location": "Espoo, Finland",
        "rating": 4,
        "text": "Professional advice for company registration and tax planning. Highly recommended for new founders."
    },
]

FAQS = {
    "Accounting & VAT": [
        {
            "q": "Do I need monthly bookkeeping for a small business?",
            "a": "Yes, regular bookkeeping helps you stay compliant and gives visibility into your finances."
        },
        {
            "q": "How often do I need to submit VAT reports?",
            "a": "Most businesses submit VAT monthly or quarterly depending on their registration."
        },
    ],
    "Business Registration": [
        {
            "q": "Can you help me open a company in Finland?",
            "a": "Yes, we guide you through the registration process, documentation and financial setup."
        },
    ],
    "Immigration": [
        {
            "q": "Do you provide guidance for Finland and other EU countries?",
            "a": "Yes, we provide general immigration guidance for Finland and selected EU countries."
        },
    ],
}

BLOG_POSTS = [
    {
        "title": "5 Key Steps To Start a Business in Finland",
        "date": "2025-01-10",
        "summary": "An overview of registration, taxation, permits and financial planning for new entrepreneurs.",
    },
    {
        "title": "Understanding VAT for SMEs in Finland",
        "date": "2025-02-01",
        "summary": "What VAT is, who needs to register and how monthly reporting works.",
    },
]


# ---------- Helper: send email ----------

def send_notification_email(subject, body):
    """
    Sends a simple email notification using the SMTP settings in Config.
    """
    try:
        msg = MIMEMultipart()
        msg["From"] = app.config["MAIL_USERNAME"]
        msg["To"] = app.config["MAIL_RECEIVER"]
        msg["Subject"] = subject

        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP(app.config["MAIL_SERVER"], app.config["MAIL_PORT"]) as server:
            if app.config.get("MAIL_USE_TLS", False):
                server.starttls()
            server.login(app.config["MAIL_USERNAME"], app.config["MAIL_PASSWORD"])
            server.send_message(msg)

        return True
    except Exception as e:
        # In dev, print error to console
        print("Error sending email:", e)
        return False


# ---------- Routes ----------

@app.context_processor
def inject_globals():
    """
    Variables available in all templates (navbar, footer, etc.).
    """
    return {
        "company_name": app.config["COMPANY_NAME"],
        "company_phone": app.config["COMPANY_PHONE"],
        "company_email": app.config["COMPANY_EMAIL"],
        "company_city": app.config["COMPANY_CITY"],
        "company_country": app.config["COMPANY_COUNTRY"],
        "business_id": app.config["BUSINESS_ID"],
        "social_links": app.config["SOCIAL_LINKS"],
        "services_list": SERVICES,
    }


@app.route("/")
def home():
    return render_template(
        "home.html",
        services=SERVICES,
        testimonials=TESTIMONIALS[:3]
    )


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/services")
def services():
    return render_template("services.html", services=SERVICES)


@app.route("/pricing")
def pricing():
    return render_template("pricing.html")


@app.route("/faq")
def faq():
    return render_template("faq.html", faqs=FAQS)


@app.route("/blog")
def blog():
    return render_template("blog.html", posts=BLOG_POSTS)


@app.route("/testimonials")
def testimonials():
    return render_template("testimonials.html", testimonials=TESTIMONIALS)


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        message = request.form.get("message")

        subject = f"New contact form submission from {name}"
        body = f"""
New contact form submission:

Name: {name}
Email: {email}
Phone: {phone}

Message:
{message}
"""

        ok = send_notification_email(subject, body)
        if ok:
            flash("Thank you for contacting us. We will get back to you soon.", "success")
        else:
            flash("There was an issue sending your message. Please try again later.", "danger")

        return redirect(url_for("contact"))

    return render_template("contact.html")


@app.route("/appointment", methods=["GET", "POST"])
def appointment():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        service = request.form.get("service")
        language = request.form.get("language")
        date = request.form.get("date")
        time = request.form.get("time")
        message = request.form.get("message")

        subject = f"New appointment request from {name}"
        body = f"""
New appointment request:

Name: {name}
Email: {email}
Phone: {phone}
Preferred Service: {service}
Preferred Language: {language}
Preferred Date: {date}
Preferred Time: {time}

Additional message:
{message}
"""

        ok = send_notification_email(subject, body)
        if ok:
            flash("Your appointment request has been sent. We will confirm the time with you.", "success")
        else:
            flash("There was an issue submitting your request. Please try again later.", "danger")

        return redirect(url_for("appointment"))

    return render_template("appointment.html", services=SERVICES)


if __name__ == "__main__":
    app.run(debug=True)

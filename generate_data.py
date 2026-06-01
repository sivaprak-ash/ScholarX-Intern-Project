"""Generate synthetic labeled dataset for document classification."""
import random
import pandas as pd

random.seed(42)

TEMPLATES = {
    "invoice": [
        "Invoice #{inv} | Bill To: {company} | Date: {date} | Due Date: {due} | "
        "Item: {item} x{qty} @ ${price:.2f} | Subtotal: ${sub:.2f} | Tax (18%): ${tax:.2f} | "
        "Total Due: ${total:.2f} | Payment terms: Net 30 | Bank: {bank} | Account: {acc}",
        "TAX INVOICE from {vendor} | Invoice No: {inv} | GSTIN: {gst} | "
        "Customer: {company} | Date: {date} | Description: {item} | Qty: {qty} | "
        "Rate: ${price:.2f} | Amount: ${sub:.2f} | GST: ${tax:.2f} | Grand Total: ${total:.2f}",
        "BILL | From: {vendor} | To: {company} | Invoice #{inv} | {date} | "
        "Services rendered: {item} | Hours: {qty} | Rate: ${price:.2f}/hr | "
        "Amount: ${sub:.2f} | Taxes: ${tax:.2f} | Amount Due: ${total:.2f} | Due: {due}",
    ],
    "contract": [
        "SERVICE AGREEMENT between {party1} ('Client') and {party2} ('Service Provider'). "
        "Effective Date: {date}. Term: {months} months. Scope: {scope}. "
        "Fees: ${fee:,}/month payable within 30 days. Confidentiality: Both parties agree to "
        "maintain strict confidentiality. Termination: Either party may terminate with {notice} days notice. "
        "Governing Law: {state}. Signatures required.",
        "NON-DISCLOSURE AGREEMENT | Parties: {party1} and {party2} | Date: {date} | "
        "Purpose: {scope} | Confidential Information includes trade secrets, business plans, "
        "financial data, and technical know-how. Obligations last {months} months after disclosure. "
        "Breach subject to injunctive relief and damages. Jurisdiction: {state}.",
        "EMPLOYMENT CONTRACT | Employer: {party1} | Employee: {party2} | Start: {date} | "
        "Role: {scope} | Compensation: ${fee:,} per annum | Benefits: health, dental, PTO. "
        "Notice Period: {notice} days. Intellectual property created during employment belongs to employer. "
        "Non-compete: {months} months post-employment within {state}.",
    ],
    "email": [
        "From: {sender} | To: {recipient} | Subject: {subject} | Date: {date} | "
        "Hi {name}, {body} Please let me know if you have any questions. "
        "Best regards, {sender_name}",
        "From: {sender} To: {recipient} CC: {cc} Date: {date} Subject: Re: {subject} | "
        "{name}, Thanks for your message. {body} Looking forward to your response. "
        "Regards, {sender_name} | {company} | {phone}",
        "INBOX | {sender} → {recipient} | {date} | {subject} | "
        "Dear {name}, I hope this email finds you well. {body} "
        "Please confirm receipt. Thanks, {sender_name} | Sent from mobile",
    ],
    "report": [
        "QUARTERLY REPORT - {quarter} {year} | {company} | Prepared by: {author} | "
        "Executive Summary: {summary} Revenue: ${rev:,}M (+{growth}% YoY). "
        "Key Highlights: {highlight1}. {highlight2}. "
        "Risks: {risk}. Outlook: {outlook}. Appendix: Financial statements attached.",
        "ANNUAL PERFORMANCE REVIEW {year} | Department: {dept} | Manager: {author} | "
        "Overview: {summary} KPIs achieved: {kpi}%. Budget utilization: {budget}%. "
        "Key Accomplishments: {highlight1}. Areas for Improvement: {highlight2}. "
        "Recommendations: {risk}. Next Steps: {outlook}.",
        "RESEARCH REPORT | Title: {title} | Author: {author} | Date: {date} | "
        "Abstract: {summary} Methodology: {highlight1}. Findings: {highlight2}. "
        "Conclusion: {risk}. Recommendations: {outlook}. References: [1] {ref1} [2] {ref2}",
    ],
}

FILLERS = {
    "inv": lambda: f"INV-{random.randint(1000,9999)}",
    "company": lambda: random.choice(["Acme Corp", "Bright Solutions", "TechNova Ltd", "GlobalMart", "Sunrise Enterprises", "Blue Ridge Inc"]),
    "vendor": lambda: random.choice(["ZenSoft", "ProServices", "DataBridge", "CloudWorks", "NetEdge"]),
    "date": lambda: f"{random.randint(1,28):02d}/{random.randint(1,12):02d}/202{random.randint(3,5)}",
    "due": lambda: f"{random.randint(1,28):02d}/{random.randint(1,12):02d}/202{random.randint(4,5)}",
    "item": lambda: random.choice(["Software License", "Consulting Services", "Web Development", "Cloud Hosting", "Marketing Campaign", "Legal Services"]),
    "qty": lambda: random.randint(1, 50),
    "price": lambda: random.uniform(50, 2000),
    "sub": lambda: random.uniform(500, 20000),
    "tax": lambda: random.uniform(50, 2000),
    "total": lambda: random.uniform(600, 25000),
    "bank": lambda: random.choice(["HDFC Bank", "SBI", "ICICI", "Axis Bank", "Citibank"]),
    "acc": lambda: f"{random.randint(100000000,999999999)}",
    "gst": lambda: f"{random.randint(10,35)}ABCDE{random.randint(1000,9999)}Z{random.randint(1,9)}",
    "party1": lambda: random.choice(["Alpha Tech", "Nexus Corp", "Vertex Ltd", "Pinnacle Group", "Summit Inc"]),
    "party2": lambda: random.choice(["John Smith", "Maria Garcia", "Ravi Kumar", "Chen Wei", "Sarah Johnson"]),
    "months": lambda: random.choice([3, 6, 12, 24]),
    "scope": lambda: random.choice(["IT consulting and software development", "marketing and brand management", "data analytics services", "HR outsourcing", "financial advisory"]),
    "fee": lambda: random.randint(5000, 50000),
    "notice": lambda: random.choice([15, 30, 60, 90]),
    "state": lambda: random.choice(["Maharashtra", "Karnataka", "Tamil Nadu", "Delhi", "California"]),
    "sender": lambda: f"{random.choice(['john','sarah','ravi','anna','mike'])}.{random.choice(['smith','kumar','jones','lee'])}@{random.choice(['gmail.com','company.com','outlook.com'])}",
    "recipient": lambda: f"{random.choice(['hr','info','manager','team','support'])}@{random.choice(['acme.com','corp.org','biz.net'])}",
    "cc": lambda: f"cc@{random.choice(['office.com','work.net'])}",
    "subject": lambda: random.choice(["Meeting Follow-up", "Project Update", "Invoice Attached", "Request for Proposal", "Schedule Change", "Quarterly Review", "Action Required"]),
    "name": lambda: random.choice(["John", "Sarah", "Ravi", "Anna", "Michael", "Priya"]),
    "body": lambda: random.choice([
        "I wanted to follow up on our last discussion regarding the project timeline.",
        "Please find attached the documents you requested for your review.",
        "We would like to schedule a call to discuss the upcoming deliverables.",
        "I am writing to inform you about the changes in the schedule.",
        "Could you please provide an update on the status of the pending items?",
    ]),
    "sender_name": lambda: random.choice(["John Smith", "Sarah Lee", "Ravi Kumar", "Anna Chen"]),
    "phone": lambda: f"+91-{random.randint(7000000000,9999999999)}",
    "quarter": lambda: random.choice(["Q1", "Q2", "Q3", "Q4"]),
    "year": lambda: random.choice([2023, 2024, 2025]),
    "author": lambda: random.choice(["Dr. Priya Sharma", "James Wilson", "Anil Mehta", "Lisa Park"]),
    "summary": lambda: random.choice([
        "The organization demonstrated strong performance across all key metrics.",
        "This period saw significant growth driven by new product launches.",
        "Despite market challenges, the team exceeded targets in most areas.",
    ]),
    "rev": lambda: round(random.uniform(10, 500), 1),
    "growth": lambda: round(random.uniform(-5, 30), 1),
    "highlight1": lambda: random.choice(["Launched three new product lines", "Reduced operational costs by 15%", "Expanded to two new markets", "Improved customer satisfaction to 92%"]),
    "highlight2": lambda: random.choice(["Onboarded 50+ enterprise clients", "Automated 40% of manual processes", "Completed ISO certification", "Deployed new CRM system"]),
    "risk": lambda: random.choice(["Supply chain disruptions remain a concern", "Regulatory compliance requirements increasing", "Talent acquisition challenges persist"]),
    "outlook": lambda: random.choice(["Strong pipeline for next quarter", "Continued investment in R&D expected", "Market expansion plans on track"]),
    "dept": lambda: random.choice(["Engineering", "Sales", "Marketing", "Operations", "Finance"]),
    "kpi": lambda: random.randint(75, 110),
    "budget": lambda: random.randint(80, 105),
    "title": lambda: random.choice(["Market Analysis 2024", "Consumer Behavior Study", "Technology Adoption Report", "Competitive Landscape Review"]),
    "ref1": lambda: "Smith et al. (2023), Journal of Business Analytics",
    "ref2": lambda: "Kumar & Lee (2024), Int'l Review of Management",
}


def fill_template(template):
    result = template
    import re
    placeholders = re.findall(r'\{(\w+)(?::[^}]*)?\}', template)
    values = {}
    for key in set(placeholders):
        if key in FILLERS:
            values[key] = FILLERS[key]()
    try:
        result = template.format(**values)
    except (KeyError, ValueError):
        pass
    return result


def generate_dataset(n_per_class=200):
    rows = []
    for label, templates in TEMPLATES.items():
        for _ in range(n_per_class):
            tmpl = random.choice(templates)
            text = fill_template(tmpl)
            rows.append({"text": text, "label": label})
    df = pd.DataFrame(rows).sample(frac=1, random_state=42).reset_index(drop=True)
    return df


if __name__ == "__main__":
    df = generate_dataset(200)
    df.to_csv("/home/claude/doc_classifier/dataset.csv", index=False)
    print(df["label"].value_counts())
    print(f"\nTotal samples: {len(df)}")
    print("\nSample:\n", df.head(2).to_string())

from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import random
from models import *
import io, csv
from fpdf import FPDF
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os
from io import BytesIO
from resources import api

app = Flask(__name__)
CORS(app, origins=["http://localhost:8080"])

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banking.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'softwareengineeringproject'

db.init_app(app)
api.init_app(app)


load_dotenv()

UPLOAD_FOLDER = "uploaded_docs" 

CATEGORY_KEYWORDS = {
    "food": ["restaurant", "dine", "swiggy", "zomato"],
    "transport": ["uber", "ola", "fuel", "metro"],
    "shopping": ["amazon", "flipkart", "mall"],
    "bills": ["electricity", "water", "gas"],
    # "transfer": ['beneficiary'], 
    "others": []
}

################################# Send Email Function #####################################

def send_email(to_email, subject, message):
    try:
        msg = MIMEText(message)
        msg["Subject"] = subject
        msg["From"] = SMTP_USERNAME
        msg["To"] = to_email

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.sendmail(SMTP_USERNAME, to_email, msg.as_string())

        print("Email sent successfully!")

    except Exception as e:
        print("Email sending failed:", e)

####################################### Transaction category Function #################################

def detect_category(description):
    """Classify transaction description into a spending category."""
    d = description.lower()
    for cat, words in CATEGORY_KEYWORDS.items():
        if any(w in d for w in words):
            return cat
    return "others"

################################# Generate OTP Function #####################################

def generate_otp():
    return str(random.randint(100000, 999999))

################################# Generate Account Number Function #####################################

def generate_account_number():
    return str(random.randint(10**14, (10**15)-1))

################################# Send Notification Function #####################################

def send_notification(user_id, title, message, user_email):
    """Create an in-app notification and send email to user."""
    from models import Notification, db
    notif = Notification(user_id=user_id, title=title, message=message)
    db.session.add(notif)
    db.session.commit()

    try:
        sender_email = SMTP_USERNAME
        sender_password = SMTP_PASSWORD

        msg = MIMEMultipart("alternative")
        msg["Subject"] = title
        msg["From"] = sender_email
        msg["To"] = user_email

        html_content = f"""
        <html>
        <body>
            <p>Dear Customer,<br><br>
            {message}<br><br>
            Regards,<br>
            Your Bank
            </p>
        </body>
        </html>
        """
        msg.attach(MIMEText(html_content, "html"))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, user_email, msg.as_string())
            print(f"Email notification sent to {user_email}")
    except Exception as e:
        print(f"Failed to send email notification: {e}")

################################# Create Notification Function #####################################

def create_notification(user_id, title, message):
    new_notification = Notification(
        user_id=user_id,
        title=title,
        message=message
    )
    db.session.add(new_notification)
    db.session.commit()
    return new_notification

############################################ Email Data ###############################################

SMTP_SERVER = os.getenv('SMTP_SERVER')
SMTP_PORT = 587
SMTP_USERNAME = os.getenv('EMAIL_USER')
SMTP_PASSWORD = os.getenv('EMAIL_PASS')

########################################## Home Route ###############################################

@app.route('/')
def home():
    return "Banking Application Started."

############################################ Register Route ##########################################

@app.route("/register", methods=["POST"])
def register():
    data = request.form if request.form else request.get_json()

    full_name = data.get("full_name")
    email = data.get("email")
    phone = data.get("phone")
    login_password_raw = data.get("login_password")
    txn_password_raw = data.get("transaction_password")

    if not login_password_raw or not txn_password_raw:
        return jsonify({"message": "Passwords are required"}), 400

    login_password = generate_password_hash(login_password_raw)
    txn_password = generate_password_hash(txn_password_raw)

    if Customer.query.filter(
        (Customer.email == email) | (Customer.phone == phone)
    ).first():
        return jsonify({"message": "Email or phone already registered"}), 400

    customer = Customer(
        full_name=full_name,
        email=email,
        phone=phone,
        login_password=login_password,
        transaction_password=txn_password,
        is_active=False
    )

    db.session.add(customer)
    db.session.commit()

    return jsonify({
        "message": "Customer registered. Proceed to document upload.",
        "customer_id": customer.id
    }), 200

############################################ KYC Upload Route ##########################################

@app.route("/kyc/upload/<int:customer_id>", methods=["POST"])
def upload_kyc(customer_id):
    customer = Customer.query.get(customer_id)
    if not customer:
        return jsonify({"message": "Customer not found"}), 404

    aadhaar = request.files.get("aadhaar")
    pan = request.files.get("pan")
    photo = request.files.get("photo")
    signature = request.files.get("signature")

    path = "uploads/kyc/"
    os.makedirs(path, exist_ok=True)

    aadhaar_file = os.path.join(path, aadhaar.filename)
    pan_file = os.path.join(path, pan.filename)
    photo_file = os.path.join(path, photo.filename)
    signature_file = os.path.join(path, signature.filename)

    aadhaar.save(aadhaar_file)
    pan.save(pan_file)
    photo.save(photo_file)
    signature.save(signature_file)

    kyc = KYC(
        customer_id=customer_id,
        aadhaar_file=aadhaar_file,
        pan_file=pan_file,
        photo_file=photo_file,
        signature_file=signature_file
    )

    db.session.add(kyc)
    db.session.commit()

    return jsonify({"message": "KYC uploaded. Now verify with OTP."}), 200

############################################ KYC OTP Route ##########################################

@app.route("/kyc/send_otp/<int:customer_id>", methods=["POST"])
def send_kyc_otp(customer_id):
    kyc = KYC.query.filter_by(customer_id=customer_id).first()
    if not kyc:
        return jsonify({"message": "Upload KYC documents first"}), 400

    otp = generate_otp()

    kyc.kyc_otp = otp
    kyc.otp_expires_at = datetime.utcnow() + timedelta(minutes=5)
    kyc.otp_verified = False

    db.session.commit()

    send_email(kyc.customer.email, "Your KYC OTP", f"Your OTP is: {otp}")

    return jsonify({"message": "KYC OTP sent"}), 200

######################################## KYC Verify OTP Route ##########################################

@app.route("/kyc/verify_otp/<int:customer_id>", methods=["POST"])
def verify_kyc_otp(customer_id):
    data = request.get_json()
    otp = data.get("otp")

    kyc = KYC.query.filter_by(customer_id=customer_id).first()
    if not kyc:
        return jsonify({"message": "KYC not found"}), 404

    if kyc.kyc_otp != otp or datetime.utcnow() > kyc.otp_expires_at:
        return jsonify({"message": "Invalid or expired OTP"}), 400

    kyc.otp_verified = True
    db.session.commit()

    send_email(
        kyc.customer.email,
        "KYC OTP Verified",
        "Your KYC OTP has been successfully verified. KYC will now be reviewed by the manager."
    )

    return jsonify({
        "message": "OTP Verified. KYC is now pending manager approval."
    }), 200

############################################ Login Route ##########################################

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    account_number = data.get("account_number")
    password = data.get("password")

    account = Account.query.filter_by(account_number=account_number).first()
    if not account:
        return jsonify({"message": "Invalid account number"}), 404

    customer = account.customer

    if not customer.is_active:
        return jsonify({"message": "Account not activated by manager"}), 403

    if not check_password_hash(customer.login_password, password):
        return jsonify({"message": "Incorrect password"}), 401

    otp = generate_otp()
    otp_entry = OTPVerification(
        otp_code=otp,
        expires_at=datetime.utcnow() + timedelta(minutes=5),
        customer_id=customer.id
    )
    db.session.add(otp_entry)
    db.session.commit()

    send_email(customer.email, "Login OTP", f"Your login OTP is: {otp}")

    return jsonify({"message": "OTP sent"}), 200

############################################ Login Verify OTP Route ##########################################

@app.route("/verify_otp", methods=["POST"])
def verify_login_otp():
    data = request.get_json()
    account_number = data.get("account_number")
    otp = data.get("otp")

    account = Account.query.filter_by(account_number=account_number).first()
    if not account:
        return jsonify({"message": "Invalid account number"}), 404

    customer = account.customer

    otp_entry = OTPVerification.query.filter_by(
        customer_id=customer.id,
        otp_code=otp,
        is_used=False
    ).first()

    if not otp_entry:
        return jsonify({"message": "Invalid or expired OTP"}), 400

    if datetime.utcnow() > otp_entry.expires_at:
        return jsonify({"message": "OTP expired"}), 400

    otp_entry.is_used = True
    db.session.commit()

    return jsonify({
        "message": "Login successful",
        "customer": {
            "id": customer.id,
            "full_name": customer.full_name,
            "account_number": account.account_number
        }
    }), 200

###################################### Forgot Password Route ##########################################

@app.route("/forgot_password", methods=["POST"])
def forgot_password():
    data = request.get_json()
    email = data.get("email")

    customer = Customer.query.filter_by(email=email).first()
    if not customer:
        return jsonify({"message": "Email not found"}), 404

    otp_code = generate_otp()
    otp_entry = OTPVerification(
        otp_code=otp_code,
        expires_at=datetime.utcnow() + timedelta(minutes=5),
        customer_id=customer.id
    )
    db.session.add(otp_entry)
    db.session.commit()

    return jsonify({"message": "OTP sent for password reset", "otp": otp_code}), 200

########################################## Reset Password Route #####################################

@app.route("/reset_password", methods=["POST"])
def reset_password():
    data = request.get_json()
    email = data.get("email")
    otp = data.get("otp")
    new_password = data.get("new_password")

    customer = Customer.query.filter_by(email=email).first()
    if not customer:
        return jsonify({"message": "Invalid email"}), 404

    otp_entry = OTPVerification.query.filter_by(customer_id=customer.id, otp_code=otp, is_used=False).first()
    if not otp_entry or datetime.utcnow() > otp_entry.expires_at:
        return jsonify({"message": "Invalid or expired OTP"}), 400

    customer.password_hash = generate_password_hash(new_password)
    otp_entry.is_used = True
    db.session.commit()

    return jsonify({"message": "Password reset successful"}), 200

########################################## GET Balance Route ##########################################

@app.route('/customer/balance/<int:customer_id>', methods=['GET'])
def get_balance(customer_id):
    account = Account.query.filter_by(customer_id=customer_id).first()
    if not account:
        return jsonify({'error': 'Account not found'}), 404
    return jsonify({'balance': account.balance})

######################################## Get Mini Transaction Route ###################################

@app.route('/customer/mini-statement/<int:customer_id>', methods=['GET'])
def mini_statement(customer_id):
    account = Account.query.filter_by(customer_id=customer_id).first()
    if not account:
        return jsonify({'error': 'Account not found'}), 404

    txns = (
        Transaction.query
        .filter_by(account_id=account.id)
        .order_by(Transaction.timestamp.desc())
        .limit(10)
        .all()
    )

    data = [{
        'id': t.id,
        'transaction_id': t.transaction_uuid,
        'type': t.transaction_type,
        'amount': t.amount,
        'timestamp': t.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        'description': t.description
    } for t in txns]

    return jsonify(data)

########################################## Get Transactions Route #####################################

@app.route('/customer/transactions/<int:customer_id>', methods=['GET'])
def get_transactions(customer_id):
    export_format = request.args.get('format', 'json')
    account = Account.query.filter_by(customer_id=customer_id).first()
    if not account:
        return jsonify({'error': 'Account not found'}), 404

    txns = (
        Transaction.query
        .filter_by(account_id=account.id)
        .order_by(Transaction.timestamp.desc())
        .all()
    )

    if export_format == 'csv':
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['ID', 'Type', 'Amount', 'Timestamp', 'Description'])
        for t in txns:
            writer.writerow([t.id, t.transaction_type, t.amount, t.timestamp, t.description])
        output.seek(0)
        return send_file(io.BytesIO(output.getvalue().encode()),
                         as_attachment=True,
                         download_name="transactions.csv",
                         mimetype="text/csv")

    elif export_format == 'pdf':
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Transaction History", ln=True, align='C')
        for t in txns:
            amount_str = f"Rs.{t.amount}"
            pdf.cell(200, 8,
                    txt=f"{t.timestamp} | {t.transaction_type} | {amount_str} | {t.description}",
                    ln=True)
        pdf_output = BytesIO()
        pdf_bytes = pdf.output(dest='S').encode('latin1')
        pdf_output.write(pdf_bytes)
        pdf_output.seek(0)

        return send_file(
            pdf_output,
            as_attachment=True,
            download_name='transactions.pdf',
            mimetype='application/pdf'
        )

    data = [{
        'id': t.id,
        'type': t.transaction_type,
        'amount': t.amount,
        'timestamp': t.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        'description': t.description
    } for t in txns]
    return jsonify(data)

########################################## Add Beneficiary Route ######################################

@app.route('/customer/add-beneficiary', methods=['POST'])
def add_beneficiary():
    data = request.get_json()
    customer_id = data.get('customer_id')
    name = data.get('name')
    bank_name = data.get('bank_name')
    account_number = data.get('account_number')
    ifsc_code = data.get('ifsc_code')
    transfer_mode = data.get('transfer_mode', 'IMPS')

    customer = Customer.query.get(customer_id)
    if not customer:
        return jsonify({'message': 'Customer not found'}), 404

    # avoid duplicates
    if Beneficiary.query.filter_by(customer_id=customer_id, account_number=account_number).first():
        return jsonify({'message': 'Beneficiary already exists'}), 400

    otp_code = generate_otp()
    otp_entry = OTPVerification(
        otp_code=otp_code,
        expires_at=datetime.utcnow() + timedelta(minutes=5),
        customer_id=customer_id
    )
    db.session.add(otp_entry)
    db.session.commit()

    beneficiary = Beneficiary(
        name=name,
        bank_name=bank_name,
        account_number=account_number,
        ifsc_code=ifsc_code,
        transfer_mode=transfer_mode,
        verified=False,
        cooling_period_end=None,
        customer_id=customer_id
    )
    db.session.add(beneficiary)
    db.session.commit()

    subject = "OTP for Adding Beneficiary"
    message = f"Hello {customer.full_name},\n\nYour OTP for adding the beneficiary {name} is: {otp_code}\nIt is valid for 5 minutes.\n\nRegards,\nYour Bank"
    try:
        send_email(customer.email, subject, message)
    except Exception as e:
        print("Error sending email:", e)
        return jsonify({'message': 'Failed to send OTP email'}), 500

    return jsonify({'message': 'OTP sent for beneficiary addition', 'otp': otp_code}), 200

########################################## Verify Beneficiary Route ####################################

@app.route('/customer/verify-beneficiary-otp', methods=['POST'])
def verify_beneficiary_otp():
    data = request.get_json()
    customer_id = data.get('customer_id')
    otp = data.get('otp')
    account_number = data.get('account_number')

    otp_entry = OTPVerification.query.filter_by(customer_id=customer_id, otp_code=otp, is_used=False).first()
    if not otp_entry or datetime.utcnow() > otp_entry.expires_at:
        return jsonify({'message': 'Invalid or expired OTP'}), 400

    beneficiary = Beneficiary.query.filter_by(customer_id=customer_id, account_number=account_number).first()
    if not beneficiary:
        return jsonify({'message': 'Beneficiary not found'}), 404

    # verify & apply cooling period (1 min)

    beneficiary.verified = True
    beneficiary.cooling_period_end = datetime.utcnow() + timedelta(minutes=1)
    otp_entry.is_used = True
    db.session.commit()

    return jsonify({'message': 'Beneficiary verified successfully. Cooling period started.'}), 200

####################################### GET All Beneficiary Route ######################################

@app.route('/customer/beneficiaries/<int:customer_id>', methods=['GET'])
def list_beneficiaries(customer_id):
    beneficiaries = Beneficiary.query.filter_by(customer_id=customer_id).all()
    result = []
    for b in beneficiaries:
        status = 'Pending Verification'
        if b.verified:
            if b.cooling_period_end and datetime.utcnow() < b.cooling_period_end:
                status = 'Cooling Period'
            else:
                status = 'Active'
        result.append({
            'name': b.name,
            'bank_name': b.bank_name,
            'account_number': b.account_number,
            'ifsc_code': b.ifsc_code,
            'transfer_mode': b.transfer_mode,
            'status': status,
            'added_at': b.added_at.strftime("%Y-%m-%d %H:%M:%S")
        })
    return jsonify(result)


####################################### Transfer Funds Route #######################################

def update_account_balance(account, amount, transaction_type):
    if transaction_type == "credit":
        account.balance += amount
    elif transaction_type == "debit":
        if account.balance < amount:
            raise ValueError("Insufficient balance")
        account.balance -= amount
    
    db.session.commit()


####################################### Update Banace Function #######################################


@app.route('/customer/transfer', methods=['POST'])
def transfer_funds():
    data = request.get_json()
    sender_id = data.get('customer_id')
    beneficiary_acc_number = data.get('beneficiary_account')
    amount = float(data.get('amount', 0))
    remarks = data.get('remarks', '')

    if amount <= 0:
        return jsonify({'message': 'Invalid transfer amount'}), 400

    sender_acc = Account.query.filter_by(customer_id=sender_id).first()
    if not sender_acc:
        return jsonify({'message': 'Sender account not found'}), 404

    if sender_acc.balance < amount:
        return jsonify({'message': 'Insufficient balance'}), 400

    beneficiary = Beneficiary.query.filter_by(
        customer_id=sender_id,
        account_number=beneficiary_acc_number
    ).first()
    if not beneficiary:
        return jsonify({'message': 'Beneficiary not found'}), 404

    if not beneficiary.verified:
        return jsonify({'message': 'Beneficiary not verified yet'}), 400

    if beneficiary.cooling_period_end and datetime.utcnow() < beneficiary.cooling_period_end:
        return jsonify({'message': 'Cooling period active. Try later.'}), 400

    receiver_acc = Account.query.filter_by(account_number=beneficiary.account_number).first()
    internal_transfer = receiver_acc is not None


    if internal_transfer and receiver_acc.id == sender_acc.id:
        return jsonify({'message': 'Cannot transfer to same account'}), 400

    debit_txn = Transaction(
        account_id=sender_acc.id,
        transaction_type='debit',
        amount=amount,
        description=f'Transfer to {beneficiary.name} ({beneficiary.account_number}) - {remarks}'
    )
    db.session.add(debit_txn)
    sender_acc.balance -= amount

    if internal_transfer:
        credit_txn = Transaction(
            account_id=receiver_acc.id,
            transaction_type='credit',
            amount=amount,
            description=f'Transfer from {sender_acc.customer.full_name} ({sender_acc.account_number})'
        )
        db.session.add(credit_txn)
        receiver_acc.balance += amount
    else:
        credit_txn = None

    db.session.commit()

    send_notification(
        sender_id,
        "Debit Alert",
        f"₹{amount} debited to {beneficiary.name}.",
        sender_acc.customer.email
    )

    if internal_transfer:
        send_notification(
            receiver_acc.customer.id,
            "Credit Alert",
            f"₹{amount} credited from {sender_acc.customer.full_name}.",
            receiver_acc.customer.email
        )

    return jsonify({
        'message': f'₹{amount} transferred successfully to {beneficiary.name} '
                   + ('(Internal Transfer)' if internal_transfer else '(External Transfer)'),
        'debit_transaction_id': debit_txn.transaction_uuid,
        'credit_transaction_id': credit_txn.transaction_uuid if credit_txn else None
    }), 200


############################### Bill Payments / Recharges / FASTag Top-up ##############################

@app.route('/customer/bill-options', methods=['GET'])
def bill_options():
    """
    Return mock biller & operator lists (used by frontend dropdowns).
    In production, replace with real provider list or an external service.
    """
    options = {
        "bill_types": ["Electricity", "Water", "Gas", "Internet", "Property Tax"],
        "electricity_providers": ["StateGrid", "CityPower", "Privault Energy"],
        "gas_providers": ["CityGas", "GovGas"],
        "internet_providers": ["NetPlus", "FiberNet"],
        "mobile_operators": ["Airtel", "Vodafone", "Jio", "BSNL"],
        "dth_providers": ["DishTV", "TataSky", "SunDirect"]
    }
    return jsonify(options), 200

########################################## Perform Debit Function ######################################

def _perform_debit(account, amount, description):
    """
    Helper to debit an account, create Transaction and update balance.
    Returns tuple (success:boolean, payload:dict)
    """
    if amount <= 0:
        return False, {"message": "Amount must be positive."}
    if account.balance < amount:
        return False, {"message": "Insufficient balance."}

    txn = Transaction(
        account_id=account.id,
        transaction_type='debit',
        amount=amount,
        description=description
    )
    account.balance -= amount
    db.session.add(txn)
    db.session.commit()

    customer_id = account.customer_id
    category_name = update_spending_category(customer_id, amount, description)

    return True, {
        "message": "Transaction successful", 
        "transaction_id": txn.id, 
        "new_balance": account.balance,
        "category": category_name
    }

########################################## Pay Bill Route ######################################

@app.route('/customer/pay-bill', methods=['POST'])
def pay_bill():
    """
    Pay a bill for a customer.
    """
    data = request.get_json() or {}
    customer_id = data.get('customer_id')
    bill_type = data.get('bill_type')
    biller = data.get('biller')
    amount = float(data.get('amount', 0))
    bill_account = data.get('bill_account', '')

    if not customer_id or not bill_type or not biller or amount <= 0:
        return jsonify({'message': 'Missing or invalid fields'}), 400

    account = Account.query.filter_by(customer_id=customer_id).first()
    if not account:
        return jsonify({'message': 'Account not found'}), 404

    customer = Customer.query.get(customer_id)
    desc = f"Bill Payment: {biller} - {bill_type}"
    if bill_account:
        desc += f" (Ref: {bill_account})"

    ok, payload = _perform_debit(account, amount, desc)

    if ok:
        message = f"₹{amount} debited for {bill_type} bill payment to {biller}. " \
                  f"Your new balance is ₹{account.balance:.2f}."
        send_notification(customer.id, "Bill Payment Successful", message, customer.email)
    else:
        message = f"Your {bill_type} bill payment of ₹{amount} to {biller} failed due to {payload['message']}."
        send_notification(customer.id, "Bill Payment Failed", message, customer.email)

    status_code = 200 if ok else 400
    return jsonify(payload), status_code

########################################## Reacharge Route ######################################

@app.route('/customer/recharge', methods=['POST'])
def recharge():
    """
    Mobile / DTH recharge.
    """
    data = request.get_json() or {}
    customer_id = data.get('customer_id')
    recharge_type = data.get('recharge_type')
    operator = data.get('operator')
    number = data.get('number')
    amount = float(data.get('amount', 0))

    if not customer_id or not recharge_type or not operator or not number or amount <= 0:
        return jsonify({'message': 'Missing or invalid fields'}), 400

    account = Account.query.filter_by(customer_id=customer_id).first()
    if not account:
        return jsonify({'message': 'Account not found'}), 404

    customer = Customer.query.get(customer_id)
    desc = f"{recharge_type} Recharge: {operator} - {number}"
    ok, payload = _perform_debit(account, amount, desc)

    if ok:
        message = f"₹{amount} debited for your {recharge_type} recharge with {operator}. " \
                  f"Your new balance is ₹{account.balance:.2f}."
        send_notification(customer.id, "Recharge Successful", message, customer.email)
    else:
        message = f"Recharge of ₹{amount} for {operator} failed due to {payload['message']}."
        send_notification(customer.id, "Recharge Failed", message, customer.email)

    status_code = 200 if ok else 400
    return jsonify(payload), status_code

########################################## Fastatg Recharge ######################################

@app.route('/customer/fastag-topup', methods=['POST'])
def fastag_topup():
    """
    FASTag top-up.
    """
    data = request.get_json() or {}
    customer_id = data.get('customer_id')
    vehicle_number = data.get('vehicle_number')
    tag_id = data.get('tag_id', '')
    amount = float(data.get('amount', 0))

    if not customer_id or not vehicle_number or amount <= 0:
        return jsonify({'message': 'Missing or invalid fields'}), 400

    account = Account.query.filter_by(customer_id=customer_id).first()
    if not account:
        return jsonify({'message': 'Account not found'}), 404

    customer = Customer.query.get(customer_id)
    desc = f"FASTag Top-up: {vehicle_number}"
    if tag_id:
        desc += f" (Tag: {tag_id})"

    ok, payload = _perform_debit(account, amount, desc)

    if ok:
        message = f"₹{amount} debited for FASTag top-up ({vehicle_number}). " \
                  f"Your new balance is ₹{account.balance:.2f}."
        send_notification(customer.id, "FASTag Top-up Successful", message, customer.email)
    else:
        message = f"FASTag top-up of ₹{amount} for {vehicle_number} failed due to {payload['message']}."
        send_notification(customer.id, "FASTag Top-up Failed", message, customer.email)

    status_code = 200 if ok else 400
    return jsonify(payload), status_code

########################################## Update SPending Category Function ######################################

def update_spending_category(customer_id, amount, description):
    category_name = detect_category(description)
    
    # Fetch existing category for the customer
    category = SpendingCategory.query.filter_by(customer_id=customer_id, category_name=category_name).first()
    
    if not category:
        # If category doesn't exist, create it
        category = SpendingCategory(
            customer_id=customer_id,
            category_name=category_name,
            budget_limit=0,  # optional, can be updated later
            spent_amount=0.0
        )
        db.session.add(category)
    
    # Update spent amount
    category.spent_amount += amount
    db.session.commit()
    
    return category_name

###################################### DELETE A BENEFICIARY Route #####################################

@app.route('/customer/delete-beneficiary', methods=['POST'])
def delete_beneficiary():
    data = request.get_json()
    customer_id = data.get('customer_id')
    account_number = data.get('account_number')

    beneficiary = Beneficiary.query.filter_by(customer_id=customer_id, account_number=account_number).first()
    if not beneficiary:
        return jsonify({'message': 'Beneficiary not found'}), 404

    db.session.delete(beneficiary)
    db.session.commit()
    return jsonify({'message': f'Beneficiary {beneficiary.name} deleted successfully.'}), 200

################################# VIEW BENEFICIARY Route #####################################

@app.route('/customer/view-beneficiary', methods=['GET'])
def view_beneficiary():
    customer_id = request.args.get('customer_id')
    account_number = request.args.get('account_number')

    beneficiary = Beneficiary.query.filter_by(customer_id=customer_id, account_number=account_number).first()
    if not beneficiary:
        return jsonify({'message': 'Beneficiary not found'}), 404

    status = 'Pending Verification'
    if beneficiary.verified:
        if beneficiary.cooling_period_end and datetime.utcnow() < beneficiary.cooling_period_end:
            status = 'Cooling Period'
        else:
            status = 'Active'

    result = {
        'name': beneficiary.name,
        'bank_name': beneficiary.bank_name,
        'account_number': beneficiary.account_number,
        'ifsc_code': beneficiary.ifsc_code,
        'transfer_mode': beneficiary.transfer_mode,
        'status': status,
        'added_at': beneficiary.added_at.strftime("%Y-%m-%d %H:%M:%S")
    }

    return jsonify(result), 200

# routes/notifications.py

################################# Get all Notifications Route #####################################
@app.route('/api/notifications/<int:user_id>', methods=['GET'])
def get_notifications(user_id):
    notifications = Notification.query.filter_by(user_id=user_id).order_by(Notification.created_at.desc()).all()
    return jsonify([n.to_dict() for n in notifications])

################################# Create New Notifications Route #####################################

@app.route('/api/notifications', methods=['POST'])
def create_new_notification():
    data = request.get_json()
    new_notif = Notification(
        user_id=data.get('user_id'),
        title=data.get('title'),
        message=data.get('message')
    )
    db.session.add(new_notif)
    db.session.commit()
    return jsonify(new_notif.to_dict()), 201

################################# Read New Notifications Route #####################################

@app.route('/api/notifications/<int:notification_id>/read', methods=['PUT'])
def mark_as_read(notification_id):
    notif = Notification.query.get(notification_id)
    if not notif:
        return jsonify({"error": "Notification not found"}), 404
    notif.is_read = True
    db.session.commit()
    return jsonify({"message": "Notification marked as read"})

################################# Delete New Notifications Route #####################################

@app.route('/api/notifications/<int:notification_id>', methods=['DELETE'])
def delete_notification(notification_id):
    notif = Notification.query.get(notification_id)
    if not notif:
        return jsonify({"error": "Notification not found"}), 404
    db.session.delete(notif)
    db.session.commit()
    return jsonify({"message": "Notification deleted"})


### Manager Code

@app.route('/manager/kyc/pending', methods=['GET'])
def get_pending_kyc():
    pending = KYC.query.filter_by(status="pending").all()
    result = []

    for k in pending:
        result.append({
            "kyc_id": k.id,
            "customer_id": k.customer_id,
            "customer_name": k.customer.full_name,
            "submitted_at": k.submitted_at,
            "aadhaar_file": k.aadhaar_file,
            "pan_file": k.pan_file,
            "photo_file": k.photo_file,
            "signature_file": k.signature_file
        })

    return jsonify(result), 200


################################# Approve Manager Route #####################################

@app.route('/manager/kyc/approve/<int:kyc_id>', methods=['POST'])
def approve_kyc(kyc_id):
    kyc = KYC.query.get(kyc_id)

    if not kyc:
        return jsonify({"error": "KYC record not found"}), 404

    if not kyc.otp_verified:
        return jsonify({"error": "Customer must verify OTP before approval"}), 400

    data = request.get_json(silent=True) or {}
    comment = data.get("comment") or request.form.get("comment", "")

    kyc.status = "approved"
    kyc.reviewed_at = datetime.utcnow()
    kyc.reviewer_comment = comment

    customer = Customer.query.get(kyc.customer_id)
    customer.is_active = True

    account_number = generate_account_number()
    account = Account(account_number=account_number, customer_id=customer.id)
    db.session.add(account)

    db.session.commit()

    initial_transaction = Transaction(
        account_id=account.id,
        transaction_type="credit",
        amount=10000.0,
        description="Initial account funding of ₹10,000"
    )
    db.session.add(initial_transaction)
    db.session.commit()

    send_email(
        customer.email,
        "KYC Approved",
        f"Dear {customer.full_name},\n\nYour KYC has been approved.\n"
        f"Your new bank account number is: {account_number}\n"
        f"You may now use all banking services."
    )

    # return jsonify({"message": "KYC Approved"}), 200
    return jsonify({
        "message": "KYC approved. Account created with ₹10,000 balance.",
        "account_number": account.account_number,
        "transaction_uuid": initial_transaction.transaction_uuid,
        "transaction_description": initial_transaction.description
    }), 200


################################# Reject KYC Request (Manager) Route ##################################

@app.route('/manager/kyc/reject/<int:kyc_id>', methods=['POST'])
def reject_kyc(kyc_id):
    kyc = KYC.query.get(kyc_id)

    if not kyc:
        return jsonify({"error": "KYC record not found"}), 404

    data = request.get_json(silent=True) or {}
    comment = data.get("comment") or request.form.get("comment", "")

    kyc.status = "rejected"
    kyc.reviewed_at = datetime.utcnow()
    kyc.reviewer_comment = comment

    db.session.commit()

    customer = Customer.query.get(kyc.customer_id)
    send_email(
        customer.email,
        "KYC Rejected",
        f"Dear {customer.full_name},\n\nYour KYC has been rejected.\n"
        f"Reason: {comment if comment else 'Not specified'}\n"
        f"Please resubmit your KYC with correct details."
    )

    return jsonify({"message": "KYC Rejected"}), 200

################################# Docuemnts Route #####################################

@app.route('/kyc_docs/<path:filename>', methods=['GET'])
def serve_kyc_document(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

########################################## Profile View ############################################

@app.route("/customer/profile/<int:customer_id>", methods=["GET"])
def get_customer_profile(customer_id):
    customer = Customer.query.get(customer_id)
    if not customer:
        return jsonify({"message": "Customer not found"}), 404

    account = Account.query.filter_by(customer_id=customer_id).first()

    kyc = KYC.query.filter_by(customer_id=customer_id).first()

    profile = {
        "customer_id": customer.id,
        "full_name": customer.full_name,
        "email": customer.email,
        "phone": customer.phone,
        "is_active": customer.is_active,
        "created_at": customer.created_at.strftime("%Y-%m-%d %H:%M:%S"),

        "account": {
            "account_number": account.account_number if account else None,
            "account_type": account.account_type if account else None,
            "balance": account.balance if account else None,
            "created_at": account.created_at.strftime("%Y-%m-%d %H:%M:%S") if account else None
        },

        "kyc": {
            "status": kyc.status if kyc else "not_submitted",
            "aadhaar_file": kyc.aadhaar_file if kyc else None,
            "pan_file": kyc.pan_file if kyc else None,
            "photo_file": kyc.photo_file if kyc else None,
            "signature_file": kyc.signature_file if kyc else None,
            "otp_verified": kyc.otp_verified if kyc else False,
            "submitted_at": kyc.submitted_at.strftime("%Y-%m-%d %H:%M:%S") if kyc else None,
            "reviewed_at": kyc.reviewed_at.strftime("%Y-%m-%d %H:%M:%S") if (kyc and kyc.reviewed_at) else None,
            "reviewer_comment": kyc.reviewer_comment if kyc else None
        }
    }

    return jsonify(profile), 200

########################################### Get KYC File ############################################

@app.route('/profile/kyc_docs/<path:filepath>', methods=['GET'])
def serve_kyc_document_profile(filepath):
    from urllib.parse import unquote
    filepath = unquote(filepath)

    if not os.path.exists(filepath):
        return jsonify({"message": "File not found"}), 404

    return send_file(filepath)

########################################### Mounesh's Code ############################################

@app.route('/api/customer/register', methods = ['POST'])
# or we can write - @app.post('/api/register')
def customer_register():
    credentials = request.get_json()
    if not Customer.query.filter_by(email=credentials["email"]).first():
        # dob_str = credentials.get("dob", "").strip()
        # if not dob_str:
        #     return jsonify({"error": "Date of Birth is required"}), 400  # Handle missing input
        dob_date = datetime.strptime(credentials["dob"], "%Y-%m-%d").date()
        count = Customer.query.count()
        new_customer = Customer(email = credentials["email"],
                                        name = credentials["name"],
                                        password = generate_password_hash(credentials["password"]),
                                        role = 1,
                                        dob = dob_date,
                                        contact_number = credentials["contact_number"],
                                        date_of_signup = datetime.now().date(),
                                        account_number = 1000+count+1,
                                        location = credentials["location"],
                                        pin_code = credentials["pincode"])
        db.session.add(new_customer)
        db.session.commit()
        return jsonify({
            "message": "Customer created successfully"
        }), 201
    
    return jsonify({
        "message": "Customer already exits!"
    }), 400


# manager registration
########################################### Manager Registration ############################################
@app.route('/api/manager/register', methods = ['POST'])
    # or we can write - @app.post('/api/register')
def manager_register():
    credentials = request.get_json()
    if not Bank_manager.query.filter_by(email=credentials["email"]).first():
        # dob_str = credentials.get("dob", "").strip()
        # if not dob_str:
        #     return jsonify({"error": "Date of Birth is required"}), 400  # Handle missing input
        
        new_manager = Bank_manager(email = credentials["email"],
                                        name = credentials["name"],
                                        password = generate_password_hash(credentials["password"]),
                                        role = 3,
                                        contact_number = credentials["contact_number"],
                                        date_of_regn = datetime.now().date())
        db.session.add(new_manager)
        db.session.commit()
        return jsonify({
            "message": "Manager created successfully"
        }), 201
    
    return jsonify({
        "message": "Manager already exits!"
    }), 400


    # employee registration
########################################### employee registration ############################################

@app.route('/api/employee/register', methods = ['POST'])
# or we can write - @app.post('/api/register')
def employee_register():
    credentials = request.get_json()
    if not Bank_employee.query.filter_by(email=credentials["email"]).first():
        # dob_str = credentials.get("dob", "").strip()
        # if not dob_str:
        #     return jsonify({"error": "Date of Birth is required"}), 400  # Handle missing input
        
        new_employee = Bank_employee(email = credentials["email"],
                                        name = credentials["name"],
                                        password = generate_password_hash(credentials["password"]),
                                        role = 2,
                                        contact_number = credentials["contact_number"],
                                        date_of_regn = datetime.now().date(),
                                        manager_id = credentials["manager_id"])
        db.session.add(new_employee)
        db.session.commit()
        return jsonify({
            "message": "Employee created successfully"
        }), 201
    
    return jsonify({
        "message": "Employee already exits!"
    }), 400

########################################### Employee Login ############################################

@app.route('/api/employee/login', methods = ['POST'])
# or we can write - @app.post('/api/register')
def employee_login():
    credentials = request.get_json()
    emp = Bank_employee.query.filter_by(email=credentials["email"]).first()
    if not emp:
        return jsonify({
            "message": "Employee does not exist"
        }), 400
    elif not check_password_hash(emp.password,credentials['password']):
        return jsonify({
            "message": "Password does not match"
        }), 400
    else:
        return jsonify({
            "message": "Login successful"
        }), 201
        
########################################### Manager Login ############################################
        
@app.route('/api/manager/login', methods = ['POST'])
# or we can write - @app.post('/api/register')
def manager_login():
    credentials = request.get_json()
    print(credentials)
    print(generate_password_hash(credentials["password"]))
    manager = Bank_manager.query.filter_by(email=credentials["email"]).first()
    print(manager.password)
    if not manager:
        return jsonify({
            "message": "Manager does not exist"
        }), 400

    elif not check_password_hash(manager.password,credentials['password']):
        return jsonify({
            "message": "Password does not match"
        }), 400
    else:
        return jsonify({
            "message": "Login successful"
        }), 201


########################################### Dummy Data Route ############################################

def create_dummy_transactions():
    try:
        txn_list = []

        customer1 = Customer.query.filter_by(email="akanuragkumar4@gmail.com").first()
        customer2 = Customer.query.filter_by(email="tech@kvqaindia.com").first()

        account1 = Account.query.filter_by(customer_id=customer1.id).first()
        account2 = Account.query.filter_by(customer_id=customer2.id).first()

        txn_list.append(Transaction(
            transaction_type="credit",
            amount=10000,
            description="Initial cash deposit",
            account_id=account1.id
        ))

        txn_list.append(Transaction(
            transaction_type="debit",
            amount=850,
            description="Swiggy Order Food",
            account_id=account1.id
        ))

        txn_list.append(Transaction(
            transaction_type="credit",
            amount=15000,
            description="Salary credited",
            account_id=account2.id
        ))

        txn_list.append(Transaction(
            transaction_type="debit",
            amount=2300,
            description="Amazon Electronics",
            account_id=account2.id
        ))

        amount = 2000

        txn_list.append(Transaction(
            transaction_type="debit",
            amount=amount,
            description=f"Transfer to {account2.account_number}",
            account_id=account1.id
        ))

        txn_list.append(Transaction(
            transaction_type="credit",
            amount=amount,
            description=f"Received from {account1.account_number}",
            account_id=account2.id
        ))

        for t in txn_list:
            db.session.add(t)
        db.session.commit()

        for acc in [account1, account2]:
            txns = Transaction.query.filter_by(account_id=acc.id).all()
            balance = 0
            for txn in txns:
                if txn.transaction_type == 'credit':
                    balance += txn.amount
                else:
                    balance -= txn.amount
            acc.balance = balance
        db.session.commit()

        return jsonify({
            "message": "Dummy transactions created successfully!",
            "user1_id": customer1.id,
            "user2_id": customer2.id,
            "user1_account": account1.account_number,
            "user2_account": account2.account_number
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@app.route('/data_add', methods=['GET', 'POST'])
def create_dummy_txn():
    return create_dummy_transactions()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

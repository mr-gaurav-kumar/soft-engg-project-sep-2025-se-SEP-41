# Database Tables Used by Chatbot

## Endpoint: `/api/chat` (POST)

The chatbot endpoint queries the following database tables to fetch customer information and provide context-aware responses.

## Tables Queried

### 1. **customers** table
**Query Location:** Line 1979 in `app.py`
```python
customer = Customer.query.get(user_id)
```

**Fields Used:**
- `id` - Customer ID (primary key, used for lookup)
- `full_name` - Customer's full name (displayed in context)

**Purpose:** Retrieves customer personal information to personalize the chatbot response.

---

### 2. **accounts** table
**Query Location:** Line 1978 in `app.py`
```python
account = Account.query.filter_by(customer_id=user_id).first()
```

**Fields Used:**
- `customer_id` - Foreign key to link with customer (used for filtering)
- `account_number` - Account number (displayed in context)
- `account_type` - Type of account (e.g., 'savings') (displayed in context)
- `balance` - Current account balance (displayed in context)
- `id` - Account ID (used to link with transactions)

**Purpose:** Retrieves account details including balance and account information to provide account-specific responses.

---

### 3. **transactions** table
**Query Location:** Lines 1993-1995 in `app.py`
```python
txns = Transaction.query.filter_by(account_id=account.id)\
       .filter(Transaction.transaction_type == 'debit')\
       .order_by(Transaction.timestamp.desc()).limit(30).all()
```

**Fields Used:**
- `account_id` - Foreign key to link with account (used for filtering)
- `transaction_type` - Type of transaction (filtered for 'debit' only)
- `timestamp` - Transaction timestamp (used for ordering, most recent first)
- `description` - Transaction description (displayed in context)
- `amount` - Transaction amount (displayed in context)

**Query Filters:**
- Filters by `account_id` to get transactions for the specific account
- Filters by `transaction_type == 'debit'` to get only debit transactions
- Orders by `timestamp` in descending order (most recent first)
- Limits to 30 most recent transactions

**Purpose:** Retrieves recent spending history to provide spending insights and answer transaction-related queries.

---

## Context Data Structure

The chatbot combines data from these tables into a context string that is passed to the AI model:

```
Customer Name: {customer.full_name}
Account Number: {account.account_number}
IFSC Code: GIRO0001 (GIROBANK Main Branch)
Account Type: {account.account_type}
Current Balance: Rs. {account.balance}

Recent Transactions: {transaction1.description} (Rs. {transaction1.amount}), {transaction2.description} (Rs. {transaction2.amount}), ...
```

## Query Flow

1. **Input:** Receives `user_id` from request JSON
2. **Step 1:** Query `accounts` table using `customer_id = user_id`
3. **Step 2:** Query `customers` table using `id = user_id`
4. **Step 3:** If both queries succeed, query `transactions` table using `account_id = account.id`
5. **Step 4:** Filter transactions for debit type only
6. **Step 5:** Order by timestamp descending and limit to 30 records
7. **Step 6:** Combine all data into context string
8. **Step 7:** Pass context to AI model for response generation

## Guest Mode

If `user_id` is not provided or is null, the chatbot operates in guest mode with the context:
```
"User is a guest (No ID provided)."
```

In guest mode, no database tables are queried.


# E-WASTE AI — Finance & Accounting Database

Covers **Module 10 (Finance & Accounting — 13 Tables)** in `backend/models/erp_finance_env_ai_audit.py` and `FinanceLedgerService` in `backend/services/erp_operations_service.py`.

---

## 1. Accounting Tables

| Table | Role |
|-------|------|
| `financial_periods` | Fiscal period boundaries per company and financial year |
| `chart_of_accounts` | Company-scoped Asset, Liability, Equity, Revenue, Expense accounts |
| `accounting_vouchers` | Voucher headers linking operational documents to ledger postings |
| `journal_entries` | Double-entry headers (`total_debit`, `total_credit`, `is_balanced`, `is_posted`, `is_audited_statement`) |
| `journal_entry_lines` | Account-level debit and credit lines (`company_id` verified against COA) |
| `expense_categories` & `expenses` | Labour, electricity, maintenance, processing, and overhead expenses |
| `income_records` | Recovered material revenue and ancillary income logs |
| `purchase_payments` & `sales_receipts` | Payables settlements and receivables receipts |
| `tax_records` | GST/VAT and transaction tax records |
| `bank_transactions` & `cash_transactions` | Treasury payment/receipt movements |

---

## 2. Double-Entry Validation & Operational Reporting Safeguards

1. **Balanced Ledger Enforcement (`FinanceLedgerService.create_journal_entry`):**
   - Rejects entries with fewer than 2 lines or `total_debit <= 0`.
   - Rejects unbalanced entries (`abs(total_debit - total_credit) > 1e-4`) before insert (`Unbalanced journal entry rejected`).
   - Verifies every line's `account_id` belongs to the posting `company_id` to prevent cross-tenant journal contamination.
2. **Non-Audited Disclosure:**
   - Every `JournalEntry` explicitly stores `is_audited_statement = False` unless explicitly verified offline outside software.
   - **Report 9 (`profit_and_loss_summary`)** returns `"is_audited_statement": False` alongside the notice: *"Operational database ledger summary only — NOT an audited statutory financial statement."*
3. **Restricted Access:**
   - All finance endpoints (`/api/v1/erp/finance/*`) and financial reports (**Reports 8 & 9**) require `require_erp_permission(..., financial=True)` — blocking non-finance operators with `HTTP 403`.

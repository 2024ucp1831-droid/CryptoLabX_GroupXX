# Password Manager - Test Cases

## 1. Introduction

The Password Manager is a simple Python application that stores usernames, website names, and passwords. The application is intentionally implemented with security weaknesses for the purpose of demonstrating vulnerability identification and SAST analysis.

The following test cases verify the core functionality and demonstrate the assigned vulnerabilities.

---

## 2. Test Case 1 - Add Password

**Objective:** Verify that a username, website, and password can be stored.

**Steps:**

1. Run the application using `python3 password_manager.py`.
2. Select option `1 - Add Password`.
3. Enter a username.
4. Enter a website.
5. Enter a password.

**Expected Result:**

The application should display:

`Password saved successfully.`

**Actual Result:**

The password is successfully stored in the database.

**Status:** PASS

---

## 3. Test Case 2 - Verify Plaintext Password Storage

**Objective:** Demonstrate the insecure storage vulnerability.

**Steps:**

1. Add a password using the application.
2. Exit the application.
3. Open the SQLite database.
4. Execute:

`SELECT * FROM passwords;`

**Expected Result:**

The stored password should be visible directly in the database.

**Actual Result:**

The username, website, and password are stored as plaintext.

**Security Issue:** Insecure Storage

**Status:** VULNERABLE / PASS

---

## 4. Test Case 3 - View Stored Passwords Without Authentication

**Objective:** Demonstrate the missing authentication vulnerability.

**Steps:**

1. Start the Password Manager.
2. No login or authentication is requested.
3. Select option `2 - View Passwords`.

**Expected Result:**

The application should require authentication before displaying stored credentials.

**Actual Result:**

The application immediately displays the stored usernames, websites, and passwords without asking the user to authenticate.

**Security Issue:** Missing Authentication

**Status:** VULNERABLE / PASS

---

## 5. Test Case 4 - Information Leakage

**Objective:** Demonstrate that sensitive information is exposed through the application output.

**Steps:**

1. Start the Password Manager.
2. Select `2 - View Passwords`.
3. Observe the terminal output.

**Expected Result:**

Passwords should not be displayed in plaintext.

**Actual Result:**

The application displays the password directly in the terminal.

Example:

`Username: testuser`

`Website: gmail.com`

`Password: MySecret123`

**Security Issue:** Information Leakage

**Status:** VULNERABLE / PASS

---

## 6. Test Case 5 - Search Password

**Objective:** Verify that a stored password can be searched using the website name.

**Steps:**

1. Start the application.
2. Select option `3 - Search Password`.
3. Enter a website that has previously been stored.

**Expected Result:**

The corresponding username, website, and password are displayed.

**Actual Result:**

The matching credentials are displayed.

**Security Observation:**

The password is exposed in plaintext during the search operation.

**Status:** PASS / VULNERABLE

---

## 7. Test Case 6 - SAST Analysis Using Bandit

**Objective:** Perform static security analysis of the Python source code.

**Steps:**

1. Navigate to the `sast` directory.
2. Run Bandit against the source directory.
3. Save the results to the SAST report.

Command:

`bandit -r ../src/ -f txt -o bandit_report.txt`

**Expected Result:**

Bandit should analyze the Python source code and report any security issues covered by its security rules.

**Actual Result:**

Bandit generates a security analysis report containing the detected findings.

**Status:** PASS

---

## 8. Test Case Summary

| Test Case | Purpose                       | Result            |
| --------- | ----------------------------- | ----------------- |
| TC-01     | Add password                  | PASS              |
| TC-02     | Verify plaintext storage      | VULNERABLE        |
| TC-03     | Verify missing authentication | VULNERABLE        |
| TC-04     | Verify information leakage    | VULNERABLE        |
| TC-05     | Search password               | PASS / VULNERABLE |
| TC-06     | Run Bandit SAST scan          | PASS              |

## 9. Conclusion

The test cases successfully demonstrate the core functionality of the Password Manager and the intentionally introduced security vulnerabilities. Bandit is used to perform static analysis of the Python source code. Manual testing is also required because not every application-level vulnerability, such as missing authentication, is necessarily detected by Bandit's rule-based analysis.


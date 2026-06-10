# Test Cases – Bridge Automation Framework

This folder contains **all test case lists** for each module of the Bridge portal.
Each file follows the same structure so it is easy to review, prioritise, and track automation status.

## Folder Structure

```
test_cases/
├── README.md                   ← This file
├── home_page_test_cases.md     ← Home Page test cases
├── registration_test_cases.md  ← (coming soon)
├── eservices_test_cases.md     ← (coming soon)
└── dashboard_test_cases.md     ← (coming soon)
```

## Columns Explained

| Column | Meaning |
|---|---|
| **TC ID** | Unique ID per test case, e.g. `HP-001` |
| **Test Case Name** | Short human-readable name |
| **Description** | What is being validated |
| **Priority** | `High / Medium / Low` |
| **Status** | `To Automate / Skipped / Automated / In Progress` |
| **Script Location** | Path to the pytest file once implemented |
| **Notes** | Any special setup, dependency, or reason for skipping |

## How to Use

1. Add rows to the relevant `*_test_cases.md` file.
2. Set **Priority** = `Low` + **Status** = `Skipped` for test cases you want to defer.
3. Set **Status** = `Automated` and fill in **Script Location** once the script is written.

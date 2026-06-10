# Test Scenarios: Subject Matter Expert (SME) Evaluation

## Positive Scenarios
| ID | Description |
|---|---|
| TS_SME_01 | Successfully login to the backend with SME/Superadmin credentials. |
| TS_SME_02 | Navigate to the **TMA Manager** module. |
| TS_SME_03 | Filter and locate assignments pending for evaluation. |
| TS_SME_04 | Verify the student's submitted assignment document (Download/View). |
| TS_SME_05 | Enter valid marks and save the evaluation. |
| TS_SME_06 | Verify the student's status updates correctly once evaluated. |

## Negative Scenarios
| ID | Description |
|---|---|
| TS_SME_07 | Enter marks exceeding the specified 'Max Marks' (e.g., 101/100). |
| TS_SME_08 | Attempt to save evaluation without awarding any marks. |
| TS_SME_09 | Attempt to award negative marks (e.g., -5). |
| TS_SME_10 | Award decimals when the system expects integers (e.g., 20.5). |
| TS_SME_11 | Verify if a finalized evaluation can be improperly modified. |

## UI/UX Scenarios
| ID | Description |
|---|---|
| TS_SME_12 | Verify clear visibility of student info and subject code. |
| TS_SME_13 | Verify ease of navigating through the list of pending assignments. |

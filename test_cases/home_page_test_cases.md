# Home Page – Test Cases

> **How to use:**
> - Change `Status` to `Skipped` for low-priority / not-so-important test cases you want to drop.
> - Change `Status` to `Automated` once the pytest script is written and link the script path.
> - `Priority` guide → `High` = must automate | `Medium` = nice to have | `Low` = skip for now

---

## Legend

| Status Value | Meaning |
|---|---|
| `To Automate` | Approved for automation, script not written yet |
| `In Progress` | Script being written |
| `Automated` | Script written and passing |
| `Skipped` | Decided NOT to automate (reason in Notes) |

---

## Test Cases

| TC ID | Test Scenario | Preconditions | Test Steps | Expected Result | Test Type | Priority | Status | Script Location | Notes |
|---|---|---|---|---|---|---|---|---|---|
| TC_HP_001 | Verify Home button navigation | User on internal page | Click Home button | User redirected to homepage | Functional | High | To Automate | | |
| TC_HP_002 | Verify Enroll Now button | User on homepage | Click Enroll Now | Registration page opens | Functional | High | To Automate | | |
| TC_HP_003 | Verify Proceed button in instruction popup | Instruction popup visible | Click Proceed | Workflow moves to next step | Functional | High | To Automate | | |
| TC_HP_004 | Verify Read More under Eligibility section | User on homepage | Click Read More | Eligibility PDF opens/downloads | Functional | Medium | To Automate | | |
| TC_HP_005 | Verify Learn More in Course tiles | User on homepage | Click Learn More on each tile | Relevant chapter/resource opens | Functional | High | To Automate | | |
| TC_HP_006 | Verify Download Self Certificate button | User on homepage | Click Download Self Certificate | Valid certificate file downloads | Functional | High | To Automate | | |
| TC_HP_007 | Verify Exams & Results dropdown links | User on homepage | Click Exam Schedule, Fee, Result | Respective page opens or Coming Soon tooltip | Functional | Medium | To Automate | | |
| TC_HP_008 | Verify Teacher Corner links | User on homepage | Click e-Service & e-Resources | Respective page opens or Coming Soon tooltip | Functional | Medium | To Automate | | |
| TC_HP_009 | Verify Important Links dropdown | User on homepage | Click FAQ, Announcements, Reports | Respective page opens | Functional | Medium | To Automate | | |
| TC_HP_010 | Verify Footer Quick Links | User on homepage | Click Home, Contact Us, Terms & Conditions | Respective page opens | Functional | Medium | To Automate | | |
| TC_HP_011 | Verify Footer Other Links | User on homepage | Click Privacy Policy, Accessibility, Sitemap | Respective page opens | Functional | Medium | To Automate | | |
| TC_HP_012 | Validate comma spacing in headings | User on Course Details page | Check heading text formatting | Proper spacing after commas | UI | Low | Skipped | | UI text validation – manual review preferred |
| TC_HP_013 | Validate spelling errors | User on Course Details page | Review content text | No spelling mistakes | UI | Low | Skipped | | UI text validation – manual review preferred |
| TC_HP_014 | Validate punctuation usage | User on homepage | Review sentence endings | Sentences end with full stop | UI | Low | Skipped | | UI text validation – manual review preferred |
| TC_HP_015 | Validate Important Videos title case consistency | User on homepage | Check video titles formatting | Consistent camel case format | UI | Low | Skipped | | UI text validation – manual review preferred |
| TC_HP_016 | Validate Important Videos tile alignment | User on homepage | Check tile layout alignment | Tiles evenly aligned | UI | Medium | To Automate | | Visual/layout check |
| TC_HP_017 | Validate Latest News alignment | User on homepage | Check bullet alignment | Uniform alignment & spacing | UI | Medium | To Automate | | Visual/layout check |
| TC_HP_018 | Validate Admission Details image relevance | User on homepage | Check displayed image | Relevant admission image displayed | UI | Low | Skipped | | Subjective check – not suitable for automation |
| TC_HP_019 | Verify Accessibility popup opens | User on homepage | Click accessibility icon | Popup opens correctly | Functional | High | To Automate | | |
| TC_HP_020 | Verify Screen Reader button functionality | Accessibility popup open | Click Screen Reader button | Screen reader toggles properly | Functional | High | To Automate | | |
| TC_HP_021 | Validate homepage idle stability | User on homepage | Leave page idle for 10 seconds | No flicker or auto refresh | Performance | High | To Automate | | Simple wait + stability check |
| TC_HP_022 | Validate mobile slider readability | Open site in mobile view | Check slider text size | Readable without zoom | UI/Mobile | High | To Automate | | Use Chrome mobile emulation |
| TC_HP_023 | Validate mobile eligibility font size | Open site in mobile view | Check eligibility & objectives text | Readable font size | UI/Mobile | High | To Automate | | Use Chrome mobile emulation |
| TC_HP_024 | Validate mobile recent announcement alignment | Open site in mobile view | Check notification alignment | Uniform alignment | UI/Mobile | Medium | To Automate | | Use Chrome mobile emulation |
| TC_HP_025 | Validate mobile Important Dates alignment | Open site in mobile view | Check list alignment | Consistent spacing & indentation | UI/Mobile | Medium | To Automate | | Use Chrome mobile emulation |
| TC_HP_026 | Validate SEO meta tags implementation | User inspects page source | Check title, meta description, keywords | Relevant SEO tags implemented | SEO | Medium | To Automate | | Read page source / head tags |

---

## Summary

| Priority | Total | To Automate | Skipped |
|---|---|---|---|
| High | 10 | 10 | 0 |
| Medium | 11 | 10 | 1 |
| Low | 5 | 0 | 5 |
| **Total** | **26** | **20** | **6** |

---

*Last Updated: 2026-02-28*

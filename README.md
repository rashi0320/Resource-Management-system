Usage & Billing System for a Resource

A Python-based CLI application designed to manage shared resources (e.g., meeting rooms, workstations, gym equipment), handle real-time capacity restrictions, and compute bills based on duration and custom pricing rules.

---

1. Overview & Logic Approach

- **Data Models**: 
  - `Resource`: Represents entities with properties like `capacity`, `first_hour_rate`, and `additional_hour_rate`. Holds current active sessions in an in-memory dictionary.
  - `BillingSystem`: Acts as a controller to register and access resources.
- **Capacity Management**: Prior to granting access to a user, the system checks whether the active sessions count is less than the resource capacity. If maximum capacity is reached, the request is rejected.
- **Pricing & Billing Rules**:
  - Duration is calculated by finding the difference between `start_time` and `end_time`.
  - Usage time is rounded up to the next complete hour (e.g., 1 hour 20 minutes is billed as 2 hours).
  - Bill Calculation Formula: `Total = First Hour Rate + (Billed Hours - 1) * Additional Hour Rate`.

---

2. Technical Assumptions

- Times are tracked in 24-hour / 12-hour timestamps using standard datetime modules.
- Minimum usage charge corresponds to 1 hour upon starting a session.
- Storage is managed in-memory as permitted by assignment guidelines (no external database or heavy frameworks required).

---

3. How to Run and Test

1. Ensure Python 3.x is installed.
2. Clone this repository and open it in VS Code:
   ```bash
   git clone <your-github-repo-link>
   cd <repo-folder

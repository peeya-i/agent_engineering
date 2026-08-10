# 🧪 Python Unit Testing & Dependency Mocking Laboratory

This directory contains a complete demonstration of unit testing, business logic validation, boundary condition checks, and external dependency mocking using Python's built-in `unittest` and `unittest.mock` libraries.

---

## 🎯 Purpose & Key Objectives

The `mock-unit-test` project demonstrates how to decouple core business logic from external dependencies (such as databases and third-party payment APIs like Stripe or PayPal) during automated testing. 

Key patterns demonstrated:
1. **Dependency Injection**: Injecting mock implementations of external services (`InventoryService` and `PaymentGateway`) into the `Order` service class.
2. **Interface Mocking**: Utilizing `unittest.mock.MagicMock` to stub return values, simulate network errors, and track call histories (`assert_called_once_with`, `assert_has_calls`).
3. **Boundary & Edge Case Testing**: Validating floating-point precision, discount thresholds ($100.00 vs $100.01), VIP pricing tiers, zero-priced items, and multi-item stock shortage rollbacks.
4. **Custom Exception Handling**: Testing domain-specific errors (`InventoryShortageError`, `PaymentFailedError`, `InvalidOrderError`).

---

## 📁 Directory Structure & File Overview

```text
mock-unit-test/
├── order_service.py        # Core e-commerce business logic & interface definitions
├── test_order_service.py   # Unit test suite with 23 test cases & mock verification
└── README.md               # Documentation & usage guide
```

### 1. [`order_service.py`](file:///home/pi-net/Documents/agent_eng_labs/agent_engineering/my-work/class-02/agy2-pprojects/mock-unit-test/order_service.py)
Implements the domain models and checkout orchestrator:
- **`Order`**: Manages cart items, calculates gross price, applies discount rules (VIP 20% flat discount vs Regular customer 10% discount over $100), and orchestrates checkout.
- **`InventoryService` & `PaymentGateway`**: Abstract interfaces raising `NotImplementedError` to represent external infrastructure.
- **Custom Exceptions**: `InventoryShortageError`, `PaymentFailedError`, `InvalidOrderError`.

### 2. [`test_order_service.py`](file:///home/pi-net/Documents/agent_eng_labs/agent_engineering/my-work/class-02/agy2-pprojects/mock-unit-test/test_order_service.py)
A test suite containing 23 unit tests across 4 key test suites:
- **Item Management**: Adding items, price validation, quantity increments, cart removal.
- **Pricing & Discounts**: Regular vs. VIP pricing, boundary checks ($100 exact boundary), floating-point rounding precision.
- **Mock Verification**: Verifying that `PaymentGateway.charge()` is called with exact expected amounts, and `InventoryService.decrement_stock()` is only invoked upon payment success.
- **Failure & Rollback Conditions**: Aborting checkout on stock shortage or payment decline without executing stock reduction.

---

## 🚀 How to Run the Unit Test Suite

Execute the tests directly using Python's built-in test runner:

```bash
python3 -m unittest test_order_service.py -v
```

### Expected Output:
```text
Ran 23 tests in 0.039s

OK
```

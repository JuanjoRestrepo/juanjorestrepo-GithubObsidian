# Programming Concepts — Foundations Every Engineer Must Know

**Sources:** Robert C. Martin, *Clean Code* (Prentice Hall, 2008); Robert C. Martin,
*The Clean Coder* (Prentice Hall, 2011); Erich Gamma, Richard Helm, Ralph Johnson, John
Vlissides (*Gang of Four*), *Design Patterns: Elements of Reusable Object-Oriented Software*
(Addison-Wesley, 1994); Thomas H. Cormen et al., *Introduction to Algorithms* (MIT Press,
4th ed. 2022) — CLRS; Niklaus Wirth, *Algorithms + Data Structures = Programs* (1976);
Brian W. Kernighan & Dennis M. Ritchie, *The C Programming Language* (1978) — foundational;
Kyle Simpson, *You Don't Know JS* series (O'Reilly, 2014–2020); David Thomas & Andrew Hunt,
*The Pragmatic Programmer* (Addison-Wesley, 20th Anniversary ed. 2019); Grady Booch,
*Object-Oriented Analysis and Design with Applications* (Addison-Wesley, 3rd ed. 2007).

---

## 1. Variables, Data Types & Memory

### Variables and Scope

A **variable** is a named binding that maps an identifier to a memory location. Its behaviour
depends on scope (where it's visible) and lifetime (when it exists). Misunderstanding these
is the source of the majority of beginner bugs.

```typescript
// Scope types in JavaScript/TypeScript
var x = 1;    // function-scoped, hoisted — avoid in modern code
let y = 2;    // block-scoped — prefer for mutable bindings
const z = 3;  // block-scoped, cannot be reassigned — prefer for all immutable bindings

function outer() {
  const a = "outer";

  function inner() {
    const b = "inner";
    console.log(a);  // ✅ Closure: inner can access outer's scope
    console.log(b);  // ✅ Own scope
  }

  // console.log(b);  // ❌ ReferenceError: b is not defined in outer scope
}
```

```python
# Python scope — LEGB rule: Local → Enclosing → Global → Built-in
x = "global"

def outer():
    x = "enclosing"

    def inner():
        # x = "local"  # would shadow enclosing
        print(x)  # prints "enclosing" — reads enclosing scope

    inner()
```

### Primitive vs Reference Types

```typescript
// Primitive types: passed by value — copies are independent
let a = 5;
let b = a;
b = 10;
console.log(a);  // 5 — unchanged

// Reference types (objects, arrays): passed by reference — mutations affect original
const arr1 = [1, 2, 3];
const arr2 = arr1;     // arr2 points to same array
arr2.push(4);
console.log(arr1);     // [1, 2, 3, 4] — mutation visible through arr1

// Defensive copy when immutability required:
const arr3 = [...arr1];  // shallow copy — top-level elements are independent
arr3.push(5);
console.log(arr1);       // [1, 2, 3, 4] — arr1 unaffected
```

### Stack vs Heap

```
Stack: fixed-size, LIFO, automatic allocation/deallocation, function call frames
  → Local variables, function arguments, return addresses
  → Fast allocation (just move stack pointer)
  → Stack overflow: too many nested function calls (infinite recursion)

Heap: dynamic, manually managed (C/C++) or garbage-collected (Python, JS, Java)
  → Objects, closures, dynamically-sized data structures
  → Slower allocation (requires finding free block)
  → Memory leak: references held to unreachable objects prevent GC
```

---

## 2. Functions — First-Class Citizens

Functions are the primary abstraction unit. They should do one thing, do it well, and do
it only. Martin's *Clean Code*: "The first rule of functions is that they should be small.
The second rule of functions is that they should be smaller than that."

### Higher-Order Functions (Functions as Values)

```typescript
// Functions can be passed as arguments (callbacks), returned from other functions, stored in variables
const numbers = [1, 2, 3, 4, 5];

const doubled   = numbers.map(n => n * 2);          // [2, 4, 6, 8, 10]
const evens     = numbers.filter(n => n % 2 === 0); // [2, 4]
const sum       = numbers.reduce((acc, n) => acc + n, 0); // 15

// Returning a function — closure captures outer variables
function multiplier(factor: number) {
  return (n: number) => n * factor;  // inner function closes over `factor`
}
const triple = multiplier(3);
console.log(triple(7));  // 21
```

```python
from functools import reduce

numbers = [1, 2, 3, 4, 5]
doubled = list(map(lambda n: n * 2, numbers))           # [2, 4, 6, 8, 10]
evens   = list(filter(lambda n: n % 2 == 0, numbers))   # [2, 4]
total   = reduce(lambda acc, n: acc + n, numbers, 0)    # 15

# List comprehension (Pythonic alternative to map/filter):
doubled = [n * 2 for n in numbers]
evens   = [n for n in numbers if n % 2 == 0]
```

### Pure Functions and Side Effects

A **pure function** always returns the same output for the same input and has no side effects
(does not read or write state outside its parameters). Pure functions are trivially testable,
parallelisable, and memoizable.

```typescript
// ✅ Pure function — no external state read/write
function add(a: number, b: number): number {
  return a + b;
}

// ❌ Impure — reads external state, different output for same input
let counter = 0;
function incrementAndGet(): number {
  return ++counter;  // side effect + reads external state
}

// ✅ Make it pure — pass state in, return new state out
function incrementAndGet(counter: number): number {
  return counter + 1;
}
```

---

## 3. Object-Oriented Programming (OOP)

The four pillars, and why each matters beyond the definition:

### Encapsulation — Hide Implementation Detail

Encapsulation bundles data and the methods that operate on it, and restricts direct access
to internal state. It's not about getters and setters — it's about protecting invariants.

```typescript
class BankAccount {
  private balance: number;  // private — cannot be set directly from outside

  constructor(initialBalance: number) {
    if (initialBalance < 0) throw new Error("Initial balance cannot be negative");
    this.balance = initialBalance;
  }

  deposit(amount: number): void {
    if (amount <= 0) throw new Error("Deposit must be positive");
    this.balance += amount;
  }

  withdraw(amount: number): void {
    if (amount > this.balance) throw new Error("Insufficient funds");
    this.balance -= amount;
  }

  getBalance(): number { return this.balance; }
  // The internal representation (could be cents, could be a BigDecimal) is hidden
}
```

### Abstraction — Expose What Matters, Hide What Doesn't

Abstraction reduces complexity by hiding implementation behind a stable interface.
Users of a class or module shouldn't need to know how it works, only what it does.

```python
# Abstract base class defines the interface contract
from abc import ABC, abstractmethod

class NotificationSender(ABC):
    @abstractmethod
    def send(self, recipient: str, message: str) -> bool: ...

# Concrete implementations hide their complexity
class EmailSender(NotificationSender):
    def send(self, recipient: str, message: str) -> bool:
        # SMTP complexity, retry logic, template rendering — all hidden here
        ...

class SlackSender(NotificationSender):
    def send(self, recipient: str, message: str) -> bool:
        # Slack API calls, OAuth handling — hidden here
        ...

# User code operates on the abstraction — doesn't know or care which transport
def notify_user(sender: NotificationSender, user_email: str, msg: str) -> None:
    sender.send(user_email, msg)
```

### Inheritance — Extending Behaviour

Inheritance creates an "is-a" relationship: a `Dog` is an `Animal`. It allows shared
behaviour to live in one place (the parent) rather than being duplicated.

**Prefer composition over inheritance** (Gang of Four, Design Patterns, 1994): inheritance
creates tight coupling between parent and child; a change to the parent can break all
children in unexpected ways. Use inheritance for genuine "is-a" relationships; use
composition ("has-a") for behaviour reuse.

```typescript
// ❌ Inheritance where composition is better:
class Logger extends Array { ... }  // Logger is-a Array? No. It uses an array internally.

// ✅ Composition — Logger has-a storage mechanism
class Logger {
  private entries: string[] = [];  // "has-a" relationship
  log(msg: string): void { this.entries.push(msg); }
}
```

### Polymorphism — Same Interface, Different Behaviour

Polymorphism allows the same interface to drive different behaviour at runtime:

```typescript
// Subtype polymorphism — method dispatch based on runtime type
abstract class Shape {
  abstract area(): number;
}

class Circle extends Shape {
  constructor(private radius: number) { super(); }
  area(): number { return Math.PI * this.radius ** 2; }
}

class Rectangle extends Shape {
  constructor(private w: number, private h: number) { super(); }
  area(): number { return this.w * this.h; }
}

// Code that works with any Shape — doesn't need to know the concrete type
function totalArea(shapes: Shape[]): number {
  return shapes.reduce((sum, shape) => sum + shape.area(), 0);
}

totalArea([new Circle(5), new Rectangle(3, 4)]);  // 78.54 + 12 = 90.54
```

---

## 4. SOLID Principles

Robert C. Martin's five principles of OOP design. Each addresses a specific class of design
problem; applying all five produces code that is easier to extend and harder to break.

**S — Single Responsibility Principle (SRP):**
A class should have only one reason to change. "Reason to change" = stakeholder/actor.
If your `User` class handles authentication, database persistence, and email sending, it has
three reasons to change — split it into three classes.

**O — Open/Closed Principle (OCP):**
Open for extension, closed for modification. Add new behaviour by adding new code (a new
subclass, a new strategy), not by editing existing code that already works.

**L — Liskov Substitution Principle (LSP):**
Subtypes must be substitutable for their base types without altering program correctness.
The classic violation: a `Square` class extending `Rectangle` that overrides `setWidth` to
also set height — now `setWidth` has different semantics in the subtype. Code expecting a
`Rectangle` breaks when given a `Square`.

**I — Interface Segregation Principle (ISP):**
No client should be forced to depend on interfaces it doesn't use. Prefer many small, focused
interfaces over one large, general-purpose interface. A `Printer` interface with `print()`,
`scan()`, `fax()` forces a dumb printer to implement `scan()` and `fax()` as stubs.

**D — Dependency Inversion Principle (DIP):**
High-level modules should not depend on low-level modules — both should depend on
abstractions. This is the architectural foundation of Ports & Adapters / Hexagonal
Architecture (see `references/clean-hexagonal-onion.md`).

```typescript
// ❌ DIP violation — high-level OrderService depends on low-level PostgresDB
class OrderService {
  private db = new PostgresDB();  // concrete, not abstract
  createOrder(order: Order) { this.db.insert(order); }
}

// ✅ DIP applied — OrderService depends on the abstraction OrderRepository
interface OrderRepository { save(order: Order): Promise<void>; }

class OrderService {
  constructor(private repo: OrderRepository) {}  // depends on interface
  async createOrder(order: Order) { await this.repo.save(order); }
}

// Wired at the composition root:
const service = new OrderService(new PostgresOrderRepository(db));
```

---

## 5. Fundamental Design Patterns (Gang of Four)

The GoF classified 23 patterns into three categories. Below are the most-encountered in
production code — understand these before the rarer ones.

### Creational Patterns

**Singleton** — ensure only one instance exists:
```typescript
class Config {
  private static instance: Config;
  private constructor(private values: Record<string, string>) {}

  static getInstance(): Config {
    if (!Config.instance) Config.instance = new Config(process.env as any);
    return Config.instance;
  }
}
// ⚠️ Singletons make testing hard (global state) — prefer dependency injection
```

**Factory Method** — delegate object creation to a method that subclasses can override:
```typescript
abstract class Notification {
  abstract send(message: string): void;
  static create(type: "email" | "sms"): Notification {
    return type === "email" ? new EmailNotification() : new SMSNotification();
  }
}
```

**Builder** — construct complex objects step-by-step:
```typescript
const query = new QueryBuilder()
  .table("orders")
  .where("status", "shipped")
  .orderBy("created_at", "DESC")
  .limit(20)
  .build();  // returns the final Query object
```

### Structural Patterns

**Adapter** — translate one interface to another:
```typescript
// Third-party library returns { lat, lng }; your code expects { latitude, longitude }
class CoordinateAdapter {
  adapt(coord: { lat: number; lng: number }) {
    return { latitude: coord.lat, longitude: coord.lng };
  }
}
```

**Decorator** — add behaviour without modifying the original class:
```typescript
// Wrap a function with logging — same interface, additional behaviour
function withLogging<T extends unknown[], R>(
  fn: (...args: T) => R,
  name: string,
): (...args: T) => R {
  return (...args) => {
    console.time(name);
    const result = fn(...args);
    console.timeEnd(name);
    return result;
  };
}
const timedFetch = withLogging(fetch, "fetch");
```

**Proxy** — control access to another object (lazy init, access control, caching):
```typescript
// Lazy-loading proxy: only creates the expensive object when first accessed
class LazyImageProxy {
  private realImage: RealImage | null = null;
  display(): void {
    if (!this.realImage) this.realImage = new RealImage(this.path);  // lazy init
    this.realImage.display();
  }
}
```

### Behavioural Patterns

**Observer** — notify dependents when state changes (event system):
```typescript
class EventEmitter<T> {
  private listeners: ((data: T) => void)[] = [];
  on(listener: (data: T) => void) { this.listeners.push(listener); }
  emit(data: T) { this.listeners.forEach(l => l(data)); }
}
const orderEvents = new EventEmitter<Order>();
orderEvents.on(order => sendConfirmationEmail(order));
orderEvents.on(order => updateInventory(order));
```

**Strategy** — encapsulate algorithms and make them interchangeable:
```typescript
type SortStrategy = (arr: number[]) => number[];
const quickSort: SortStrategy = arr => { /* ... */ return arr; };
const mergeSort: SortStrategy = arr => { /* ... */ return arr; };

class Sorter {
  constructor(private strategy: SortStrategy) {}
  sort(arr: number[]) { return this.strategy(arr); }
}
```

**Command** — encapsulate a request as an object (enables undo/redo, queuing):
```typescript
interface Command { execute(): void; undo(): void; }

class TextEditor {
  private history: Command[] = [];

  execute(cmd: Command) { cmd.execute(); this.history.push(cmd); }
  undo() { this.history.pop()?.undo(); }
}
```

---

## 6. Data Structures

The choice of data structure determines the time complexity of your operations. Choose
based on your access pattern, not familiarity.

| Structure | Access | Search | Insert | Delete | Use when |
|---|---|---|---|---|---|
| Array | O(1) | O(n) | O(n) | O(n) | Index-based access, cache-friendly iteration |
| Linked List | O(n) | O(n) | O(1) at head | O(1) with ref | Frequent insert/delete at head/tail, no random access needed |
| Stack | — | — | O(1) push | O(1) pop | LIFO: undo/redo, call stack, DFS |
| Queue | — | — | O(1) enqueue | O(1) dequeue | FIFO: BFS, task scheduling, event processing |
| Hash Map | — | O(1) avg | O(1) avg | O(1) avg | Key-value lookup — most frequently the right answer |
| BST (balanced) | — | O(log n) | O(log n) | O(log n) | Sorted data with frequent search/insert/delete |
| Heap | O(1) min/max | — | O(log n) | O(log n) | Priority queue: Dijkstra, task scheduling by priority |
| Trie | — | O(L) | O(L) | O(L) | Prefix search, autocomplete (L = string length) |
| Graph | — | O(V+E) | — | — | Relationships: social networks, routes, dependencies |

### Hash Maps — The Most Important Data Structure

```typescript
// A frequency counter — O(n) time using a hash map instead of O(n²) nested loops
function twoSum(nums: number[], target: number): [number, number] | null {
  const seen = new Map<number, number>();  // value → index
  for (let i = 0; i < nums.length; i++) {
    const complement = target - nums[i];
    if (seen.has(complement)) return [seen.get(complement)!, i];
    seen.set(nums[i], i);
  }
  return null;
}
// O(n) time, O(n) space — vs O(n²) brute force with nested loops
```

---

## 7. Algorithms and Big O Notation

**Big O notation** describes how an algorithm's time or space requirements grow as input
size grows. It's a worst-case upper bound — ignore constants and lower-order terms.

```
O(1)       — constant: hash map lookup, array access by index
O(log n)   — logarithmic: binary search, balanced BST operations
O(n)       — linear: scanning an array once, linear search
O(n log n) — linearithmic: efficient sorting (merge sort, heap sort, TimSort)
O(n²)      — quadratic: nested loops (bubble sort, naive string matching)
O(2ⁿ)      — exponential: recursive fibonacci without memoization, brute-force combinations
O(n!)      — factorial: generating all permutations
```

**Practical rule:** if your input is N = 10⁶ (1 million):
- O(n): 1M operations — fast (milliseconds)
- O(n log n): ~20M operations — acceptable
- O(n²): 10¹² operations — will not finish in your lifetime

### Recursion vs Iteration

Recursion expresses solutions that have natural self-similar structure (trees, divide-and-
conquer). Every recursive solution can be rewritten iteratively (using an explicit stack).

```typescript
// Recursive (natural, but O(n) call stack depth — stack overflow risk)
function factorial(n: number): number {
  if (n <= 1) return 1;              // base case — mandatory
  return n * factorial(n - 1);       // recursive case
}

// Tail-recursive (compiler-optimized in some runtimes)
function factorial(n: number, acc = 1): number {
  if (n <= 1) return acc;
  return factorial(n - 1, n * acc);  // result passed as accumulator
}

// Iterative (no stack overflow risk)
function factorial(n: number): number {
  let result = 1;
  for (let i = 2; i <= n; i++) result *= i;
  return result;
}
```

**Memoization** — cache recursive subproblem results (top-down dynamic programming):
```typescript
function fibonacci(n: number, memo = new Map<number, number>()): number {
  if (n <= 1) return n;
  if (memo.has(n)) return memo.get(n)!;  // cache hit — O(1)
  const result = fibonacci(n - 1, memo) + fibonacci(n - 2, memo);
  memo.set(n, result);
  return result;
}
// O(n) time with memoization vs O(2ⁿ) without it
```

---

## 8. Concurrency and Async Programming

### Concurrency vs Parallelism

```
Concurrency: dealing with multiple things at once (structure)
  → One CPU core, multiple tasks interleaved (time-slicing)
  → Node.js event loop: single-threaded but handles thousands of I/O operations concurrently

Parallelism: doing multiple things at once (execution)
  → Multiple CPU cores executing simultaneously
  → Python multiprocessing, Java threads, Rust async with a multi-threaded runtime
```

### The Event Loop (JavaScript/Node.js)

```typescript
console.log("1 — sync");

setTimeout(() => console.log("3 — macro-task"), 0);

Promise.resolve().then(() => console.log("2 — micro-task"));

console.log("4 — sync");

// Output: 1, 4, 2, 3
// Micro-tasks (Promise callbacks) drain before macro-tasks (setTimeout)
// Understanding this is essential for debugging async JavaScript
```

### async/await — Sequential Async Code

```typescript
// ❌ Sequentially awaiting unrelated operations (wastes time)
async function loadDashboard(userId: string) {
  const user   = await db.getUser(userId);    // 100ms
  const orders = await db.getOrders(userId);  // 100ms
  return { user, orders };                    // total: 200ms
}

// ✅ Parallel async with Promise.all (independent operations run concurrently)
async function loadDashboard(userId: string) {
  const [user, orders] = await Promise.all([
    db.getUser(userId),    // starts immediately
    db.getOrders(userId),  // starts immediately (not waiting for user)
  ]);                      // total: 100ms (max of both)
  return { user, orders };
}
```

### Race Conditions and Mutexes

A **race condition** occurs when the outcome depends on the order of interleaved concurrent
operations — non-deterministic and notoriously hard to debug.

```python
# ❌ Race condition: two coroutines reading-then-writing (non-atomic)
counter = 0

async def increment():
    global counter
    temp = counter       # read
    await asyncio.sleep(0)  # yield — another coroutine may run here
    counter = temp + 1   # write (may overwrite the other coroutine's increment)

# ✅ Use asyncio.Lock to serialize access to shared state
lock = asyncio.Lock()

async def increment_safe():
    global counter
    async with lock:     # only one coroutine enters at a time
        counter += 1
```

---

## 9. Code Quality Principles

### DRY, KISS, YAGNI

**DRY — Don't Repeat Yourself** (Thomas & Hunt, *The Pragmatic Programmer*):
Every piece of knowledge should have a single, unambiguous representation in the system.
Duplication of logic (not data) means a fix in one place must be replicated in N others —
the ones you forget become bugs.

**KISS — Keep It Simple, Stupid:**
The simplest solution that works is almost always the best one. Complexity is a cost, not
a feature. If you find yourself writing a clever solution, ask: will the next developer
understand this in 2 years? Would a simpler approach be 90% as good at 10% of the cost?

**YAGNI — You Aren't Gonna Need It:**
Don't implement something until you actually need it. Speculative generality is wasted
work that adds complexity for features that often never get built.

### Naming

Martin's rule: the length of a name should be proportional to the scope in which it's used.
Loop variable `i` in a 3-line loop is fine. A function called `process()` in a 500-line
module is not.

```typescript
// ❌ Misleading names
function d(a: any[], n: number): any[] { return a.slice(0, n); }

// ✅ Intent-revealing names
function getTopItems(items: Product[], count: number): Product[] {
  return items.slice(0, count);
}
```

### Functions Should Do One Thing

```typescript
// ❌ One function doing three things — hard to test, hard to change
function processOrder(orderId: string) {
  const order = db.find(orderId);    // data access
  order.status = "shipped";         // business logic
  db.save(order);                   // persistence
  emailService.send(order.email);   // side effect
}

// ✅ Separated concerns — each function has one responsibility, one reason to change
async function processOrder(orderId: string, repo: OrderRepo, notifier: Notifier) {
  const order = await repo.findById(orderId);
  const shipped = order.markAsShipped();    // domain logic returns new state
  await repo.save(shipped);
  await notifier.notifyShipped(shipped);
}
```

---

## 10. Debugging Techniques

### Systematic Debugging

```
1. Reproduce the bug reliably — if you can't reproduce it, you can't fix it
2. Reduce the test case — what is the minimum code that triggers the bug?
3. Read the error message fully — the answer is often in the message you skimmed
4. Check your assumptions — add logging/assertions to verify what you "know" is true
5. Binary search — if you don't know where the bug is, comment out half the code. Bug gone?
   → In the commented half. Bug still there? → In the other half. Repeat.
6. Rubber duck debugging — explain the code aloud, line by line; the bug often reveals itself
7. Check recent changes — git blame, git log; if it worked yesterday, what changed?
8. Read the documentation for the library/API you're calling — often the "bug" is misuse
```

### Debugging Tools

```typescript
// Strategic console.log — add context, not just values
console.log("[OrderService.processOrder] order:", JSON.stringify(order, null, 2));

// Assertion: fail loudly when invariants are violated
function withdraw(balance: number, amount: number): number {
  console.assert(amount > 0, "Withdrawal amount must be positive");
  console.assert(amount <= balance, "Insufficient balance");
  return balance - amount;
}

// Node.js debugger — breakpoints in VS Code or via --inspect
// node --inspect-brk index.js  → attach VS Code debugger for step-through debugging
```

---

## 11. Programming Paradigms

**Imperative:** describe how to do something step-by-step (C, early JavaScript).
**Declarative:** describe what you want, not how (SQL, React JSX, CSS).
**Object-Oriented (OOP):** model the world as interacting objects with state and behaviour.
**Functional (FP):** avoid mutable state; compose pure functions that transform data.
**Event-Driven:** program flow is determined by events (clicks, messages, I/O completions) —
central to Node.js, GUIs, and microservice event architectures.

Most modern languages (TypeScript, Python, Kotlin, Scala, Rust) are multi-paradigm — use
the right paradigm for the problem rather than dogmatically applying one. Functional
programming's emphasis on pure functions and immutable data makes concurrent code
dramatically safer; OOP's encapsulation and inheritance model domain hierarchies naturally.

```typescript
// Functional style — compose small pure functions
const processData = (data: number[]) =>
  data
    .filter(n => n > 0)           // only positive
    .map(n => n * 2)              // double
    .reduce((sum, n) => sum + n, 0);  // sum

// OOP style — same logic, different expression
class DataProcessor {
  constructor(private data: number[]) {}
  filtered() { return this.data.filter(n => n > 0); }
  doubled() { return this.filtered().map(n => n * 2); }
  sum() { return this.doubled().reduce((s, n) => s + n, 0); }
}
```

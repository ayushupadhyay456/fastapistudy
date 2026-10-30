"""
=============================================================================
OBJECT-ORIENTED PROGRAMMING (OOP) IN PYTHON - CORE CONCEPTS & PATTERNS
=============================================================================
"""

from abc import ABC, abstractmethod


# =============================================================================
# 1. INSTANCE VS CLASS ATTRIBUTES (THE MUTABLE SHARING TRAP)
# =============================================================================

# PITFALL: Attributes defined directly inside the class body belong to the
# class itself, NOT the individual instance. If mutable, all instances share it.


class BadStudent:
    grades = []  # ❌ CLASS ATTRIBUTE: Shared across every instance!


s1 = BadStudent()
s2 = BadStudent()
s1.grades.append(90)
# print(s2.grades) -> [90]  <-- Mutated both students!


class GoodStudent:
    school_name = "Tech Academy"  # Class attribute (fine for shared constants)

    def __init__(self, name: str):
        self.name = name  # Instance attribute
        self.grades = []  #  Unique list allocated per instance


# =============================================================================
# 2. ENCAPSULATION & ACCESS MODIFIERS (CONVENTIONS & NAME MANGLING)
# =============================================================================

# Python does NOT enforce true "private" members at the compiler level.
# It uses naming conventions and runtime Name Mangling.


class BankAccount:
    def __init__(self, owner: str, balance: float):
        self.owner = owner  # Public: Accessible anywhere
        self._routing_number = 12345  # Protected: Intended for internal/subclass use only
        self.__balance = balance  # Private: Triggers Name Mangling

    def get_balance(self) -> float:
        return self.__balance


acc = BankAccount("Ayush", 1000.0)
# acc.__balance  -> Raises AttributeError!
# Python mangles `__balance` internally to `_BankAccount__balance`:
# print(acc._BankAccount__balance) -> 1000.0 (Accessible, but breaks convention)


# =============================================================================
# 3. GETTERS & SETTERS THE PYTHONIC WAY: @property
# =============================================================================

# Problem: In Java/C++, you write explicit get_x() and set_x().
# Solution: Python uses @property to keep attribute access clean while adding validation.


class Temperature:
    def __init__(self, celsius: float):
        self._celsius = celsius

    @property
    def celsius(self) -> float:
        """Getter for celsius."""
        return self._celsius

    @celsius.setter
    def celsius(self, value: float) -> None:
        """Setter with validation."""
        if value < -273.15:
            raise ValueError("Temperature below absolute zero is impossible!")
        self._celsius = value






temp = Temperature(25.0)
temp.celsius = 30.0  # Calls the setter transparently
# temp.celsius = -300.0  # Raises ValueError


# =============================================================================
# 4. METHOD TYPES: INSTANCE vs @classmethod vs @staticmethod
# =============================================================================


class Order:
    base_tax_rate = 0.05

    def __init__(self, amount: float):
        self.amount = amount

    # 1. Instance Method: Receives 'self', accesses/modifies instance state
    def total(self) -> float:
        return self.amount * (1 + self.base_tax_rate)

    # 2. Class Method: Receives 'cls', accesses/modifies class state.
    #    Common use case: Alternative constructors / Factory methods.
    @classmethod
    def from_string(cls, order_str: str) -> "Order":
        # Parsing "Order:100.50"
        amount = float(order_str.split(":")[1])
        return cls(amount)

    # 3. Static Method: Does not receive 'self' or 'cls'.
    #    A regular utility function placed inside the class namespace.
    @staticmethod
    def is_valid_currency(code: str) -> bool:
        return code in {"USD", "EUR", "INR", "GBP"}


# =============================================================================
# 5. INHERITANCE & super() (METHOD RESOLUTION ORDER - MRO)
# =============================================================================


class Animal:
    def __init__(self, name: str):
        self.name = name

    def speak(self) -> str:
        return "Some generic sound"


class Dog(Animal):
    def __init__(self, name: str, breed: str):
        super().__init__(name)  # Forward initialization to parent class
        self.breed = breed

    def speak(self) -> str:
        return f"{self.name} barks"


# MRO inspects how Python resolves inheritance order (C3 Linearization):
# Dog.mro() -> [Dog, Animal, object]


# =============================================================================
# 6. ABSTRACT BASE CLASSES (INTERFACES / CONTRACTS)
# =============================================================================

# Prevents direct instantiation of incomplete base classes.
# Guarantees subclasses implement essential methods at runtime.


class DatabaseConnector(ABC):
    @abstractmethod
    def connect(self) -> None:
        """Must be implemented by subclasses."""
        pass

    @abstractmethod
    def execute_query(self, query: str) -> list:
        """Must be implemented by subclasses."""
        pass


class PostgresConnector(DatabaseConnector):
    def connect(self) -> None:
        # Implementation details...
        pass

    def execute_query(self, query: str) -> list:
        return [{"status": "success"}]


# connector = DatabaseConnector()  # ❌ TypeError: Can't instantiate abstract class


# =============================================================================
# 7. ESSENTIAL MAGIC (DUNDER) METHODS
# =============================================================================


class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    # __str__: Human-readable format (for print() and end users)
    def __str__(self) -> str:
        return f"Point({self.x}, {self.y})"

    # __repr__: Unambiguous format (for debugging and logging)
    def __repr__(self) -> str:
        return f"Point(x={self.x!r}, y={self.y!r})"

    # __eq__: Custom equality logic (default compares memory address)
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Point):
            return False
        return self.x == other.x and self.y == other.y

    # __hash__: Required if using custom class instances inside sets or dict keys!
    def __hash__(self) -> int:
        return hash((self.x, self.y))

    # __lt__: Enables standard sorting: list_of_points.sort()
    def __lt__(self, other: "Point") -> bool:
        return (self.x, self.y) < (other.x, other.y)

    # __add__: Operator overloading (p1 + p2)
    def __add__(self, other: "Point") -> "Point":
        return Point(self.x + other.x, self.y + other.y)


p1 = Point(1, 2)
p2 = Point(3, 4)
p3 = p1 + p2  # Calls p1.__add__(p2) -> Point(4, 6)
point_set = {p1, p2}  # Works safely because __hash__ and __eq__ are defined


# =============================================================================
# 8. MEMORY OPTIMIZATION WITH __slots__
# =============================================================================

# Standard Python objects store instance attributes in a dynamic dictionary (__dict__).
# This adds significant memory overhead if instantiating millions of objects (e.g., Tree Nodes).
# FIX: __slots__ restricts attributes to a fixed tuple, removing __dict__ overhead.


class HeavyNode:
    def __init__(self, val: int):
        self.val = val
        self.left = None
        self.right = None


class LeanNode:
    __slots__ = ("val", "left", "right")  # Drops __dict__; saves ~40-50% memory

    def __init__(self, val: int):
        self.val = val
        self.left = None
        self.right = None


# =============================================================================
# 9. CONTEXT MANAGERS (__enter__ & __exit__)
# =============================================================================

# Powers the 'with' statement for deterministic resource management and cleanup.


class ManagedResource:
    def __enter__(self):
        # Setup resource (e.g., acquire lock, open file/connection)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Teardown logic runs even if an exception was raised inside the with block.
        # Returning True suppresses the raised exception; False allows it to propagate.
        return False
# SQLite Inventory Management System

A CLI-based inventory management application written in Python and powered by SQLite. Features full CRUD functionality, color-coded console outputs, and low-stock alert thresholds.

## Key Features

- **Full CRUD Operations:**
  - **Create:** Add new products with name, description, quantity, price, and category.
  - **Read:** List all products or search specific items by ID.
  - **Update:** Selectively update name, description, stock quantity, price, or category.
  - **Delete:** Remove entries by ID, category, or product name.
- **Low Stock Monitoring:** Built-in alerts for products with stock levels $\le 5$ units, featuring visual indicators (🚫 Agotado, 🔴 Muy Bajo, 🟡 Bajo).
- **Console UI:** Enhanced CLI experience using `colorama` for colored feedback messages.
- **SQL Safety:** Uses parameterized queries (`?`) to prevent SQL injection vulnerabilities.

## Prerequisites

- **Python 3.8+**
- **Colorama** library

Install `colorama`:
```bash
pip install colorama
```

## Database Schema

The system automatically initializes an SQLite database (`inventario.db`) with the following table structure:

| Field | Type | Constraint |
| :--- | :--- | :--- |
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT |
| `nombre` | TEXT | NOT NULL |
| `descripcion` | TEXT | — |
| `cantidad` | INTEGER | NOT NULL |
| `precio` | REAL | NOT NULL |
| `categoria` | TEXT | — |

## How to Run

Execute the main script from your terminal:

```bash
python "TFI Joaquin Rendano.py"
```

### Main Menu Options

```text
==================================================
Sistema de Gestión Básica De Productos
==================================================

1. Agregar producto
2. Mostrar productos
3. Actualizar producto
4. Buscar producto
5. Eliminar producto
6. Ver productos con stock bajo
7. Salir
```

## License

This project was developed as a Final Project (TFI) and is open for educational use.
## StorageLayer

```StorageLayer
 ├── Page
 │    └── rows: list of dicts
 ├── TableFile
 │    └── pages: list of Page
 ├── BufferPool
 │    └── page cache in RAM
 ├── WAL
 │    └── log operations for crash recovery

```

---

## **Module Overview**

### **Purpose**

* Implement **durability and crash recovery** for your Python-based database.
* Ensure that all database operations are **logged before being applied** to disk (Write-Ahead Logging).
* Allow **safe replay** of operations after a crash without duplicating logs.

---

### **Components**

#### 1. **WAL Class**

* **Purpose:** Log all operations with timestamps before applying them to table files.
* **Key Methods:**

  * `log(operation, table_name, row)` → writes operation to WAL file and memory.
  * `replay(db)` → reads WAL entries and applies them to the database using `_delete_no_log` (or `_insert_no_log` for inserts).
* **Features:**

  * Stores timestamps for auditing.
  * In-memory list (`entries`) allows fast replay without reading the file.
  * Works for crash recovery and auditing.

#### 2. **Table Class**

* **Purpose:** Represents a database table, manages pages, and provides CRUD operations.
* **Delete Workflow:**

  * `delete(criteria)` → logs the delete in WAL → calls `_delete_no_log(criteria)`
  * `_delete_no_log(criteria)` → deletes rows in memory and flushes pages to disk **without logging**, safe for WAL replay.
* **Key Concept:** `_delete_no_log` separates **applying changes to disk** from **logging**, preventing infinite recursion during replay.

---

### **Workflow Summary**

**Normal Delete:**

```
delete(criteria)
   ├─> WAL.log("DELETE", table_name, criteria)  # durability
   └─> _delete_no_log(criteria)                # update pages & disk
```

**Recovery (WAL Replay):**

```
replay(db)
   └─> _delete_no_log(criteria from WAL)      # reapply operations without logging
```

---

### **Key Benefits**

* **Durability:** Every operation is logged before being applied.
* **Crash Recovery:** Database can be restored exactly by replaying WAL.
* **Atomicity:** Deletes (or inserts) are applied entirely during replay.
* **Auditability:** Timestamped log entries allow tracking of operations.




# XAMPP MySQL Backup & Restore

Simple automated backup and restore script for XAMPP MySQL databases.

## What It Does

1. **Validates** paths and permissions
2. **Backs up** current data to `data_2` folder (safety copy)
3. **Cleans** old MySQL files and folders
4. **Restores** fresh data from backup folder

## Setup

1. Place `xampp.py` in any folder
2. Edit paths in CONFIG section if needed:
   ```python
   'source': r'C:\xampp\mysql\data'          # Current database
   'backup': r'C:\xampp\mysql\data_2'        # Backup location
   'restore_src': r'C:\xampp\mysql\backup'   # Backup files to restore
   'restore_dest': r'C:\xampp\mysql\data'    # Where to restore
   ```

## Usage

**Test mode (preview without changes):**
```python
CONFIG['dry_run'] = True
python xampp.py
```

**Real mode (execute operations):**
```python
CONFIG['dry_run'] = False
python xampp.py
```

## Important

- **Run as Administrator** (Windows)
- Script logs to `backup.log` automatically
- `ibdata1` file is protected (never deleted)
- Folders deleted: mysql, performance_schema, phpmyadmin, test
- If error occurs, backup is already saved in `data_2`

## Folders Affected

| Folder | Action |
|--------|--------|
| `data` | Cleaned & restored |
| `data_2` | Backup copy created here |
| `backup` | Source of restore files |

## Exit Codes

- `0` = Success
- `1` = Error occurred

## Logs

Check `backup.log` for detailed operation history.

---

**Status:** Script works perfectly ✓

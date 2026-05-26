import shutil
import os
import logging
import sys

# Fix Windows console encoding issue
if sys.platform == 'win32':
    import codecs
    sys.stdout.reconfigure(encoding='utf-8')

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler('backup.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger()

CONFIG = {
    'source': r'C:\xampp\mysql\data',
    'backup': r'C:\xampp\mysql\data_2',
    'restore_src': r'C:\xampp\mysql\backup',
    'restore_dest': r'C:\xampp\mysql\data',
    'delete_folders': {'mysql', 'performance_schema', 'phpmyadmin', 'test'},
    'keep_files': {'ibdata1'},
    'exclude_restore': {'ibdata1'},
    'dry_run': False
}

def validate():
    """Validate paths and permissions."""
    src, backup, restore_src, restore_dest = (
        CONFIG['source'], CONFIG['backup'],
        CONFIG['restore_src'], CONFIG['restore_dest']
    )
    
    if not os.path.exists(src):
        raise FileNotFoundError(f"Source not found: {src}")
    if not os.path.exists(restore_src):
        raise FileNotFoundError(f"Backup not found: {restore_src}")
    if not os.access(src, os.R_OK):
        raise PermissionError(f"No read access: {src}")
    if not os.access(restore_dest, os.W_OK):
        raise PermissionError(f"No write access: {restore_dest}")
    
    logger.info("[OK] Validation passed")
    return True

def backup():
    """Create backup of data folder."""
    src, dest, dry_run = CONFIG['source'], CONFIG['backup'], CONFIG['dry_run']
    
    logger.info(f"Backing up {src}")
    
    if os.path.exists(dest):
        if dry_run:
            logger.info(f"[DRY] Remove {dest}")
        else:
            shutil.rmtree(dest, ignore_errors=False)
    
    if not dry_run:
        shutil.copytree(src, dest)
    else:
        logger.info(f"[DRY] Copy {src} -> {dest}")
    
    logger.info("[OK] Backup complete")

def cleanup():
    """Clean data folder, keeping essential files."""
    base_dir = CONFIG['restore_dest']
    to_delete = CONFIG['delete_folders']
    keep = CONFIG['keep_files']
    dry_run = CONFIG['dry_run']
    
    logger.info(f"Cleaning {base_dir}")
    deleted = 0
    
    for item in os.listdir(base_dir):
        path = os.path.join(base_dir, item)
        
        if os.path.isdir(path) and item in to_delete:
            if not dry_run:
                shutil.rmtree(path, ignore_errors=True)
            logger.info(f"  Delete folder: {item}")
            deleted += 1
        
        elif os.path.isfile(path) and item not in keep:
            try:
                if not dry_run:
                    os.remove(path)
                logger.info(f"  Delete file: {item}")
                deleted += 1
            except PermissionError:
                logger.warning(f"  Skip (in use): {item}")
    
    logger.info(f"[OK] Cleanup complete ({deleted} deleted)")

def restore():
    """Restore data from backup."""
    src, dest = CONFIG['restore_src'], CONFIG['restore_dest']
    exclude = CONFIG['exclude_restore']
    dry_run = CONFIG['dry_run']
    
    logger.info(f"Restoring from {src}")
    copied = 0
    
    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dest_path = os.path.join(dest, item)
        
        if item.lower() in {x.lower() for x in exclude}:
            logger.info(f"  Skip (protected): {item}")
            continue
        
        if os.path.isdir(src_path):
            if os.path.exists(dest_path):
                logger.info(f"  Skip (exists): {item}")
                continue
            if not dry_run:
                shutil.copytree(src_path, dest_path)
            logger.info(f"  Restore folder: {item}")
            copied += 1
        
        elif os.path.isfile(src_path) and not os.path.exists(dest_path):
            if not dry_run:
                shutil.copy2(src_path, dest_path)
            logger.info(f"  Restore file: {item}")
            copied += 1
    
    logger.info(f"[OK] Restore complete ({copied} restored)")

def main():
    try:
        logger.info("=" * 50)
        logger.info(f"Starting (Dry-run: {CONFIG['dry_run']})")
        logger.info("=" * 50)
        
        validate()
        backup()
        cleanup()
        restore()
        
        logger.info("=" * 50)
        logger.info("[OK] ALL COMPLETE")
        logger.info("=" * 50)
    
    except Exception as e:
        logger.error(f"[FAIL] {e}")
        return False
    
    return True

if __name__ == '__main__':
    sys.exit(0 if main() else 1)
import os
import logging
import tempfile

def setup_logger():
    log_file_name = "mongoguard.log"

    try:
        user_cwd = os.getcwd()
        log_path = os.path.join(user_cwd, log_file_name)
    except PermissionError:
        log_path = os.path.join(tempfile.gettempdir(), log_file_name)
        print("Permission denied to write in the current directory. Using temporary directory for logs.")
    except Exception as ex:
        raise Exception("Failed to set up logger") from ex

    logging.basicConfig(
        filename=log_path,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    logging.info(f"Created {os.path.basename(log_path)} file in {log_path}")
    return logging.getLogger(__name__)

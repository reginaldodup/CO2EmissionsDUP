from pathlib import Path
import os

root_dir = Path(__file__).parent.parent
data_dir = Path(root_dir, os.path.join('0_data'))
notebooks_dir = Path(root_dir, os.path.join('1_notebooks'))
presentation_dir = Path(root_dir, os.path.join('presentation'))

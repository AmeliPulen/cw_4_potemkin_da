from pathlib import Path


CURRENT_PATH = Path(__file__).parent
PATH_FILE = Path.joinpath(CURRENT_PATH, 'src', 'vacancies.json')
PATH_AREA_FILE = Path.joinpath(CURRENT_PATH, 'src', 'areas.json')
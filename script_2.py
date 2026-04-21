from pathlib import Path
print(Path('output/annaheaner-site-blue-lite.zip').stat().st_size)
print(len(list(Path('output/annaheaner-site-blue-lite/assets/images').glob('*.jpg'))))
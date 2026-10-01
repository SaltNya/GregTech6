"""Run the production JEI scissor calculation with translated recipe poses, without starting Minecraft."""
from pathlib import Path
import os
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
cache = Path(os.environ.get('GRADLE_USER_HOME', Path.home() / '.gradle')) / 'caches/modules-2/files-2.1/org.joml/joml'
joml = next(p for p in cache.rglob('joml-1.10.5.jar'))
package = 'com/gregtech/gregtech/jei'
jdk = next((line.split('=', 1)[1].strip().replace('\\\\', '\\')
            for line in (ROOT / 'gradle.properties').read_text().splitlines()
            if line.startswith('org.gradle.java.home=')), os.environ.get('JAVA_HOME'))
def executable(name):
    return str(Path(jdk) / 'bin' / name) if jdk else name

with tempfile.TemporaryDirectory(prefix='gt6-preview-test-') as directory:
    subprocess.run([executable('javac'), '--release', '17', '-cp', str(joml), '-d', directory,
                    str(ROOT / f'src/main/java/{package}/PreviewViewport.java'),
                    str(ROOT / f'src/test/java/{package}/PreviewViewportContracts.java')], check=True)
    subprocess.run([executable('java'), '-cp', directory + os.pathsep + str(joml),
                    'com.gregtech.gregtech.jei.PreviewViewportContracts'], check=True)

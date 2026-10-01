"""Capture real large-crucible hull vertex UVs without starting Minecraft or a GPU."""
from pathlib import Path
import os
import subprocess
import tempfile
ROOT = Path(__file__).resolve().parents[1]
cp = (ROOT / 'build/classpath/runGameTestServer_minecraftClasspath.txt').read_text(encoding='utf-8').strip().replace('\n', os.pathsep)
cp += os.pathsep + str(ROOT / 'build/classes/java/main')
with tempfile.TemporaryDirectory(prefix='gt6-crucible-uv-') as folder:
    args=Path(folder)/'javac.args'
    sources=[ROOT/'src/main/java/com/gregtech/gregtech/client/LargeCrucibleHullFace.java', ROOT/'src/test/java/com/gregtech/gregtech/client/LargeCrucibleUvContracts.java']
    args.write_text('\n'.join('"'+str(x).replace('\\','/')+'"' for x in ['-proc:none','-cp',cp,'-d',folder,*sources]),encoding='utf-8')
    subprocess.run(['javac','@'+str(args)],check=True,cwd=ROOT)
    subprocess.run(['java','-cp',folder+os.pathsep+cp,'com.gregtech.gregtech.client.LargeCrucibleUvContracts'],check=True,cwd=ROOT)

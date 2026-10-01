"""Run isolated Gradle integration checks for the production ProcessResources subclass."""
from pathlib import Path
import subprocess
import tempfile
import os

ROOT=Path(__file__).resolve().parents[1]

def main():
    parent=ROOT/'build/resource-sync-tests';parent.mkdir(parents=True,exist_ok=True)
    fixture=Path(tempfile.mkdtemp(prefix='run-',dir=parent))
    source=fixture/'source';source.mkdir();output=fixture/'output'
    def write(name,data):
        path=source/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
    def run(token='first'):
        log=fixture/f'gradle-{len(list(fixture.glob("gradle-*.log")))}.log'
        command=[str(ROOT/'gradlew.bat'),'verifyResourceSync','--offline','--console=plain',
                 '-PresourceSyncFixture='+fixture.as_posix(),'-PresourceSyncToken='+token]
        with log.open('w',encoding='utf-8') as f:
            result=subprocess.run(command,cwd=ROOT,stdout=f,stderr=subprocess.STDOUT)
        text=log.read_text(encoding='utf-8',errors='replace')
        if result.returncode:raise AssertionError(text[-6000:])
        return text
    write('keep.bin',bytes(range(256)));write('nested/change.txt',b'old');write('remove.txt',b'remove')
    write('metadata.txt',b'${token}')
    run();assert (output/'metadata.txt').read_bytes()==b'first'
    original_time=(output/'keep.bin').stat().st_mtime_ns
    write('nested/change.txt',b'new');write('added.txt',b'new file');(source/'remove.txt').unlink()
    log=run()
    assert 'incremental' in log and (output/'keep.bin').stat().st_mtime_ns==original_time,log
    assert (output/'nested/change.txt').read_bytes()==b'new' and (output/'added.txt').read_bytes()==b'new file'
    assert not (output/'remove.txt').exists()
    run('second');assert (output/'metadata.txt').read_bytes()==b'second'
    (output/'keep.bin').write_bytes(b'external modification')
    run('second');assert (output/'keep.bin').read_bytes()==bytes(range(256))
    assert 'UP-TO-DATE' in run('second')
    # Explicitly named files owned by this temporary fixture only.
    for path in source.rglob('*'):
        if path.is_file():path.unlink()
    run('second');assert not any(p.is_file() for p in output.rglob('*'))
    print('PASS: add/change/delete, unchanged output untouched, expansion, external output repair, up-to-date, empty source cleanup')
    print('Fixture and logs:',fixture)

if __name__=='__main__':main()

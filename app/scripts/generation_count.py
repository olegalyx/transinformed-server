import inotify.adapters
import gzip

# Script to update total number of files generated

def _main():
    i = inotify.adapters.Inotify()

    i.add_watch('/var/log')

    for event in i.event_gen(yield_nones=False):
        (_, type_names, path, filename) = event

        print("PATH=[{}] FILENAME=[{}] EVENT_TYPES={}".format(
              path, filename, type_names))
        
        if "access" and "gz" in filename and type_names[0] == 'IN_MODIFY':
            with gzip.open(path + "/" + filename) as log:
                data = log.readlines()
                for entry in data:
                    if "POST" in str(entry):
                        with open("/home/Beawitched/files_generated.txt", 'r') as f:
                            count = int(f.read())
                            count+= 1
                        with open("/home/Beawitched/files_generated.txt", 'w') as f:
                            f.write(str(count))


if __name__ == '__main__':
    _main()
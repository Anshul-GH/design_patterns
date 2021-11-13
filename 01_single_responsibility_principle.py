import os

class Journal:
    def __init__(self):
        self.entries = []
        self.count = 0

    def add_entry(self, text):
        self.count += 1
        self.entries.append(f'Entry {self.count}: {text}')

    def remove_entry(self, pos):
        del self.entries[pos]

    def __str__(self):
        return '\n'.join(self.entries)

    # the following remaining functions in the class
    # voilate the single responsibility principle
    def save(self, filename):
        file = open(filename, 'w')
        file.write(str(self))
        file.close()

    def load(self, filename):
        file = open(filename, 'r')
        for record in file:
            self.entries.append(record)
        file.close()

    def load_from_web(self, uri):
        pass

# seperation of concerns
class PersistenceManager:
    @staticmethod
    def save_to_file(journal, filename):
        file = open(filename, 'w')
        file.write(str(journal))
        file.close()

# test the Journal class
j = Journal()
j.add_entry("I had a great time today.")
j.add_entry("I ate a bug.")
print(f"Journal Entries: \n{j}")

# test the seperated persistence code
file_path = os.getcwd() + "\data\journal.txt"
PersistenceManager.save_to_file(j, file_path)

with open(file_path) as fh:
    print("\nReading from the file:")
    print(fh.read())

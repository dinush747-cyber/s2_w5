from abc import ABC, abstractmethod
class Filter(ABC):
    def __init__(self, name):
        self.name = name
    @abstractmethod
    def apply(self, value):
        pass
    def check(self, value):
        status = "PASS" if self.apply(value) else "FAIL"
        print(f"[{status}] {self.name}: {value}")
        return status    
class ExtensionFilter(Filter):
    def __init__(self, allowed):
        self.allowed = allowed
        self.name = allowed
    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, value):
        new_name = ",".join(value)
        self._name = "Extension(" + new_name +")"
    def apply(self, value):
        return value[-4] == "."
class MaxSizeFilter(Filter):
    def __init__(self, max_size: int):
        self.max_size = max_size
        self.name = max_size
    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, value):
        self._name = f"MaxSize({value})"
    def apply(self, value):
        return len(value) <= self.max_size
class NoSpacesFilter(Filter):
    def __init__(self):
        self.name = "NoSpaces"
    def apply(self, value):
        return " " not in value
class StartsWithLetterFilter:
    def __init__(self):        
        self.name = "StartsWithLetter"
    def apply(self, value):
        if value and 'a' <= value[0] <= 'z':
            return True
        return False
    def check(self, value):
        status = "PASS" if self.apply(value) else "FAIL"
        print(f"[{status}] {self.name}: {value}")
        return status
class UploadReport:
    def __init__(self):
        self.entries = []
    def add(self, filter_name, value, passed):
        self.entries.append((filter_name, value, passed))
    def summary(self):
        total = len(self.entries)
        passed = sum(1 for item in self.entries if item[-1]== "PASS")
        failed = sum(1 for item in self.entries if item[-1]=="FAIL")
        print(f"Total: {total}, Passed: {passed}, Failed: {failed}")
class UploadField:
    def __init__(self, field_name):
        self.field_name = field_name
        self.filters = []
        self.report = UploadReport()
    def add_filter(self, filter_obj):
        self.filters.append(filter_obj)
    def validate(self, value):
        print(f'Validating {self.field_name}: "{value}"')
        all_passed = True
        for filter in self.filters:
            checking = filter.check(value)
            self.report.add(self.field_name, value, checking)
            if checking== "FAIL":
                all_passed = False
        return all_passed
    def show_report(self):
        print(f"--- Report for{self.field_name} ---")
        self.report.summary()

upload = UploadField('avatar')
upload.add_filter(ExtensionFilter(['jpg', 'png', 'pdf']))
upload.add_filter(MaxSizeFilter(20))
upload.add_filter(NoSpacesFilter())
upload.add_filter(StartsWithLetterFilter())

valid1 = upload.validate('profile_pic.jpg')
print(f'Valid: {valid1}')
print()

valid2 = upload.validate('my document.exe')
print(f'Valid: {valid2}')
print()

valid3 = upload.validate('123.png')
print(f'Valid: {valid3}')
print()

upload.show_report()

try:
    f = Filter('test')
except TypeError:
    print('Cannot instantiate abstract class')
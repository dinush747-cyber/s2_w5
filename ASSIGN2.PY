from abc import ABC, abstractmethod
class Filter(ABC):
    def __init__(self, name):
        self.name = name
    @abstractmethod
    def apply(self, value):
        pass
    def check(self, value):
        apply = self.apply(value)
        status = "PASS" if apply else "FAIL"
        print(f"[{status}] {self.name}: {value}")
        return apply    
class ExtensionFilter(Filter):
    def __init__(self, allowed):
        self.allowed = allowed
        self.name = "Extension(" + ",".join(self.allowed) +")"
    def apply(self, value):
        for i in range(len(value)-1, -1, -1):
            if value[i] == ".":
                dot = value[i+1:]
                return dot in self.allowed
        return False
class MaxSizeFilter(Filter):
    def __init__(self, max_size: int):
        self.max_size = max_size
        self.name = f"MaxSize({self.max_size})"
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
        return value and (("a" <= value[0]<= "z" ) or ("A" <= value[0] <= "Z") )
    def check(self, value):
        apply = self.apply(value)
        status = "PASS" if apply else "FAIL"
        print(f"[{status}] {self.name}: {value}")
        return apply
class UploadReport:
    def __init__(self):
        self.entries = []
    def add(self, filter_name, value, passed):
        self.entries.append((filter_name, value, passed))
    def summary(self):
        total = len(self.entries)
        passed = sum(1 for item in self.entries if item[-1])
        failed = sum(1 for item in self.entries if not item[-1])
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
            self.report.add(filter.name, value, checking)
            if not checking:
                all_passed = False
        return all_passed
    def show_report(self):
        print(f"--- Report for {self.field_name} ---")
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
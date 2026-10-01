from abc import ABC, abstractmethod

class Document(ABC):
    @abstractmethod
    def render(self) -> str:
        pass
class Report(Document):
    def render(self) -> str:
        return "Дані за звітний період"
class Invoice(Document):
    def render(self) -> str:
        return "До сплати 1 500.00 грн."
class Contract(Document):
    def render(self) -> str:
        return "Контракт."
class NullDocument(Document):
    def render(self) -> str:
        return ""
    
class DocumentFactory:
    @staticmethod
    def create(doc_type: str) -> Document:
        match doc_type.strip().lower():
            case "report":
                return Report()
            case "invoice":
                return Invoice()
            case "contract":
                return Contract()
            case _:
                return NullDocument()

if __name__ == "__main__":
    test_types = ["report", "invoice", "contract", "unknown_type"]
    for type in test_types:
        doc = DocumentFactory.create(type)
        output = doc.render()
        if output:
            print(output)
        else:
            print(f"Невідомий документ типу: '{type}'")








from collections import UserDict
import typing as t
import json


class FieldNotes:
    """
    Class parent representing a field used in the record of the notes book.
    """
    def __init__(self, value: str) -> None:
        self.value = value

    def __valid_value(self, value) -> None:
        if not isinstance(value , str) :
            raise TypeError(f'Value {value} not corect have to be str')
        
    @property
    def value(self) -> str:
        return self._value
    
    @value.setter
    def value(self, value: str, validation: t.Callable | None = None) -> None:
        self.__valid_value(value)
        if validation is not None : validation(value)
        self._value = value
               
    def __str__(self) -> str:
        return f'{self.value}'
    
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(value={self.value})'
    
    def __eq__(self, other) -> bool:
        if hasattr(other, "value"):
            value = other.value
        else:
            value = other
        return self.value == value


class NoteTag(FieldNotes):
    """
    Class representing the Note tag field in a record in the notes book.
    """
    def __note_tag_validation(self, note_tag: str) -> None:
        if not (2 <= len(note_tag) <= 20):
            raise ValueError("Tag is too short or long")
        if not note_tag.startswith('#'):
            raise ValueError("Tag should start with #")


    @FieldNotes.value.setter
    def value(self, note_tag: str) -> None:
        FieldNotes.value.fset(self, note_tag, self.__note_tag_validation)



class NoteBody(FieldNotes):
    """
    Class representing the Note body field in a record in the notes book.
    """
    def __note_body_validation(self, note_body: str) -> None:
        if not (1 <= len(note_body) <= 300):
            raise ValueError("Tag is too short or long")

    @FieldNotes.value.setter
    def value(self, note_body: str) -> None:
        FieldNotes.value.fset(self, note_body, self.__note_body_validation)



class RecordNote:
    """
     Class representing a record of a note in a notes book.

    Attributes:
        note_id (int): The unique identifier of the note.
        note_name (NoteName | str): The name of the note.
        note_body (NoteBody | str): The content of the note.
        note_tags (list[NoteTag] | list[str]): A list of tags associated with the note.
    """
    counter: int = 0

    def __init__(
            self,
            note_body :NoteBody | str, 
            note_tags: list[NoteTag] | list[str] = [],
            note_id: None = None,
            ) -> None:
        
        self.note_id = str(self.unic_id(note_id)) 
        self.note_tags = [self._tag(note_tag) for note_tag in note_tags] 
        self.note_body = self._body(note_body)

    
    def unic_id(self, id) -> int:
        if id is None :
            __class__.counter += 1
            return self.counter
        else:
            return id

    
    def _tag(self, tag: str | NoteTag) -> NoteTag:
        if not isinstance(tag, NoteTag):
            tag = NoteTag(tag)
        return tag

    
    def _body(self, body: str | NoteBody) -> NoteBody:
        if not isinstance(body, NoteBody):
            body = NoteBody(body)
        return body    

    def add_notetag(self, note_tag: NoteTag | str):
        """
        Add a new notetag to the list of notetag for the note.
        Args:
            notetag (Notetag) or try valid Str: The notetag is already added to the note.
        Returns:
            None: This method does not return any value.
        """ 
        if (note_tag := self._tag(note_tag)) in self.note_tags:
            raise ValueError("This notetag has already been added")
        self.note_tags.append(note_tag)

    def remove_notetag(self, note_tag: NoteTag | str) -> None:
        """
        Remove a notetag from the list of notetag for the note.

        Args:
            notetag (Notetag) or try valid Str: The notetag to be removed from the note.
        Raises:
            ValueError: If the notetag is not found in the notetag's list of notetags.
        Returns: 
            None: This method does not return any value.
        """
        try:
            self.note_tags.remove(self._tag(note_tag))
        except ValueError:
            raise ValueError(f"phone: {note_tag} not exists")

    
    def __str__(self) -> str:
        
        return (
            f'\n\tID: {self.note_id}\n'
            f'\tNote tags: {" ".join(map(str,self.note_tags))}\n'
            f'\t{self.note_body}\n')
    
    def to_dict(self) -> dict[int, dict[list[str], str]]:
        note_tags = [str(note_tag) for note_tag in self.note_tags]
        note_body = None if self.note_body is None else str(self.note_body)
        return {
            str(self.note_id): {
                "Tags": note_tags,
                "Note": note_body,
            },
        }

class NotesBook(UserDict):
    """
    A class representing an notes book, which is a dictionary 
    with note_id as keys and record notes objects as values.
    """
    def add_note_record(self, note_record: RecordNote):
        if not isinstance(note_record, RecordNote):
            raise TypeError("Note Record must be an instance of the RecordNote class.")
        self.data[note_record.note_id] = note_record 

    
    def find_note_record(self, key_note_id: str): 
        if (note_record := self.data.get(key_note_id)) is None:
            raise ValueError("There isn't such note")
        return note_record
    
    
    def find_note_record_tag(self, tag: str) -> list[RecordNote]:
        list_rec_notes = []

        for rec_note in self.data.values():         
            if (tag := rec_note._tag(tag)) in rec_note.note_tags:
                list_rec_notes.append(rec_note)

        return list_rec_notes    

    def __delaitem__(self, key: str) -> None:
        """
        Delete a record from the note book by its ID.

        Args:
            key (str): The name of the record to delete.
        Raises:
            KeyError: If the provided ID is not found in the note book.
        """
        if not isinstance(key, str):
            raise KeyError("Value must be string")
        if not key in self.data:
            raise KeyError(f"Can't delete note {key} isn't in note Book")
        del self.data[key]

    def __str__(self) -> str:
        return '\n'.join([str(r) for r in self.values()])
    
    def to_dict(self) -> dict:
        """
        Convert the notes book to a dictionary.

        Returns:
            dict: A dictionary representing the notes book.
        """
        res_dict = {}
        for note_record in self.data.values():
            res_dict.update(note_record.to_dict())
        return res_dict
    
    def from_dict(self, data_json: dict) -> None:
        """
        Load data from a dictionary into the notes book.

        Args:
            data_json (dict): A dictionary containing data for the address book.
        Raises:
            TypeError: If the provided data is not a dictionary.
        """
        if not isinstance(data_json, dict):
            raise TypeError("this is not dict")
        
        for key, value in data_json.items():
            self.add_note_record(
                RecordNote(note_id=key, note_tags=value['Tags'], note_body=value['Note'])
            )    


if __name__ == "__main__":
    tag_1 = NoteTag("#inc")
    tag_11 = NoteTag('#text')
    note_1 = NoteBody("hello I'm the first note")
    rec_1 = RecordNote(note_1,[tag_1, tag_11])

    tag_2 = NoteTag("#digit")
    note_2 = NoteBody("hello I'm the second note")
    rec_2 = RecordNote(note_2, [tag_2])

    tag_3 = NoteTag("#letter")
    note_3 = NoteBody("hello I'm the third note")
    rec_3 = RecordNote(note_3, [tag_3])

    # print(rec_1, rec_2, rec_3)

   

    rec_1.remove_notetag("#inc")
    
    tag_12 = NoteTag("#additional")
    
    rec_2.add_notetag(tag_3)

    # print(rec_1, rec_2)


    nb = NotesBook()
    nb.add_note_record(rec_1)
    nb.add_note_record(rec_2)
    nb.add_note_record(rec_3)

    # print(nb)

    # print(nb.find_note_record("2"))

    # print(nb.find_note_record_tag('#letter'))

    with open('data_note.json', 'w', encoding='utf-8') as f:
        json.dump(nb.to_dict(), f, ensure_ascii=False, indent=4)


    with open('data_note.json', 'r', encoding='utf-8') as f:
        restore_data = json.load(f)
        print(restore_data)
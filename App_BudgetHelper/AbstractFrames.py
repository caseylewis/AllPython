from Libs.GuiLib.gui_helpers import *


style_btn_delete = style_btn
style_btn_delete['width'] = 3


class AbstractEditFrame(Frame):
    class EditFrameModes:
        ADD = 0
        UPDATE = 1
    _modes = EditFrameModes

    def __init__(self, root, object_type, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        # SET OBJECT TYPE FOR LATER
        self.object_type = object_type

        # SET MODE TO CREATE BY DEFAULT
        self.mode = self._modes.ADD

        # TITLE
        self._title = Label(self, text="Create {}".format(object_type.object_name), **style_lbl_title)
        self._title.grid(row=0, column=0, **grid_frame_primary)

        # INPUT FRAME
        self._input_frame = Frame(self, **style_frame_primary)
        self._input_frame.grid(row=1, column=0, **grid_frame_primary)
        self._input_frame.grid_columnconfigure(0, weight=1)
        self._input_frame.grid_columnconfigure(1, weight=1)

        # INPUT LABELS
        style_lbl_input = copy_dict(style_lbl)
        style_lbl_input['anchor'] = E
        grid_lbl_input = copy_dict(grid_lbl)
        grid_lbl_input['sticky'] = 'nse'
        for key, idx in zip(self.object_type.keys.all_keys, self.object_type.idxs.all_indices):
            lbl = Label(self._input_frame, text=key, **style_lbl_input)
            lbl.grid(row=idx, column=0, **grid_lbl_input)

        # INPUT ENTRIES
        self._entry_dict = {}
        self.set_entries()

        # CREATE NAME LABEL FOR WHEN UPDATING AN OBJECT, BUT DON'T GRID
        self._name_lbl = Label(self._input_frame, **style_lbl)
        self._name_lbl.grid(row=self.object_type.idxs.NAME, column=1, **grid_lbl)
        self._name_lbl.grid_remove()

        # BUTTONS FRAME
        self._buttons_frame = Frame(self._input_frame, **style_frame_primary)
        self._buttons_frame.grid(row=len(self.object_type.idxs.all_indices)+1, column=1, **grid_frame_primary)
        self._buttons_frame.grid_columnconfigure(0, weight=1)
        self._buttons_frame.grid_columnconfigure(1, weight=1)

        # ADD
        self.add_object_btn = Button(self._buttons_frame, text="Add", **style_btn)
        self.add_object_btn.grid(row=0, column=1, **grid_btn)

        # UPDATE
        self.update_object_btn = Button(self._buttons_frame, text="Update", **style_btn)
        self.update_object_btn.grid(row=0, column=1, **grid_btn)
        self.update_object_btn.grid_remove()

        # CLEAR
        self._clear_btn = Button(self._buttons_frame, text="Clear", command=lambda: self.__handle_clear_btn(), **style_btn)
        self._clear_btn.grid(row=0, column=0, **grid_btn)

        # CANCEL
        self._cancel_btn = Button(self._buttons_frame, text="Cancel", command=lambda: self.__handle_cancel_btn(), **style_btn)
        self._cancel_btn.grid(row=0, column=0, **grid_btn)
        self._cancel_btn.grid_remove()

    @abstractmethod
    def set_entries(self):
        pass

    def clear_entries(self):
        for key, entry in self._entry_dict.items():
            entry.default()

    def get_object_from_entries(self):
        value_dict = {}
        if self.mode == self._modes.ADD:
            for key, entry in self._entry_dict.items():
                value_dict[key] = entry.get()
        elif self.mode == self._modes.UPDATE:
            value_dict[self.object_type.keys.NAME] = self._name_lbl['text']
            for key, entry in self._entry_dict.items():
                if key == self.object_type.keys.NAME:
                    continue
                value_dict[key] = entry.get()
        object = self.object_type(**value_dict)
        return object

    def __set_entries(self, object):
        self._name_lbl['text'] = object[self.object_type.keys.NAME]
        for key, entry in self._entry_dict.items():
            if key == self.object_type.keys.NAME:
                continue
            entry.set(object[key])

    def change_to_add_mode(self):
        self.mode = self._modes.ADD
        # BUTTONS
        self.update_object_btn.grid_remove()
        self._cancel_btn.grid_remove()

        self.add_object_btn.grid()
        self._clear_btn.grid()

        # SWITCH LABEL TO ENTRY
        self._name_lbl.grid_remove()
        self._entry_dict[self.object_type.keys.NAME].grid()

        # CLEAR ENTRIES
        self.clear_entries()

    def change_to_update_mode(self, object):
        self.mode = self._modes.UPDATE
        # BUTTONS
        self.add_object_btn.grid_remove()
        self._clear_btn.grid_remove()

        self.update_object_btn.grid()
        self._cancel_btn.grid()

        # SWITCH ENTRY TO LABEL
        self._entry_dict[self.object_type.keys.NAME].grid_remove()
        self._name_lbl.grid()

        self.__set_entries(object)

    def __handle_clear_btn(self):
        self.clear_entries()

    def __handle_cancel_btn(self):
        self.change_to_add_mode()
        self.clear_entries()


class AbstractViewFrame(Frame):
    style_btn_edit = copy_dict(style_btn)
    style_btn_edit['width'] = 4

    def __init__(self, root, object_type, on_edit_func=None, on_delete_func=None, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        # SET OBJECT TYPE FOR LATER
        self.object_type = object_type

        # FUNCTION TO HANDLE WHEN SUBMIT IS CLICKED
        self.on_edit_callback = on_edit_func
        self.on_delete_callback = on_delete_func

        # TITLE
        self._title = Label(self, text="{} View".format(self.object_type.object_name), **style_lbl_title)
        self._title.grid(row=0, column=0, **grid_lbl)

        # OBJECT LIST FRAME
        self._object_list_frame = Frame(self, **style_frame_primary)
        self._object_list_frame.grid(row=1, column=0, **grid_frame_primary)
        self._object_list_frame.grid_columnconfigure(0, weight=1)
        self._object_list_frame.grid_rowconfigure(0, weight=0)
        self._object_list_frame.grid_rowconfigure(1, weight=1)

        # COLUMN FRAME
        self._column_frame = Frame(self._object_list_frame, **style_frame_primary)
        self._column_frame.grid(row=0, column=0, **grid_frame_primary)
        for idx in self.object_type.idxs.all_indices:
            self._column_frame.grid_columnconfigure(idx, weight=1)
        # EDIT
        self._style_edit = copy_dict(style_lbl)
        self._style_edit['width'] = 4
        self._edit_col = Label(self._column_frame, **self._style_edit)
        self._edit_col_idx = len(self.object_type.idxs.all_indices) + 1
        self._edit_col.grid(row=0, column=self._edit_col_idx, **grid_lbl)
        # DELETE
        self._style_delete = copy_dict(style_lbl)
        self._style_delete['width'] = 3
        self._delete_col = Label(self._column_frame, **self._style_delete)
        self._delete_col_idx = self._edit_col_idx + 1
        self._delete_col.grid(row=0, column=self._delete_col_idx, **grid_lbl)

        # COLUMN LABELS
        style_lbl_col = copy_dict(style_lbl)
        style_lbl_col['bg'] = style_lbl['fg']
        style_lbl_col['fg'] = style_lbl['bg']
        for key, idx in zip(self.object_type.keys.all_keys, self.object_type.idxs.all_indices):
            lbl = Label(self._column_frame, text=key, **style_lbl_col)
            lbl.grid(row=0, column=idx, **grid_lbl)

        # OBJECT SCROLL FRAME
        self._object_scroll_frame = ScrollFrame(self._object_list_frame, hide_scroll_bar=True)
        self._object_scroll_frame.config(**style_frame_primary)
        self._object_scroll_frame.grid(row=1, column=0, **grid_frame_primary)
        self._object_scroll_frame.view_port.grid_columnconfigure(0, weight=1)
        self._next_index = 0
        self._object_row_dict = {}

    # FINISHED
    def populate_objects(self, objects_list: list):
        for object in objects_list:
            self.add_object(object)

    def update_object(self, object):
        for gui_object in self._object_row_dict.values():
            if gui_object[self.object_type.keys.NAME]['text'] == object[self.object_type.keys.NAME]:
                for key in self.object_type.keys.required_keys:
                    gui_object[key]['text'] = object[key]
                print("Updated {}: [ {} ]".format(self.object_type.object_name, object[self.object_type.keys.NAME]))
                break

    def add_object(self, object):
        # CREATE NEW OBJECT FRAME
        object_frame = Frame(self._object_scroll_frame.view_port, **style_frame_primary)
        object_frame.grid(row=self._next_index, column=0, **grid_frame_primary)
        for idx in self.object_type.idxs.all_indices:
            object_frame.grid_columnconfigure(idx, weight=1)
        row_dict = {}
        row_dict['frame'] = object_frame

        # CREATE LABELS
        for key, idx in zip(self.object_type.keys.all_keys, self.object_type.idxs.all_indices):
            lbl = Label(object_frame, text=object[key], **style_lbl)
            lbl.grid(row=0, column=idx, **grid_lbl)
            row_dict[key] = lbl

        # APPEND WIDGET DICT TO OBJECT ROW DICT
        self._object_row_dict[self._next_index] = row_dict
        # EDIT
        edit_btn = Button(object_frame, text="Edit", command=lambda idx=self._next_index: self.__handle_edit_btn(idx), **self.style_btn_edit)
        edit_btn.grid(row=0, column=self._edit_col_idx, **grid_btn)
        row_dict['edit'] = edit_btn
        # DELETE
        delete_btn = Button(object_frame, text="[x]", command=lambda idx=self._next_index: self.__handle_delete_btn(idx), **style_btn)
        delete_btn.grid(row=0, column=self._delete_col_idx, **grid_btn)
        row_dict['delete'] = delete_btn

        # INCREMENT NEXT INDEX
        self._next_index += 1

    def __get_object_from_index(self, index):
        value_dict = {}
        for key, idx in zip(self.object_type.keys.all_keys, self.object_type.idxs.all_indices):
            value_dict[key] = self._object_row_dict[index][key]['text']
        return value_dict

    def __get_index_from_object(self, object):
        for idx, row_dict in self._object_row_dict.items():
            if object[self.object_type.keys.NAME] == row_dict[self.object_type.keys.NAME]['text']:
                return idx

    def set_object_at_index(self, index, object):
        for key, idx in zip(self.object_type.keys, self.object_type.idxs.all_indices):
            self._object_row_dict[index][key]['text'] = object[key]

    def delete_object(self, object):
        delete_idx = self.__get_index_from_object(object)
        # DELETE CURRENT INDEX
        for widget in self._object_row_dict[delete_idx].values():
            widget.destroy()
        self._next_index -= 1
        # SHIFT HIGHER INDICES DOWN
        while delete_idx < self._next_index:
            self._object_row_dict[delete_idx] = self._object_row_dict[delete_idx + 1]

            current_frame = self._object_row_dict[delete_idx]['frame']
            frame_row = current_frame.grid_info()['row']
            current_frame.grid(row=frame_row-1)

            current_edit = self._object_row_dict[delete_idx]['edit']
            current_edit.config(command=lambda idx=delete_idx: self.__handle_edit_btn(idx))
            current_delete = self._object_row_dict[delete_idx]['delete']
            current_delete.config(command=lambda idx=delete_idx: self.__handle_delete_btn(idx))

            delete_idx += 1
        self._object_row_dict.pop(self._next_index)

    def __handle_delete_btn(self, index):
        if self.on_delete_callback is not None:
            object = self.__get_object_from_index(index)
            self.on_delete_callback(object)

    def __handle_edit_btn(self, index):
        if self.on_edit_callback is not None:
            object = self.__get_object_from_index(index)
            self.on_edit_callback(object)


if __name__ == '__main__':
    root = Tk()
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)

    # frame = ExpenseEditFrame()
    #
    # frame.grid(row=0, column=0, sticky='nsew')

    root.mainloop()

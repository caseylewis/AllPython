from Libs.GuiLib.gui_helpers import *
from App_BudgetHelper.accounts import *
from App_BudgetHelper.AbstractFrames import *


style_btn_delete = style_btn
style_btn_delete['width'] = 3


class AccountEditFrame(AbstractEditFrame):
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, Account, *args, **kwargs)

    def set_entries(self):
        for key, idx in zip(self.object_type.keys.all_keys, self.object_type.idxs.all_indices):
            entry = EntryPlus(self._input_frame, **style_entry)
            entry.grid(row=idx, column=1, **grid_entry)
            self._entry_dict[key] = entry


class AccountViewFrame(AbstractViewFrame):
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, Account, *args, **kwargs)


class AccountFrame(ContentFrame):
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, "Accounts", *args, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        class AccountFrameIndices:
            EDIT_FRAME = 0
            VIEW_FRAME = 1
            # LOGGER = 2
        self._account_frame_idxs = AccountFrameIndices
        self.view_port.grid_columnconfigure(0, weight=1)
        self.view_port.grid_columnconfigure(1, weight=0)
        self.view_port.grid_columnconfigure(2, weight=1)
        self.view_port.grid_rowconfigure(self._account_frame_idxs.EDIT_FRAME, weight=0)
        self.view_port.grid_rowconfigure(self._account_frame_idxs.VIEW_FRAME, weight=1)
        # self.view_port.grid_rowconfigure(self._account_frame_idxs.LOGGER, weight=0)

        # ACCOUNT EDIT FRAME
        self.account_edit_frame = AccountEditFrame(self.view_port, **style_frame_primary)
        self.account_edit_frame.grid(row=self._account_frame_idxs.EDIT_FRAME, column=1, **grid_frame_primary)

        # ACCOUNT VIEW FRAME
        self.account_view_frame = AccountViewFrame(self.view_port, on_edit_func=self.__edit_account, **style_frame_primary)
        self.account_view_frame.grid(row=self._account_frame_idxs.VIEW_FRAME, column=0, columnspan=3, **grid_frame_primary)

        # # LOGGER
        # self._logger = LoggerPlus(self.view_port, **style_logger)
        # self._logger.grid(row=self._account_frame_idxs.LOGGER, column=0, columnspan=3, **grid_logger)

    def handle_close(self):
        # self._accounts_json_manager.export_data(self._accounts_list)
        return

    def __edit_account(self, account):
        self.account_edit_frame.change_to_update_mode(account)


if __name__ == '__main__':
    root = Tk()
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)

    # TEST FOR ACCOUNT EDIT FRAME
    # def add_account():
    #     raw_account = frame.get_account_from_entries()
    #     print(raw_account)
    #     frame.clear_entries()
    #
    #
    # def update_account():
    #     account = frame.get_account_from_entries()
    #     print(account)
    #     frame.change_to_add_mode()
    #
    #
    # frame = AccountEditFrame(root)
    # frame.add_account_btn.config(command=lambda: add_account())
    # frame.update_account_btn.config(command=lambda: update_account())
    # frame.change_to_update_mode(test_account)
    ####################################################################################################################

    # TEST FOR ACCOUNT VIEW FRAME
    # def edit_button_clicked(account_name):
    #     print(account_name)
    #
    # frame = AccountViewFrame(root, on_edit_func=edit_button_clicked, on_delete_func=edit_button_clicked)
    # frame.populate_accounts([test_account])
    # frame.add_account(test_account)
    ####################################################################################################################

    # # TEST FOR ACCOUNTFRAME
    def add_account():
        raw_account = frame.account_edit_frame.get_object_from_entries()
        print(raw_account)
        frame.account_view_frame.add_object(Account(**raw_account))
        frame.account_edit_frame.clear_entries()


    def update_account():
        account = frame.account_edit_frame.get_object_from_entries()
        print(account)
        new_account = Account(**account)
        frame.account_view_frame.update_object(new_account)
        frame.account_edit_frame.change_to_add_mode()

    def delete_account(account):
        print(account)
        frame.account_view_frame.delete_object(account)

    frame = AccountFrame(root, height=800, **style_frame_primary)
    frame.account_edit_frame.add_object_btn.config(command=lambda: add_account())
    frame.account_edit_frame.update_object_btn.config(command=lambda: update_account())
    frame.account_view_frame.on_delete_callback = delete_account

    frame.account_view_frame.populate_objects([test_account])

    # GRID WHICHEVER FRAME
    frame.grid(row=0, column=0, sticky='nsew')

    root.mainloop()

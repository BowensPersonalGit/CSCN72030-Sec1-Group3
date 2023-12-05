from PyQt5.QtWidgets import QApplication, QMessageBox


def showPopup(text, details):
    """Show a warning popup with the given text and details"""
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)
    msg.setWindowTitle("Warning")
    msg.setText(text)
    msg.setInformativeText(details)
    msg.setStandardButtons(QMessageBox.Ok)
    msg.setDefaultButton(QMessageBox.Ok)

    # wait for user response
    retval = msg.exec_() # STOPS PROGRAM

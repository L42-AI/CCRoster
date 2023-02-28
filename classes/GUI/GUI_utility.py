from PySide6.QtWidgets import QHBoxLayout

def SetNullMargin(widget: QHBoxLayout, top=0, bottom=0, right=0, left=0, spacing=0) -> QHBoxLayout:
    widget.setContentsMargins(left, top, right, bottom)
    widget.setSpacing(spacing)
    return widget
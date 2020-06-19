styleMain = """
QListView{
    border: 0px;
    background-color: #991b1e;
    font-size: 13px;
}
QListView::item {
    color: white;
    height: 50px;
}
QListView::item:hover {
    background-color: #850407;
    border: 0px;
}
QListView::item:selected {
    background-color: #850407;
    font-weight: bold;
    border: 0px;
}
"""

styleSub = """
QListView{
    border: 0px;
}
QListView::item {
    height: 50px;
}
QListView::item:hover {
    background-color: #f0a3a5;
    border: 0px;
}
QListView::item:selected {
    background-color: #f0a3a5;
    font-weight: bold;
    border: 0px;
}
"""

# -------------NAV BAR-----------------
NavMenuStyle = """
    QFrame {
        background-color: rgba(0, 0, 0, 0.05);
        border: 5px;
        border-radius: 13px;
    }
    }"""

NavButtonStyle = """
    QPushButton {
        background-color: transparent;
        color: #1e1e1e;
        padding: 3px 32px;
        font-size: 10px;
        width: 55px;
        height 55px;
        padding-bottom: 15px;

        qproperty-iconSize: 24px 24px;  /* wielkość ikony w przycisku */
    }
    QPushButton:hover {
        background-color: #9a9a9a;
    }
    QPushButton:pressed {
        background-color: #1c6691;
        font-size: 14px;
    }"""
# -------------MAIN MENU---------------

scrollAreaStyle = """
QScrollArea {
        border: none;
       background: #f0f0f0;

   }"""

categoryBoxStyle = """
QGroupBox {
    font-size: 24px;
    font-weight: bold;
    border: 1px solid #ccc;
    border-radius: 15px;
    margin-top: 10px;
    padding-top: 15px;
    
}
"""

categoryButtonStyle = """
QPushButton {
    background-color: #fff;
    border: 1px solid #ddd;
    border-radius: 15px;
    padding: 10px;
    text-align: center;
    font-weight: normal;
    font-size: 18px;
    max-height: 100px;
    margin: 5px
    
}

QPushButton:hover {
    background-color: #e6e6e6;
    border: 1px solid #ccc;
    }
"""

secondaryButtonStyle = """
QPushButton {
    background-color: #fff;
    border: 1px solid #ddd;
    border-radius: 15px;
    padding: 10px;
    text-align: center;
    font-weight: normal;
    font-size: 14px;
    max-height: 35px;
}

QPushButton:hover {
    background-color: #e6e6e6;
    border: 1px solid #ccc;
    }
"""


# -------------HOME PAGE---------------
headerStyle = """
.QLabel {
    font-size: 24px;
    font-weight: bold;
    color: #333;
    margin-bottom: 10px;
}
"""

textStyle = """
QLabel {
    font-size: 16px;
    color: #555;
    "alignment": "left",
    }
"""

# -------------Icon---------------
iconButtonStyle = """
QPushButton {
    background-color: #2C3E50;
    border: 2px solid #34495E;
    border-radius: 10px;
    padding: 5px;
}
QPushButton:hover {
    background-color: #34495E;
    border: 2px solid #2980B9;
}
QPushButton:pressed {
    background-color: #2980B9;
}
"""


#----------Graphy-----------------
lineeditStyle = """
QLineEdit {
    border: 2px solid;
    border-radius: 1px;
    padding: 5px;
    text-align: left;
    font-size: 12px;
}
"""

iconStyle= """

    QPushButton {

        border: none;
       
        padding: 5px;
        text-align: center;

    }



"""


#-----------Custom Widgets-----------
DeletebuttonStyle = """
            QPushButton {
                background-color: transparent;  /* Przezroczyste tło */
                color: #ff4444;
                border: 1px solid #ff4444;
                border-radius: 5px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: rgba(255, 68, 68, 0.2);  /* Lekko czerwone tło przy hover */
                color: #ff6666;
                border: 1px solid #ff6666;
            }
            QPushButton:pressed {
                background-color: rgba(255, 68, 68, 0.4);
            }
"""
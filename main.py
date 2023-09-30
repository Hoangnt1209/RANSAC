import os  # Thư viện os để làm việc với hệ điều hành
from ransac import *  # Import các hàm từ thư viện ransac
from PyQt5 import uic  # Thư viện PyQt5 để tạo giao diện người dùng
from PIL import Image as im  # Thư viện PIL để làm việc với hình ảnh
import matplotlib.pyplot as plt  # Thư viện matplotlib để hiển thị hình ảnh
from PyQt5.QtGui import QPixmap  # Thư viện PyQt5 để hiển thị hình ảnh trên giao diện
from PyQt5.QtWidgets import QApplication, QMainWindow, QPlainTextEdit, QFileDialog  # Các thành phần giao diện

PATH = "interface.ui"  # Đường dẫn đến tệp giao diện .ui


class interface(QMainWindow):
    def __init__(self):
        super(interface, self).__init__()
        uic.loadUi(PATH, self)  # Tải giao diện từ tệp .ui
        self.show()

        self.image_ref = None  # Biến lưu trữ đường dẫn hình ảnh tham chiếu
        self.image_ali = None  # Biến lưu trữ đường dẫn hình ảnh căn chỉnh

        # Cài đặt các nút;
        self.pushButton.clicked.connect(self.linktoimage_ref)  # Khi nút được nhấn, gọi phương thức linktoimage_ref
        self.pushButton_2.clicked.connect(self.linktoimage_ali)  # Khi nút được nhấn, gọi phương thức linktoimage_ali
        self.pushButton_3.clicked.connect(self.enter)  # Khi nút được nhấn, gọi phương thức enter

    def linktoimage_ref(self):
        self.image_ref = QFileDialog.getOpenFileName(
            filter='*.jpg *.png')  # Hiển thị hộp thoại chọn tệp và lưu đường dẫn hình ảnh tham chiếu vào biến
        self.label.setPixmap(QPixmap(self.image_ref[0]))  # Hiển thị hình ảnh tham chiếu trên nhãn
        self.lineEdit.setText(self.image_ref[0])  # Hiển thị đường dẫn hình ảnh tham chiếu trong ô văn bản

    def linktoimage_ali(self):
        self.image_ali = QFileDialog.getOpenFileName(
            filter='*.jpg *.png')  # Hiển thị hộp thoại chọn tệp và lưu đường dẫn hình ảnh căn chỉnh vào biến
        self.label_2.setPixmap(QPixmap(self.image_ali[0]))  # Hiển thị hình ảnh căn chỉnh trên nhãn
        self.lineEdit_2.setText(self.image_ali[0])  # Hiển thị đường dẫn hình ảnh căn chỉnh trong ô văn bản

    def enter(self):
        img1 = cv.imread(self.image_ref[0], cv.IMREAD_COLOR)  # Đọc hình ảnh tham chiếu
        img2 = cv.imread(self.image_ali[0], cv.IMREAD_COLOR)  # Đọc hình ảnh căn chỉnh

        imgRes = alignImages(img2, img1)  # Căn chỉnh hình ảnh căn chỉnh theo hình ảnh tham chiếu
        cv.imwrite("image.png", imgRes)  # Lưu kết quả căn chỉnh vào tệp "image.png"

        self.label_3.setPixmap(QPixmap("image.png"))  # Hiển thị kết quả căn chỉnh trên nhãn
        self.lineEdit_3.setText("Done......!")  # Hiển thị thông báo "Done......!" trong ô văn bản


if __name__ == "__main__":
    app = QApplication([])  # Tạo đối tượng ứng dụng QApplication
    myprogram = interface()  # Tạo đối tượng giao diện
    app.exec()  # Chạy ứng dụng

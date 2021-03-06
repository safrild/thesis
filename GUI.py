import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget
from gauss_noise_reduction import *

# kepek beolvasasa es tombbe helyezese
Lake = cv2.imread('Lake.jpg', cv2.IMREAD_GRAYSCALE)
Tower = cv2.imread('Tower.jpg', cv2.IMREAD_GRAYSCALE)
Wall = cv2.imread('Wall.jpg', cv2.IMREAD_GRAYSCALE)
Lake256 = cv2.imread('Lake_256.jpg', cv2.IMREAD_GRAYSCALE)
images = {"Lake": Lake,
          "Lake256": Lake256,
          "Tower": Tower,
          "Wall": Wall}
kernels = {"3x3": 1,
           "5x5 (time consuming)": 2}
radiuses = {"1": 1,
            "2": 2}
range_sigmas = {"10": 10,
                "20": 20,
                "40": 40,
                "60": 60,
                "80": 80,
                "100": 100}


def window():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    win = QWidget()
    win.setGeometry(200, 200, 300, 300)
    win.setWindowTitle("Menu")
    layout = QVBoxLayout()
    # algorithm chooser
    label1 = QtWidgets.QLabel()
    label1.setText("Algorithm: ")
    layout.addWidget(label1)
    comboBoxAlgorithm = QtWidgets.QComboBox(win)
    comboBoxAlgorithm.addItems(
        ["Sigma", "Kuwahara", "Gradient inverse weighted method", "Gradient inverse weighted method NEW", "Bilateral",
         "Bilateral constant time"])
    layout.addWidget(comboBoxAlgorithm)
    # Sigma a zajosításhoz
    label2 = QtWidgets.QLabel(win)
    label2.setText("Sigma value: ")
    layout.addWidget(label2)
    comboBoxSigma = QtWidgets.QComboBox(win)
    comboBoxSigma.addItems(["20", "40", "80"])
    layout.addWidget(comboBoxSigma)
    # Kernel size
    label4 = QtWidgets.QLabel(win)
    label4.setText("Kernel size: ")
    layout.addWidget(label4)
    comboBoxKernel = QtWidgets.QComboBox(win)
    comboBoxKernel.addItems(kernels)
    layout.addWidget(comboBoxKernel)
    # input photo
    label3 = QtWidgets.QLabel(win)
    label3.setText("Input photo: ")
    layout.addWidget(label3)
    comboBoxInput = QtWidgets.QComboBox(win)
    comboBoxInput.addItems(images)
    layout.addWidget(comboBoxInput)
    # radius
    label5 = QtWidgets.QLabel(win)
    label5.setText("Radius: ")
    layout.addWidget(label5)
    label5.hide()
    comboBoxR = QtWidgets.QComboBox(win)
    comboBoxR.addItems(radiuses)
    layout.addWidget(comboBoxR)
    comboBoxR.hide()
    # range sigma
    label6 = QtWidgets.QLabel(win)
    label6.setText("Range sigma: ")
    layout.addWidget(label6)
    label6.hide()
    sliderRangeSigma = QtWidgets.QSlider(Qt.Horizontal)
    sliderRangeSigma.setMinimum(0)
    sliderRangeSigma.setMaximum(100)
    sliderRangeSigma.setValue(40)
    layout.addWidget(sliderRangeSigma)
    sliderRangeSigma.hide()
    # spatial sigma
    label7 = QtWidgets.QLabel(win)
    label7.setText("Spatial sigma: ")
    layout.addWidget(label7)
    label7.hide()
    sliderSpaceSigma = QtWidgets.QSlider(Qt.Horizontal)
    sliderSpaceSigma.setMinimum(0)
    sliderSpaceSigma.setMaximum(100)
    sliderSpaceSigma.setValue(40)
    layout.addWidget(sliderSpaceSigma)
    sliderSpaceSigma.hide()
    # GIW_new tobbszori alkalmazas
    label8 = QtWidgets.QLabel(win)
    label8.setText("Repeat times: ")
    label8.hide()
    layout.addWidget(label8)
    comboBoxGIWRepeat = QtWidgets.QComboBox(win)
    comboBoxGIWRepeat.addItems(["1", "2", "3"])
    layout.addWidget(comboBoxGIWRepeat)
    comboBoxGIWRepeat.hide()
    # run button
    btnRun = QtWidgets.QPushButton(win)
    btnRun.setText("Run algorithm")
    btnRun.setCheckable(True)
    layout.addWidget(btnRun)
    comboBoxAlgorithm.currentIndexChanged.connect(lambda: update_window())

    def update_window():
        comboBoxKernel.clear()
        label5.hide()
        comboBoxR.hide()
        label4.show()
        comboBoxKernel.show()
        label6.hide()
        sliderRangeSigma.hide()
        label7.hide()
        sliderSpaceSigma.hide()
        label8.hide()
        comboBoxGIWRepeat.hide()
        if comboBoxAlgorithm.currentText() == "Kuwahara":
            comboBoxKernel.addItem("5x5 (time consuming)")
        elif comboBoxAlgorithm.currentText() == "Bilateral":
            comboBoxKernel.addItem("5x5 (time consuming)")
            label6.show()
            sliderRangeSigma.show()
            label7.show()
            sliderSpaceSigma.show()
        elif comboBoxAlgorithm.currentText() == "Gradient inverse weighted method NEW":
            comboBoxKernel.addItems(kernels)
            label8.show()
            comboBoxGIWRepeat.show()
        else:
            comboBoxKernel.addItems(kernels)

    win.setLayout(layout)
    win.show()

    btnRun.clicked.connect(
        lambda: call_algorithm(comboBoxAlgorithm.currentText(), comboBoxSigma.currentText(),
                               comboBoxInput.currentText(), comboBoxKernel.currentText(),
                               sliderRangeSigma.value(), sliderSpaceSigma.value(), comboBoxGIWRepeat.currentText()))

    sys.exit(app.exec_())


def call_algorithm(algorithm, sigmaparam, inputphoto, kernelsize, range_sigmaparam, space_sigmaparam, giw_repeat_times):
    global final
    print("\n")
    print(algorithm)
    print(sigmaparam)
    print(inputphoto)
    print(kernels[kernelsize])
    print("\n")
    sigma = int(sigmaparam)
    range_sigma = range_sigmaparam
    if algorithm == "Kuwahara":
        final = kuwahara(images[inputphoto], sigma)
    elif algorithm == "Gradient inverse weighted method":
        final = gradient_inverse_weighted(images[inputphoto], sigma, kernels[kernelsize])
    elif algorithm == "Sigma":
        final = sigmaAlgorithm(images[inputphoto], sigma, kernels[kernelsize])
    elif algorithm == "Bilateral":
        final = bilateral(images[inputphoto], sigma, kernels[kernelsize], range_sigma,
                          space_sigmaparam)
    elif algorithm == "Gradient inverse weighted method NEW":
        if giw_repeat_times == "1":
            final = GIW_new(images[inputphoto], sigma, kernels[kernelsize], False)
        elif giw_repeat_times == "2":
            first = GIW_new(images[inputphoto], sigma, kernels[kernelsize], False)
            final = GIW_new(first, sigma, kernels[kernelsize], True)
        else:
            first = GIW_new(images[inputphoto], sigma, kernels[kernelsize], False)
            second = GIW_new(first, sigma, kernels[kernelsize], True)
            final = GIW_new(second, sigma, kernels[kernelsize], True)
    elif algorithm == "Bilateral constant time":
        final = constant_time_bilateral(images[inputphoto], sigma)
    cv2.imshow('Image after denoising', final)


window()
cv2.waitKey(0)
cv2.destroyAllWindows()

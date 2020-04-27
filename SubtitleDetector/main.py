from Gui.Gui import Gui
from PyQt5 import QtWidgets
from VideoLoad.VideoLoad import VideoParser
from Ctpn.ctpn_model import CTPN
import Ctpn.config as config
import sys,os,torch
gpu = True
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    gui = Gui()

    model = CTPN()
    weights = os.path.join(config.checkpoints_dir, 'ctpn_0.2899.pth')
    device = torch.device('cuda:0' if gpu else 'cpu')
    model.load_state_dict(torch.load(weights, map_location=device)['model_state_dict'])
    model.to(device)
    model.eval()

    videoParser = VideoParser(model,device)
    gui.SetVideoParser(videoParser)

    gui.show()
    sys.exit(app.exec_())
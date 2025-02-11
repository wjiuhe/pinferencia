import base64
import pathlib
from io import BytesIO

import torch
from main import Net
from PIL import Image
from torchvision import transforms

from pinferencia import Server
from pinferencia.handlers import BaseHandler


class MNISTHandler(BaseHandler):
    transform = transforms.Compose(
        [
            transforms.ToTensor(),
            transforms.Normalize((0.1307,), (0.3081,)),
        ]
    )
    use_cuda = torch.cuda.is_available()
    device = torch.device("cuda" if use_cuda else "cpu")

    def load_model(self):
        model = Net().to(self.device)
        model.load_state_dict(torch.load(self.model_path))
        model.eval()
        return model

    def predict(self, data):
        image = Image.open(BytesIO(base64.b64decode(data)))
        tensor = self.transform(image)
        input_data = torch.stack([tensor]).to(self.device)
        return self.model(input_data).argmax(1).tolist()[0]


service = Server(model_dir=pathlib.Path(__file__).parent.resolve())
service.register(
    model_name="mnist",
    model="mnist_cnn.pt",
    handler=MNISTHandler,
    load_now=True,
)

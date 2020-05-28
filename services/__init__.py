from .extractor_service import ExtractorService
from .selector_service import SelectorService
from .send_data_service import SendDataService
from .update_data_service import UpdateDataService


send = SendDataService()
extractor = ExtractorService()
selector = SelectorService()
update = UpdateDataService()

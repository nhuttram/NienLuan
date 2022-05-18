from import_export import resources
from .models import Loai_San_Pham,San_Pham

class LoaiReource(resources.ModelResource):
    class meta():
        model = Loai_San_Pham

class SanPhamReource(resources.ModelResource):
    class meta():
        model = San_Pham
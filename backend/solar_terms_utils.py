import json
from datetime import datetime
import os

def load_solar_terms_flat(json_path=None):
    """
    加载节气数据并转换为扁平list: [{"name":..., "datetime":...}]
    """
    if not json_path:
        backend_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(backend_dir, "solar_terms_data.json")
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    flat = []
    for year, terms in data.items():
        for name, dtstr in terms.items():
            # 兼容无秒
            if len(dtstr) == 16:
                dtstr = dtstr + ":00"
            flat.append({"name": name, "datetime": dtstr, "year": int(year)})
    # 按时间排序
    flat.sort(key=lambda x: datetime.strptime(x["datetime"], "%Y-%m-%d %H:%M:%S"))
    return flat

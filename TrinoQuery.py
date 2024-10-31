import pandas as pd
import requests
from sqlalchemy import URL,create_engine

def read_trino_query(user, password, host, port, query):
    # Cấu hình URL connection cho Trino
    connection_url = URL.create(
        "trino",
        username=user,
        password=password,
        host=host,
        port=port,
        query={
            "http_scheme": "https",
            "verify": "false"
        }
    )
    # Tạo một session HTTP tùy chỉnh với timeout vô hiệu hóa
    http_session = requests.Session()
    http_session.timeout = None  # Vô hiệu hóa timeout
    http_session.verify = False
    # Tạo engine sử dụng session HTTP tùy chỉnh và thông tin kết nối
    engine = create_engine(
        connection_url,
        connect_args={
            "http_session": http_session
        },
        echo=True,  # Bật logging để dễ dàng debug
        pool_pre_ping=True,  # Kiểm tra kết nối trước khi sử dụng để tự động khôi phục các kết nối hỏng
        pool_size=5,  # Số lượng kết nối tối thiểu trong pool
        max_overflow=10,  # Số lượng kết nối tối đa có thể tạo ra ngoài số lượng tối thiểu
        pool_timeout=30,  # Thời gian chờ tối đa (giây) để lấy kết nối từ pool
        pool_recycle=1800  # Tái sử dụng kết nối sau khoảng thời gian (giây)
    )
    conn = engine.connect()
    result = pd.read_sql_query(query, conn)
    conn.close()
    engine.dispose()
    return result


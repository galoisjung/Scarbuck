from urllib.parse import quote

search_db_username = 'searchadm'
search_db_password = 't3q!9327@'
search_db_name = 'searchdb'
search_db_host = '192.168.0.81'
search_db_port = '39613'
search_db_uri = "postgresql+psycopg2://{DB_USER}:%s@{DB_HOST}:{DB_PORT}/{DB_NAME}".format(
    DB_USER=search_db_username,
    DB_HOST=search_db_host,
    DB_PORT=search_db_port,
    DB_NAME=search_db_name
) % quote(search_db_password)

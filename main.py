import data_import_support as dis

exc_name="krakeneur"
start_stamp=dis.unix_to_timestamp(1406851200)
end_stamp=dis.unix_to_timestamp(1514764800)

dis.import_from_csv_w_ticks(exc_name, start_stamp, end_stamp)
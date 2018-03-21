import data_import_support as dis

exc_name="korbitkrw"
start_stamp=dis.unix_to_timestamp(1377993600)
end_stamp=dis.unix_to_timestamp(1514764800)

dis.import_from_csv_w_ticks(exc_name, start_stamp, end_stamp)